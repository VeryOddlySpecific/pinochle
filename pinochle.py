# import pyCardDeck as pycd 

# pinochle_ranks = ['9', '10', 'J', 'Q', 'K', 'A']
# pinochle_suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
# pinochle_deck = pycd.Deck()

# json_cards = pinochle_deck.export('json')
# print(json_cards)

# import pyCardDeck 
# import yaml

# my_pinochle_deck = yaml.load(open('pinochle_deck.yml'))
# print(my_pinochle_deck)

import random
import json

# get meld options from meld.json
# meld_options = json.load(open('meld.json'))

card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
card_names = ['9', 'J', 'Q', 'K', '10', 'A']

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
            hand_str = ''
            for card in self.cards:
                hand_str += f'| {card.name}{card.suit[0]}({card.rank}) | '
                
            print(hand_str)
        else:
            for card in self.cards:
                print(card)

    def calc_meld(self):
        hand_meld = Meld(self)
        run_values = hand_meld.get_run_values()
        for suit in run_values:
            for item in run_values[suit]:
                print(f'{suit}: {item}')

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
        self.melds = []

    def get_run_values(self):
        # find all sequences of cards in a suit
        # where card.rank is greater than or equal to 2
        run_values = {}
        for suit in card_suits:
            run_values[suit] = {}
            for card in self.hand.cards:
                if card.suit == suit and card.rank >= 2:
                    run_values[suit]['values'] = []
                    run_values[suit]['values'].append(card.rank)
            run_values[suit]['values'].sort()

        print(run_values)
        input('Press enter to continue')
        # run percentages
        for suit, run_val in run_values:
            # get number of unique values in run
            # e.g. 3, 3, 5 has 2 unique values
            unique_values = len(set(run_val['values']))
            run_percentage = unique_values / 5
            run_values[suit]['percentage'] = run_percentage

        return run_values

    def __repr__(self):
        return f'Meld with {len(self.melds)} melds'

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