## Introduction
This repository contains my solution to the assignment.

## Thought process for specific library choices made
*   Flask: I selected Flask as my webframework as it is lightweight and easy to setup as the main 
specification is to complete the assignment within a specific timeframe.
*   SQLite: I used SQLite as I have experience with it.
## Prerequisites
Code has been tested on python version 3.8.0 and 3.10.0
## Setting up the repository
1. Open a terminal within the project folder
2. run "pip install -r requirements.txt" or create a virtual environment using the requirements manually

## Scripts content
Run "python main.py" to start server then use the endpoinds below

This script contains 3 endpoinds listen below:
1. Get the statistics 
2. Calculate the statistics
3. Get results

Example 1:
1. http://127.0.0.1:9000/functions/get_statistics?owner=microsoft&repo=AI-For-Beginners
2. http://127.0.0.1:9000/functions/calculate?owner=microsoft&repo=AI-For-Beginners
3. http://127.0.0.1:9000/functions/average_results?owner=microsoft&repo=AI-For-Beginners

Example 2:
1. http://127.0.0.1:9000/functions/get_statistics?owner=cta-wave&repo=device-observation-framework
2. http://127.0.0.1:9000/functions/calculate?owner=cta-wave&repo=device-observation-framework
3. http://127.0.0.1:9000/functions/average_results?owner=cta-wave&repo=device-observation-framework


The final request will return the results for the average consecutive duration between additions and deletions for that specific repository in days

