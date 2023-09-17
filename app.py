from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from card import Card
from rarity import Rarity
from convertor import Convertor

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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

__CARDINAL_IN_URL__ = "%23"

def fixPlayerTag(playerTag):
    if len(playerTag) == 0:
        return ""

    if playerTag[0] == "#":
        playerTag = __CARDINAL_IN_URL__ + playerTag[1:]
    elif playerTag[0] != "%":
        playerTag = __CARDINAL_IN_URL__ + playerTag
        
    return playerTag

def getPlayerData(playerTag):
    playerTag = fixPlayerTag(playerTag)

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


# >--------------------------------------{ Pages }--------------------------------------<

__INVALID_PlAYER_TAG__ = "Invalid player tag!"
__OVERWHELMING_REQUESTS_AMOUNT__ = "Too much requests right now! Try again later."
__API_UNDER_MAINTENANCE__ = "Clash royale API is under maintenance. Try again later."
__UNKNOWN_ERROR__ = "Unknown error."

def interpretStatusCode(statusCode):
    match statusCode:
        case 200:
            return None
        case 404:
            return __INVALID_PlAYER_TAG__
        case 429:
            return __OVERWHELMING_REQUESTS_AMOUNT__
        case 503:
            return __API_UNDER_MAINTENANCE__
        case 500:
            return __UNKNOWN_ERROR__
        
    return str(statusCode)

@app.route('/calculate', methods=['POST'])
def calculate():
    playerTag = request.form.get('clash_royale_tag')
    
    playerData = getPlayerData(playerTag)
    errorMessage = interpretStatusCode(playerData.status_code)
    
    if errorMessage != None:
        flash(errorMessage, "error")
        return redirect(url_for('main'))
    
    cards = getPlayerCards(playerData.json())
    evolvingCosts = calculateEvolvingCostMultiple(cards)
    
    return render_template('index.html', total_cost=evolvingCosts)
    
@app.route('/')
def main():
    return render_template('index.html', total_cost=None)


if __name__ == '__main__':
    app.run(debug=True)