Introduction
I selected Flask as it is lightweight and very quick to setup
I then spent time going over the github REST API and used postman to play around with the API to find the exact data I wanted. 
Setup:
1. Open a terminal within the project folder
2. run "pip install -r requirements.txt" or create a virtual environment using the requirements

There are 3 steps to using this script correct. Those steps are:
1. Get the statistics
2. Calculate the statistics
3. Get results

Example using real repo:

1. http://127.0.0.1:9000/github/get_statistics?owner=microsoft&repo=AI-For-Beginners
2. http://127.0.0.1:9000/calculate?owner=microsoft&repo=AI-For-Beginners
3. http://127.0.0.1:9000/average_results?owner=microsoft&repo=AI-For-Beginners

The final request will return the results for the average consecutive duration between additions and deletions for that specific repository in days

All data is saved to a database using SQLite