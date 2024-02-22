import csv
import json
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
def get_stock(driver, ticker_symbol):
    url = f'https://finance.yahoo.com/quote/{ticker_symbol}'
    r = driver.get(url)  # will add timeout here
    soup = BeautifulSoup(r.text, 'html.parser')

    # Extract stock data from the HTML
    stock = {
        'ticker': ticker_symbol,
        'regularMarketPrice': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text.strip(),
        'regularMarketChange': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[1].text.strip(),
        'regularMarketChangePercent': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[2].text.strip(),
        'quote': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[2].text.strip(),

        # scraping the stock data from the "Summary" table
        'previous_close': soup.find('table', {'class': 'W(100%)'}).find_all('td')[1].text.strip(),
        'open_value': soup.find('table', {'class': 'W(100%)'}).find_all('td')[3].text.strip(),
        'bid': soup.find('table', {'class': 'W(100%)'}).find_all('td')[5].text.strip(),
        'ask': soup.find('table', {'class': 'W(100%)'}).find_all('td')[7].text.strip(),
        'days_range': soup.find('table', {'class': 'W(100%)'}).find_all('td')[9].text.strip(),
        'week_range': soup.find('table', {'class': 'W(100%)'}).find_all('td')[11].text.strip(),
        'volume': soup.find('table', {'class': 'W(100%)'}).find_all('td')[13].text.strip(),
        'avg_volume': soup.find('table', {'class': 'W(100%)'}).find_all('td')[5].text.strip(),
        'market_cap': soup.find('table', {'class': 'W(100%) M(0) Bdcl(c)'}).find_all('td')[1].text.strip(),
        'beta': soup.find('table', {'class': 'W(100%) M(0) Bdcl(c)'}).find_all('td')[3].text.strip(),
        'pe_ratio': soup.find('table', {'class': 'W(100%) M(0) Bdcl(c)'}).find_all('td')[5].text.strip(),
        'eps': soup.find('table', {'class': 'W(100%) M(0) Bdcl(c)'}).find_all('td')[7].text.strip(),
        'earnings_date': soup.find('table', {'class': 'W(100%) M(0) Bdcl(c)'}).find_all('td')[9].text.strip(),
        'dividend_yield': soup.find('table', {'class': 'W(100%) M(0) Bdcl(c)'}).find_all('td')[11].text.strip(),
        'ex_dividend_date': soup.find('table', {'class': 'W(100%) M(0) Bdcl(c)'}).find_all('td')[13].text.strip(),
        'year_target_est': soup.find('table', {'class': 'W(100%) M(0) Bdcl(c)'}).find_all('td')[15].text.strip(),
    }
    return stock


if len(sys.argv) < 2:
    print("Usage: python script.py <ticker_symbol1> <ticker_symbol2> ...")
    sys.exit(1)

# Extract ticker symbols from command line arguments
ticker_symbols = sys.argv[1:]
# Get stock data for each ticker symbol
stockdata = [get_stock(requests, symbol) for symbol in ticker_symbols]

# Writing stock data to a JSON file
with open('C:/Users/zachb/PycharmProjects/webscraping/stock_data.json', 'w', encoding='utf-8') as f:
    json.dump(stockdata, f)

# Writing stock data to a CSV file with aligned values
CSV_FILE_PATH = 'C:/Users/zachb/PycharmProjects/webscraping/stock_data.csv'
with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = stockdata[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(stockdata)

# Writing stock data to an Excel file
EXCEL_FILE_PATH = 'C:/Users/zachb/PycharmProjects/webscraping/stock_data.xlsx'
df = pd.DataFrame(stockdata)
df.to_excel(EXCEL_FILE_PATH, index=False)



