#Stocks from DAX, MDAX, SDAX, ATX, S&P500, Nasdaq, EuroStoxx500,
#import python libraries

#import yfinance as yf
#import pandas as pd
#from yahoofinancials import YahooFinancials

#import time
#import datetime

#df_yahoo.tail()
#df_yahoo.head()

#ticker = yf.Ticker("AAPL")
#aapl_df = ticker.history(period="5y")
#aapl_df['Close'].plot(title="APPLE's stock price")

#df_yahoo = yf.download("FB",
#start='2020-09-15',
#end='2020-11-15',
#progress=False)


import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests


def save_dax_tickers():
    resp = requests.get('https://de.wikipedia.org/wiki/DAX')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        if ticker.endswith("\n"):
            ticker = ticker[:-1]
        tickers.append(ticker)
    with open("daxtickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers

    pass

import yfinance as yf
import yahoofinancials
import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests


def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        if ticker.endswith("\n"):
            ticker = ticker[:-1]
        tickers.append(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers


# save_sp500_tickers()
def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime.now()
    close_data = []
    for ticker in tickers:
        df_yahoo = yf.download(ticker,
                               start='2020-09-15',
                               end='2020-11-15',
                               progress=False)
        df_yahoo = df_yahoo.Close
        df_yahoo.name = ticker + "_Close"
        if not df_yahoo.empty:
            close_data.append(df_yahoo)
    close_data = pd.concat(
        close_data,
        axis=1,
        join="outer"
    )
    close_data.to_csv(r"C:\Users\fmuel\OneDrive\Desktop\S&P500.csv")
    pass

if __name__ == '__main__':
    save_sp500_tickers()
    get_data_from_yahoo()
