from Card import Card
from PokerHand import PokerHand
from itertools import combinations
from random import choice
import pandas as pd

# human_readable returns [(pair, two_pair, ...), (card ranks)]

class ProbabilityCalculator:
    # For sorting pandas dataframes
    hand_type_indexes = {
        'High Card': 8,
        'Pair': 7,
        'Two Pair': 6,
        'Three of a Kind': 5,
        'Straight': 4,
        'Flush': 3,
        'Full House': 2,
        'Four of a Kind': 1,
        'Straight Flush': 0
    }

    def __init__(self, card1: Card, card2: Card, opponents:int=8):
        '''Defines a class that calculates the probability that at least one
            player a[t a Texas Holdem table beats a given hand.
        
        After instantiation, this class's instance variables should NEVER be 
            altered or deleted, and new instance variables should NEVER be 
            declared.
        
        Positional arguments:
        card1 (Card): One card in the player's hand.
        card2 (Card): Another card in the player's hand.
        
        Instance variables:
        player (PokerHand): A continuously updated PokerHand object
            representing the player's hand, including community cards.
        hands (dict[str: int]): A continuously updated dictionary
            representing all possible hands. Keys are strings representing 
            each hand's hole cards, such as 'KH5S' for a King of Hearts and a 
            5 of Spades. Values are ints representing the hand's strength 
            (including community cards), as defined by the PokerHand class.
        community_cards: A continuously updated list representing community
            cards.
        opponents (int): The number of other players in play. Defaults to 8.
        n (int): The number of random samples used for estimation. Defaults to
            10,000.

        Methods:
        add_community: Adds cards to the instance's community cards.
        estimate: Uses random sampling to estimate the probability of at 
            least one player at the table beating the player's hand.

        '''
        if not isinstance(card1, Card):
            raise TypeError('Positional variable card1 must be of type Card.')
        if not isinstance(card2, Card):
            raise TypeError('Positional variable card2 must be of type Card.')

        self.player: PokerHand = PokerHand([card1, card2])

        if not isinstance(opponents, int):
            raise TypeError('Optional variable opponents must be of type int.')
        self.opponents = opponents

        possible_cards: list[str] = ['2H', '2D', '2S', '2C', '3H', '3D', 
                                     '3S', '3C', '4H', '4D', '4S', '4C',
                                     '5H', '5D', '5S', '5C', '6H', '6D', 
                                     '6S', '6C', '7H', '7D', '7S', '7C', 
                                     '8H', '8D', '8S', '8C', '9H', '9D', 
                                     '9S', '9C', 'TH', 'TD', 'TS', 'TC', 
                                     'JH', 'JD', 'JS', 'JC', 'QH', 'QD', 
                                     'QS', 'QC', 'KH', 'KD', 'KS', 'KC', 
                                     'AH', 'AD', 'AS', 'AC']
        possible_cards.remove(str(card1))
        possible_cards.remove(str(card2))

        self.hands: dict[str: int] = {}
        possible_hands: tuple = combinations(possible_cards, 2)
        for hand in possible_hands:
            c1, c2 = hand[0], hand[1]
            # Storing hand strenghts as a dictionary shortens probability 
            # estimation time, as the strength only has to be determiend once.
            self.hands[f'{c1}{c2}'] = PokerHand([Card(c1),
                                                Card(c2)]).best_hand()['value']

        self.community_cards: list[Card] = []
        
    def add_community(self, *new_cards: Card) -> None:
        '''Updates the ProbabilityCalculator to include new community_cards.
            Removes newly impossible hands accordingly. Also updates best_hand
            values for each hand in the hands dictionary.
        
        Arguments:
        *new_cards: Any number of Card objects, representing the newly drawn
            community cards.
        
        Output: None
        '''
        for card in new_cards:
            if not isinstance(card, Card):
                raise TypeError('All arguments must be of type Card.')
            if card in self.community_cards:
                raise ValueError('No arguments can already exist in \
                                 community_cards.')

        if len(set(new_cards)) != len(new_cards):
            # Catchces if duplicate cards were entered as arguments.
            raise ValueError('All arguments must be unique.')

        for card in new_cards:
            # self.player isn't part of the hands dictionary, so it has to 
            # get updated independently.
            self.player.append(card)

        self.community_cards.extend(new_cards)
        hand_list = set(self.hands.keys())
        
        for hand in hand_list:
            c1, c2 = Card(hand[:2]), Card(hand[2:])
            if (c1 in self.community_cards) or (c2 in self.community_cards):
                # Hands that contain a community card are impossible, so they 
                # can safely be removed from the hands dictionary.
                del self.hands[hand]
                continue
            full_hand = PokerHand(self.community_cards + [c1, c2])
            self.hands[hand] = full_hand.best_hand()['value']
    
    def estimate(self, n:int=10000) -> float:
        '''Estimates the probability that at least one person has a hand
            better than the player's.
        
        Arguments:
        n (int): The number of simulations to use in the estimate. Defaults to
            10000.

        Output: float in [0, 1] representing the estimated probability that
        every opponent has a hand weaker than the player's.
        '''

        # Not copying the keys screws up the loop because dictionary items 
        # get removed during iteration.
        possible_hands: list = self.hands.keys()
        sample_maxes: list[int] = []
        for game_sample in range(n):
            game_strengths: list[int] = []
            compatible_hands: list[str] = list(possible_hands)
            for opponent in range(self.opponents):
                new_hand = choice(compatible_hands)
                compatible_hands: list[str] = [hand for hand in compatible_hands
                                               if (new_hand[:2] not in hand) and
                                               (new_hand[2:] not in hand)]
                game_strengths.append(self.hands[new_hand])
            sample_maxes.append(max(game_strengths))
        num_better = len([game for game in sample_maxes if game < self.player.best_hand()['value']])

        return num_better/n
    
    def estimate_chart(self, n:int=10000) -> dict:
        '''Estimates the probability that each type of the hand is the 
            strongest at the table, excluding the player's.
        
        Arguments:
        n (int): The number of simulations to use in the estimate. Defaults to
            10000.
        
        Output: Dictionary in which the name of each type of hand is the key 
            and the probability of it being the strongest at the table is the 
            value. Also includes key/value pairs for "the player's hand but 
            stronger" and "the player's hand but weaker".
        '''
        
        # Not copying the keys screws up the loop because dictionary items 
        # get removed during iteration.
        possible_hands: list = self.hands.keys()

        hand_types = {
            'Straight Flush': [],
            'Four of a Kind': [],
            'Full House': [],
            'Flush': [],
            'Straight': [],
            'Three of a Kind': [],
            'Two Pair': [],
            'Pair': [],
            'High Card': []
        }
        

        for game_sample in range(n):
            game_strengths: list[int] = []
            compatible_hands: list[str] = list(possible_hands)
            for opponent in range(self.opponents):
                new_hand = choice(compatible_hands)
                compatible_hands: list[str] = [hand for hand in compatible_hands
                                               if (new_hand[:2] not in hand) and
                                               (new_hand[2:] not in hand)]
                game_strengths.append(self.hands[new_hand])
            
            top = max(game_strengths)

            # Gets the first digit of the best hand
            # Using the builtin is probably faster but needs some refactoring
            if len(self.community_cards) == 0:
                hand_type = top // 256
            else:
                hand_type = top // 1048576
            match hand_type:
                case 0: hand_types['High Card'].append(top)
                case 1: hand_types['Pair'].append(top)
                case 2: hand_types['Two Pair'].append(top)
                case 3: hand_types['Three of a Kind'].append(top)
                case 4: hand_types['Straight'].append(top)
                case 5: hand_types['Flush'].append(top)
                case 6: hand_types['Full House'].append(top)
                case 7: hand_types['Four of a Kind'].append(top)
                case 8: hand_types['Straight Flush'].append(top)
        
        hand_counts = {hand_name: len(hand_types[hand_name]) for hand_name in hand_types}
        types_frame: pd.DataFrame = pd.DataFrame.from_dict(hand_counts, orient='index')
        types_frame.reset_index(inplace=True)
        types_frame.columns = 'Hand', 'Count'

        player_strength: int = self.player.best_hand()['level']
        player_hand_type = player_strength // 1048576
        match player_hand_type:
            case 0: player_hand_type = 'High Card'
            case 1: player_hand_type = 'Pair'
            case 2: player_hand_type = 'Two Pair'
            case 3: player_hand_type = 'Three of a Kind'
            case 4: player_hand_type = 'Straight'
            case 5: player_hand_type = 'Flush'
            case 6: player_hand_type = 'Full House'
            case 7: player_hand_type = 'Four of a Kind'
            case 8: player_hand_type = 'Straight Flush'
        
        index_high: int = self.hand_type_indexes[player_hand_type]-0.5
        index_low: int = self.hand_type_indexes[player_hand_type]+0.5

        types_frame.loc[index_high] = f'{player_hand_type} (High)', 0
        types_frame.loc[index_low] = f'{player_hand_type} (Low)', 0
        
        for hand_strength in hand_types[player_hand_type]:
            if hand_strength > player_strength:
                types_frame.at[index_high, 'Count'] += 1
            elif hand_strength < player_strength:
                types_frame.at[index_low, 'Count'] += 1
        types_frame.drop(self.hand_type_indexes[player_hand_type], inplace=True)

        types_frame['Probability'] = types_frame['Count'].map(lambda count: count/n)
        types_frame.drop('Count', axis=1, inplace=True)

        types_frame.reset_index(drop=True, inplace=True)

        return types_frame
