import random
import json

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
                        total_points += 80
                    
                    # include multiplier
                    total_points *= multiplier

                    meld_name = f'{str(total_points)} {card_name}s'
                    self.melds[meld_name] = set_meld

    def check_sequences(self):
        pass
        # check for marriages
        # K and Q of the same suit

        # check for run
        # 5 cards in sequence of the same suit, starting with J

        # check for double run
        # 2 instances of 5 cards in sequence of the same suit, starting with J

    def check_specials(self):
        pass
        # check for diss
        # 9s of trump suit

        # check for pinochle
        # J of diamonds and Q of spades

        # check for double pinochle
        # 2 instances of J of diamonds and Q of spades

    def get_run_values(self):
        # initial hand
        hand = self.hand.cards
        run_checker = {
            'Hearts': [],
            'Diamonds': [],
            'Clubs': [],
            'Spades': []
        }
        for card in hand:
            # print("  Card in the hand is: ")
            # print(card)
            # print("  ")

            # input("   press enter to run next check. Next check is to see if card would be in a run")

            if card.rank < 2:
                # print("  Card rank is less than 2, so skipping")
                continue
                
            # print("  Card rank is greater than 2, " + str(card.rank) + ", so adding card to run_checker array.")
            run_checker[card.suit].append(card)

            # input("   card has been checked and processed, press enter to move to the next card.")

            # print("  ")
            # print("  current run_checker array is: ")
            # for suit in run_checker:
            #     print("      " + suit + ": ")
            #     for card in run_checker[suit]:
            #         print("          " + str(card.name) + "-" + str(card.suit))
            # print("  ")

        for suit in run_checker:
            # checking how much of a run each suit has
            unique_values = len(set([card.rank for card in run_checker[suit]]))
            # print("   ")
            # print("   number of unique values in run_checker array for " + suit + " is: " + str(unique_values))
            # print("   ")    

            base_run_percentage = str(int( (unique_values / 5) * 100 )) + "%"
            # print("   base run percentage for " + suit + " is: " + base_run_percentage) 

        # get longest run in run_checker array
        longest_run = None
        for suit in run_checker:
            if longest_run is None or len(run_checker[suit]) > len(longest_run):
                longest_run = run_checker[suit]

        print("   ")
        print("   longest run is: ")
        for card in longest_run:
            print("      " + str(card.name) + "-" + str(card.suit))

        # calculate current run value in points
        # where 150 points is a full run
        unique_values = len(set([card.rank for card in longest_run]))
        run_percentage = unique_values / 5
        current_run_value = run_percentage * 150

        print("   ")
        print("   current run value is: " + str(current_run_value))

        quit()

    def old_get_run_values(self):
        # find all sequences of cards in a suit
        # where card.rank is greater than or equal to 2
        run_values = {}
        for suit in card_suits:
            run_values[suit] = {}
            for card in self.hand.cards:
                if card.suit == suit and card.rank >= 2:
                    run_values[suit]['values'] = []
                    run_values[suit]['values'].append(card.rank)
            if len(run_values[suit]['values']) == 0:
                del run_values[suit]
            else:
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