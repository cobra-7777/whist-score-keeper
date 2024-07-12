from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QRect

class PlayerFrame(QFrame):
    def __init__(self, player_name, points, stars, role=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_name = player_name
        self.points = points
        self.stars = stars
        self.role = role
        self.setFixedSize(500, 110)  # Increased height to provide space for the text at the top
        self.player_font = QFont('Impact', 26)
        self.role_font = QFont('Impact', 24)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up the pen and brush for the border
        if self.role == 'DEALER':
            pen = QPen(QColor('#1E90FF'), 2)
            text_color = QColor('#1E90FF')
        elif self.role == 'CALLER':
            pen = QPen(QColor('#32CD32'), 2)
            text_color = QColor('#32CD32')
        else:
            pen = QPen(QColor('white'), 2)
            text_color = QColor('white')
        
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        # Draw the rounded rectangle border
        rect = self.rect().adjusted(10, 32, -10, -10)  # Adjusted top margin to provide space for the text
        painter.drawRoundedRect(rect, 10, 10)

        # Draw the role text at the top center, slightly above the border
        if self.role:
            painter.setFont(self.role_font)
            painter.setPen(text_color)
            text_rect = QRect(rect.left() + (rect.width() - 100) // 2, rect.top() - 50, 100, 64)
            painter.drawText(text_rect, Qt.AlignCenter, self.role)

        # Draw the player name and points inside the rectangle, moved up slightly to center vertically
        painter.setFont(self.player_font)
        painter.setPen(QColor('white'))
        painter.drawText(QRect(rect.left() + 10, rect.top() + 12, 220, 50), Qt.AlignLeft, self.player_name)
        painter.drawText(QRect(rect.right() - 230, rect.top() + 12, 220, 50), Qt.AlignRight, f'Points: {self.points}')

    def get_stars(self):
        return self.stars