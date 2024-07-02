import sys
import os
from PyQt5.QtWidgets import QDialog, QComboBox, QSizePolicy, QSpacerItem, QHBoxLayout, QFrame, QGraphicsOpacityEffect, QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QPen, QPainterPath
from pywinstyles import apply_style

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

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

class PlayerFrame(QFrame):
    def __init__(self, player_name, points, stars, role=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_name = player_name
        self.points = points
        self.stars = stars
        self.role = role
        self.setFixedSize(400, 80)  # Increased height to provide space for the text at the top
        self.player_font = QFont('Palatino Linotype', 14)
        self.role_font = QFont('Palatino Linotype', 10)

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
        rect = self.rect().adjusted(10, 20, -10, -10)  # Adjusted top margin to provide space for the text
        painter.drawRoundedRect(rect, 10, 10)

        # Draw the role text at the top center, slightly above the border
        if self.role:
            painter.setFont(self.role_font)
            painter.setPen(text_color)
            text_rect = QRect(rect.left() + (rect.width() - 60) // 2, rect.top() - 25, 60, 20)
            painter.drawText(text_rect, Qt.AlignCenter, self.role)

        # Draw the player name and points inside the rectangle, moved up slightly to center vertically
        painter.setFont(self.player_font)
        painter.setPen(QColor('white'))
        painter.drawText(QRect(rect.left() + 10, rect.top() + 15, 150, 20), Qt.AlignLeft, self.player_name)
        painter.drawText(QRect(rect.right() - 150, rect.top() + 15, 140, 20), Qt.AlignRight, f'Points: {self.points}')

    def get_stars(self):
        return self.stars


class HandDialog(QDialog):
    def __init__(self, players, parent=None):
        super().__init__(parent)
        self.players = players
        self.calls = ['7 Normal',
                      '7 Tilt',
                      '7 Good/Strong',
                      '7 Halves',
                      '7 Quarters',
                      '8 Normal',
                      '8 Tilt',
                      '8 Good/Strong',
                      '8 Halves',
                      '8 Quarters',
                      '9 Normal',
                      'Normal Sun',
                      '9 Tilt',
                      '9 Good/Strong',
                      '9 Halves',
                      '9 Quarters',
                      '10 Normal',
                      'Clean Sun',
                      '10 Tilt',
                      '10 Good/Strong',
                      '10 Halves',
                      '10 Quarters',
                      '11 Normal',
                      'Table Show',
                      '11 Tilt',
                      '11 Good/Strong',
                      '11 Halves',
                      '11 Quarters',
                      '12 Normal',
                      'Super Table Show',
                      '12 Tilt',
                      '12 Good/Strong',
                      '12 Halves',
                      '12 Quarters',
                      '13 Normal',
                      '13 Tilt',
                      '13 Good/Strong',
                      '13 Halves',
                      '13 Quarters'
                      ]
        
        self.possible_tricks = ['0',
                                '1',
                                '2',
                                '3',
                                '4',
                                '5',
                                '6',
                                '7',
                                '8',
                                '9',
                                '10',
                                '11',
                                '12',
                                '13'
                                ]


        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Complete A Hand")
        self.setFixedSize(400, 500)
        self.setStyleSheet('background-color: #111111; color: white;')
        apply_style(self, "dark")

        layout = QVBoxLayout()

        def add_label_and_combo(label_text, combo_box):
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setStyleSheet('color: white;')
            h_layout.addWidget(label)
            h_layout.addWidget(combo_box)
            layout.addLayout(h_layout)

        self.caller_combo = QComboBox()
        for player, _, _ in self.players:
            self.caller_combo.addItem(player)
        self.caller_combo.setStyleSheet('background-color: white; color: black;')
        self.caller_combo.currentIndexChanged.connect(self.update_partner_combo)
        add_label_and_combo("Who got the calling?:", self.caller_combo)

        self.call_combo = QComboBox()
        for i in self.calls:
            self.call_combo.addItem(i)
        self.call_combo.setStyleSheet('background-color: white; color: black;')
        self.call_combo.currentIndexChanged.connect(self.update_partner_combo)
        add_label_and_combo("What was played?:", self.call_combo)

        self.partner_combo = QComboBox()
        for player, _, _ in self.players:
            self.partner_combo.addItem(player)
        self.partner_combo.setStyleSheet('background-color: white; color: black;')
        add_label_and_combo("Who was partner?:", self.partner_combo)

        self.tricks_input = QComboBox()
        for i in self.possible_tricks:
            self.tricks_input.addItem(i)
        self.tricks_input.setStyleSheet('background-color: white; color: black;')
        add_label_and_combo("Number of tricks won?:", self.tricks_input)

        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        complete_button = QPushButton("Complete", self)
        complete_button.clicked.connect(self.complete_hand)
        complete_button.setFixedSize(250, 65)
        complete_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; color: black; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        complete_button.setFont(QFont('Palatino Linotype', 14))
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(complete_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_partner_combo(self):
        selected_call = self.call_combo.currentText()
        solo_calls = ['7 Quarters', 
                      '8 Quarters', 
                      'Normal Sun', 
                      '9 Quarters', 
                      'Clean Sun', 
                      '10 Quarters',
                      'Table Show',
                      '11 Quarters',
                      'Super Table Show',
                      '12 Quarters',
                      '13 Quarters'
                      ]
        
        if selected_call in solo_calls:
            self.partner_combo.setCurrentIndex(self.caller_combo.currentIndex())
            self.partner_combo.setEnabled(False)
        else:
            self.partner_combo.setEnabled(True)

    def complete_hand(self):
        caller = self.caller_combo.currentText()
        call = self.call_combo.currentText()
        partner = self.partner_combo.currentText()
        tricks_won = int(self.tricks_input.currentText())

        hand_info = (caller, call, partner, tricks_won)
        self.parent().update_standings(hand_info)
        self.accept()


class WhistScoreKeeper(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Whist Score Keeper")
        self.width = 500
        self.height = 700
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet('background-color: #111111;')
        self.setWindowIcon(QIcon(resource_path('resources/FullLogo.ico')))

        self.players = [("Player 1", 0, 0), ("Player 2", 0, 0), ("Player 3", 0, 0), ("Player 4", 0, 0)]
        self.dealer_index = 0
        self.caller_index = 1
        self.hands_played = 0

        #Score card
        self.scorecard = {
            '7 Normal': [-4, -4, -3, -3, -2, -2, -1, 1, 1, 2, 2, 3, 3, 4],
            '7 Tilt': [-5, -5, -4, -3, -3, -2, -1, 1, 1, 2, 3, 3, 4, 4],
            '7 Good/Strong': [-6, -5, -5, -4, -3, -2, -2, 1, 2, 2, 3, 4, 5, 5],
            '7 Halves': [-8, -7, -6, -5, -4, -3, -2, 1, 2, 3, 4, 5, 6, 7],
            '7 Quarters': [-8, -7, -6, -5, -4, -3, -2, 1, 2, 3, 4, 5, 6, 7],
            '8 Normal': [-9, -8, -7, -6, -5, -4, -3, -2, 1, 2, 3, 4, 5, 6],
            '8 Tilt': [-11, -10, -9, -8, -6, -5, -4, -3, 1, 3, 4, 5, 6, 8],
            '8 Good/Strong': [-14, -12, -11, -9, -8, -6, -5, -3, 2, 3, 5, 6, 8, 9],
            '8 Halves': [-16, -14, -12, -11, -9, -7, -5, -4, 2, 4, 5, 7, 9, 11],
            '8 Quarters': [-16, -14, -12, -11, -9, -7, -5, -4, 2, 4, 5, 7, 9, 11],
            '9 Normal': [-20, -18, -16, -14, -12, -10, -8, -6, -4, 2, 4, 6, 8, 10],
            '9 Tilt': [-25, -23, -20, -18, -15, -13, -10, -8, -5, 3, 5, 8, 10, 13],
            '9 Good/Strong': [-30, -27, -24, -21, -18, -15, -12, -9, -6, 3, 6, 9, 12, 15],
            '9 Halves': [-35, -32, -28, -25, -21, -18, -14, -11, -7, 4, 7, 11, 14, 18],
            '9 Quarters': [-35, -32, -28, -25, -21, -18, -14, -11, -7, 4, 7, 11, 14, 18],
            '10 Normal': [-44, -40, -36, -32, -28, -24, -20, -16, -12, -8, 4, 8, 12, 16],
            '10 Tilt': [-55, -50, -45, -40, -35, -30, -25, -15, -10, 5, 10, 15, 20],
            '10 Good/Strong': [-66, -60, -54, -48, -42, -36, -30, -24, -18, -12, 6, 12, 18, 24],
            '10 Halves': [-77, -70, -63, -56, -49, -42, -35, -28, -21, -14, 7, 14, 21, 28],
            '10 Quarters': [-77, -70, -63, -56, -49, -42, -35, -28, -21, -14, 7, 14, 21, 28],
            '11 Normal': [-96, -88, -80, -72, -64, -56, -48, -40, -32, -24, -16, 8, 16, 24],
            '11 Tilt': [-120, -110, -100, -90, -80, -70, -60, -50, -40, -30, -20, 10, 20, 30],
            '11 Good/Strong': [-144, -132, -120, -108, -96, -84, -72, -60, -48, -36, -24, 12, 24, 36],
            '11 Halves': [-168, -154, -140, -126, -112, -98, -84, -70, -56, -42, -28, 14, 28, 42],
            '11 Quarters': [-168, -154, -140, -126, -112, -98, -84, -70, -56, -42, -28, 14, 28, 42],
            '12 Normal': [-208, -192, -176, -160, -144, -128, -112, -96, -80, -64, -48, -32, 16, 32],
            '12 Tilt': [-260, -240, -220, -200, -180, -160, -140, -120, -100, -80, -60, -40, 20, 40],
            '12 Good/Strong': [-312, -288, -264, -240, -216, -192, -168, -144, -120, -96, -72, -48, 24, 48],
            '12 Halves': [-364, -336, -308, -280, -252, -224, -196, -168, -140, -112, -84, -56, 28, 56],
            '12 Quarters': [-364, -336, -308, -280, -252, -224, -196, -168, -140, -112, -84, -56, 28, 56],
            '13 Normal': [-448, -416, -384, -352, -320, -288, -256, -224, -192, -160, -128, -96, -64, 32],
            '13 Tilt': [-560, -520, -480, -440, -400, -360, -320, -280, -240, -200, -160, -120, -80, 40],
            '13 Good/Strong': [-672, -624, -576, -528, -480, -432, -384, -336, -288, -240, -192, -144, -96, 48],
            '13 Halves': [-784, -728, -672, -616, -560, -504, -448, -392, -336, -280, -224, -168, -112, 56],
            '13 Quarters': [-784, -728, -672, -616, -560, -504, -448, -392, -336, -280, -224, -168, -112, 56]
        }

        #Special game rules
        self.special_games = {
            'Normal Sun': {
                'max_allowed_tricks': 1,
                'win_points': 9,
                'lose_points': -9,
                'opponent_win_points': 3,
                'opponent_lose_points': -3
            },
            'Clean Sun': {
                'max_allowed_tricks': 0,
                'win_points': 18,
                'lose_points': -18,
                'opponent_win_points': 6,
                'opponent_lose_points': -6
            },
            'Table Show': {
                'max_allowed_tricks': 0,
                'win_points': 36,
                'lose_points': -36,
                'opponent_win_points': 12,
                'opponent_lose_points': -12
            },
            'Super Table Show': {
                'max_allowed_tricks': 0,
                'win_points': 72,
                'lose_points': -72,
                'opponent_win_points': 24,
                'opponent_lose_points': -24
            }
        }

        # Set up the initial layout
        self.init_ui()

    def init_ui(self):
        apply_style(self,"dark")
        self.normal_font = QFont('Palatino Linotype', 14)
        self.backbtn_font = QFont('Palatino Linotype', 10)
        self.dealer_label_font = QFont('Palatino Linotype', 10)

        # Start fresh game button
        self.start_fresh_game_button = QPushButton("START A NEW GAME", self)
        self.start_fresh_game_button.clicked.connect(self.start_fresh_game)
        self.start_fresh_game_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        self.start_fresh_game_button.setFixedSize(250,60)
        self.start_fresh_game_button.setFont(self.normal_font)
        self.start_fresh_game_button.move(125,425)

        # Load existing game button
        self.load_existing_game_button = QPushButton("LOAD EXISTING GAME", self)
        self.load_existing_game_button.clicked.connect(self.load_existing_game)
        self.load_existing_game_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        self.load_existing_game_button.setFixedSize(250,50)
        self.load_existing_game_button.setFont(self.normal_font)
        self.load_existing_game_button.move(125, 520)

        self.logo_label = QLabel(self)
        logo_pixmap = QPixmap(resource_path('resources/FullLogo_Transparent.png'))
        logo_width = 400
        logo_height = 370
        scaled_pixmap = logo_pixmap.scaled(logo_width, logo_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.resize(400,370)
        self.logo_label.move(49,20)

        self.effect = QGraphicsOpacityEffect(self)
        self.logo_label.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b'opacity')
        self.animation.setDuration(3000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        

        self.logo_label.show()
        self.start_fresh_game_button.show()
        self.load_existing_game_button.show()
        

    def start_fresh_game(self):
        self.clear_ui()
        self.init_new_game_ui()

    def load_existing_game(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Game", "", "Whist Game Files (*.wst);;All Files (*)", options=options)
        if file_name:
            self.load_game(file_name)

    def init_new_game_ui(self):
        # Player name inputs
        self.player1_input = QLineEdit(self)
        self.player1_input.setPlaceholderText("Player 1 Name")
        self.player1_input.setStyleSheet('background-color: white;')
        self.player1_input.resize(250,35)
        self.player1_input.move(125,120)
        self.player1_input.setFont(self.normal_font)


        self.player2_input = QLineEdit(self)
        self.player2_input.setPlaceholderText("Player 2 Name")
        self.player2_input.setStyleSheet('background-color: white;')
        self.player2_input.resize(250,35)
        self.player2_input.move(125,190)
        self.player2_input.setFont(self.normal_font)

        self.player3_input = QLineEdit(self)
        self.player3_input.setPlaceholderText("Player 3 Name")
        self.player3_input.setStyleSheet('background-color: white;')
        self.player3_input.resize(250,35)
        self.player3_input.move(125,260)
        self.player3_input.setFont(self.normal_font)

        self.player4_input = QLineEdit(self)
        self.player4_input.setPlaceholderText("Player 4 Name")
        self.player4_input.setStyleSheet('background-color: white;')
        self.player4_input.resize(250,35)
        self.player4_input.move(125,330)
        self.player4_input.setFont(self.normal_font)

        # Start game button
        self.start_game_button = QPushButton("Start New Game", self)
        self.start_game_button.clicked.connect(self.start_new_game)
        self.start_game_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        self.start_game_button.setFixedSize(250,60)
        self.start_game_button.setFont(self.normal_font)
        self.start_game_button.move(125,450)

        self.back_button = QPushButton('<- Back', self)
        self.back_button.clicked.connect(self.back_to_main_menu)
        self.back_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        self.back_button.setFixedSize(70,30)
        self.back_button.setFont(self.backbtn_font)
        self.back_button.move(10,10)
        
        
        self.player1_input.show()
        self.player2_input.show()
        self.player3_input.show()
        self.player4_input.show()
        self.start_game_button.show()
        self.back_button.show()

    def init_main_ui(self):
        # Create a vertical layout to hold all player frames
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        # Hands played label
        self.hands_played_label = QLabel(f'Hands Played: {self.hands_played}')
        self.hands_played_label.setFont(QFont('Palatino Linotype', 14))
        self.hands_played_label.setStyleSheet('color: white;')
        self.hands_played_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.hands_played_label)
        
        
        main_layout.addSpacerItem(QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.player_frames = {}
        
        # Create a container widget for the leaderboard
        leaderboard_container = QWidget()
        leaderboard_layout = QVBoxLayout(leaderboard_container)
        leaderboard_layout.setAlignment(Qt.AlignCenter)

        for i, (player, points, stars) in enumerate(self.players):
            role = None
            if i == self.dealer_index:
                role = 'DEALER'
            elif i == self.caller_index:
                role = 'CALLER'

            player_frame = PlayerFrame(player, points, stars, role)
            player_frame.setObjectName(player)
            leaderboard_layout.addWidget(player_frame)

            self.player_frames[player] = player_frame

        

        # Add the leaderboard container to the main layout
        #main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(leaderboard_container, alignment=Qt.AlignCenter)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


        # Create a container widget and set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        container.setFixedSize(500, 700)

        self.setCentralWidget(container)

        # Complete a hand button
        self.complete_hand_button = QPushButton("Complete a Hand", self)
        self.complete_hand_button.clicked.connect(self.complete_hand)
        self.complete_hand_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        self.complete_hand_button.setFont(QFont('Palatino Linotype', 14))
        self.complete_hand_button.setFixedSize(250,65)
        self.complete_hand_button.move(125,500)
        self.complete_hand_button.show()
        
        self.star_labels = {}

        # Stars
        self.p1_star_label = QLabel(self)
        star_pixmap = QPixmap(resource_path('resources/star.png')).scaled(20,20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.p1_star_label.setPixmap(star_pixmap)
        self.p1_star_label.setFixedSize(20,20)
        self.p1_star_label.move(8,129)
        self.p1_star_label.show()
        self.p1_text_label = QLabel(f'- {self.players[0][2]}',self) # REPLACE WITH ACTUAL STAR AMOUNT
        self.p1_text_label.move(32,133)
        self.p1_text_label.resize(25,12)
        self.p1_text_label.setStyleSheet('color: white;')
        self.p1_text_label.setFont(QFont('Palatino Linotype', 11))
        self.p1_text_label.show()
        self.star_labels[self.players[0][0]] = self.p1_text_label

        # Stars
        self.p2_star_label = QLabel(self)
        #star_pixmap = QPixmap('resources/star.png').scaled(20,20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.p2_star_label.setPixmap(star_pixmap)
        self.p2_star_label.setFixedSize(20,20)
        self.p2_star_label.move(8,215)
        self.p2_star_label.show()
        self.p2_text_label = QLabel(f'- {self.players[1][2]}',self) # REPLACE WITH ACTUAL STAR AMOUNT
        self.p2_text_label.move(32,219)
        self.p2_text_label.resize(25,12)
        self.p2_text_label.setStyleSheet('color: white;')
        self.p2_text_label.setFont(QFont('Palatino Linotype', 11))
        self.p2_text_label.show()
        self.star_labels[self.players[1][0]] = self.p2_text_label

        # Stars
        self.p3_star_label = QLabel(self)
        #star_pixmap = QPixmap('resources/star.png').scaled(20,20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.p3_star_label.setPixmap(star_pixmap)
        self.p3_star_label.setFixedSize(20,20)
        self.p3_star_label.move(8,301)
        self.p3_star_label.show()
        self.p3_text_label = QLabel(f'- {self.players[2][2]}',self) # REPLACE WITH ACTUAL STAR AMOUNT
        self.p3_text_label.move(32,305)
        self.p3_text_label.resize(25,12)
        self.p3_text_label.setStyleSheet('color: white;')
        self.p3_text_label.setFont(QFont('Palatino Linotype', 11))
        self.p3_text_label.show()
        self.star_labels[self.players[2][0]] = self.p3_text_label

        # Stars
        self.p4_star_label = QLabel(self)
        #star_pixmap = QPixmap('resources/star.png').scaled(20,20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.p4_star_label.setPixmap(star_pixmap)
        self.p4_star_label.setFixedSize(20,20)
        self.p4_star_label.move(8,387)
        self.p4_star_label.show()
        self.p4_text_label = QLabel(f'- {self.players[3][2]}',self) # REPLACE WITH ACTUAL STAR AMOUNT
        self.p4_text_label.move(32,391)
        self.p4_text_label.resize(25,12)
        self.p4_text_label.setStyleSheet('color: white;')
        self.p4_text_label.setFont(QFont('Palatino Linotype', 11))
        self.p4_text_label.show()
        self.star_labels[self.players[3][0]] = self.p4_text_label

    def complete_hand(self):
        self.hand_dialog = HandDialog(self.players, self)
        self.hand_dialog.exec_()


    def start_new_game(self):
        player1 = self.player1_input.text()
        player2 = self.player2_input.text()
        player3 = self.player3_input.text()
        player4 = self.player4_input.text()

        if player1 and player2 and player3 and player4:

            participant_names = '-'.join([player1, player2, player3, player4])
            game_file_name = f'Game-{participant_names}.wst'

            if os.path.exists(game_file_name):
                #QMessageBox.warning(self, "Game Already Exists", "A game with these players already exists. Delete it before starting a new one.")
                self.show_custom_message_box('Game Already Exists', "A game with these players already exists. Please delete it to start a new one.")
                return

            
            self.players = [(player1, 0, 0), (player2, 0, 0), (player3, 0, 0), (player4, 0, 0)]
            self.save_game()
            self.clear_ui()
            self.init_main_ui()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter all player names.")

    def load_game(self, file_name):
        # Load the game state from the file
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Parse the file content
        loaded_players = []
        hands_played = 0
        dealer_index = 0
        caller_index = 0

        for line in lines:
            parts = line.strip().split(',')
            if parts[0] == 'hands_played':
                hands_played = int(parts[1])
            elif parts[0] == 'dealer_index':
                dealer_index = int(parts[1])
            elif parts[0] == 'caller_index':
                caller_index = int(parts[1])
            else:
                player = parts[0]
                points = int(parts[1])
                stars = int(parts[2])
                loaded_players.append((player, points, stars))

        # Update the game state
        self.players = loaded_players
        self.hands_played = hands_played
        self.dealer_index = dealer_index
        self.caller_index = caller_index

        # Update the UI
        self.clear_ui()
        self.init_main_ui()
        self.update_ui_for_loaded_game()

    def update_ui_for_loaded_game(self):
        # Update the hands played label
        self.hands_played_label.setText(f'Hands Played: {self.hands_played}')

        # Update player frames
        for i, (player, points, stars) in enumerate(self.players):
            player_frame = self.player_frames[player]
            player_frame.points = points
            player_frame.stars = stars
            player_frame.role = None
            if i == self.dealer_index:
                player_frame.role = 'DEALER'
            elif i == self.caller_index:
                player_frame.role = 'CALLER'
            player_frame.update()

        # Update star labels
        for player, points, stars in self.players:
            self.star_labels[player].setText(f'- {stars}')

    def back_to_main_menu(self):
        self.clear_ui()
        self.init_ui()

    def clear_ui(self):
        for widget in self.findChildren(QWidget):
            widget.hide()


    def update_standings(self, hand_info):
        # Update the main UI and save the game state
        caller, call, partner, tricks_won = hand_info

        print(f"SELF.PLAYERS BEFORE CALCULATING SCORE: {self.players}")

        if call in self.special_games:
            player_points, opponent_points = self.calculate_special_game_score(call, tricks_won)
            self.distribute_special_game_points(caller, player_points, opponent_points)
        else:
            tricks_called = int(call.split()[0])
            points = self.calculate_score(call, tricks_called, tricks_won)
            self.distribute_points(caller, partner, points, call)
        
        self.hands_played += 1
        self.hands_played_label.setText(f'Hands Played: {self.hands_played}')

        self.dealer_index = (self.dealer_index + 1) % len(self.players)
        self.caller_index = (self.caller_index + 1) % len(self.players)
        
        for i, (player, points, stars) in enumerate(self.players):
            player_frame = self.player_frames[player]
            player_frame.points = points
            player_frame.stars = stars
            player_frame.role = None
            if i == self.dealer_index:
                player_frame.role = 'DEALER'
            elif i == self.caller_index:
                player_frame.role = 'CALLER'
            player_frame.update()

        print(f"SELF.PLAYERS AFTER UPDATE_STANDINGS: {self.players}")

        if self.hands_played >= 12:
            self.end_game()  

        self.save_game()

    def calculate_score(self, call, tricks_called, tricks_won):
        scores = self.scorecard[call]
        return scores[tricks_won]
    
    def calculate_special_game_score(self, game, tricks_won):
        rules = self.special_games[game]
        if tricks_won <= rules["max_allowed_tricks"]:
            # Player won
            return rules["win_points"], rules["opponent_lose_points"]
        else:
            # Player lost
            return rules["lose_points"], rules["opponent_win_points"]
        
    def distribute_points(self, caller, partner, points, call):

        caller_index = next(i for i, p in enumerate(self.players) if p[0] == caller)
        partner_index = next(i for i, p in enumerate(self.players) if p[0] == partner)

        print(f"SELF.PLAYERS BEFORE DISTRIBUTING POINTS: {self.players}")

        if call in ["7 Quarters", "8 Quarters", "9 Quarters", "10 Quarters", "11 Quarters", "12 Quarters", "13 Quarters"] or caller == partner:
            # Solo game
            self.players[caller_index] = (self.players[caller_index][0], 
                                          self.players[caller_index][1] + points * 3,
                                          self.players[caller_index][2]
                                          )
            for i, (player, score, stars) in enumerate(self.players):
                if player != caller:
                    self.players[i] = (player, score - points, stars)
        else:
            # Regular game
            self.players[caller_index] = (self.players[caller_index][0], 
                                          self.players[caller_index][1] + points,
                                          self.players[caller_index][2]
                                          )
            self.players[partner_index] = (self.players[partner_index][0], 
                                           self.players[partner_index][1] + points,
                                           self.players[partner_index][2]
                                           )
            print(f"SELF.PLAYERS RIGHT BEFORE LOOP IN DISTRIBUTE POINTS: {self.players}")
            for i, (player, current_points, stars) in enumerate(self.players):
                if player != caller and player != partner:
                    self.players[i] = (player, current_points - points, stars)

    def distribute_special_game_points(self, caller, player_points, opponent_points):
        caller_index = next(i for i, p in enumerate(self.players) if p[0] == caller)
        self.players[caller_index] = (self.players[caller_index][0], 
                                self.players[caller_index][1] + player_points,
                                self.players[caller_index][2]
                                )
        for i, (player, score, stars) in enumerate(self.players):
            if player != caller:
                self.players[i] = (player, score + opponent_points, stars)

    def end_game(self):
        winners = self.get_winner()
        winner_names = ', '.join([winner[0] for winner in winners])

        #QMessageBox.information(self, "Game Over", f"The winner is: {winner_names}")
        self.show_custom_message_box("Game Over", f"The winner is: {winner_names}")

        self.hands_played = 0
        self.hands_played_label.setText(f'Hands Played: {self.hands_played}')
        
        for i, (player, points, stars) in enumerate(self.players):
            self.players[i] = (player, 0, stars)  # Reset points, keep stars

        for i, (player, points, stars) in enumerate(self.players):
            player_frame = self.player_frames[player]
            player_frame.points = points
            player_frame.stars = stars
            player_frame.role = None
            if i == self.dealer_index:
                player_frame.role = 'DEALER'
            elif i == self.caller_index:
                player_frame.role = 'CALLER'
            player_frame.update()

        for player in self.players:
            self.star_labels[player[0]].setText(f'- {player[2]}')
        
        self.save_game()

    def get_winner(self):
        highest_score = max(self.players, key=lambda player: player[1])[1]
        winners = [player for player in self.players if player[1] == highest_score]
        
        for i, player in enumerate(self.players):
            if player[1] == highest_score:
                self.players[i] = (player[0], 0, player[2] + 1)  # Reset score, increment stars

        return winners
    
    def save_game(self):
        # Generate the file name based on the participant names
        participant_names = '-'.join([player[0] for player in self.players])
        file_name = f"Game-{participant_names}.wst"

        # Save the game state to the file
        with open(file_name, 'w') as file:
            for player, points, stars in self.players:
                file.write(f"{player},{points},{stars}\n")
            file.write(f"hands_played,{self.hands_played}\n")
            file.write(f"dealer_index,{self.dealer_index}\n")
            file.write(f"caller_index,{self.caller_index}\n")

    def show_custom_message_box(self, title, text):
        msg_box = CustomMessageBox(self)
        msg_box.set_message(title, text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


def main():
    app = QApplication(sys.argv)
    window = WhistScoreKeeper()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()