"""This file has the main pipe of work for the preprocessing of the replays inside
HotsAPI.
"""

import boto3  # Used as a wrapper of the Amazon AWS S3 service
import requests  # Used to send the GET requests to HotsAPI
import datetime  # Used to define the date of the replays to be processed


def date_to_string(date):
    """Transforms a datetime object into a string in the format Year-Month-Day
    
    Arguments:
        date {datetime} -- datetime object to be transformed
    
    Returns:
        string -- date string transformed
    """

    return date.strftime("%Y-%m-%d")

def parse_date(date):
    """Transforms a date in string format into a datetime object
    
    Arguments:
        date {string} -- date to be transformed into a datetime
    
    Returns:
        datetime -- datetime object of the input date
    """

    return datetime.datetime.strptime(date, "%Y-%m-%d")


actual_date = None
try:  # Parse the last date from the file, if it exists
    with open('last_date.txt', 'r') as date_file:
        actual_date = parse_date(date_file.read())
except FileNotFoundError:  # If there is no file, we use today's date
    actual_date = datetime.datetime.now()

# Parse the replays, one day at a time. The parse occurs backwards, that means, the most recent replays first
while True:
    # Save to the file the last date parsed
    with open('last_date.txt', 'w') as date_file:
        date_file.write(date_to_string(actual_date))
    # Get the info from the API
    break

