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
                print(replay["filename"])
                try:
                    picks_and_bans = utils.parse(replay["filename"] + ".StormReplay")
                except Exception as error:
                    print(error)
                    continue
                print(picks_and_bans)
                if len(picks_and_bans["picks"]) != 10:
                    print("Incorrect number of pick")
                    continue
                if len(picks_and_bans["bans"]) != 6:
                    for i in range(6 - len(picks_and_bans["bans"])):
                        picks_and_bans["bans"].append(None)
                # Add the data into the databse
                query = """INSERT INTO replay 
                (game_type, map, ban1, ban2, ban3, ban4, ban5, ban6,
                pick1, pick2, pick3, pick4, pick5, pick6, pick7, pick8, pick9, pick10,
                level1, level2, level3, level4, level5, level6, level7, level8, level9, level10) 
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                data = (replay["game_type"],
                replay["game_map"]["name"],
                picks_and_bans["bans"][0],
                picks_and_bans["bans"][1],
                picks_and_bans["bans"][2],
                picks_and_bans["bans"][3],
                picks_and_bans["bans"][4],
                picks_and_bans["bans"][5],
                picks_and_bans["picks"][0]['hero'],
                picks_and_bans["picks"][1]['hero'],
                picks_and_bans["picks"][2]['hero'],
                picks_and_bans["picks"][3]['hero'],
                picks_and_bans["picks"][4]['hero'],
                picks_and_bans["picks"][5]['hero'],
                picks_and_bans["picks"][6]['hero'],
                picks_and_bans["picks"][7]['hero'],
                picks_and_bans["picks"][8]['hero'],
                picks_and_bans["picks"][9]['hero'],
                picks_and_bans["picks"][0]['level'],
                picks_and_bans["picks"][1]['level'],
                picks_and_bans["picks"][2]['level'],
                picks_and_bans["picks"][3]['level'],
                picks_and_bans["picks"][4]['level'],
                picks_and_bans["picks"][5]['level'],
                picks_and_bans["picks"][6]['level'],
                picks_and_bans["picks"][7]['level'],
                picks_and_bans["picks"][8]['level'],
                picks_and_bans["picks"][9]['level'])
                CURSOR.execute(query, data)
                CONN.commit()
                print("replay added!")
        actual_page += 1

    actual_date = actual_date - datetime.timedelta(days=1)
    # Should probably add a finishing condition here
