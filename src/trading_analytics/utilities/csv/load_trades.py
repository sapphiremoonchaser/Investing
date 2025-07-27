# Imports
import pandas as pd
import logging
from typing import List, Union

from trading_analytics.data.enum.security_type import SecurityType
from trading_analytics.data.enum.trade_action import TradeAction
from trading_analytics.data.enum import TradeSubAction
from trading_analytics.data.enum import OptionType
from trading_analytics.data.data_model.entry.stock_entry import StockEntry
from trading_analytics.data.data_model import DividendEntry
from trading_analytics.data.data_model.entry.option_entry import OptionEntry

# Configure logging to a file
logger = logging.getLogger(__name__)

def load_trades_from_excel(
        file_path: str
) -> List[Union[StockEntry, DividendEntry, OptionEntry]]:
    # Read excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        logger.error(f"Failed to read Excel file {file_path}. {e}")

    trades = []
    for _, row in df.iterrows():
        try:
            common_fields = {
                "trade_id": int(row["trade_id"]),
                "strategy_id": int(row["strategy_id"]),
                "brokerage": str(row["brokerage"]),
                "account": str(row["account"]),
                "strategy": str(row["strategy"]),
                "security": SecurityType(row["security_type"]),
                "trade_date": pd.to_datetime(row["trade_date"]).date(),
                "symbol": str(row["symbol"]),
                "action": TradeAction(row["action"]),
                "sub_action": TradeSubAction(row["sub_action"]),
                "quantity": float(row["quantity"]),
                "fees": float(row["fees"]),
            }
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Failed to parse row for (trade_id={row.get('trade_id', 'unknown')}): {e}")

        # Create appropriate entry based on security type
        try:
            if common_fields['security'] in [SecurityType.STOCK, SecurityType.ETF]:
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
                try:
                    trade = OptionEntry(
                        **common_fields,
                        expiration_date=pd.to_datetime(row["expiration_date"]).date() if not pd.isna(row.get("expiration_date")) else None,
                        strike=float(row.get("strike", 0.0)),
                        premium=float(row.get("premium", 0.0)),
                        option_type=OptionType[row["option_type"].upper()] if row.get("option_type") else None
                    )
                except Exception as e:
                    x = 1
                    raise ValueError(f"Failed to parse row for (trade_id={row.get('trade_id')}): {e}")
            else:
                logger.error(f"Invalid security type for (trade_id={row['trade_id']}): {common_fields['security']}")
                continue

            trades.append(trade)

        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error creating trade entry for (trade_id={row['trade_id']}): {e}")
            continue

    return trades
