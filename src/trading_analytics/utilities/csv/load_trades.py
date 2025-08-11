"""Loads trade entries from an Excel file into a list of trade objects.

This module defines a function to read trade data from an Excel file and convert it into
a list of `StockEntry`, `DividendEntry`, or `OptionEntry` objects based on the security type.
It handles data parsing, validation, and error logging for robust processing of trade records.

Functions:
    load_trades_from_excel: Reads trade data from an Excel file and returns a list of trade entries.
"""
import pandas as pd
import logging
from typing import (
    List,
    Union,
)

from trading_analytics.data.data_model.entry.dividend_entry import DividendEntry
from trading_analytics.data.enum.option_type import OptionType
from trading_analytics.data.enum.security_type import SecurityType
from trading_analytics.data.enum.sub_action import SubAction
from trading_analytics.data.enum.trade_action import Action
from trading_analytics.data.data_model.entry.stock_entry import StockEntry
from trading_analytics.data.data_model.entry.option_entry import OptionEntry

# Configure logging to a file
logger = logging.getLogger(__name__)

def load_trades_from_excel(
    file_path: str
) -> List[Union[StockEntry, DividendEntry, OptionEntry]]:
    """Loads trade entries from an Excel file into a list of trade objects.

        Reads an Excel file using pandas and converts each row into a `StockEntry`, `DividendEntry`,
        or `OptionEntry` based on the security type. Validates and parses common fields for all trade
        types and specific fields for each security type, logging errors for invalid rows without
        raising exceptions unless the file cannot be read.

        Args:
            file_path (str): Path to the Excel file containing trade data.

        Returns:
            List[Union[StockEntry, DividendEntry, OptionEntry]]: A list of parsed trade entry objects.

        Raises:
            Exception: If the Excel file cannot be read (e.g., file not found, invalid format).
    """
    # Read excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        logger.error(f"Failed to read Excel file {file_path}. {e}")
        raise e

    # Assign values from csv rows to a Series
    trades = []
    row: pd.Series
    for _, row in df.iterrows():
        try:
            common_fields = {
                "trade_id": int(str(row["trade_id"])),
                "strategy_id": int(str(row["strategy_id"])),
                "brokerage": str(row["brokerage"]),
                "account": str(row["account"]),
                "strategy": str(row["strategy"]),
                "security": SecurityType(row["security_type"]),
                "trade_date": pd.to_datetime(row["trade_date"]).date(),
                "symbol": str(row["symbol"]),
                "action": Action(row["action"]),
                "sub_action": SubAction(row["sub_action"]),
                "quantity": float(str(row["quantity"])),
                "fees": float(str(row["fees"])),
            }
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Failed to parse row for (trade_id={row.get('trade_id', 'unknown')}): {e}")
            raise e

        # Create appropriate entry based on security type
        try:
            # Stock or ETF, assign price_per_share
            if common_fields['security'] in [SecurityType.STOCK, SecurityType.ETF]:
                trade = StockEntry(
                    **common_fields,
                    price_per_share=float(row.get("price_per_share", 0.0))
                )

            # Dividend, assign dividend_amount
            elif common_fields['security'] == SecurityType.DIVIDEND:
                trade = DividendEntry(
                    **common_fields,
                    dividend_amount=float(row.get("dividend_amount", 0.0))
                )

            # Option, assign expiration date, strike, premium, option_type
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
                    raise ValueError(f"Failed to parse row for (trade_id={row.get('trade_id')}): {e}")
            else:
                logger.error(f"Invalid security type for (trade_id={row['trade_id']}): {common_fields['security']}")
                continue

            trades.append(trade)

        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error creating trade entry for (trade_id={row['trade_id']}): {e}")
            continue

    return trades
