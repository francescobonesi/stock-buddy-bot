class Portfolio:
    def __init__(self):
        self._data = self._extract_data()
        self._price_references = self._extract_buy_references()
        self._collected_data = None

    @staticmethod
    def _extract_data():
        import csv
        with open("portfolio.csv", "r") as file:
            return list(csv.DictReader(file, delimiter=","))

    def _extract_buy_references(self):
        references = {}
        for elem in self._data:
            if elem.get("operation") != "buy":
                continue
            references[elem.get("reference")] = float(elem.get("price"))
        return references

    def elaborate(self, current_price):
        buy = 0
        bought_original_value = 0
        sell = 0
        hold = 0
        hold_original_value = 0
        cashed_original_value = 0
        cashed_value = 0

        for elem in self._data:
            quantity = float(elem.get("quantity"))
            reference = elem.get("reference")
            price = float(elem.get("price"))

            if elem.get("operation") == "buy":
                hold += quantity
                buy += quantity
                hold_original_value += price * quantity
                bought_original_value += price * quantity

            elif elem.get("operation") == "sell":
                hold -= quantity
                sell += quantity
                cashed_value += quantity * price
                original_sold = self._price_references[reference] * quantity
                hold_original_value -= original_sold
                cashed_original_value += original_sold

        cashed_gain = cashed_value - cashed_original_value
        cashed_increment = cashed_gain / cashed_original_value

        current_value = hold * current_price

        gain_on_hold = current_value - hold_original_value
        gain_on_bought = current_value - bought_original_value
        increment_on_hold = gain_on_hold / hold_original_value
        increment_on_bought = gain_on_bought / bought_original_value

        suggested_shares_to_sell = round(gain_on_bought / current_price, 0)
        is_suggested_to_sell = True if suggested_shares_to_sell >= 1 else False

        self._collected_data = {
            "hold": round(hold, 2),
            "buy": round(buy, 2),
            "bought_original_value": round(bought_original_value, 2),
            "sell": round(sell, 2),
            "hold_original_value": round(hold_original_value, 2),
            "hold_current_value": round(current_value, 2),
            "gain_on_hold": round(gain_on_hold, 2),
            "gain_on_bought": round(gain_on_bought, 2),
            "increment_on_hold": increment_on_hold,
            "increment_on_bought": increment_on_bought,
            "increment_on_hold_percentage":
                f"{'+' if increment_on_hold > 0 else ''}{round(100*increment_on_hold,2)}%",
            "increment_on_bought_percentage":
                f"{'+' if increment_on_bought > 0 else ''}{round(100*increment_on_bought,2)}%",
            "cashed": round(cashed_value, 2),
            "cashed_original_value": round(cashed_original_value, 2),
            "cashed_gain": round(cashed_gain, 2),
            "cashed_increment": cashed_increment,
            "cashed_increment_percentage": f"{'+' if cashed_increment > 0 else ''}{round(100*cashed_increment,2)}%",
            "is_suggested_to_sell": is_suggested_to_sell,
            "suggested_shares_to_sell": suggested_shares_to_sell
        }
        return self._collected_data


if __name__ == '__main__':
    x = Portfolio()
    print(x.elaborate(150))
