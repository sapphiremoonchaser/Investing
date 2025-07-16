import logging
import sys

import openpyxl
import pandas as pd
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QAbstractItemView
)
from PySide6.QtCore import Qt
from src.utilities.fetch_market_data import fetch_current_stock_price, fetch_options_data
from src.journal.core.calculate_profit import (
    get_current_positions,
    calculate_qty_and_profit,
    iterate_current_position_types
)
from src.utilities.csv.load_trades import load_trades_from_excel

class PortfolioWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio Manager")
        self.setGeometry(100, 100, 1200, 600)

        # Create the main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Create Portfolio Tab
        portfolio_tab = QWidget()
        portfolio_layout = QVBoxLayout(portfolio_tab)

        # Create table for portfolio data
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Brokerage",
            "Account",
            "Symbol",
            "Current Price",
            "Original Buy-In",
            "Adjusted Buy-In",
            "Quantity (Shares)",
            "Quantity (Options)",
            "Profit"
        ])

        # Adjust Table Properties
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Connect double-click event to toggle options
        self.table.cellDoubleClicked.connect(self.toggle_options)

        portfolio_layout.addWidget(self.table)
        self.tabs.addTab(portfolio_tab, "Portfolio")

        # Track expanded rows and their options data
        self.expanded_rows = {}
        self.options_data = {}

        # Populate table with sample data
        self.populate_table()


    def populate_table(self):
        """Populate the table with data from a CSV file and fetch current prices."""
        # Path to your CSV file (update this to your actual file path)
        file_path = "C:/Users/viole/dev/Investing-data/trades/trades.xlsx"

        try:
            # Load trades from Excel
            try:
                trades = load_trades_from_excel(file_path)
                print(f"Loaded {len(trades)} trades from {file_path}")
            except Exception as e:
                print(f"Error loading trades: {e}")
                raise

            # Calculate quantities and profits
            try:
                quantity_dict = calculate_qty_and_profit(trades)
                print("Calculated quantities and profits")
            except Exception as e:
                print(f"Error calculating quantities and profits: {e}")
                raise

            # Get current positions
            try:
                current_positions = get_current_positions(quantity_dict)
            except Exception as e:
                print(f"Error calculating quantities and profits: {e}")
                raise

            if (current_positions is None
                    or (isinstance(current_positions, pd.DataFrame) and current_positions.empty)
                    or (isinstance(current_positions, pd.Series) and current_positions.empty)
            ):
                print("No current positions found.")
                self.table.setRowCount(1)
                self.table.setItem(0, 0, QTableWidgetItem("No current positions found."))
                self.table.setSpan(0, 0, 1, 9)
                return

            # Set row count based on current positions
            self.table.setRowCount(len(current_positions) if isinstance(current_positions, pd.DataFrame) else len(current_positions))

            # Populate table
            for idx, stock_data in iterate_current_position_types(current_positions):
                if isinstance(current_positions, pd.DataFrame):
                    row_data = row_data[1]  # Extract the row data from DataFrame iterator
                # Use get() to handle missing 'Symbol' column
                symbol = row_data.get('Symbol', 'N/A')
                # Fetch current price for the symbol, skip if symbol is missing or invalid
                current_price = None
                if symbol != 'N/A' and isinstance(symbol, str):
                    stock_data = fetch_current_stock_price(symbol)
                    if stock_data.is_valid:
                        current_price = stock_data.current_price
                    else:
                        print(f"Stock {symbol} is likely delisted or invalid.")
                        current_price = None  # Keep as None for delisted stocks

                # Calculate profit (if needed)
                original_buy_in = float(row_data.get('Original Buy-In', 0.0))
                quantity_shares = float(row_data.get('Quantity (Shares)', 0.0))
                profit = (current_price - original_buy_in) * quantity_shares if current_price else 0.0

                # Insert data into table
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data.get('brokerage', ''))))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(row_data.get('account', ''))))
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data.get('symbol', ''))))
                self.table.setItem(row_idx, 3, QTableWidgetItem(f"{current_price:.2f}" if current_price else "N/A"))
                self.table.setItem(row_idx, 4, QTableWidgetItem(f"{original_buy_in:.2f}"))
                self.table.setItem(row_idx, 5, QTableWidgetItem(str(row_data.get('Adjusted Buy-In', '0.0'))))
                self.table.setItem(row_idx, 6, QTableWidgetItem(str(row_data.get('Quantity (Shares)', '0'))))
                self.table.setItem(row_idx, 7, QTableWidgetItem(str(row_data.get('Quantity (Options)', '0'))))
                self.table.setItem(row_idx, 8, QTableWidgetItem(f"{profit:.2f}"))

        except FileNotFoundError:
            print(f"CSV file {file_path} not found.")
        except Exception as e:
            print(f"Error reading CSV or populating table: {e}")


    def toggle_options(self, row, column):
        """Handle double-click to toggle options data for a row."""
        symbol = self.table.item(row, 2).text()  # Get symbol from column 2
        if row in self.expanded_rows:
            # Collapse: Remove the options row
            self.table.removeRow(row + 1)
            del self.expanded_rows[row]
            del self.options_data[row]
        else:
            # Expand: Fetch and display options data
            try:
                options = fetch_options_data(symbol)
                self.expanded_rows[row] = True
                self.options_data[row] = options
                # Insert a new row for options data
                self.table.insertRow(row + 1)
                # Format options data as a string (first 3 options for brevity)
                options_str = " | ".join(
                    [f"Strike: ${o['strike']:.2f}, Price: ${o['lastPrice']:.2f}, Exp: {o['expiration']}"
                     for o in options[:3]]
                ) if options else "No options data available"
                self.table.setItem(row + 1, 0, QTableWidgetItem(options_str))
                self.table.setSpan(row + 1, 0, 1, 9)  # Span across all columns
            except ValueError as e:
                print(f"Error fetching options for {symbol}: {e}")
                self.table.insertRow(row + 1)
                self.table.setItem(row + 1, 0, QTableWidgetItem(f"Error: {str(e)}"))
                self.table.setSpan(row + 1, 0, 1, 9)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PortfolioWindow()
    window.show()
    sys.exit(app.exec())