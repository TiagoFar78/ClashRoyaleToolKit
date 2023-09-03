from flask import Flask
from flask import render_template
from flask import request
import requests
from card import Card
from rarity import Rarity
from convertor import Convertor

app = Flask(__name__)

# >-----------------------------------{ Calculations }-----------------------------------<

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


# >--------------------------------------{ Player }--------------------------------------<

def fixPlayerTag(playerTag):
    pass

def getPlayerData(playerTag):
    #playerTag = fixPlayerTag(playerTag)

    with open('token.txt', 'r') as file:
        api_key = file.read()

    api_url = f"https://api.clashroyale.com/v1/players/{playerTag}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    response = requests.get(api_url, headers=headers)
    return response

def getPlayerCards(playerData):
    cards = []
    for json_card in playerData["cards"]:
        card = Convertor.to_card(json_card)
        if card:
            cards.append(card)

    return cards


# >--------------------------------------{ Player }--------------------------------------<

def interpretStatusCode(statusCode):
    if statusCode == 200:
        return None
        
    return str(statusCode)

@app.route('/calculate', methods=['POST'])
def calculate():
    playerTag = request.form.get('clash_royale_tag')
    
    playerData = getPlayerData(playerTag)
    errorMessage = interpretStatusCode(playerData.status_code)
    
    if errorMessage != None:
        return errorMessage
    
    cards = getPlayerCards(playerData.json())
    evolvingCosts = calculateEvolvingCostMultiple(cards)
    
    return render_template('index.html', total_cost=evolvingCosts)
    
@app.route('/')
def index():
    return render_template('index.html', total_cost=None)


if __name__ == '__main__':
    app.run(debug=True)