from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ColorProperty, NumericProperty
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.app import MDApp

from chatbot import intents, tag
from tokens import cmc_token
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import requests
import json

import re
import webbrowser
import random


app = MDApp.get_running_app()


def write_json(data, filename='response.json'):  # creating a new file with the response in jason format
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


## API for prices
def get_cmc_data(crypto):
    URLCOIN = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'  # website where API is
    params = {'symbol': crypto, 'convert': 'USD'}
    headers = {'X-CMC_PRO_API_KEY': cmc_token}

    r = requests.get(URLCOIN, headers=headers, params=params).json()
    price = r['data'][crypto]['quote']['USD']['price']  # the path for gather the currency prices

    return price

    ## API  for onehour


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



class Chat(MDScreen):
    messages = ListProperty()
    bot_message_color = ColorProperty([0.192, 0.45, 0.18, 0.5])  # rgba value between 0 and 1
    user_message_color = ColorProperty([0.133, 0.2, 0.266, 0.5])
    delay = NumericProperty(0.1)  # delay between bots messages
    user_message_delay = NumericProperty(0.5)  # delay between user messages (to avoid spamming)

    def answer(self, text, *args):
        # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # with open('intents.json', 'r')as f:
        #     intents = json.load(f)
        # FILE = "data.pth"
        # data = torch.load(FILE)
        #
        # input_size = data["input_size"]
        # hidden_size = data["hidden_size"]
        # output_size = data["output_size"]
        # all_words = data["all_words"]
        # tags = data["tags"]
        # model_state = data["model_state"]
        #
        # model = NeuralNet(input_size, hidden_size, output_size).to(device)
        # model.load_state_dict(model_state)
        # model.eval()
        #
        # bot_name = "Bitbot"
        # print("lets chat")
        # while True:
        #     sentence = input('YOU: ')
        #     if sentence == "quit":
        #         break
        #     sentence = tokenize(sentence)
        #     X = bag_of_words(sentence, all_words)
        #     X = X.reshape(1, X.shape[0])
        #     X = torch.from_numpy(X)
        #
        #     output = model(X)
        #     _, predicted = torch.max(output, dim=1)
        #     tag = tags[predicted.item()]
        #
        #     probs = torch.softmax(output, dim=1)
        #     prob = probs[0][predicted.item()]
        #
        #     if prob.item() > 0.75:
        #         for intent in intents["intents"]:
        #             if tag == intent["tag"]:
        #                 print(f"{bot_name}: {random.choice(intent['response'])}")
        #     else:
        #         print(f"{bot_name}:i do not understand...")


        #text is user's message
        for intent in intents["intents"]:
            if text == 'hi' or text == 'hey' or text == 'hello':
                response = "Hey. I am Bitbot for more information type info."
                self.add_message(response, 'left', self.bot_message_color),
            elif text==tag==intent["tag"]:
                response==(f"{random.choice(intent['response'])}")
                self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'info':
            #     response = "Bitbot can answer question like:\n" " - what is bitcoin price? for cryptocurrency price \n" " - what is bitcoin? for theritical aspect \n" " - website. for open website of cryptoccurency trading \n" " - what is the change of percentage for bitcoin for 1 hour? for getting the percentage of changing in hour \n" " - what is the change of percentage for bitcoin for 24 hours?  for getting the percentage of changing for 24hours \n" " - what is the change of percentage for bitcoin for one month? for getting the percentage of changing for one month \n"
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'website'or text=='navigate me to the website' or text=='provide me a website':
            #     webbrowser.open(r"https://coinmarketcap.com/")
            #     response = "hope that help."
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'how are you?':
            #     response = "I am fine thank you"
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'bye' or text == 'cao' or text == 'goodbye':
            #     response = "Bye hope to see you again"
            #     self.add_message(response, 'left', self.bot_message_color),
            #
            #     ## THEORITICAL ASPECT
            # elif text == 'what is bitcoin?':
            #     response = "Bitcoin is a cryptocurrency invented in 2008 by an unknown person or group of people using the name Satoshi Nakamoto. The currency began use in 2009 when its implementation was released as open-source software."
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is ethereum?':
            #     response = "Ethereum is a decentralized, open-source blockchain featuring smart contract functionality. Ether is the native cryptocurrency of the platform. It is the second-largest cryptocurrency by market capitalization, after Bitcoin. Ethereum is the most actively used blockchain"
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is litecoin?':
            #     response = "Litecoin is a peer-to-peer cryptocurrency and open-source software project released under the MIT/X11 license. Litecoin was an early bitcoin spinoff or altcoin, starting in October 2011. In technical details, Litecoin is nearly identical to Bitcoin."
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is xpr?':
            #     response = "XPR is often referred to as 'real cryptocurrency'; it is a token that uses Ripple network to enable money transfers between various currencies. Most clearing systems nowadays use US dollars as a base currency for conversion. "
            #     self.add_message(response, 'left', self.bot_message_color),
            #
            # elif text == 'Satoshi Nakamoto' or text== 'Satoshi' or text== 'bitcoin creator' or text=='who create bitcoin?':
            #     response = "Satoshi Nakamoto is the name used by the presumed pseudonymous person or persons who developed bitcoin, authored the bitcoin white paper, and created and deployed bitcoin's original reference implementation. As part of the implementation, Nakamoto also devised the first blockchain database.In the process, Nakamoto was the first to solve the double-spending problem for digital currency using a peer-to-peer network. Nakamoto was active in the development of bitcoin up until December 2010.Many people have claimed, or have been claimed, to be Nakamoto. "
            #     self.add_message(response, 'left', self.bot_message_color),
            #
            # elif text == 'Gavin Wood'or text=='Gavin' or text=='ethereum creator' or text=='who create ethereum?':
            #     response = "Gavin Wood is a British computer programmer, co-founder of Ethereum and creator of Polkadot. He invented Solidity and wrote the Yellow Paper specifying the Ethereum Virtual Machine. Wood served as the Ethereum Foundation's first chief technology officer. After leaving Ethereum in 2016, he co-founded Parity Technologies (formerly Ethcore), which develops core infrastructure for Ethereum, Bitcoin, Zcash and Polkadot. "
            #     self.add_message(response, 'left', self.bot_message_color),
            #
            # elif text == 'Charlie Lee'or text=='Charlie' or text=='litecoin creator' or text=='who create litecoin?':
            #     response = "Charles Lee is a computer scientist, best known as the creator of Litecoin. He serves as the managing director of the Litecoin Foundation.As of July 2013, he also worked for Coinbase."
            #     self.add_message(response, 'left', self.bot_message_color),
            #
            # elif text == 'Jed McCaleb'or text=='Jed' or text=='xpr creator' or text=='who create xpr?':
            #     response = "Jed McCaleb is an American programmer and entrepreneur. He is a co-founder and the CTO of Stellar.Prior to co-founding Stellar, McCaleb founded and served as the CTO of the company Ripple until 2013. McCaleb is also known for creating Mt. Gox, and the peer-to-peer eDonkey and Overnet networks as well as the eDonkey2000 application."
            #     self.add_message(response, 'left', self.bot_message_color),
            #
            #     ## cryptoccurency prices
            # elif text == 'what is bitcoin price?'or text=='bitcoin price'or text=='price of bitcoin'or text=='btc' or text=='BTC':
            #     response = "The Bitcoin price is " + "{:.2f}$".format(float(get_cmc_data('BTC')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is ethereum price?'or text=='ethereum price'or text=='price of ethereum'or text=='eth' or text=='ETH':
            #     response = "The Ethereum price is " + "{:.2f}$".format(float(get_cmc_data('ETH')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is litecoin price?'or text=='litecoin price'or text=='price of litecoin'or text=='ltc' or text=='LTC':
            #     response = "The Litecoin price is " + "{:.2f}$".format(float(get_cmc_data('LTC')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is xpr price?'or text=='xpr price'or text=='price of xpr'or text=='xpr' or text=='XPR':
            #     response = "The XPR price is " + "{:.2f}$".format(float(get_cmc_data('XPR')))
            #     self.add_message(response, 'left', self.bot_message_color),
            #
            #     ##cryptoccurency percentage changes for 1hour
            # elif text == 'what is the change of percentage for bitcoin for 1 hour?' :
            #     response = "The percentage of bitcoin change for 1 hour is  " + "{:.2f}%".format(
            #         float(get_hour_data('BTC')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is the change percentage for ethereum for 1 hour?'or text=='ethereum change 1 hour'or text=='ethereum change one hour'or text=='1 hour change for ethereum'or text== 'eth 1 hour change':
            #     response = "The percentage for ethereum change for 1 hour is  " + "{:.2f}%".format(
            #         float(get_hour_data('ETH')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is the change of percentage for litecoin for 1 hour?'or text=='litecoin change 1 hour'or text=='litecoin change one hour'or text=='1 hour change for litecoin'or text== 'ltc 1 hour change':
            #     response = "The percentage for litecoin change for 1 hour is  " + "{:.2f}%".format(
            #         float(get_hour_data('LTC')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is the change of percentage for xpr for 1 hour?'or text=='xpr change 1 hour'or text=='xpr change one hour'or text=='1 hour change for xpr'or text== 'xpr 1 hour change':
            #     response = "The percentage for xpr change for 1 hour is   " + "{:.2f}%".format(float(get_hour_data('XPR')))
            #     self.add_message(response, 'left', self.bot_message_color),
            #
            #     ##cryptoccurency percentage changes for 24hour
            # elif text == 'what is the change of percentage for bitcoin for 24 hours?'or text=='bitcoin change 24 hours'or text=='24 hours change for bitcoin'or text== 'btc 24 hours change':
            #     response = "The percentage for bitcoin change for 24 hours is  " + "{:.2f}%".format(
            #         float(get_twentyhour_data('BTC')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is the change of percentage for ethereum for 24 hours?'or text=='ethereum change 24 hours'or text=='24 hours change for ethereum'or text== 'eth 24 hours change':
            #     response = "The percentage for ethereum change for 24 hours is  " + "{:.2f}%".format(
            #         float(get_twentyhour_data('ETH')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is the change of percentage for litecoin for 24 hour?'or text=='litecoin change 24 hours'or text=='24 hours change for litecoin'or text== 'ltc 24 hours change':
            #     response = "The percentage for litecoin change for 24 hour is   " + "{:.2f}%".format(
            #         float(get_twentyhour_data('LTC')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is the change of percentage for xpr for 24 hour?'or text=='xpr change 24 hours'or text=='24 hours change for xpr'or text== 'xpr 24 hours change':
            #     response = "The percentage for xpr change for 24 hour is   " + "{:.2f}%".format(
            #         float(get_twentyhour_data('XPR')))
            #     self.add_message(response, 'left', self.bot_message_color),
            #
            #     ##cryptoccurency percentage changes for 1month
            # elif text == 'what is the change of percentage for bitcoin for one month?'or text=='bitcoin change 1 month'or text=='bitcoin change one month'or text=='1 month change for bitcoin'or text== 'btc 1 month change':
            #     response = "The percentage for bitcoin change for one month is  " + "{:.2f}%".format(
            #         float(get_onemonth_data('BTC')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is the change of percentage for ethereum for one month?'or text=='ethereum change 1 month'or text=='ethereum change one month'or text=='1 month change for ethereum'or text== 'eth 1 month change':
            #     response = "The percentage for ethereum change for one month is  " + "{:.2f}%".format(
            #         float(get_onemonth_data('ETH')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is the change of percentage for litecoin for one month?'or text=='litecoin change 1 month'or text=='litecoin change one month'or text=='1 month change for litecoin'or text== 'ltc 1 month change':
            #     response = "The percentage for litecoin change for one month is  " + "{:.2f}%".format(
            #         float(get_onemonth_data('LTC')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # elif text == 'what is the cahnge of percentage for xpr for one month?'or text=='xpr change 1 month'or text=='xpr change one month'or text=='1 month change for xpr'or text== 'xpr 1 month change':
            #     response = "The percentage for xpr change for one month is  " + "{:.2f}%".format(
            #         float(get_onemonth_data('XPR')))
            #     self.add_message(response, 'left', self.bot_message_color),
            # else:
            #     response = "i do not understand, try again"
            #    self.add_message(response, 'left', self.bot_message_color),

    def add_message(self, text, side, color):
        # create a message for the recycleview
        self.messages.append({
            'message_id': len(self.messages),
            'text': text,
            'side': side,
            'bg_color': color,
            'text_size': [None, None],
        })

    def update_message_size(self, message_id, texture_size):
        # when the label is updated, we want to make sure the displayed size is
        # proper

        max_width = self.ids.box.width
        one_line = dp(50)

        # if the texture is too big, limit its size
        if texture_size[0] >= max_width * 2 / 3:
            self.messages[message_id] = {
                **self.messages[message_id],
                'text_size': (max_width * 2 / 3, None),
                '_size': texture_size,
            }

        # if it was limited, but is now too small to be limited, raise the limit
        elif texture_size[0] < max_width * 2 / 3 and \
                texture_size[1] > one_line:
            self.messages[message_id] = {
                **self.messages[message_id],
                'text_size': (max_width * 2 / 3, None),
                '_size': texture_size,
            }

        # just set the size
        else:
            self.messages[message_id] = {
                **self.messages[message_id],
                '_size': texture_size,
            }

    @staticmethod
    def focus_textinput(textinput):
        textinput.focus = True

    def send_message(self, textinput):
        text = textinput.text.strip()
        send_btn = self.ids.send_btn
        if text == '':
            self.focus_textinput(textinput)
            # elif text == 'how are you?':
            #    self.focus_textinput(textinput)
            return

        def enable_send_btn(dt):
            send_btn.disabled = False

        if self.user_message_delay > 0:
            send_btn.disabled = True
            Clock.schedule_once(enable_send_btn, self.user_message_delay)

        textinput.text = ''
        self.add_message(text, 'right', self.user_message_color)
        self.focus_textinput(textinput)
        Clock.schedule_once(lambda *args: self.answer(text), self.delay)
        self.scroll_bottom()

    def scroll_bottom(self):
        rv = self.ids.rv
        box = self.ids.box
        if rv.height < box.height:
            Animation.cancel_all(rv, 'scroll_y')
            Animation(scroll_y=0, t='out_quad', d=.5).start(rv)


class BackButton(ButtonBehavior, BoxLayout):
    pass


Builder.load_file('chat.kv')
