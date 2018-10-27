"""This file has the main pipe of work for the preprocessing of the replays inside
HotsAPI.
"""

import requests
import utils
import datetime
import psycopg2


CONN = psycopg2.connect(host="localhost", database="IIC2433-HOTSY", user="hotsy", password="hotsy")
CURSOR = CONN.cursor()


actual_date = None
try:  # Parse the last date from the file, if it exists
    with open('last_date.txt', 'r') as date_file:
        actual_date = utils.parse_date(date_file.read())
except FileNotFoundError:  # If there is no file, we use today's date
    actual_date = datetime.datetime.now()

# Parse the replays, one day at a time. The parse occurs backwards, that means, the most recent replays first
while True:
    # Save to the file the last date parsed
    with open('last_date.txt', 'w') as date_file:
        date_file.write(utils.date_to_string(actual_date))
    # Get the info from the API
    actual_page = 1
    while True:
        replays_info = requests.get("https://hotsapi.net/api/v1/replays/paged", params={"page": actual_page, "start_date": utils.date_to_string(actual_date)})
        replays = replays_info.json()["replays"]
        if len(replays) == 0:
            break
        for replay in replays:
            if replay['game_type'] in ['TeamLeague', 'HeroLeague', 'UnrankedDraft']:  # We are only interested on replays with draft
                #parse
                pass
        actual_page += 1

    actual_date = actual_date - datetime.timedelta(days=1)
    # Should probably add a finishing condition here
    break
