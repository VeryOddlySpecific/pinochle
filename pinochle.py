import random
import json

card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
card_names = ['9', 'J', 'Q', 'K', '10', 'A']
meld_values = {
    '4 Aces': 100,
    '4 Kings': 80,
    '4 Queens': 60,
    '4 Jacks': 40,
    'run': 150,
    'double run': 300,
    'marriage': 40,
    'double marriage': 80,
    'pinochle': 40,
    'double pinochle': 300
}

class Suit:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return f'{self.name}'

class Card:
    def __init__(self, suit, name, rank, is_counted):
        self.suit = suit
        self.name = name
        self.rank = rank
        self.counted = is_counted
        self.lines = self.get_lines()

    def get_lines(self):
        name_space = 5 - len(self.name) - 1
        upper_name = self.name + ' ' * (name_space - 1)

        suit_name_space = 5 - len(self.suit)
        suit_name_space_half = suit_name_space // 2
        suit_name = ' ' * suit_name_space_half + self.suit + ' ' * (suit_name_space_half - 1)
        suit_abbr = self.suit[0]

        lower_name = ' ' * (name_space - 1) + self.name

        abbr_space = 5 - len(suit_abbr) - len(self.name) - 1
        suit_abbr_space = ' ' * (abbr_space - 1)

        line_1 = f'┌───┐'
        line_2 = f'|{self.name}{suit_abbr}{suit_abbr_space}│'
        line_3 = f'└───┘'
        return [line_1, line_2, line_3]

        line_1 = f'┌─────────┐'
        line_2 = f'│{upper_name}│'
        line_3 = f'│         │'
        line_4 = f'│{suit_name}│'
        line_5 = f'│         │'
        line_6 = f'│{lower_name}│'
        line_7 = f'└─────────┘'
        return [line_1, line_2, line_3, line_4, line_5, line_6, line_7]

    def __repr__(self):
        card_lines = self.lines
        return '\n'.join(card_lines)

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
        self.sort_cards()

    def remove_card(self, card):
        if card not in self.cards:
            raise ValueError('Card not in hand')
        self.cards.remove(card)

    def sort_cards(self):
        # sort cards by suit, then by rank within suit
        self.cards.sort(key=lambda x: (x.suit, x.rank))

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f'Hand with {len(self)} cards'

    def show_hand(self, shorthand=False):
        if shorthand:
            top_border = '┌────────┐ ' * len(self.cards)
            bot_border = '└────────┘ ' * len(self.cards)
            
            print(top_border)
            hand_str = ''
            for card in self.cards:
                if len(card.name) == 1:
                    card.name = ' ' + card.name
                hand_str += f'| {card.name}{card.suit[0]}({card.rank}) | '
                
            print(hand_str)

            print(bot_border)
        else:
            for card in self.cards:
                print(card)

    def calc_meld(self):
        hand_meld = Meld(self)
        hand_meld.show_melds()
        # run_values = hand_meld.get_run_values()
        # for suit in run_values:
        #     for item in run_values[suit]:
        #         print(f'{suit}: {item}')

class Deck:
    def __init__(self):
        self.cards = []
        for suit in card_suits:
            index = 0
            for name in card_names:
                is_card_counted = index > 2
                new_card = Card(suit, name, int(index) + 1, is_card_counted)
                self.cards.append(new_card)
                self.cards.append(new_card)
                index += 1

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError('Not enough cards left in the deck')
        return [self.cards.pop() for _ in range(num_cards)]

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f'Deck of {len(self)} cards'

    def show_cards(self):
        for card in self.cards:
            print(card)

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def draw(self, deck, num_cards):
        drawn_cards = deck.deal(num_cards)
        for card in drawn_cards:
            self.hand.add_card(card)

    def show_hand(self, shorthand=False):
        print(self.hand.show_hand(shorthand=shorthand))

    def show_meld(self):
        self.hand.calc_meld()

    def get_name(self):
        return self.name

    def get_hand(self):
        return self.hand

    def __repr__(self):
        return f'Player {self.name}'

class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.players = []
        self.max_players = 2

    def add_score(self, points):
        self.score += points
    
    def add_player(self, player):
        if len(self.players) == self.max_players:
            raise ValueError('Team is full')
        self.players.append(player)

    def remove_player(self, player):
        if player not in self.players:
            raise ValueError('Player not in team')
        self.players.remove(player)

    def show_players(self):
        for player in self.players:
            print(player)

    def __repr__(self):
        return f'{self.name} with score of {self.score}'

