#importing files
import telebot
import os
import json
from dotenv import load_dotenv
import requests


load_dotenv()
BOT_API_KEY=os.getenv("BOT_API_KEY")
YAHOO_API_KEY=os.getenv("YAHOO_API_KEY")

#create the bot
bot=telebot.TeleBot(BOT_API_KEY)


#deal with start or greet command
@bot.message_handler(commands=['start','greet'])
def greet(message):
    bot.send_message(message.chat.id,"Hello! Welcome to your personal Trader Buddy")




#returning market price information about a stock
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




#returning trending stocks in a market
def trending_request(message):
    request=message.text.split(' ')
    if len(request)<2 or request[0].lower() not in "trending":
        return False
    else:
        return True



@bot.message_handler(func=trending_request)
def get_trending_stocks(message):
    regions=message.text.split(' ')[1:]
    basic_url='https://yfapi.net/v1/finance/trending/'
    headers = {
    'x-api-key': YAHOO_API_KEY
    }
    regions_allowed=['US','AU','CA','FR','DE','HK','US','IT','ES','GB','IN']
    regions_allowed=set(regions_allowed)
    stocks_symbols=[]
    region_string=[]
    for i in regions:
        if i not in regions_allowed:
            continue
        url=basic_url+i.upper()
        response = requests.request("GET", url, headers=headers)
        print(response.text)
        response=json.loads(response.text)
       
        trending_stocks=response["finance"]["result"][0]["quotes"][0:5]
        for j in trending_stocks:
            stocks_symbols.append(j['symbol'])
        stocks_string=', '.join(stocks_symbols)
        region_string.append(("Trending stocks in "+i+"\n"+stocks_string))
    if(len(region_string))==0:
        return_text="Error, please check the regions and try again"
    else:
        return_text='\n\n'.join(region_string)
    bot.send_message(message.chat.id,return_text)



bot.polling()