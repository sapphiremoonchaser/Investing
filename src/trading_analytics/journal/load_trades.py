from multiprocessing.connection import default_family

import pandas as pd
from trading_analytics.data.data_model.trade_entry import Brokerage, SecurityType, TradeAction, TradeStrategy
from trading_analytics.data.data_model.stock_entry import StockEntry
from trading_analytics.data.data_model.dividend_entry import DividendEntry
from trading_analytics.data.data_model.option_entry import OptionEntry, OptionType
import logging

# Configure logging to a file
logging_file_path = "C:/Users/viole/dev/Investing-logging/loading_trade_errors.log"
logging.basicConfig(filename=logging_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def load_trades_from_excel(file_path: str) -> list:
    # Read excel file
    df = pd.read_excel(file_path)

    trades = []
    for _, row in df.iterrows():
        # Parse strategy as a list of TradeStrategy enums
        strategy_str = row["strategy"]
        if pd.isna(strategy_str):
            # default if strategy is empty in excel
            strategies = [TradeStrategy.BASIC_TRADE]
        else:
            # Split comma-separated strategies and convert to enums
            strategy_list = [s.strip().upper() for s in strategy_str.split(",")]
            try:
                strategies = [TradeStrategy[s] for s in strategy_list]
            except KeyError as e:
                print(f"Invalid strategy in row {row}: {e}")
                continue


        # Common fields for all trade types
        common_fields = {
            "trade_id": int(row["trade_id"]),
            "strategy_id": int(row["strategy_id"]),
            "brokerage": Brokerage(row["brokerage"]),
            "account": str(row["account"]),
            "strategy": strategies,
            "security": SecurityType(row["security_type"]),
            "trade_date": pd.to_datetime(row["trade_date"]).date(),
            "symbol": str(row["symbol"]),
            "action": TradeAction(row["action"]),
            "quantity": float(row["quantity"]),
            "fees": float(row["fees"]),
        }

        # Create appropriate entry based on security type
        try:
            if common_fields['security'] == SecurityType.STOCK:
                trade = StockEntry(
                    **common_fields,
                    price_per_share=float(row["price_per_share"])
                )
            elif common_fields['security'] == SecurityType.DIVIDEND:
                trade = DividendEntry(
                    **common_fields,
                    dividend_amount=float(row["dividend_amount"])
                )
            elif common_fields['security'] == SecurityType.OPTION:
                trade = OptionEntry(
                    **common_fields,
                    expiration_date=pd.to_datetime(row["expiration_date"]).date(),
                    strike=float(row["strike"]),
                    premium=float(row["premium"]),
                    option_type=OptionType[row["option_type"].upper()]
                )
            else:
                raise ValueError(f"Put in the right security type, biotch! Choose from list({SecurityType}. You entered {common_fields['security']}")
            trades.append(trade)
        except (KeyError, ValueError) as e:
            print(f"Error processing {row}: {e}")
            continue

    return trades
