
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import time
from yahoo_historical import Fetcher


# ## Read ETF Table


etf_df = pd.read_csv('Files/etf_canada.csv')

etf_df = etf_df[['Symbol', 'Issuer', 'Name', 'Asset Class',
                 'Inception Date', 'Total Assets (MM)', 'MER', 'Inverse', 'Leveraged',
                 'Currency Hedged', 'Active Managed']].copy()


# ## Extract all ETF Total Assets and P/E Ratio

# ### ETF class to extract financial metrics


class etf():
    def __init__(self, tickers=None):
        """

        :param tickers: List of tickers
        """
        self.tickers = tickers
        self.key_stats = ['P/E Ratio', 'Market Cap1', 'P/B Ratio', 'Beta:']

    def get_etf_profile(self, ticker):
        """
        Get financial metrics for individual ticker
        :param ticker: 1 ticker
        :return: dictionary of financial metrics
        """
        url = r"https://web.tmxmoney.com/quote.php?qm_symbol={}".format(ticker)
        response = requests.get(url)
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            raw_txt = soup.get_text()
            raw_txt = re.sub('[\r\n\t]', ' ', raw_txt)

            stat_dict = {}

            for stat in self.key_stats:
                stat_regex = re.search(f'{stat}', raw_txt)
                position = stat_regex.span()[1]
                text = raw_txt[position + 1: position + 25]
                text = text.lstrip()
                stat_dict[stat] = text[:text.find(' ')]

            details = {ticker: stat_dict}
            return details
        except:
            return None

    def extract(self):
        """
        calls get_etf_profile for list of tickers
        :return: pandas dataframe of financial metrics
        """
        # Set empty dataframe for storing
        df = pd.DataFrame()

        # Loop through etf list to get details
        for index, tick in enumerate(self.tickers):
            profile = self.get_etf_profile(tick)

            # pause
            time.sleep(3)

            if profile is not None:
                df_sub = pd.DataFrame.from_dict(profile, orient='index')
                df = df.append(df_sub)
        return df


etf_list = etf_df.Symbol.tolist()

etf_details = etf(etf_list).extract()


#etf_details.to_csv('etf_all.csv')


# ## Extract historical data

def data_fetcher(etflist, start, end):
    """
    Takes in a list of etf symbols
    returns pandas dataframe of price details and dividends
    """
    price_df = pd.DataFrame()
    errors = []
    for e in etflist:
        try:
            data = Fetcher(e, start, end)
            pricedata = data.getHistorical()
            if 'Date' in data.getHistorical().columns.tolist():
                pricedata['ticker'] = e
                price_df = price_df.append(pricedata)
        except KeyError:
            errors.append(e)
        else:
            pass

    return price_df, errors


etf_his_list = [re.sub(r'\.', '-', i) + '.TO' for i in etf_details.index.tolist()]
etf_history, err = data_fetcher(etf_his_list, [2012, 1, 1], [2019, 9, 21])

#etf_history.to_csv('etf_history.csv')



