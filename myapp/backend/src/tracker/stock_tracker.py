from const.const import API_KEY, STOCK_HISTORY_API_KEY
import requests
import json
import yfinance as yf
class Stock:
    current_price = 0
    high_today = 0
    low_today = 0
    open_price = 0
    previous_close = 0
    _ticker = ""
    name = ""
    currency = "USD"
    _history = {}

    def update_name(self):
        url = f"https://finnhub.io/api/v1/stock/profile2?symbol={self._ticker}&token={API_KEY}"
        response = requests.get(url)
        data = response.json()
        self.name = data.get("name", self._ticker)

    # get stock history
    # type here is the stock history in months or in years (MONTH, YEAR)
    # for now the type is not exist yet
    def get_stock_history(self):

        data = yf.download(self._ticker, period="1mo", interval="1d")

        data.columns = [col[0] for col in data.columns]
        data = data.reset_index()
        #remove timezone info from Date column
        data["Date"] = data["Date"].astype(str)
        data["Date"] = data["Date"].str.replace("T00:00:00Z", "")

        history = []

        for _, row in data.iterrows():
            history.append({
                "date": str(row["Date"]),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"])
            })

        return history
    
    def update(self):
        url = f"https://finnhub.io/api/v1/quote?symbol={self._ticker}&token={API_KEY}"
        response = requests.get(url)
        data = response.json()
        self.current_price = data["c"]
        self.high_today = data["h"]
        self.low_today = data["l"]
        self.open_price = data["o"]
        self.previous_close = data["pc"]
        self.update_name()
        if self.currency != "USD":
            self.exchange_to_currency()
        else:
            self.currency = "USD"
    #get set 
    def get_key(self):
        return self._ticker
    
    def __init__(self, ticker):
        self._ticker = ticker
        self.update()


class StockTracker:
    _stocks = {}
    _currency = "USD"
    def __init__(self):
        self._stocks = {
            "AAPL": Stock("AAPL"),
            "GOOGL": Stock("GOOGL"),
            "AMZN": Stock("AMZN")
        }
        self._currency = "USD"
    
    def get_currency(self):
        return self._currency
    
    def get_stocks(self):
        return self._stocks

    def add_stock(self, ticker):
        if ticker not in self._stocks:
            self._stocks[ticker] = Stock(ticker)

    def update_all(self):
        for stock in self._stocks.values():
            stock.update()

    def exchange_currency(self, currency):
        url = f"https://open.er-api.com/v6/latest/{self._currency}"
        data = requests.get(url).json()
        rate = data["rates"][currency]

        for stock in self._stocks.values():
            stock.current_price *= rate
            stock.high_today *= rate
            stock.low_today *= rate
            stock.open_price *= rate
            stock.previous_close *= rate
            stock.currency = currency

        self._currency = currency
    def get_stock_history(self, key):
        return self._stocks[key].get_stock_history()
    


            

        
