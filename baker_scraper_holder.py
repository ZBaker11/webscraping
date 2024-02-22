import csv
import json
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
def get_stock(driver, ticker_symbol):
    url = f'https://finance.yahoo.com/quote/{ticker_symbol}/holders'
    r = driver.get(url, headers=headers)  # will add timeout here
    soup = BeautifulSoup(r.text, 'html.parser')

    # Extract stock data from the HTML
    stock = {
        'ticker': ticker_symbol,
        'Major Holders 1': soup.find('table', {'class': 'W(100%) M(0) BdB Bdc($seperatorColor)'}).find_all('tr')[0].text.strip(),
        'Major Holders 2': soup.find('table', {'class': 'W(100%) M(0) BdB Bdc($seperatorColor)'}).find_all('tr')[1].text.strip(),
        'Major Holders 3': soup.find('table', {'class': 'W(100%) M(0) BdB Bdc($seperatorColor)'}).find_all('tr')[2].text.strip(),
        'Major Holders 4': soup.find('table', {'class': 'W(100%) M(0) BdB Bdc($seperatorColor)'}).find_all('tr')[3].text.strip(),
        'Top Institutional Holder 1': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            0].text.strip(),
        'Top Institutional Holder 2': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            5].text.strip(),
        'Top Institutional Holder 3': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            10].text.strip(),
        'Top Institutional Holder 4': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            15].text.strip(),
        'Top Institutional Holder 5': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            20].text.strip(),
        'Top Institutional Holder 6': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            25].text.strip(),
        'Top Institutional Holder 7': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            30].text.strip(),
        'Top Institutional Holder 8': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            35].text.strip(),
        'Top Institutional Holder 9': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            40].text.strip(),
        'Top Institutional Holder 10': soup.find('table', {'class': 'W(100%) BdB Bdc($seperatorColor)'}).find_all('td')[
            45].text.strip(),
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
with open('C:/Users/zachb/PycharmProjects/webscraping/stock_holder_data.json', 'w', encoding='utf-8') as f:
    json.dump(stockdata, f)

# Writing stock data to a CSV file with aligned values
CSV_FILE_PATH = 'C:/Users/zachb/PycharmProjects/webscraping/stock_holder_data.csv'
with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = stockdata[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(stockdata)

# Writing stock data to an Excel file
EXCEL_FILE_PATH = 'C:/Users/zachb/PycharmProjects/webscraping/stock_holder_data.xlsx'
df = pd.DataFrame(stockdata)
df.to_excel(EXCEL_FILE_PATH, index=False)



