from flask import Flask
from flask import render_template
import requests
from card import Card
from rarity import Rarity
from convertor import Convertor

app = Flask(__name__)

def calculateEvolvingCostMultiple(cards):
    total_gold_needed = 0

    for card in cards:
        total_gold_needed += calculateEvolvingCostSingle(card)

    return total_gold_needed

def calculateEvolvingCostSingle(card):
    total_gold_needed = 0
    count = card.count
    rarity = card.rarity
    level = card.level

    if rarity.isOnMaxLevel(level):
        return 0

    cards_to_level_up = rarity.getCardsAmountToLevelUp(level)
    while count >= cards_to_level_up:
        total_gold_needed += rarity.getGoldToLevelUp(level)

        level += 1
        if rarity.isOnMaxLevel(level):
            break

        count -= cards_to_level_up
        cards_to_level_up = rarity.getCardsAmountToLevelUp(level)

    return total_gold_needed

@app.route('/')
def hello_world():
    player_tag = "%2320CJR09UC"  # Replace with the player tag you want to query
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjU0Yzc2Njk1LWIwYzQtNGU0NS05NmRjLWQxZDZiNDMwOTljNSIsImlhdCI6MTY5MzA2ODgwMSwic3ViIjoiZGV2ZWxvcGVyL2IwYTg1OGFhLWUxYjYtNzc1OC1iYTM0LTBjMWJjMThjNGYyZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMDkuNDkuNTguMTYxIl0sInR5cGUiOiJjbGllbnQifV19.xO9ilrKrVRcOiWF7WDYBrr-9eNb4aqHmzFzJjTiY8pm_ZS5GQseVWlDmhYtAFBmvWHR-BncZlph12qbWij6wkg"  # Replace with your Clash Royale API key

    api_url = f"https://api.clashroyale.com/v1/players/{player_tag}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        cards = []
        for json_card in json_response["cards"]:
            card = Convertor.to_card(json_card)
            if card:
                cards.append(card)

        return str(calculateEvolvingCostMultiple(cards))
    else:
        print(f"API request failed with response code: {response.status_code}")
        return str(-1)

    #return render_template('index.html')
    
    
if __name__ == '__main__':
    app.run(debug=True)