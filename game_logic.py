import uuid

class WhistGameFourPlayers:
    def __init__(self):
        super().__init__()

        # Unique identifier
        self.game_id = str(uuid.uuid4())

        # Set up players
        self.players = [("Player 1", 0, 0, 0, 0, 0), # Name, Points, Stars, Bronze Crowns, Silver Crowns, Gold Crowns
                        ("Player 2", 0, 0, 0, 0, 0), 
                        ("Player 3", 0, 0, 0, 0, 0), 
                        ("Player 4", 0, 0, 0, 0, 0)]
        
        # Dealer/Caller and Amount of Hands Played
        self.dealer_index = 0
        self.caller_index = 1
        self.hands_played = 0

        # History
        self.history = [[] for _ in range(12)]

        # Turn History for reverting
        self.revert_history = []

        #Scorecard
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

        # Special Games Scorecard
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

    
    def get_players(self):
        return self.players
    

    def get_player_data(self, player_name):
        for player, points, stars in self.players:
            if player == player_name:
                return points, stars
        return None, None 
    
    
    def get_dealer_index(self):
        return self.dealer_index
    
    
    def get_caller_index(self):
        return self.caller_index
    
    
    def get_hands_played(self):
        return self.hands_played
    
    
    def set_players(self, players):
        self.players = players

    
    def set_dealer_index(self, dealer_index):
        self.dealer_index = dealer_index

    
    def set_caller_index(self, caller_index):
        self.caller_index = caller_index

    
    def set_hands_played(self, hands_played):
        self.hands_played = hands_played

    
    def calculate_score(self, call, tricks_won):
        scores = self.scorecard[call]
        return scores[tricks_won]
    

    def is_special_game(self, call):
        return call in self.special_games
    
    
    def get_game_id(self):
        return self.game_id
    
    
    def set_game_id(self, id):
        self.game_id = id

    
    def update_points_history(self):
        current_points = [points for _, points, _, _, _, _ in self.players]
        if self.hands_played <= 12:
            self.history[self.hands_played - 1] = current_points
    

    def get_history(self):
        return self.history
    
    
    def set_history(self, history):
        self.history = history

    
    def clear_history(self):
        self.history = [[] for _ in range(12)]

    
    def save_current_state(self):
        state = {
            'players': [player[:] for player in self.players],
            'hands_played': self.hands_played,
            'dealer_index': self.dealer_index,
            'caller_index': self.caller_index,
            'history': [history[:] for history in self.history]
        }
        self.revert_history.append(state)

    
    def revert_last_state(self):
        if self.revert_history:
            last_state = self.revert_history.pop()
            self.players = last_state['players']
            self.hands_played = last_state['hands_played']
            self.dealer_index = last_state['dealer_index']
            self.caller_index = last_state['caller_index']
            self.history = last_state['history']
            return True
        return False
    
    
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

        if call in ["7 Quarters", "8 Quarters", "9 Quarters", "10 Quarters", "11 Quarters", "12 Quarters", "13 Quarters"] or caller == partner:
            # Solo game
            self.players[caller_index] = (self.players[caller_index][0], 
                                          self.players[caller_index][1] + points * 3,
                                          self.players[caller_index][2],
                                          self.players[caller_index][3],
                                          self.players[caller_index][4],
                                          self.players[caller_index][5]
                                          )
            for i, (player, score, stars, bronze, silver, gold) in enumerate(self.players):
                if player != caller:
                    self.players[i] = (player, score - points, stars, bronze, silver, gold)
        else:
            # Regular game
            self.players[caller_index] = (self.players[caller_index][0], 
                                          self.players[caller_index][1] + points,
                                          self.players[caller_index][2],
                                          self.players[caller_index][3],
                                          self.players[caller_index][4],
                                          self.players[caller_index][5]
                                          )
            self.players[partner_index] = (self.players[partner_index][0], 
                                           self.players[partner_index][1] + points,
                                           self.players[partner_index][2],
                                           self.players[partner_index][3],
                                           self.players[partner_index][4],
                                           self.players[partner_index][5]
                                           )

            for i, (player, current_points, stars, bronze, silver, gold) in enumerate(self.players):
                if player != caller and player != partner:
                    self.players[i] = (player, current_points - points, stars, bronze, silver, gold)

    
    def distribute_special_game_points(self, caller, player_points, opponent_points):
        caller_index = next(i for i, p in enumerate(self.players) if p[0] == caller)
        self.players[caller_index] = (self.players[caller_index][0], 
                                self.players[caller_index][1] + player_points,
                                self.players[caller_index][2],
                                self.players[caller_index][3],
                                self.players[caller_index][4],
                                self.players[caller_index][5]
                                )
        for i, (player, score, stars, bronze, silver, gold) in enumerate(self.players):
            if player != caller:
                self.players[i] = (player, score + opponent_points, stars, bronze, silver, gold)

    
    def get_winner(self):
        highest_score = max(self.players, key=lambda player: player[1])[1]
        winners = [player for player in self.players if player[1] == highest_score]

        print(f"Players before incrementing stars: {self.players}")

        for i, player in enumerate(self.players):
            if player[1] == highest_score:
                self.players[i] = (player[0], 0, player[2] + 1, player[3], player[4], player[5])  # Reset score, increment stars

        print(f"Players after incrementing stars: {self.players}")

        self.check_and_award_crowns()

        return winners
    

    def check_and_award_crowns(self):
        award_crown = False

        # Check if any player should be awarded crowns
        for i, player in enumerate(self.players):
            name, points, stars, bronze, silver, gold = player
            if stars >= 12:
                stars = 0
                award_crown = True

                # Increment crown based on current crown level
                if gold > 0:
                    gold += 1
                    if gold >= 12:
                        gold = 12 # PLayer is supreme winner
                elif silver > 0:
                    silver += 1
                    if silver >= 12:
                        silver = 0
                        gold += 1
                elif bronze > 0:
                    bronze += 1
                    if bronze >= 12:
                        bronze = 0
                        silver += 1
                else:
                    bronze += 1

                self.players[i] = (name, points, stars, bronze, silver, gold)

        # Reset stars for all players if any player was awarded a crown
        if award_crown:
            for i, player in enumerate(self.players):
                name, points, stars, bronze, silver, gold = player
                self.players[i] = (name, points, 0, bronze, silver, gold)