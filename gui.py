import sys
import os
import random
import glob
import ctypes
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QSizePolicy, QSpacerItem, QHBoxLayout, QFrame, QGraphicsOpacityEffect, QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QPen, QPainterPath, QFontMetrics
from pywinstyles import apply_style
from gui_utils.hand_dialog import HandDialog
from gui_utils.player_frame import PlayerFrame
from gui_utils.custom_info_box import InfoMessageBox
from gui_utils.game_history_dialog import GameHistoryDialog
from game_logic import WhistGameFourPlayers
game = WhistGameFourPlayers()

# combination of two ideas, 12 star, you get new icon, get 12 of new icon, it upgrades. etc.

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class WhistScoreKeeper(QMainWindow):

    ##########################################################
    # SETUP                                                  #
    ##########################################################

    def __init__(self):
        super().__init__()

        # General Attributes
        self.setWindowTitle("Whist Score Keeper")
        self.width = 1200
        self.height = 950
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet('background-color: #111111;')
        self.setWindowIcon(QIcon(resource_path('resources/FullLogo.ico')))
        apply_style(self,"dark")

        #Fonts
        self.new_game_button_font = QFont('Impact', 27)
        self.load_game_button_font = QFont('Impact', 24)
        self.new_game_input_font = QFont('Impact', 24)
        self.backbtn_font = QFont('Impact', 15)
        self.hands_played_font = QFont('Impact', 26)
        
        self.normal_font = QFont('Palatino Linotype', 14)
        self.dealer_label_font = QFont('Palatino Linotype', 10)

        # ICONS
        self.check_icon = QIcon(resource_path('resources/check-circle.png'))
        self.back_icon = QIcon(resource_path('resources/arrow-left-circle'))
        self.load_icon = QIcon(resource_path("resources/saveicon.png"))
        self.play_icon = QIcon(resource_path("resources/playicon.png"))
        self.revert_icon = QIcon(resource_path('resources/revert.png'))
        self.history_icon = QIcon(resource_path('resources/clipboard.png'))
        self.shuffle_icon = QIcon(resource_path('resources/shuffle.png'))

        # Set up the initial layout
        self.load_main_menu()



    ##########################################################
    # LOAD MAIN MENU                                         #
    ##########################################################

    def load_main_menu(self):
        # START NEW GAME BUTTON
        self.start_fresh_game_button = QPushButton("  START A NEW GAME", self)
        self.start_fresh_game_button.clicked.connect(self.start_fresh_game)
        self.start_fresh_game_button.setIcon(self.play_icon)
        self.start_fresh_game_button.setIconSize(QSize(48, 48))
        self.start_fresh_game_button.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                border: 3px solid #155936;
                border-radius: 10px;
                color: black;
            }
            QPushButton:hover {
                background-color: #81C784;
                border-color: #28a745;
            }
            QPushButton:pressed {
                background-color: #218838;
                border-color: #1e7e34;
            }
        """)
        self.start_fresh_game_button.setFixedSize(450,100)
        self.start_fresh_game_button.setFont(self.new_game_button_font)
        self.start_fresh_game_button.move((self.width - 450) // 2 , 575)


        # LOAD EXISTING GAME BUTTON
        self.load_existing_game_button = QPushButton("  LOAD EXISTING GAME", self)
        self.load_existing_game_button.clicked.connect(self.load_existing_game)
        self.load_existing_game_button.setIcon(self.load_icon)
        self.load_existing_game_button.setIconSize(QSize(48, 48))
        self.load_existing_game_button.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                border: 3px solid #1565C0;
                border-radius: 10px;
                color: black;
            }
            QPushButton:hover {
                background-color: #64B5F6;
                border-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #1E88E5;
                border-color: #1565C0;
            }
        """)
        self.load_existing_game_button.setFixedSize(450,80)
        self.load_existing_game_button.setFont(self.load_game_button_font)
        self.load_existing_game_button.move((self.width - 450) // 2, 710)


        # LOGO LABEL
        self.logo_label = QLabel(self)
        logo_pixmap = QPixmap(resource_path('resources/FullLogo_Transparent.png'))
        logo_width = 550
        logo_height = 550
        scaled_pixmap = logo_pixmap.scaled(logo_width, logo_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.resize(logo_width, logo_height)
        self.logo_label.move((self.width - 550) // 2,10)

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

    
    ##########################################################
    # NEW GAME SETUP UI                                      #
    ##########################################################

    def load_four_player_new_game_ui(self):
        # Player name inputs
        self.player1_input = QLineEdit(self)
        self.player1_input.setPlaceholderText("Player 1 Name")
        self.player1_input.setStyleSheet('background-color: white;')
        self.player1_input.resize(400,60)
        self.player1_input.move((self.width - 400) // 2, 180)
        self.player1_input.setFont(self.new_game_input_font)

        self.player2_input = QLineEdit(self)
        self.player2_input.setPlaceholderText("Player 2 Name")
        self.player2_input.setStyleSheet('background-color: white;')
        self.player2_input.resize(400,60)
        self.player2_input.move((self.width - 400) // 2, 280)
        self.player2_input.setFont(self.new_game_input_font)

        self.player3_input = QLineEdit(self)
        self.player3_input.setPlaceholderText("Player 3 Name")
        self.player3_input.setStyleSheet('background-color: white;')
        self.player3_input.resize(400,60)
        self.player3_input.move((self.width - 400) // 2, 380)
        self.player3_input.setFont(self.new_game_input_font)

        self.player4_input = QLineEdit(self)
        self.player4_input.setPlaceholderText("Player 4 Name")
        self.player4_input.setStyleSheet('background-color: white;')
        self.player4_input.resize(400,60)
        self.player4_input.move((self.width - 400) // 2, 480)
        self.player4_input.setFont(self.new_game_input_font)

        # Start game button
        self.start_game_button = QPushButton("  Start New Game", self)
        self.start_game_button.clicked.connect(self.start_new_game)
        self.start_game_button.setIcon(self.play_icon)
        self.start_game_button.setIconSize(QSize(48,48))
        self.start_game_button.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                border: 3px solid #155936;
                border-radius: 10px;
                color: black;
            }
            QPushButton:hover {
                background-color: #81C784;
                border-color: #28a745;
            }
            QPushButton:pressed {
                background-color: #218838;
                border-color: #1e7e34;
            }
        """)
        self.start_game_button.setFixedSize(500,80)
        self.start_game_button.setFont(self.new_game_button_font)
        self.start_game_button.move((self.width - 500) // 2, 600)


        self.back_button = QPushButton(' Back', self)
        self.back_button.clicked.connect(self.back_to_main_menu)
        self.back_button.setIcon(self.back_icon)
        self.back_button.setIconSize(QSize(25,25))
        self.back_button.setStyleSheet("""
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
        self.back_button.setFixedSize(100,50)
        self.back_button.setFont(self.backbtn_font)
        self.back_button.move(20, 20)
        
        
        self.player1_input.show()
        self.player2_input.show()
        self.player3_input.show()
        self.player4_input.show()
        self.start_game_button.show()
        self.back_button.show()
    

    ##########################################################
    # LOAD THE MAIN SCORE KEEPER UI                          #
    ##########################################################

    def init_main_ui(self):
        
        # Hands played label
        self.hands_played_label = QLabel(f'Hands Played: {game.get_hands_played()}', self)
        self.hands_played_label.setFont(self.hands_played_font)
        self.hands_played_label.setStyleSheet('color: white;')
        self.hands_played_label.setAlignment(Qt.AlignCenter)
        self.hands_played_label.resize(238,95)
        self.hands_played_label.move((self.width - 140) // 2, 20)
        self.hands_played_label.show()

        self.hands_played_icon = QLabel(self)
        hands_played_icon_pixmap = QPixmap(resource_path('resources/hands_played_icon.png'))
        hands_played_icon_height = 80
        hands_played_icon_width = 80
        hands_played_icon_scaled_pixmap = hands_played_icon_pixmap.scaled(hands_played_icon_width, hands_played_icon_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.hands_played_icon.setPixmap(hands_played_icon_scaled_pixmap)
        self.hands_played_icon.resize(hands_played_icon_width, hands_played_icon_height)
        self.hands_played_icon.move(435,25)
        self.hands_played_icon.show()

        
        # Create and position player frames
        self.player_frames = {}
        player_label_positions = [
            ((self.width - 600) // 2, 160),
            ((self.width - 600) // 2, 310),
            ((self.width - 600) // 2, 460),
            ((self.width - 600) // 2, 610)
        ]

        for i, (player, points, stars, _, _, _) in enumerate(game.get_players()):
            role = None
            if i == game.get_dealer_index():
                role = 'DEALER'
            elif i == game.get_caller_index():
                role = 'CALLER'

            player_frame = PlayerFrame(player, points, stars, role, self)
            player_frame.setObjectName(player)
            player_frame.move(*player_label_positions[i])
            player_frame.show()

            self.player_frames[player] = player_frame

        # Complete a hand button
        self.complete_hand_button = QPushButton("  Complete a Hand", self)
        self.complete_hand_button.clicked.connect(self.complete_hand)
        self.complete_hand_button.setIcon(self.check_icon)
        self.complete_hand_button.setIconSize(QSize(48,48))
        self.complete_hand_button.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                border: 3px solid #155936;
                border-radius: 10px;
                color: black;
            }
            QPushButton:hover {
                background-color: #81C784;
                border-color: #28a745;
            }
            QPushButton:pressed {
                background-color: #218838;
                border-color: #1e7e34;
            }
        """)
        self.complete_hand_button.setFont(self.new_game_button_font)
        self.complete_hand_button.setContentsMargins(20,20,20,20)
        self.complete_hand_button.setFixedSize(400,80)
        self.complete_hand_button.move((self.width - 400) // 2 , 765)
        self.complete_hand_button.show()

        # Revert button
        self.revert_button = QPushButton("  Revert Last Hand", self)
        self.revert_button.clicked.connect(self.revert_last_game)
        self.revert_button.setIcon(self.revert_icon)
        self.revert_button.setIconSize(QSize(42,42))
        self.revert_button.setStyleSheet("""
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
        self.revert_button.setFont(self.new_game_button_font)
        self.revert_button.setFixedSize(350,60)
        self.revert_button.move((self.width - 350) // 2 , 870)
        self.revert_button.show()

        # Main Menu button
        self.menu_button = QPushButton(" Main Menu", self)
        self.menu_button.clicked.connect(self.back_to_main_menu)
        self.menu_button.setIcon(self.back_icon)
        self.menu_button.setIconSize(QSize(25,25))
        self.menu_button.setStyleSheet("""
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
        self.menu_button.setFont(self.backbtn_font)
        self.menu_button.setFixedSize(150,40)
        self.menu_button.move(20, 20)
        self.menu_button.show()

        # Shuffle players button
        self.shuffle_players_button = QPushButton("  Shuffle Seats", self)
        self.shuffle_players_button.clicked.connect(self.shuffle_players)
        self.shuffle_players_button.setIcon(self.shuffle_icon)
        self.shuffle_players_button.setIconSize(QSize(42,42))
        self.shuffle_players_button.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                border: 3px solid #1565C0;
                border-radius: 10px;
                color: black;
            }
            QPushButton:hover {
                background-color: #64B5F6;
                border-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #1E88E5;
                border-color: #1565C0;
            }
        """)
        self.shuffle_players_button.setFont(self.new_game_button_font)
        self.shuffle_players_button.setFixedSize(320,60)
        self.shuffle_players_button.move((self.width // 6) - (320 // 2), 800)
        self.shuffle_players_button.show()

        # History Button
        self.history_button = QPushButton(' Game History', self)
        self.history_button.clicked.connect(self.show_history_dialog)
        self.history_button.setIcon(self.history_icon)
        self.history_button.setIconSize(QSize(42,42))
        self.history_button.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                border: 3px solid #1565C0;
                border-radius: 10px;
                color: black;
            }
            QPushButton:hover {
                background-color: #64B5F6;
                border-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #1E88E5;
                border-color: #1565C0;
            }
        """)
        self.history_button.setFont(self.new_game_button_font)
        self.history_button.setFixedSize(300,60)
        self.history_button.move((5 * self.width // 6) - (320 // 2), 800)
        self.history_button.show()
        
        self.star_labels = {}
        self.crown_labels = {}

        self.setup_star_labels()
        self.setup_crown_labels()


    ##########################################################
    # UPDATE SCORES ON UI FUNCTION                           #
    ##########################################################

    def update_standings(self, hand_info):

        # temporarily save current state to be able to revert it
        game.save_current_state()

        # Update the main UI and save the game state
        caller, call, partner, tricks_won, joiner, joiner_tricks_won = hand_info

        if game.is_special_game(call):
            player_points, opponent_points = game.calculate_special_game_score(call, tricks_won)
            game.distribute_special_game_points(caller, player_points, opponent_points)
            if joiner:
                joiner_points, joiner_opponent_points = game.calculate_special_game_score(call, joiner_tricks_won)
                game.distribute_special_game_points(joiner, joiner_points, joiner_opponent_points)
        else:
            points = game.calculate_score(call, tricks_won)
            game.distribute_points(caller, partner, points, call)
        
        game.set_hands_played(game.get_hands_played() + 1)
        self.hands_played_label.setText(f'Hands Played: {game.get_hands_played()}')

        game.update_points_history()

        game.set_dealer_index((game.get_dealer_index() + 1) % len(game.get_players()))
        game.set_caller_index((game.get_caller_index() + 1) % len(game.get_players()))
        
        for i, (player, points, stars, _, _, _) in enumerate(game.get_players()):
            player_frame = self.player_frames[player]
            player_frame.points = points
            player_frame.stars = stars
            player_frame.role = None
            if i == game.get_dealer_index():
                player_frame.role = 'DEALER'
            elif i == game.get_caller_index():
                player_frame.role = 'CALLER'
            player_frame.update()

        if game.get_hands_played() >= 12:
            self.end_game()  

        self.save_game()


    ##########################################################
    # END GAME FUNCTION                                      #
    ##########################################################

    def end_game(self):
        winners = game.get_winner()
        winner_names = ', '.join([winner[0] for winner in winners])

        game.set_hands_played(0)
        self.hands_played_label.setText(f'Hands Played: {game.get_hands_played()}')
        
        players = game.get_players()
        print(f"Players before resetting points in end_game: {players}")
        for i, (player, points, stars, bronze, silver, gold) in enumerate(players):
            players[i] = (player, 0, stars, bronze, silver, gold)  # Reset points, keep stars
        game.set_players(players)

        print(f"Players after resetting points in end_game: {game.get_players()}")

        for i, (player, points, stars, _, _, _) in enumerate(game.get_players()):
            player_frame = self.player_frames[player]
            player_frame.points = points
            player_frame.stars = stars
            player_frame.role = None
            if i == game.get_dealer_index():
                player_frame.role = 'DEALER'
            elif i == game.get_caller_index():
                player_frame.role = 'CALLER'
            player_frame.update()

        for player in game.get_players():
            self.star_labels[player[0]].setText(f'{player[2]}')

        game.clear_history()
        
        self.save_game()

        self.show_winner_ui(winner_names)


    ##########################################################
    # UTIL FUNCTIONS                                         #
    ##########################################################

    def clear_ui(self):
        for widget in self.findChildren(QWidget):
            widget.hide()

    
    def back_to_main_menu(self):
        self.clear_ui()
        self.load_main_menu()

    
    def start_fresh_game(self):
        self.clear_ui()
        self.load_four_player_new_game_ui()


    def show_winner_ui(self, winners):
        self.clear_ui()
        self.display_winner(winners)

    
    def load_existing_game(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Game", "", "Whist Game Files (*.wst);;All Files (*)", options=options)
        if file_name:
            self.load_game(file_name)

    
    def save_game(self):
        # Generate the file name based on the participant names
        participant_names = '-'.join([player[0] for player in game.get_players()])
        game_id = game.get_game_id()
        history = game.get_history()
        file_name = f"Game-{participant_names}-{game_id}.wst"
        existing_files = glob.glob(f'*{game_id}.wst')

        if existing_files:
            existing_file = existing_files[0]
            if existing_file != file_name:
                os.rename(existing_file, file_name)

        print(f"Players at the time of saving: {game.get_players()}")

        # Save the game state to the file
        with open(file_name, 'w') as file:
            for player, points, stars, bronze, silver, gold in game.get_players():
                file.write(f"{player},{points},{stars},{bronze},{silver},{gold}\n")
            file.write(f"hands_played,{game.get_hands_played()}\n")
            file.write(f"dealer_index,{game.get_dealer_index()}\n")
            file.write(f"caller_index,{game.get_caller_index()}\n")
            file.write(f'game_id,{game_id}\n')

            # Save history
            for i, game_points in enumerate(history, start=1):
                if game_points:
                    history_line = f'history_{i},' + ','.join([f'{player[0]}={points}' for player, points in zip(game.get_players(), game_points)])
                    file.write(history_line + '\n')
    

    def load_game(self, file_name):
        # Load the game state from the file
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Parse the file content
        loaded_players = []
        hands_played = 0
        dealer_index = 0
        caller_index = 0
        game_id = None
        history = [[] for _ in range(12)]

        for line in lines:
            parts = line.strip().split(',')
            if parts[0] == 'hands_played':
                hands_played = int(parts[1])
            elif parts[0] == 'dealer_index':
                dealer_index = int(parts[1])
            elif parts[0] == 'caller_index':
                caller_index = int(parts[1])
            elif parts[0] == 'game_id':
                game_id = parts[1]
            elif parts[0].startswith('history_'):
                round_number = int(parts[0].split('_')[1])
                game_points = []
                for p in parts[1:]:
                    if '=' in p:
                        game_points.append(int(p.split('=')[1]))
                    else:
                        game_points.append('')  # Append empty string for missing values
                history[round_number - 1] = game_points
            else:
                player = parts[0]
                points = int(parts[1])
                stars = int(parts[2])
                bronze = int(parts[3])
                silver = int(parts[4])
                gold = int(parts[5])
                loaded_players.append((player, points, stars, bronze, silver, gold))

        # Update the game state
        game.set_players(loaded_players)
        game.set_hands_played(hands_played)
        game.set_dealer_index(dealer_index)
        game.set_caller_index(caller_index)
        game.set_game_id(game_id)
        game.set_history(history)

        # Update the UI
        self.clear_ui()
        self.init_main_ui()
        self.update_ui_for_loaded_game()

    
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

            
            players = [(player1, 0, 0, 0, 0, 0), (player2, 0, 0, 0, 0, 0), (player3, 0, 0, 0, 0, 0), (player4, 0, 0, 0, 0, 0)]
            game.set_players(players)
            self.save_game()
            self.clear_ui()
            self.init_main_ui()
        
        else:
            QMessageBox.warning(self, "Input Error", "Please enter all player names.")

    
    def complete_hand(self):
        self.hand_dialog = HandDialog(game.get_players(), self)
        self.hand_dialog.exec_()

    
    def shuffle_players(self):
        if game.get_hands_played() > 0:
            msg_box = InfoMessageBox('Not Allowed', 'You cannot shuffle players in the middle of a game.', self)
            msg_box.exec_()
            return
        
        players = game.get_players()
        random.shuffle(players)
        game.set_players(players)
        self.update_ui_on_shuffle()
        self.save_game()

    
    def show_history_dialog(self):
        history = game.get_history()
        dialog = GameHistoryDialog(history, game.get_players(), self)
        dialog.exec_()


    def revert_last_game(self):
        if game.revert_last_state():
            self.update_ui_for_loaded_game()  # Update UI to reflect the reverted state
            self.save_game()  # Save the reverted state to the file
        else:
            QMessageBox.warning(self, "Warning", "No previous state to revert to.")
    
    ##########################################################
    # UI SETUP HELPER FUNCTIONS                              #
    ##########################################################

    def setup_star_labels(self):
        star_pixmap = QPixmap(resource_path('resources/star.png')).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        y_positions = [148, 298, 448, 598]
        
        for i, player in enumerate(game.get_players()):
            player_name, _, stars, _, _, _ = player

            star_label = QLabel(self)
            star_label.setPixmap(star_pixmap)
            star_label.setFixedSize(40, 40)
            star_label.move(310, y_positions[i])
            star_label.show()

            text_label = QLabel(f'{stars}', self)
            text_label.move(358, y_positions[i] + 8)
            text_label.resize(50, 22)
            text_label.setStyleSheet('color: white;')
            text_label.setFont(QFont('Impact', 20))
            text_label.show()

            self.star_labels[player_name] = text_label


    def update_star_labels(self):
        for player in self.game.get_players():
            player_name, _, stars, _, _, _ = player
            if player_name in self.star_labels:
                self.star_labels[player_name].setText(f'{stars}')

    
    def setup_crown_labels(self):
        # Crown pixmaps
        bronze_crown_pixmap = QPixmap(resource_path('resources/bronze_crown.png')).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        silver_crown_pixmap = QPixmap(resource_path('resources/silver_crown.png')).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        gold_crown_pixmap = QPixmap(resource_path('resources/gold_crown.png')).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        y_positions = [148, 298, 448, 598]
        
        for i, player in enumerate(game.get_players()):
            player_name, _, _, bronze_crowns, silver_crowns, gold_crowns = player

            # Bronze Crowns
            if bronze_crowns > 0:
                bronze_crown_label = QLabel(self)
                bronze_crown_label.setPixmap(bronze_crown_pixmap)
                bronze_crown_label.setFixedSize(40, 40)
                bronze_crown_label.move(400, y_positions[i])
                bronze_crown_label.show()

                bronze_crown_text = QLabel(f'{bronze_crowns}', self)
                bronze_crown_text.move(448, y_positions[i] + 8)
                bronze_crown_text.resize(50, 22)
                bronze_crown_text.setStyleSheet('color: white;')
                bronze_crown_text.setFont(QFont('Impact', 20))
                bronze_crown_text.show()

                self.crown_labels[player_name + '_bronze'] = bronze_crown_text

            # Silver Crowns
            elif silver_crowns > 0:
                silver_crown_label = QLabel(self)
                silver_crown_label.setPixmap(silver_crown_pixmap)
                silver_crown_label.setFixedSize(40, 40)
                silver_crown_label.move(400, y_positions[i])
                silver_crown_label.show()

                silver_crown_text = QLabel(f'{silver_crowns}', self)
                silver_crown_text.move(448, y_positions[i] + 8)
                silver_crown_text.resize(50, 22)
                silver_crown_text.setStyleSheet('color: white;')
                silver_crown_text.setFont(QFont('Impact', 20))
                silver_crown_text.show()

                self.crown_labels[player_name + '_silver'] = silver_crown_text

            # Gold Crowns
            elif gold_crowns > 0:
                gold_crown_label = QLabel(self)
                gold_crown_label.setPixmap(gold_crown_pixmap)
                gold_crown_label.setFixedSize(40, 40)
                gold_crown_label.move(400, y_positions[i])
                gold_crown_label.show()

                gold_crown_text = QLabel(f'{gold_crowns}', self)
                gold_crown_text.move(448, y_positions[i] + 8)
                gold_crown_text.resize(50, 22)
                gold_crown_text.setStyleSheet('color: white;')
                gold_crown_text.setFont(QFont('Impact', 20))
                gold_crown_text.show()

                self.crown_labels[player_name + '_gold'] = gold_crown_text

                # No crowns, create empty label
            else:
                empty_label = QLabel(self)
                empty_label.setFixedSize(70, 42)
                empty_label.move(400, y_positions[i])
                empty_label.show()

                self.crown_labels[player_name + '_empty'] = empty_label

    
    def update_crown_labels(self):
        for player in game.get_players():
            player_name, _, _, bronze_crowns, silver_crowns, gold_crowns = player

            # Update Bronze Crowns
            if bronze_crowns > 0 and player_name + '_bronze' in self.crown_labels:
                self.crown_labels[player_name + '_bronze'].setText(f'{bronze_crowns}')

            # Update Silver Crowns
            if silver_crowns > 0 and player_name + '_silver' in self.crown_labels:
                self.crown_labels[player_name + '_silver'].setText(f'{silver_crowns}')

            # Update Gold Crowns
            if gold_crowns > 0 and player_name + '_gold' in self.crown_labels:
                self.crown_labels[player_name + '_gold'].setText(f'{gold_crowns}')
    

    def update_ui_for_loaded_game(self):
        # Update the hands played label
        self.hands_played_label.setText(f'Hands Played: {game.get_hands_played()}')

        # Update player frames
        for i, (player, points, stars, _, _, _) in enumerate(game.get_players()):
            player_frame = self.player_frames[player]
            player_frame.points = points
            player_frame.stars = stars
            player_frame.role = None
            if i == game.get_dealer_index():
                player_frame.role = 'DEALER'
            elif i == game.get_caller_index():
                player_frame.role = 'CALLER'
            player_frame.update()

        # Update star labels
        for player, points, stars, _, _, _ in game.get_players():
            self.star_labels[player].setText(f'{stars}')
        
        self.setup_crown_labels()

    def update_ui_on_shuffle(self):
        player_label_positions = [
        ((self.width - 600) // 2, 160),
        ((self.width - 600) // 2, 310),
        ((self.width - 600) // 2, 460),
        ((self.width - 600) // 2, 610)
        ]

        self.hands_played_label.setText(f'Hands Played: {game.get_hands_played()}')

        # Clear the existing player frames
        for player_frame in self.player_frames.values():
            player_frame.hide()
            player_frame.setParent(None)

        # Recreate the player frames in the new order
        self.player_frames = {}
        for i, (player, points, stars, _, _, _) in enumerate(game.get_players()):
            role = None
            if i == game.get_dealer_index():
                role = 'DEALER'
            elif i == game.get_caller_index():
                role = 'CALLER'

            player_frame = PlayerFrame(player, points, stars, role)
            player_frame.setObjectName(player)
            player_frame.setParent(self)  # Assuming this is the main container
            player_frame.move(*player_label_positions[i])
            player_frame.show()
            self.player_frames[player] = player_frame


        for star_label in self.star_labels.values():
            star_label.hide()
            star_label.setParent(None)
            star_label.deleteLater()
        
        self.star_labels.clear()

        for crown_key, crown_label in list(self.crown_labels.items()):
            if '_empty' not in crown_key:
                crown_label.hide()
                crown_label.setParent(None)
                crown_label.deleteLater()
                del self.crown_labels[crown_key]

        self.setup_star_labels()
        self.setup_crown_labels()

        # Ensure the complete hand button is visible
        self.complete_hand_button.show()

    
    def display_winner(self, winner):

        # OKAY BUTTON
        self.okay_button = QPushButton("OKAY", self)
        self.okay_button.clicked.connect(self.reset_ui_for_new_game)
        self.okay_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        self.okay_button.setFixedSize(400,80)
        self.okay_button.setFont(self.new_game_button_font)
        self.okay_button.move((self.width - 400) // 2 , 720)

        # WINNER NAME
        font = self.new_game_button_font
        font_metrics = QFontMetrics(font)
        text = f'THE WINNER(S) ARE: {winner}'
        text_width = font_metrics.horizontalAdvance(text)

        self.winner_name_label = QLabel(text, self)
        self.winner_name_label.setFont(self.new_game_button_font)
        self.winner_name_label.resize(text_width,100)
        self.winner_name_label.setStyleSheet('color: white;')
        self.winner_name_label.move((self.width - text_width) // 2, 580)

        # LOGO LABEL
        self.winner_label = QLabel(self)
        logo_pixmap = QPixmap(resource_path('resources/winner_logo.png'))
        logo_width = 750
        logo_height = 550
        scaled_pixmap = logo_pixmap.scaled(logo_width, logo_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.winner_label.setPixmap(scaled_pixmap)
        self.winner_label.resize(logo_width, logo_height)
        self.winner_label.move((self.width - 750) // 2, 10)

        self.effect = QGraphicsOpacityEffect(self)
        self.winner_label.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b'opacity')
        self.animation.setDuration(3000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

        # SHOW
        self.winner_label.show()
        self.okay_button.show()
        self.winner_name_label.show()

    
    def reset_ui_for_new_game(self):
        # Hide the winner UI components
        self.winner_label.hide()
        self.okay_button.hide()
        self.winner_name_label.hide()

        self.init_main_ui()
        self.update_ui_for_loaded_game()




def main():
    app = QApplication(sys.argv)
    window = WhistScoreKeeper()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":

    # Set DPI awareness to be DPI unaware (100% scaling)
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception as e:
        print(f"Failed to set DPI awareness: {e}")

    main()