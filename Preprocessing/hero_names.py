import requests
import json

if __name__ == '__main__':
    heroes = requests.get("https://hotsapi.net/api/v1/heroes")
    hero_names = dict()
    for hero in heroes.json():
        hero_names[hero['name']] = {
            "short_name": hero["short_name"],
            "attribute_id": hero["attribute_id"]
        }
    with open('hero_names.json', 'w') as file:
        json.dump(hero_names, file)
