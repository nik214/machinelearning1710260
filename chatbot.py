import random
import json
from tokens import cmc_token
import requests
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('intents.json', 'r')as f:
    intents = json.load(f)
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Bitbot"


def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent['response'])
            elif msg == 'what is bitcoin price?' or msg == 'bitcoin price' or msg == 'price of bitcoin' or msg == 'btc' or msg =='BTC':
                return "The Bitcoin price is " + "{:.2f}$".format(float(get_cmc_data('BTC')))
            elif msg == 'what is ethereum price?' or msg == 'ethereum price' or msg == 'price of ethereum' or msg =='eth' or  msg =='ETH':
                return  "The Ethereum price is " + "{:.2f}$".format(float(get_cmc_data('ETH')))
            elif msg == 'what is litecoin price?' or msg == 'litecoin price' or msg == 'price of litecoin' or msg=='ltc' or msg == 'LTC':
                return  "The Litecoin price is " + "{:.2f}$".format(float(get_cmc_data('LTC')))
            elif msg == 'what is xpr price?' or msg == 'xpr price' or msg == 'price of xpr' or msg == 'xpr' or msg == 'XPR':
                return  "The XPR price is " + "{:.2f}$".format(float(get_cmc_data('XPR')))

            elif msg == 'what is the change of percentage for bitcoin for 1 hour?' or msg == 'bitcoin change 1 hour' or msg == 'bitcoin change one hour' or msg == '1 hour change for bitcoin' or msg == 'btc 1 hour change':
                return "The percentage of bitcoin change for 1 hour is  " + "{:.2f}%".format(
                    float(get_hour_data('BTC')))
            elif msg == 'what is the change percentage for ethereum for 1 hour?' or msg == 'ethereum change 1 hour' or msg == 'ethereum change one hour' or msg == '1 hour change for ethereum' or msg == 'eth 1 hour change':
                return  "The percentage for ethereum change for 1 hour is  " + "{:.2f}%".format(
                    float(get_hour_data('ETH')))
            elif msg == 'what is the change of percentage for litecoin for 1 hour?' or msg == 'litecoin change 1 hour' or msg == 'litecoin change one hour' or msg == '1 hour change for litecoin' or msg == 'ltc 1 hour change':
                return  "The percentage for litecoin change for 1 hour is  " + "{:.2f}%".format(
                    float(get_hour_data('LTC')))

            elif msg == 'what is the change of percentage for xpr for 1 hour?' or msg == 'xpr change 1 hour' or msg == 'xpr change one hour' or msg == '1 hour change for xpr' or msg == 'xpr 1 hour change':
                return  "The percentage for xpr change for 1 hour is   " + "{:.2f}%".format(
                    float(get_hour_data('XPR')))


            elif msg == 'what is the change of percentage for bitcoin for 24 hours?' or msg == 'bitcoin change 24 hours' or msg == '24 hours change for bitcoin' or msg == 'btc 24 hours change':
                return  "The percentage for bitcoin change for 24 hours is  " + "{:.2f}%".format(
                    float(get_twentyhour_data('BTC')))
            elif msg == 'what is the change of percentage for ethereum for 24 hours?' or msg == 'ethereum change 24 hours' or msg == '24 hours change for ethereum' or msg == 'eth 24 hours change':
                return  "The percentage for ethereum change for 24 hours is  " + "{:.2f}%".format(
                    float(get_twentyhour_data('ETH')))
            elif msg == 'what is the change of percentage for litecoin for 24 hour?' or msg == 'litecoin change 24 hours' or msg == '24 hours change for litecoin' or msg == 'ltc 24 hours change':
                return  "The percentage for litecoin change for 24 hour is   " + "{:.2f}%".format(
                    float(get_twentyhour_data('LTC')))

            elif msg == 'what is the change of percentage for xpr for 24 hour?' or msg == 'xpr change 24 hours' or msg == '24 hours change for xpr' or msg == 'xpr 24 hours change':
                return  "The percentage for xpr change for 24 hour is   " + "{:.2f}%".format(
                    float(get_twentyhour_data('XPR')))


            elif msg == 'what is the change of percentage for bitcoin for one month?' or msg == 'bitcoin change 1 month' or msg == 'bitcoin change one month' or msg == '1 month change for bitcoin' or msg == 'btc 1 month change':
                return  "The percentage for bitcoin change for one month is  " + "{:.2f}%".format(
                    float(get_onemonth_data('BTC')))
            elif msg == 'what is the change of percentage for ethereum for one month?' or msg == 'ethereum change 1 month' or msg == 'ethereum change one month' or msg == '1 month change for ethereum' or msg == 'eth 1 month change':
                return "The percentage for ethereum change for one month is  " + "{:.2f}%".format(
                    float(get_onemonth_data('ETH')))
            elif msg == 'what is the change of percentage for litecoin for one month?' or msg == 'litecoin change 1 month' or msg == 'litecoin change one month' or msg == '1 month change for litecoin' or msg == 'ltc 1 month change':
                return "The percentage for litecoin change for one month is  " + "{:.2f}%".format(
                    float(get_onemonth_data('LTC')))
            elif msg == 'what is the cahnge of percentage for xpr for one month?' or msg == 'xpr change 1 month' or msg == 'xpr change one month' or msg == '1 month change for xpr' or msg == 'xpr 1 month change':
                return "The percentage for xpr change for one month is  " + "{:.2f}%".format(
                    float(get_onemonth_data('XPR')))
    return "i do not understand..."


def get_cmc_data(crypto):
    URLCOIN = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'  # website where API is
    params = {'symbol': crypto, 'convert': 'USD'}
    headers = {'X-CMC_PRO_API_KEY': cmc_token}

    r = requests.get(URLCOIN, headers=headers, params=params).json()
    price = r['data'][crypto]['quote']['USD']['price']  # the path for gather the currency prices

    return price
def get_hour_data(crypto):
    URLCOIN = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'  # website where API is
    params = {'symbol': crypto, 'convert': 'USD'}
    headers = {'X-CMC_PRO_API_KEY': cmc_token}
    r = requests.get(URLCOIN, headers=headers, params=params).json()
    onehour = r['data'][crypto]['quote']['USD']['percent_change_1h']
    return onehour


## API for 24 hours
def get_twentyhour_data(crypto):
    URLCOIN = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'  # website where API is
    params = {'symbol': crypto, 'convert': 'USD'}
    headers = {'X-CMC_PRO_API_KEY': cmc_token}
    r = requests.get(URLCOIN, headers=headers, params=params).json()
    twentyfourhour = r['data'][crypto]['quote']['USD']['percent_change_24h']
    return twentyfourhour


## API for one month
def get_onemonth_data(crypto):
    URLCOIN = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'  # website where API is
    params = {'symbol': crypto, 'convert': 'USD'}
    headers = {'X-CMC_PRO_API_KEY': cmc_token}
    r = requests.get(URLCOIN, headers=headers, params=params).json()
    onemonth = r['data'][crypto]['quote']['USD']['percent_change_30d']
    return onemonth
