import json
import os.path

from trading_analytics.data.data_model.entry.stock_entry import StockEntry


def __main(json_file_path: str) -> None:
    """This function is the main function for the example

    :param json_file_path: filepath to json file

    :return: None
    """
    if not os.path.exists(json_file_path):
        FileNotFoundError(f"Yo, your file is missing dawg! {json_file_path}")

    with open(json_file_path, "r") as file:
        data = json.load(file)

    stock_entries = []
    for entry in data:
        stock_entries.append(
            StockEntry(**entry)
        )

    x = 1


if __name__ == "__main__":
    __main(
        json_file_path="dummy_stock_trades.json",
    )