from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pywinstyles import apply_style

class CustomMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        apply_style(self, 'dark')
        self.setStyleSheet("""
            QMessageBox {
                color: white;
            }
            QPushButton {
                background-color: #DD9637; 
                border: 2px solid #E5C26B; 
                border-radius: 5px;
                color: black;
                padding: 5px 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #E2B258;
                border: none;
            }
            QPushButton:pressed {
                background-color: #DD9637;
                border: none;
            }
            QLabel {
                color: white;
            }
        """)

        self.setFont(QFont('Palatino Linotype', 11))
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

    def set_message(self, title, text):
        self.setWindowTitle(title)
        self.setText(text)

    def add_buttons(self, buttons):
        for button in buttons:
            self.addButton(button)