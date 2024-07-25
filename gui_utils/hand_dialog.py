from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtGui import QFont
from pywinstyles import apply_style

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

        self.labels = {}
        self.combos = {}

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Complete A Hand")
        self.setFixedSize(700, 750)
        self.setStyleSheet('background-color: #111111; color: white;')
        apply_style(self, "dark")

        layout = QVBoxLayout()

        def add_label_and_combo(label_tag, label_text, combo_box):
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFont(QFont('Impact', 26))
            label.setStyleSheet('color: white;')
            combo_box.setFont(QFont('Impact', 20))
            combo_box.setFixedSize(300,40)
            h_layout.addWidget(label)
            h_layout.addWidget(combo_box)
            layout.addLayout(h_layout)
            self.labels[label_tag] = label
            self.combos[label_tag] = combo_box

        self.caller_combo = QComboBox()
        for player, _, _, _, _, _ in self.players:
            self.caller_combo.addItem(player)
        self.caller_combo.setStyleSheet('background-color: white; color: black;')
        self.caller_combo.currentIndexChanged.connect(self.update_partner_combo)
        add_label_and_combo("caller", "Who got the calling?:", self.caller_combo)

        self.call_combo = QComboBox()
        for i in self.calls:
            self.call_combo.addItem(i)
        self.call_combo.setStyleSheet('background-color: white; color: black;')
        self.call_combo.currentIndexChanged.connect(self.update_partner_combo)
        add_label_and_combo("played", "What was played?:", self.call_combo)

        self.partner_combo = QComboBox()
        for player, _, _, _, _, _ in self.players:
            self.partner_combo.addItem(player)
        self.partner_combo.setStyleSheet('background-color: white; color: black;')
        add_label_and_combo("partner", "Who was partner?:", self.partner_combo)

        self.joiner_input = QComboBox()
        self.joiner_input.addItem('No Joiners')
        for player, _, _, _, _, _ in self.players:
            self.joiner_input.addItem(player)
        self.joiner_input.setStyleSheet('background-color: white; color: black;')
        add_label_and_combo("joiner", 'Did anyone join the call?:', self.joiner_input)
        self.labels["joiner"].hide()
        self.combos["joiner"].hide()

        self.tricks_input = QComboBox()
        for i in self.possible_tricks:
            self.tricks_input.addItem(i)
        self.tricks_input.setStyleSheet('background-color: white; color: black;')
        add_label_and_combo("tricks", "Caller tricks won:", self.tricks_input)

        self.joiner_tricks_input = QComboBox()
        for i in self.possible_tricks:
            self.joiner_tricks_input.addItem(i)
        self.joiner_tricks_input.setStyleSheet('background-color: white; color: black;')
        add_label_and_combo("joiner_tricks", "Joiner tricks won:", self.joiner_tricks_input)
        self.labels["joiner_tricks"].hide()
        self.combos["joiner_tricks"].hide()

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
        complete_button.setFont(QFont('Impact', 27))
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
                      '9 Quarters', 
                      '10 Quarters',
                      '11 Quarters',
                      '12 Quarters',
                      '13 Quarters'
                    ]
        
        joinable_calls = ['Normal Sun',
                          'Clean Sun',
                          'Table Show',
                          'Super Table Show'
                        ]
        
        if selected_call in solo_calls:
            self.combos["partner"].setCurrentIndex(self.caller_combo.currentIndex())
            self.combos["partner"].setEnabled(False)
            self.labels["partner"].show()
            self.combos["partner"].show()
            self.labels["joiner"].hide()
            self.combos["joiner"].hide()
            self.labels["joiner_tricks"].hide()
            self.combos["joiner_tricks"].hide()
        elif selected_call in joinable_calls:
            self.labels["partner"].hide()
            self.combos["partner"].hide()
            self.labels["joiner"].show()
            self.combos["joiner"].show()
            self.labels["joiner_tricks"].show()
            self.combos["joiner_tricks"].show()
            self.update_joiner_combo()
        else:
            self.combos["partner"].setEnabled(True)
            self.labels["partner"].show()
            self.combos["partner"].show()
            self.labels["joiner"].hide()
            self.combos["joiner"].hide()
            self.labels["joiner_tricks"].hide()
            self.combos["joiner_tricks"].hide()

    
    def update_joiner_combo(self):
        caller = self.caller_combo.currentText()
        self.combos["joiner"].clear()
        self.combos["joiner"].addItem('No Joiners')
        for player, _, _, _, _, _ in self.players:
            if player != caller:
                self.combos["joiner"].addItem(player)


    def complete_hand(self):
        caller = self.caller_combo.currentText()
        call = self.call_combo.currentText()
        partner = self.partner_combo.currentText()
        tricks_won = int(self.tricks_input.currentText())

        joinable_calls = ['Normal Sun', 'Clean Sun', 'Table Show', 'Super Table Show']

        if call in joinable_calls:
            joiner = self.joiner_input.currentText()
            joiner_tricks_won = int(self.joiner_tricks_input.currentText())
            if joiner == 'No Joiners':
                joiner_tricks_won = None
                joiner = None
        else:
            joiner_tricks_won = None
            joiner = None

        hand_info = (caller, call, partner, tricks_won, joiner, joiner_tricks_won)
        self.parent().update_standings(hand_info)
        self.accept()