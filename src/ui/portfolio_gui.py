import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget, QTableWidget, QAbstractItemView
)

from PySide6.QtCore import Qt

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
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Platform",
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
        # Sample data with options details
        # ToDo: replace with my data sources
        sample_data = [
            {
                "main": ("Broker1", "Main", "AAPL", 150.25, 120.50, 125.75, 100, 2, 2975.00),
                "options": [
                    ("2025-12-20", 155.00, 1),
                    ("2026-01-17", 160.00, 1)
                ]
            },
            {
                "main": ("Broker2", "Retirement", "MSFT", 280.10, 200.00, 210.50, 50, 0, 4025.00),
                "options": []
            },
            {
                "main": ("Broker1", "Main", "TSLA", 700.00, 600.00, 610.00, 20, 1, 2000.00),
                "options": [("2025-11-15", 710.00, 1)]
            }
        ]


