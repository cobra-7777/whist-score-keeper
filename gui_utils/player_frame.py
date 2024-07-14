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
        self.setFixedSize(600, 110)  # Increased height to provide space for the text at the top
        self.player_font = QFont('Impact', 26)
        self.role_font = QFont('Impact', 24)
        self.points_font = QFont('Impact', 26)

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

        # Draw the player name inside the rectangle, moved up slightly to center vertically
        painter.setFont(self.player_font)
        painter.setPen(QColor('white'))
        painter.drawText(QRect(rect.left() + 10, rect.top() + 12, 220, 50), Qt.AlignLeft, self.player_name)

        # Set the color for the points
        if self.points < 0:
            points_color = QColor('red')
        elif self.points > 0:
            points_color = QColor('#00FF00')
        else:
            points_color = QColor('white')

        # Draw the "Points: " text in white
        points_text = "Points: "
        points_value = str(self.points)

        # Get the width of the "Points: " text
        painter.setFont(self.points_font)
        painter.setPen(QColor('white'))
        points_text_width = painter.fontMetrics().width(points_text)

        # Draw the "Points: " text
        points_text_rect = QRect(rect.right() - 175, rect.top() + 12, points_text_width, 50)
        painter.drawText(points_text_rect, Qt.AlignRight, points_text)

        # Draw the points value with the respective color
        painter.setPen(points_color)
        points_value_rect = QRect(points_text_rect.right() + 5, rect.top() + 12, 70, 50)
        painter.drawText(points_value_rect, Qt.AlignLeft, points_value)

    def get_stars(self):
        return self.stars