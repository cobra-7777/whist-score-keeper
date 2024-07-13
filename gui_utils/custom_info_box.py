from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pywinstyles import apply_style

class InfoMessageBox(QMessageBox):
    def __init__(self, title, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(text)
        apply_style(self, 'dark')  # Assuming you have a function to apply styles
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
        self.setFont(QFont('Impact', 20))
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setStandardButtons(QMessageBox.Ok)
        self.setFixedSize(500, 300)  # Adjust size as needed