"""In this file the replay files are downloaded, parsed and later later deleted, to save space.
"""

import subprocess
import os
import json
import datetime
import boto3
import unidecode


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
    # Generate the needed files
    download_replay(filename)
    run_heroprotocol()
    # Delete the .StormReplay file
    delete_replay()

    # Parse the needed data
    to_return = {
        "picks": [],
        "bans": []
        }
    with open("trackerevents.json", "r") as file:
        events = list()
        for i, line in enumerate(file):
            if i in range(10, 26):
                events.append(json.loads(line))
    with open("attributeevents.json", "r") as file:
        attributeevents = json.load(file)["scopes"]
    for i in events:
        if i["_event"] == "NNet.Replay.Tracker.SHeroPickedEvent":
            hero = unidecode.unidecode(i["m_hero"])
            for j in range(1, 11):
                if attributeevents[str(j)]["4002"][0]['value'] == HERO_NAMES[hero]['attribute_id']:
                    to_return["picks"].append({
                        "hero": hero,
                        "level": attributeevents[str(j)]["4008"][0]['value']
                    })
        elif i["_event"] == "NNet.Replay.Tracker.SHeroBannedEvent":
            to_return["bans"].append(i["m_hero"])

    return to_return


if __name__ == "__main__":
    # Useless code for testing purposes
    parse("00488be0-7f21-f1c5-335e-133e12be4023.StormReplay")
