import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from termcolor import colored
import keyboard
import os



endDate = datetime.today()

if datetime.weekday(endDate) > 4:
    endDate = endDate - timedelta(days=(datetime.weekday(endDate) - 4))

startDate = endDate - timedelta(days=10)

if datetime.weekday(startDate) > 4:
    startDate = startDate - timedelta(days=(datetime.weekday(startDate) - 4))


tickers_list = []

stockTicker = input("Enter ticker symbol for Stock \n")


while(stockTicker != "0"):
    tickers_list.append(stockTicker)
    stockTicker = input("Enter ticker symbol for Stock or Enter '0' to continue \n")
    #print(tickers_list)

os.system('cls' if os.name == 'nt' else 'clear')


data = pd.DataFrame(columns=tickers_list)

ticker_data = {}
closing_data_8_day = {}
closing_data_50_day = {}

eight_day_moving_average = {}
fifty_day_moving_average = {}


for ticker in tickers_list:
    ticker = ticker.upper()
    try:
        stock_data = yf.download(ticker, startDate, endDate, progress=False)
    except:
        print(f"{ticker} is invalid")
    else:

        try:
            date = f"{yf.Ticker(ticker).cash_flow.columns[0]}"
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except:
            continue

        if 'Adj Close' in stock_data.columns:  
                closing_prices = stock_data['Adj Close'].values
                closing_data_8_day[ticker] = closing_prices
        else:
            print(f"Warning: 'Adj Close' not found for {ticker}")


startDate = endDate - timedelta(days=60)

if datetime.weekday(startDate) > 4:
    startDate = startDate - timedelta(days=(datetime.weekday(startDate) - 4))


for ticker in tickers_list:
    ticker = ticker.upper()
    try:
        stock_data = yf.download(ticker, startDate, endDate, progress=False)
    except:
        print(f"{ticker} is invalid")
    else:
        try:
            date = f"{yf.Ticker(ticker).cash_flow.columns[0]}"
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except:
            continue
        if 'Adj Close' in stock_data.columns:
            closing_prices = stock_data['Adj Close'].values
            closing_data_50_day[ticker] = closing_prices
        else:
            print(f"Warning: 'Adj Close' not found for {ticker}")

def averageFinder(prices):
    return sum(prices) / len(prices) 


for ticker, prices in closing_data_8_day.items():
    eight_day_moving_average[ticker] = averageFinder(prices)
    
for ticker, prices in closing_data_50_day.items():
    print(colored(ticker, attrs=['bold'])) 
    fifty_day_moving_average[ticker] = averageFinder(prices)
    print("8-day moving average")
    if(eight_day_moving_average[ticker] > fifty_day_moving_average[ticker] or eight_day_moving_average[ticker] == fifty_day_moving_average[ticker]):
        print(colored(eight_day_moving_average[ticker], 'green'))  
    else:
        print(colored(eight_day_moving_average[ticker], 'red'))
    print("50-day moving average")
    if(eight_day_moving_average[ticker] < fifty_day_moving_average[ticker]):
        print(colored(f"{fifty_day_moving_average[ticker]} \n", 'green'))
    else:
        print(colored(f"{fifty_day_moving_average[ticker]} \n", "red"))
    
print("Press Escape key to exit.")
while True:
    if keyboard.is_pressed('esc'):
        break



