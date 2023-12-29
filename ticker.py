import datetime

import yfinance as yf


class TickerData:
    def __init__(self, ticker_name):
        self._ticker_name = ticker_name
        self._ticker = yf.Ticker(ticker_name)
        self._history = self._ticker.history()

    def get_history(self):
        return self._history

    def _get_last_two_closed_date_indexes(self):
        last_index_in_data = self._history.index[-1]
        today_str = str(datetime.date.today())
        print(f"Last index in data: {last_index_in_data}")
        print(f"Today: {today_str}")
        if str(last_index_in_data)[:10] == today_str:
            print("Market is open")
            return self._history.index[-2], self._history.index[-3]
        else:
            print("Market is close")
            return self._history.index[-1], self._history.index[-2]

    def get_last_two_closed_date_prices(self):
        last_date_index, previous_date_index = self._get_last_two_closed_date_indexes()
        last_date_price = self._history.loc[last_date_index]['Close']
        previous_date_price = self._history.loc[previous_date_index]['Close']
        increment = (last_date_price - previous_date_price) / previous_date_price

        return {
            "last_date": str(last_date_index)[:10],
            "price": last_date_price,
            "increment": increment,
            "increment_percentage": round(increment * 100, 2),
            "previous_date": str(previous_date_index)[:10],
            "previous_price": previous_date_price
        }

    def get_now_or_last_updated_price(self):
        last_index_in_data = self._history.index[-1]
        price = self._history.loc[last_index_in_data]['Close']

        previous_index = self._history.index[-2]
        previous_price = self._history.loc[previous_index]['Close']
        increment = (price - previous_price) / previous_price

        return {
            "date": str(last_index_in_data)[:10],
            "price": price,
            "increment": increment,
            "increment_percentage":
                f"{'+' if increment > 0 else ''}{round(increment * 100, 2)}%"
        }
