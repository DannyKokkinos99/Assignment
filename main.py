"""Script used to calculate the average duration between addittions and deletions for specific Reddit Repositories by making REST API calls"""

from datetime import datetime, timezone
import time
import sqlite3
from flask import Flask, request
import requests
import numpy as np

app = Flask(__name__)


@app.route("/github/get_statistics")
def get_repo_statistics():
    """Gets the statistics for a specific repo then saves it to a database"""
    # Get query parameters

    owner = request.args.get("owner")
    repo = request.args.get("repo")

    while True:
        # Make request

        url = f"https://api.github.com/repos/{owner}/{repo}/stats/code_frequency"
        response = requests.get(url, timeout=60)

        if response.status_code == 202:
            print("Statistics are being compiled...")
            time.sleep(10)
        elif response.status_code == 200:
            events = response.json()
            dates, additions, deletions = extract_data(
                events, 0, owner =owner, repo= repo
            )  # splits the events into separate arrays
            write_to_database(
                owner, repo, dates, additions, deletions
            )  # saves data to the database
            # Process events as needed

            message = "Data has been saved to database."
            return {"status": "SUCCESS", "message": message}
        else:
            message = "Failed to save data to database."
            return {"status": "FAILED", "message": message}, response.status_code


@app.route("/average_results")
def display_results():
    """displays average results to user"""
    # Get query parameters

    owner = request.args.get("owner")
    repo = request.args.get("repo")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM Calculations WHERE Owner = '{owner}' AND Repo = '{repo}';"
    cursor.execute(query)
    events = cursor.fetchall()

    return {
        "Owner": events[0][0],
        "Repo": events[0][1],
        "Average_addition": events[0][2],
        "Average_deletion": events[0][3],
    }


@app.route("/calculate")
def calculate():
    """Calculates the average between events"""
    # Get query parameters

    owner = request.args.get("owner")
    repo = request.args.get("repo")
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        # Query to select data from the database for a specific owner and repo

        query = f"SELECT * FROM Data WHERE Owner = '{owner}' AND Repo = '{repo}';"
        cursor.execute(query)
        events = cursor.fetchall()
        dates, additions, deletions = extract_data(events, 1)
        average_addition = calculate_average_duration(additions, dates)
        average_deletion = calculate_average_duration(deletions, dates)
        # SQL statement to insert data into the table

        insert_statement = "INSERT INTO Calculations (Owner, Repo, avarage_addition, avarage_deletion) VALUES (?, ?, ?, ?)"
        # Execute the insert statement for each set of data

        data_to_insert = [(owner, repo, average_addition, average_deletion)]
        cursor.executemany(insert_statement, data_to_insert)

        # Commit the transaction

        conn.commit()

        # Close the connection

        conn.close()
        message = f"Calculations for {owner}/{repo} complete."
        return {"status": "SUCCESS", "message": message}
    except sqlite3.Error as e:
        message = f"Database error:{e}"
        return {"status": "FAILED", "message": message}


def calculate_average_duration(event, dates):
    """Calculates the avarage between non-zero consecutive numbers"""
    average_temp = []
    for i in range(len(event)):
        if event[i] == 0:
            continue
        for j in range(i + 1, len(event)):
            if event[j] == 0:
                continue
            average_temp.append(days_between_unix_dates(dates[i], dates[j]))
            break
    return round(np.mean(average_temp), 2)


def write_to_database(owner, repo, dates, additions, deletions):
    """Writes the data to the database"""
    try:
        # Connect to the SQLite database

        conn = sqlite3.connect("database.db")
        # Create a cursor object

        cursor = conn.cursor()
        # Structure the data
        data_to_insert = []
        for i, _ in enumerate(dates):
            row = (owner, repo, dates[i], additions[i], deletions[i])
            data_to_insert.append(row)
        # SQL statement to insert data into the table

        insert_statement = "INSERT INTO Data (Owner, Repo, Date, Additions, Deletions) VALUES (?, ?, ?, ?, ?)"

        # Execute the insert statement for each set of data

        cursor.executemany(insert_statement, data_to_insert)

        # Commit the transaction

        conn.commit()

        # Close the connection

        conn.close()
        message = "Database connection successful."
        return {"status": "SUCCESS", "message": message}
    except sqlite3.Error as e:
        message = f"Database connection error: {e}"
        return {"status": "FAILED", "message": message}


def extract_data(events, seletion, owner=None,repo=None):
    """Extracts data from response into local variables"""
    dates = []
    additions = []
    deletions = []
    check_array = []
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    query = f"SELECT GROUP_CONCAT(DISTINCT Date) FROM Data WHERE Owner = '{owner}' AND Repo = '{repo}';"
    cursor.execute(query)
    check = cursor.fetchone()
    conn.close()
    if check and check[0]:
        check_array.append(check[0].split(','))

    if seletion == 0:
        for index, data in enumerate(events):
            if index == 500:  # exits if events exceed 500
                break
            if str(data[0]) not in check_array:
                dates.append(data[0])
                additions.append(data[1])
                deletions.append(data[2])
        return dates, additions, deletions
    elif seletion == 1:
        for _, data in enumerate(events):
            dates.append(data[2])
            additions.append(data[3])
            deletions.append(data[4])
        return dates, additions, deletions


def days_between_unix_dates(timestamp1, timestamp2):
    """Functions used to conver unix dates to datetime and find the difference"""
    # Convert Unix timestamps to datetime objects

    date1 = datetime.fromtimestamp(timestamp1, tz=timezone.utc)
    date2 = datetime.fromtimestamp(timestamp2, tz=timezone.utc)

    # Calculate the difference between the datetime objects

    difference = date2 - date1

    # Extract the number of days from the difference

    days = difference.days

    return days


if __name__ == "__main__":
    app.run(debug=True, port=9000)