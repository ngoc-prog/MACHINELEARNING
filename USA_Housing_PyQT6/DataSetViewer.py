from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
import pandas as pd


class DataSetViewer(QDialog):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Dataset Viewer - House Pricing Prediction")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'Avg. Area Income',
            'Avg. Area House Age',
            'Avg. Area Number of Rooms',
            'Avg. Area Number of Bedrooms',
            'Area Population',
            'Price'
        ])

        # Stretch columns to fill width
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self):
        """Load data from CSV file"""
        try:
            df = pd.read_csv(self.filename)
            self.table.setRowCount(len(df))

            for i in range(len(df)):
                for j in range(6):
                    item = QTableWidgetItem(str(df.iloc[i, j]))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(i, j, item)

        except Exception as e:
            print(f"Error loading data: {e}")