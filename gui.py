import sys
import os
from PyQt5.QtWidgets import QDialog, QComboBox, QSizePolicy, QSpacerItem, QHBoxLayout, QFrame, QGraphicsOpacityEffect, QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QPen, QPainterPath
from pywinstyles import apply_style
from gui_utils.hand_dialog import HandDialog
from gui_utils.custom_messagebox import CustomMessageBox
from gui_utils.player_frame import PlayerFrame
from game_logic import WhistGameFourPlayers
game = WhistGameFourPlayers()

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

        # Set up the initial layout
        self.load_main_menu()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define the pen to draw the line
        pen = QPen(QColor('red'), 2, Qt.SolidLine)
        painter.setPen(pen)

        # Calculate the center of the window
        center_x = self.width // 2

        # Draw the vertical line
        painter.drawLine(center_x, 0, center_x, self.height)


    ##########################################################
    # LOAD MAIN MENU                                         #
    ##########################################################

    def load_main_menu(self):

        # START NEW GAME BUTTON
        self.start_fresh_game_button = QPushButton("START A NEW GAME", self)
        self.start_fresh_game_button.clicked.connect(self.start_fresh_game)
        self.start_fresh_game_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        self.start_fresh_game_button.setFixedSize(450,100)
        self.start_fresh_game_button.setFont(self.new_game_button_font)
        self.start_fresh_game_button.move((self.width - 450) // 2 , 575)


        # LOAD EXISTING GAME BUTTON
        self.load_existing_game_button = QPushButton("LOAD EXISTING GAME", self)
        self.load_existing_game_button.clicked.connect(self.load_existing_game)
        self.load_existing_game_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
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
        self.start_game_button = QPushButton("Start New Game", self)
        self.start_game_button.clicked.connect(self.start_new_game)
        self.start_game_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        self.start_game_button.setFixedSize(500,80)
        self.start_game_button.setFont(self.new_game_button_font)
        self.start_game_button.move((self.width - 500) // 2, 600)

        self.back_button = QPushButton('<- Back', self)
        self.back_button.clicked.connect(self.back_to_main_menu)
        self.back_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
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
        self.hands_played_label.resize(225,95)
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
            ((self.width - 500) // 2, 180),
            ((self.width - 500) // 2, 330),
            ((self.width - 500) // 2, 480),
            ((self.width - 500) // 2, 630)
        ]

        for i, (player, points, stars) in enumerate(game.get_players()):
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
        self.complete_hand_button = QPushButton("Complete a Hand", self)
        self.complete_hand_button.clicked.connect(self.complete_hand)
        self.complete_hand_button.setStyleSheet("""
            QPushButton { background-color: #DD9637; border: 5px solid #E5C26B; border-radius: 10px; }
            QPushButton:hover { background-color: #E2B258; border: none; }
            QPushButton:pressed { background-color: #DD9637; border: none; }
        """)
        self.complete_hand_button.setFont(self.new_game_button_font)
        self.complete_hand_button.setFixedSize(400,80)
        self.complete_hand_button.move((self.width - 400) // 2 , 790)
        self.complete_hand_button.show()
        
        self.star_labels = {}

        self.setup_star_labels()


    ##########################################################
    # UPDATE SCORES ON UI FUNCTION                           #
    ##########################################################

    def update_standings(self, hand_info):
        # Update the main UI and save the game state
        caller, call, partner, tricks_won = hand_info

        print(f"SELF.PLAYERS BEFORE CALCULATING SCORE: {self.players}")

        if game.is_special_game():
            player_points, opponent_points = game.calculate_special_game_score(call, tricks_won)
            game.distribute_special_game_points(caller, player_points, opponent_points)
        else:
            points = game.calculate_score(call, tricks_won)
            game.distribute_points(caller, partner, points, call)
        
        game.set_hands_played(game.get_hands_played() + 1)
        self.hands_played_label.setText(f'Hands Played: {game.get_hands_played()}')

        game.set_dealer_index((game.get_dealer_index() + 1) % len(game.get_players()))
        game.set_caller_index((game.get_caller_index() + 1) % len(game.get_players()))
        
        for i, (player, points, stars) in enumerate(game.get_players()):
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

        if game.get_hands_played() >= 12:
            self.end_game()  

        self.save_game()


    ##########################################################
    # END GAME FUNCTION                                      #
    ##########################################################

    def end_game(self):
        winners = game.get_winner()
        winner_names = ', '.join([winner[0] for winner in winners])

        #QMessageBox.information(self, "Game Over", f"The winner is: {winner_names}")
        self.show_custom_message_box("Game Over", f"The winner is: {winner_names}")

        game.set_hands_played(0)
        self.hands_played_label.setText(f'Hands Played: {game.get_hands_played}')
        
        players = game.get_players()
        for i, (player, points, stars) in enumerate(players):
            players[i] = (player, 0, stars)  # Reset points, keep stars
        game.set_players(players)

        for i, (player, points, stars) in enumerate(game.get_players()):
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
            self.star_labels[player[0]].setText(f'- {player[2]}')
        
        self.save_game()


    ##########################################################
    # UTIL FUNCTIONS                                         #
    ##########################################################

    def show_custom_message_box(self, title, text):
        msg_box = CustomMessageBox(self)
        msg_box.set_message(title, text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


    def clear_ui(self):
        for widget in self.findChildren(QWidget):
            widget.hide()

    
    def back_to_main_menu(self):
        self.clear_ui()
        self.load_main_menu()

    
    def start_fresh_game(self):
        self.clear_ui()
        self.load_four_player_new_game_ui()

    
    def load_existing_game(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Game", "", "Whist Game Files (*.wst);;All Files (*)", options=options)
        if file_name:
            self.load_game(file_name)

    
    def save_game(self):
        # Generate the file name based on the participant names
        participant_names = '-'.join([player[0] for player in game.get_players()])
        file_name = f"Game-{participant_names}.wst"

        # Save the game state to the file
        with open(file_name, 'w') as file:
            for player, points, stars in game.get_players():
                file.write(f"{player},{points},{stars}\n")
            file.write(f"hands_played,{game.get_hands_played()}\n")
            file.write(f"dealer_index,{game.get_dealer_index()}\n")
            file.write(f"caller_index,{game.get_caller_index()}\n")
    

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
        game.set_players(loaded_players)
        game.set_hands_played(hands_played)
        game.set_dealer_index(dealer_index)
        game.set_caller_index(caller_index)

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

            
            players = [(player1, 0, 0), (player2, 0, 0), (player3, 0, 0), (player4, 0, 0)]
            game.set_players(players)
            self.save_game()
            self.clear_ui()
            self.init_main_ui()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter all player names.")

    
    def complete_hand(self):
        self.hand_dialog = HandDialog(game.get_players(), self)
        self.hand_dialog.exec_()

    
    ##########################################################
    # UI SETUP HELPER FUNCTIONS                              #
    ##########################################################

    def setup_star_labels(self):
        star_pixmap = QPixmap(resource_path('resources/star.png')).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        y_positions = [168, 318, 468, 618]
        
        for i, player in enumerate(game.get_players()):
            player_name, _, stars = player

            star_label = QLabel(self)
            star_label.setPixmap(star_pixmap)
            star_label.setFixedSize(40, 40)
            star_label.move(360, y_positions[i])
            star_label.show()

            text_label = QLabel(f'{stars}', self)
            text_label.move(410, y_positions[i] + 10)
            text_label.resize(40, 20)
            text_label.setStyleSheet('color: white;')
            text_label.setFont(QFont('Impact', 18))
            text_label.show()

            self.star_labels[player_name] = text_label


    def update_star_labels(self):
        for player in self.game.get_players():
            player_name, _, stars = player
            if player_name in self.star_labels:
                self.star_labels[player_name].setText(f'{stars}')
    

    def update_ui_for_loaded_game(self):
        # Update the hands played label
        self.hands_played_label.setText(f'Hands Played: {game.get_hands_played()}')

        # Update player frames
        for i, (player, points, stars) in enumerate(game.get_players()):
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
        for player, points, stars in game.get_players():
            self.star_labels[player].setText(f'{stars}')


def main():
    app = QApplication(sys.argv)
    window = WhistScoreKeeper()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()