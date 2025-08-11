import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QTableWidget
)

from trading_analytics.journal.core.portfolio_data import load_and_process_portfolio_data
from trading_analytics.utilities.fetch_market_data import fetch_options_data


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
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
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
        file_path = "C:/Users/viole/dev/Investing-data/trades/trades.xlsx"

        try:
            # Load and process data using the new module
            positions = load_and_process_portfolio_data(file_path)
            if not positions:
                print("No current positions found.")
                self.table.setRowCount(1)
                self.table.setItem(0, 0, QTableWidgetItem("No current positions found."))
                self.table.setSpan(0, 0, 1, 7)
                return

            # Set row count
            self.table.setRowCount(len(positions))

            # Populate table
            for row, position in enumerate(positions):
                self.table.setItem(row, 0, QTableWidgetItem(position.symbol))
                self.table.setItem(row, 1, QTableWidgetItem(
                    f"{position.current_price:.2f}" if position.current_price else "N/A"))
                self.table.setItem(row, 2, QTableWidgetItem(
                    f"{position.original_buy_in:.2f}" if position.original_buy_in else "N/A"))
                self.table.setItem(row, 3, QTableWidgetItem(
                    f"{position.adjusted_buy_in:.2f}" if position.adjusted_buy_in else "N/A"))
                self.table.setItem(row, 4, QTableWidgetItem(str(position.stock_qty)))
                self.table.setItem(row, 5, QTableWidgetItem(str(position.option_qty)))
                self.table.setItem(row, 6, QTableWidgetItem(f"{position.profit:.2f}" if position.profit else "N/A"))

        except FileNotFoundError:
            print(f"Excel file {file_path} not found.")
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem(f"Excel file {file_path} not found."))
            self.table.setSpan(0, 0, 1, 7)
        except Exception as e:
            print(f"Error reading Excel or populating table: {e}")
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
            self.table.setSpan(0, 0, 1, 7)


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