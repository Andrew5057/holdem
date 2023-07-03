from Card import Card
from Deck import Deck
from PokerHand import PokerHand
from itertools import combinations
from random import choice

# human_readable returns [(pair, two_pair, ...), (card ranks)]

class ProbabilityCalculator:

    def __init__(self, card1: Card, card2: Card):
        '''Defines a class that calculates the probability that at least one
            player at a Texas Holdem table beats a given hand.
        
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
                                                Card(c2)]).best_hand()

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
            self.hands[hand] = full_hand.best_hand()
    
    def estimate(self, opponents:int=8, n:int=10000) -> float:
        '''Estimates the probability that at least one person has a hand
            better than the player's.
        
        Arguments:
        opponents (int): The number of other players in play. Defaults to 8.
        n (int): The number of random samples used for estimation. Defaults to
            10,000.

        Output: float in [0, 1] representing the estimated probability that
        at least one opponent has a hand better than the player's.
        '''
        if not isinstance(opponents, int):
            raise TypeError('Default argument opponents must be of type int.')
        if not isinstance(n, int):
            raise TypeError('Default argument n must be of type int.')

        # Not copying the keys screws up the loop because dictionary items 
        # get removed during iteration.
        possible_hands: list = self.hands.keys()
        sample_maxes: list[int] = []
        for game_sample in range(n):
            game_strengths: list[int] = []
            compatible_hands: list[str] = list(possible_hands)
            for opponent in range(opponents):
                new_hand = choice(compatible_hands)
                compatible_hands: list[str] = [hand for hand in compatible_hands
                                               if (new_hand[:2] not in hand) and
                                               (new_hand[2:] not in hand)]
                game_strengths.append(self.hands[new_hand])
            sample_maxes.append(max(game_strengths))
        num_better = len([game for game in sample_maxes if game > self.player.best_hand()])

        return num_better/n
    
    def estimate_chart(self, opponents:int=8, n:int=10000) -> dict:
        '''Estimates the probability that each type of the hand is the 
            strongest at the table, excluding the player's.
        
        Arguments:
        opponents (int): The number of other players in play. Defaults to 8.
        n (int): The number of random samples used for estimation. Defaults to
            10,000.
        
        Output: Dictionary in which the name of each type of hand is the key 
            and the probability of it being the strongest at the table is the 
            value. Also includes key/value pairs for "the player's hand but 
            stronger" and "the player's hand but weaker".
        '''
        if not isinstance(opponents, int):
            raise TypeError('Default argument opponents must be of type int.')
        if not isinstance(n, int):
            raise TypeError('Default argument n must be of type int.')

        # Not copying the keys screws up the loop because dictionary items 
        # get removed during iteration.
        possible_hands: list = self.hands.keys()
        straight_flushes: list[int] = []
        four_of_a_kinds: list[int] = []
        full_houses: list[int] = []
        flushes: list[int] = []
        straights: list[int] = []
        three_of_a_kinds: list[int] = []
        two_pairs: list[int] = []
        pairs: list[int] = []
        high_cards: list[int] = []

        for game_sample in range(n):
            game_strengths: list[int] = []
            compatible_hands: list[str] = list(possible_hands)
            for opponent in range(opponents):
                new_hand = choice(compatible_hands)
                compatible_hands: list[str] = [hand for hand in compatible_hands
                                               if (new_hand[:2] not in hand) and
                                               (new_hand[2:] not in hand)]
                game_strengths.append(self.hands[new_hand])
            
            top = max(game_strengths)
            # Gets the first digit of the best hand
            hand_type = top // 1048576
            match hand_type:
                case 0: high_cards.append(top)
                case 1: pairs.append(top)
                case 2: two_pairs.append(top)
                case 3: three_of_a_kinds.append(top)
                case 4: straights.append(top)
                case 5: flushes.append(top)
                case 6: full_houses.append(top)
                case 7: four_of_a_kinds.append(top)
                case 8: straight_flushes.append(top)
        
        probabilities = {
            'Straight Flush': len(straight_flushes) / n, 
            'Four of a Kind': len(straight_flushes) / n, 
            'Full House': len(straight_flushes) / n, 
            'Flush': len(straight_flushes) / n, 
            'Straight': len(straight_flushes) / n, 
            'Three of a Kind': len(straight_flushes) / n, 
            'Two Pair': len(straight_flushes) / n, 
            'Pair': len(straight_flushes) / n, 
            'High Card': len(straight_flushes) / n
        }

        return probabilities

        # ADD HAND BUT HIGHER AND HAND BUT LOWER