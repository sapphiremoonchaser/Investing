from multiprocessing.connection import default_family
from operator import index

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
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        logging.error(f"Failed to read Excel file {file_path}. {e}")

    trades = []
    for _, row in df.iterrows():
        # Parse strategy as a list of TradeStrategy enums
        strategy_str = row["strategy"]
        if pd.isna(strategy_str):
            # default if strategy is empty in excel
            strategies = [TradeStrategy.BASIC_TRADE]
        else:
            # Split comma-separated strategies and convert to enums
            strategy_list = [s.strip().upper().replace(" ", "_") for s in strategy_str.split(",")]
            try:
                strategies = [TradeStrategy[s] for s in strategy_list]
            except KeyError as e:
                print(f"Invalid strategy in row {row}: {e}")
                continue


        # Common fields for all trade types
        try:
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
        except (KeyError, ValueError, TypeError) as e:
            logging.error(f"Failed to parse row {index + 2}: (trade_id={row.get('trade_id', 'unknown')}): {e}")

        # Create appropriate entry based on security type
        try:
            if common_fields['security'] == SecurityType.STOCK:
                trade = StockEntry(
                    **common_fields,
                    price_per_share=float(row.get("price_per_share", 0.0))
                )
            elif common_fields['security'] == SecurityType.DIVIDEND:
                trade = DividendEntry(
                    **common_fields,
                    dividend_amount=float(row.get("dividend_amount", 0.0))
                )
            elif common_fields['security'] == SecurityType.OPTION:
                trade = OptionEntry(
                    **common_fields,
                    expiration_date=pd.to_datetime(row["expiration_date"]).date() if not pd.isna(row.get("expiration_date")) else None,
                    strike=float(row.get("strike", 0.0)),
                    premium=float(row.get("premium", 0.0)),
                    option_type=OptionType[row["option_type"].upper()] if row.get("option_type") else None
                )
            else:
                logging.error(f"Invalid security type in row {index + 2} (trade_id={row['trade_id']}): {common_fields['security']}")
                continue

            trades.append(trade)

        except (KeyError, ValueError, TypeError) as e:
            logging.error(f"Error creating trade entry in row {index + 2}: (trade_id={row['trade_id']}): {e}")
            continue

    return trades
