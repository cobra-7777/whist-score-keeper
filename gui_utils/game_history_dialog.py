from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class GameHistoryDialog(QDialog):
    def __init__(self, history, players, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game History")
        self.setFixedSize(1000, 800)
        self.setStyleSheet('background-color: #111111; color: white;')

        self.x_icon = QIcon(resource_path('../resources/x.png'))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setRowCount(12)  # 12 games
        self.table.setColumnCount(len(players))  # Number of players
        self.table.setHorizontalHeaderLabels([player for player, _, _, _, _, _ in players])
        self.table.setVerticalHeaderLabels([f'Game {i+1}' for i in range(12)])

        # Set table styles
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
            }
            QHeaderView::section {
                background-color: #DD9637;
                color: black;
                padding: 4px;
            }
        """)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)

        header_font = QFont('Impact', 28)  # Adjust the font size for headers
        item_font = QFont('Impact', 26)  # Adjust the font size for items

        self.table.horizontalHeader().setFont(header_font)
        self.table.verticalHeader().setFont(header_font)

        # Manually set the font for each section of the headers
        for i in range(self.table.columnCount()):
            item = self.table.horizontalHeaderItem(i)
            if item:
                item.setFont(header_font)

        for i in range(self.table.rowCount()):
            item = self.table.verticalHeaderItem(i)
            if item:
                item.setFont(header_font)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        for i, game_points in enumerate(history):
            for j, points in enumerate(game_points):
                item = QTableWidgetItem(str(points))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(item_font)  # Set the font for each table item
                self.table.setItem(i, j, item)

        layout.addWidget(self.table)

        self.close_button = QPushButton(" Close")
        self.close_button.setIcon(self.x_icon)
        self.close_button.setIconSize(QSize(42,42))
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #EF5350;
                border: 3px solid #C62828;
                border-radius: 10px;
                color: black;
            }
            QPushButton:hover {
                background-color: #E57373;
                border-color: #C62828;
            }
            QPushButton:pressed {
                background-color: #EF5350;
                border-color: #C62828;
            }
        """)
        self.close_button.setFont(QFont('Impact', 20))
        self.close_button.setFixedSize(200, 50)  # Adjusted button size
        layout.addWidget(self.close_button, alignment=Qt.AlignCenter)

    def update_table(self, history):
        self.table.setRowCount(len(history))
        for i, game_points in enumerate(history):
            for j, points in enumerate(game_points):
                item = QTableWidgetItem(str(points))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)