import telebot
import os
import json
from dotenv import load_dotenv

import requests


load_dotenv()
BOT_API_KEY=os.getenv("BOT_API_KEY")
YAHOO_API_KEY=os.getenv("YAHOO_API_KEY")

bot=telebot.TeleBot(BOT_API_KEY)

@bot.message_handler(commands=['start','greet'])
def greet(message):
    bot.send_message(message.chat.id,"Hello! Welcome to your personal Trader Buddy")


def quote_request(message):
    request=message.text.split(' ')
    if len(request)<2 or request[0].lower() not in "quote":
        return False
    else:
        return True

@bot.message_handler(func=quote_request)
def get_quote(message):
    #function to return the daily high, daily low, and the daily range
    stocks=message.text.split(' ')[1:]
    requested_stocks=','.join(i.upper() for i in stocks)
    print(requested_stocks)
    url = "https://rest.yahoofinanceapi.com/v6/finance/quote"

    querystring = {"symbols":requested_stocks}

    headers = {
    'x-api-key': YAHOO_API_KEY
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    quote=json.loads(response.text)
    if(len(quote["quoteResponse"]["result"])>0):
        stock_results=quote["quoteResponse"]["result"]
        market_price_ranges=[]
        for i in stock_results:
            market_price_ranges.append(i["shortName"]+"  \nPrevious Day Close Price: "+str(i["regularMarketPreviousClose"])+" "+i["currency"]+"  \nCurrent Day Open Price: "+str(i["regularMarketOpen"])+" "+i["currency"]+"  \nDaily Market Range: "+i["regularMarketDayRange"]+" "+i["currency"])
        market_price_range='\n\n\n'.join(market_price_ranges)
        bot.send_message(message.chat.id,market_price_range)
    else:
        bot.send_message(message.chat.id, "Data related to these stocks weren't found. Check them again?")





bot.polling()