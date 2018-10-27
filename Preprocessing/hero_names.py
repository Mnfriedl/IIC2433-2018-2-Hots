"""Generates the file hero_names.json with the use of HotsAPI.
"""


import requests
import json
import unidecode

if __name__ == '__main__':
    heroes = requests.get("https://hotsapi.net/api/v1/heroes")
    hero_names = dict()
    for hero in heroes.json():
        hero_names[unidecode.unidecode(hero['name'])] = [hero['name'], hero['short_name'], hero['attribute_id']]
        for i in hero['translations']:
            hero_names[unidecode.unidecode(hero['name'])].append(i)
    with open('hero_names.json', 'w') as file:
        json.dump(hero_names, file)
