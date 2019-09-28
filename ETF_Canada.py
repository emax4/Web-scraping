import requests 
from bs4 import BeautifulSoup
import pandas as pd

url = r"https://en.wikipedia.org/wiki/List_of_Canadian_exchange-traded_funds"
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.text, "html.parser")

# find all table rows
table_list = []
trtags = soup.findAll('tr')
for row in trtags:
    trtag = row.findAll('td')
    table_row = [td.get_text() for td in trtag]
    table_row = [td.strip() for td in table_row]
    table_list.append(table_row)

# Find table head
thtag = trtags[0].findAll('th')
table_headers = [th.get_text() for th in thtag]
table_headers = [th.strip() for th in table_headers]


# Pass lists to dataframe
etf = pd.DataFrame.from_records(table_list[1:])

# Rename columns
etf.columns = table_headers

# Remove TSX:
etf['Symbol'] = etf['Symbol'].str.replace('TSX: ', '')
# etf.to_csv('etf_canada.csv')
