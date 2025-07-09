import json
import os.path

from src.data.data_model.market.stock_data import CurrentStockData
from utilities.fetch_market_data import fetch_current_stock_price


def __main__(json_file_path: str) -> None:

    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"Yo, your file is missing dawg! {json_file_path}")

    with open(json_file_path, "r") as file:
        data = json.load(file)

    stock_entries = []
    for entry in data:
        symbol = entry.get("symbol")
        if symbol:
            try:
                stock_data = fetch_current_stock_price(symbol)
                stock_entries.append(stock_data)
            except ValueError as e:
                print(f"Error fetching price for {symbol}: {e}")
        else:
            print("Skipping entry with missing or invalid symbol.")

    x = 1


if __name__ == "__main__":
    __main__(json_file_path="dummy_stock_data.json")