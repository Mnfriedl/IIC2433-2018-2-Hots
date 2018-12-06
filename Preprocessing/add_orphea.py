import json

with open('hero_names.json', 'r') as file:
    HERO_NAMES = json.load(file)

HERO_NAMES["Orphea"] = [
            "orphea",
            "orféa",
            "奥菲娅",
            "歐菲亞",
            "orphéa",
            "orfea",
            "орфея",
            "오르피아"
        ]

with open('hero_names.json', 'w') as file:
    json.dump(HERO_NAMES, file)