class Meld:
    def __init__(self, hand):
        self.hand = hand
        self.melds = {} 
        self.check_sets()
        self.check_sequences()
        self.check_specials()
        self.meld_value = self.calc_meld_value()

    def calc_meld_value(self):
        total_value = 0
        for meld in self.melds:
            total_value += self.melds[meld]['points']

    def check_sets(self):
        # check for 4 of a kind
        valid_ranks = [2, 3, 4, 6]
        cards = self.hand.cards
        
        for rank in valid_ranks:
            # checking for rank
            # example: rank 2
            card_name = card_names[rank - 1]
            if rank == 6:
                card_name = 'A'
            set_meld = [card for card in cards if card.rank == rank]

            # if there are at least 4 cards of the same rank
            if len(set_meld) >= 4:
                # check if all 4 suits are represented
                # if so, add to melds

                # get all suits in the set
                suits = [card.suit for card in set_meld]

                # if there are 4 unique suits
                if len(set(suits)) == 4:
                    multiplier = 1
                    # if there are 8 cards of the same rank
                    if len(set_meld) == 8:
                        multiplier = 10

                    # J (rank 2) is worth 40 points
                    # Q (rank 3) is worth 60 points
                    # K (rank 4) is worth 80 points
                    # A (rank 6) is worth 100 points
                    total_points = rank * 20
                    if rank == 6:
                        total_points -= 20
                    
                    # include multiplier
                    total_points *= multiplier

                    meld_name = f'{str(total_points)} {card_name}s'
                    self.melds[meld_name] = set_meld

            else:
                pc_of_single_meld = len(set_meld) / 4
                pc_of_double_meld = len(set_meld) / 8
                single_meld_name  = f'{pc_of_single_meld * 100}% of {card_name}s around'
                double_meld_name  = f'{pc_of_double_meld * 100}% of double {card_name}s around'
                self.melds[single_meld_name] = set_meld
                self.melds[double_meld_name] = set_meld

    def check_sequences(self):
        # pass
        # check for marriages
        # K and Q of the same suit
        for suit in card_suits:
            king = [card for card in self.hand.cards if card.rank == 4 and card.suit == suit]
            queen = [card for card in self.hand.cards if card.rank == 3 and card.suit == suit]
            if len(king) > 0 and len(queen) > 0 and not (len(king) == 2 and len(queen) == 2):
                # add to melds
                meld_name = f'marriage of {suit}'
                self.melds[meld_name] = king + queen
            if len(king) == 2 and len(queen) == 2:
                # add to melds
                meld_name = f'double marriage of {suit}'
                self.melds[meld_name] = king + queen

        # check for run
        # 5 cards in sequence of the same suit, starting with J
        for suit in card_suits:
            # get all cards that qualify to be part of a run in the given suit
            run_cards = [card for card in self.hand.cards if card.suit == suit and card.rank >= 2]

            if len(run_cards) >= 5 and len(run_cards) < 10:
                # check if single run
                # e.g. J, Q, K, 10, A
                run_set_check = set([card.rank for card in run_cards])

                if len(run_set_check) == 5:
                    # add to melds
                    meld_name = f'run of {suit}'
                    self.melds[meld_name] = run_cards

            # check if double run
            elif len(run_cards) == 10:
                meld_name = f'double run of {suit}'
                self.melds[meld_name] = run_cards

            else:
                # get how close the run is to being a meld in a percentage
                pc_of_single_run = len(run_cards) / 5
                pc_of_double_run = len(run_cards) / 10
                single_run_name  = f'{pc_of_single_run * 100}% of run of {suit}'
                double_run_name  = f'{pc_of_double_run * 100}% of double run of {suit}'
                self.melds[single_run_name] = run_cards
                self.melds[double_run_name] = run_cards

    def check_specials(self):
        pass
        # check for diss
        # 9s of trump suit

        # check for pinochle
        # J of diamonds and Q of spades
        j_diamonds  = [card for card in self.hand.cards if card.rank == 2 and card.suit == 'Diamonds']
        q_spades    = [card for card in self.hand.cards if card.rank == 3 and card.suit == 'Spades']
        num_jd      = len(j_diamonds)
        num_qs      = len(q_spades)
        pinochle    = 0

        if num_jd > 0 and num_qs > 0:            
            if num_jd + num_qs == 4:
                pinochle = 'double'
            elif num_jd and num_qs:
                pinochle = 'single'

        if pinochle:
            meld_name = f'{pinochle} pinochle'
            self.melds[meld_name] = j_diamonds + q_spades

        # get how close the pinochle is to being a meld
        # render as x legs of pinochle
        num_legs    = num_jd + num_qs
        meld_name   = f'{num_legs} leg(s) of pinochle'
        self.melds[meld_name] = j_diamonds + q_spades


    def __repr__(self):
        return f'Meld with {len(self.melds)} melds'

    def show_melds(self):
        for meld in self.melds:
            print(meld)

deck = Deck()
deck.shuffle()

player_1 = Player('Player 1')
player_2 = Player('Player 2')
player_3 = Player('Player 3')
player_4 = Player('Player 4')

team_1 = Team('Team 1')
team_2 = Team('Team 2')

team_1.add_player(player_1)
team_1.add_player(player_3)
team_2.add_player(player_2)
team_2.add_player(player_4)

deal_order = [player_1, player_2, player_3, player_4]

# while deck length is greater than 0
while len(deck) > 0:
    for player in deal_order:
        player.draw(deck, 3)

player_1.show_hand(shorthand=True)
player_1.show_meld()