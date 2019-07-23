import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.iata.org/about/members/Pages/airline-list.aspx?All=true'
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.text, "html.parser")
#iata_table = soup.findAll('table', {'class':'basictable-2'})

#iata_rows = soup.findAll('tr', {'class':'blue'})


def substring_indexes(substring, string):
    """ 
    Generate indices of where substring begins in string

    >>> list(find_substring('me', "The cat says meow, meow"))
    [13, 19]
    """
    last_found = -1  # Begin at -1 so the next position to search from is 0
    while True:
        # Find next index of substring, by starting after its last known position
        last_found = string.find(substring, last_found + 1)
        if last_found == -1:  
            break  # All occurrences have been found
        yield last_found

# find all table rows
mytable_list = []

trtags = soup.findAll('tr')
for row in trtags:
    trtags = row.findAll('td')
    if len(trtags) == 5:
            #empty = []
            empty = [td.get_text() for td in trtags]
            mytable_list.append(empty)

# Pass lists to dataframe
iata_df = pd.DataFrame.from_records(mytable_list[1:])
iata_df.columns = mytable_list[0]
