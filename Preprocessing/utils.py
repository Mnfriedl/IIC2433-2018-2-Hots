"""In this file the replay files are downloaded, parsed and later later deleted, to save space.
"""

import subprocess
import os
import json
import datetime
import boto3


# Global variables
S3CLIENT = boto3.client('s3')
with open("hero_names.json", "r") as file:
    HERO_NAMES = json.load(file)


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

def get_hero_name(name):
    """It takes the name of a hero in any format, and returns a standarized name
    for that hero. It uses the hero_names.json file, which was built using the
    hotsapi heroes endpoint, and then some name variations were added by hand later.
    
    Arguments:
        name {string} -- Name of the hero
    
    Returns:
        string -- Standarized name of the hero
    """

    for key in HERO_NAMES:
        if name in HERO_NAMES[key]:
            return key

def download_replay(filename, output_filename="actual_replay.StormReplay"):
    """Uses boto3 to download a .StormReplay file from the HotsAPI Amazon S3 bucket.
    You need to have your AWSAccessKeyId and AWSSecretKey configured in the amazon
    AWS CLI, because the bucket has requester pays enabled.
    
    Arguments:
        filename {string} -- Name of the replay inside the Amazon S3 bucket to be downloaded.
    
    Keyword Arguments:
        output_filename {string} -- Name of the .StormReplay file to be saved (default: {"actual_replay.StormReplay"})
    """

    response = S3CLIENT.get_object(Bucket='hotsapi',
                                Key=filename, 
                                RequestPayer='requester')
    response_content = response['Body'].read()

    with open('./{}'.format(output_filename), 'wb') as file:
        file.write(response_content)

def delete_replay(filename="actual_replay.StormReplay"):
    """Deletes a file. Used to delete the .StormReplay files after they are parsed, as
    we don't want to accumulate the files, only the info.
    
    Keyword Arguments:
        filename {string} -- Name of the file to be deleted. (default: {"actual_replay.StormReplay"})
    """

    os.remove(filename)

def run_heroprotocol(filename="actual_replay.StormReplay"):
    """Runs the Blizzard's heroprotocol parser for .StormReplay files and outputs to output.json
    
    Keyword Arguments:
        filename {str} -- Name of the replay file to be parsed by Blizzard's heroprotocol (default: {"actual_replay.StormReplay"})
    """
    subprocess.run("python2 heroprotocol/heroprotocol.py --attributeevents {} --json > attributeevents.json".format(filename), shell=True)
    subprocess.run("python2 heroprotocol/heroprotocol.py --trackerevents {} --json > trackerevents.json".format(filename), shell=True)

def parse(filename):
    """Function that encapsulates every task needed to be done in order to parse a replay.
    It will download the file from the amazon s3 bucket, run blizzard's heroprotocol, delete
    the replay file to save space (each replay is like 1MB - 2MB), parse the relevant information
    (picked heroes and hero level, and also banned heroes, all in event order).
    
    Arguments:
        filename {string} -- Name of the file stored in the amazon S3 bucket of hotsapi. 
    
    Returns:
        [dict] -- Dictionary containing picks and bans in happening order. Picks also include hero level.
    """

    # Generate the needed files
    download_replay(filename)
    run_heroprotocol()
    # Delete the .StormReplay file
    delete_replay()

    # Parse the needed data
    to_return = {
        "picks": [],
        "bans": [],
        "winner": None
        }
    with open("trackerevents.json", "r") as file:
        events = list()
        lines = file.readlines()
        for line in lines[10: 26]:
            events.append(json.loads(line))
    
        # Start from the bottom up to look for the winner
        i = len(lines) - 1
        while True:
            line = json.loads(lines[i])
            should_break = False
            if line["_eventid"] == 10 and line["m_eventName"] == "EndOfGameTalentChoices":
                # Get if the hero won or not
                winner = None
                player_id = None
                for j in line["m_stringData"]:
                    if j["m_key"] == "Win/Loss":
                        winner = 1 if j["m_value"] == "Win" else 0
                for j in line["m_intData"]:
                    if j["m_key"] == "PlayerID":
                        player_id = j["m_value"]
                if winner and player_id:
                    should_break = True
                    break
            if should_break:
                break
            i -= 1
        if player_id in [1, 4, 5, 8, 9]:
            to_return['winner'] = winner
        else:
            if winner == 1:
                to_return['winner'] = 0
            else:
                to_return['winner'] = 1

    with open("attributeevents.json", "r") as file:
        attributeevents = json.load(file)["scopes"]

    for i in events:
        if i["_event"] == "NNet.Replay.Tracker.SHeroPickedEvent":
            hero = get_hero_name(i["m_hero"].lower().replace(" ", ""))
            for j in range(1, 11):
                if get_hero_name(attributeevents[str(j)]["4002"][0]['value'].lower().replace(" ", "")) == hero:
                    to_return["picks"].append({
                        "hero": hero,
                        "level": int(attributeevents[str(j)]["4008"][0]['value'])
                    })
        elif i["_event"] == "NNet.Replay.Tracker.SHeroBannedEvent":
            to_return["bans"].append(get_hero_name(i["m_hero"].lower().replace(" ", "")))
    os.remove("attributeevents.json")
    os.remove("trackerevents.json")

    return to_return


if __name__ == "__main__":
    # Useless code for testing purposes
    print(parse("94f977fd-38a6-5164-5c7e-2cc5be357bfe.StormReplay"))
