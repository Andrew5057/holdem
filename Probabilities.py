from Card import Card
from Deck import Deck
from PokerHand import PokerHand
from itertools import combinations


class ProbabilityCalculator:

    def __init__(self, cards: list[Card], n_players: int):
        
        self.player: PokerHand = PokerHand(cards)
        self.deck: Deck = Deck()
        self.deck.remove(cards[0])
        self.deck.remove(cards[1])

        possible_cards: list[str] = ['2H', '2D', '2S', '2C', '3H', '3D', 
                                     '3S', '3C', '4H', '4D', '4S', '4C',
                                     '5H', '5D', '5S', '5C', '6H', '6D', 
                                     '6S', '6C', '7H', '7D', '7S', '7C', 
                                     '8H', '8D', '8S', '8C', '9H', '9D', 
                                     '9S', '9C', 'TH', 'TD', 'TS', 'TC', 
                                     'JH', 'JD', 'JS', 'JC', 'QH', 'QD', 
                                     'QS', 'QC', 'KH', 'KD', 'KS', 'KC', 
                                     'AH', 'AD', 'AS', 'AC']
        possible_cards.remove(str(cards[0]))
        possible_cards.remove(str(cards[1]))
        self.hands: dict[str: int] = {}
        possible_hands = combinations(self.possible_cards, 2)
        for hand in possible_hands:
            c1, c2 = hand[0], hand[1]
            self.hands[f'{c1}{c2}'] = PokerHand(Card(c1),
                                                Card(c2)).best_hand()
        
        self.state = 0

        self.community_cards = []
        
    def next(self, *new_cards: Card) -> None:
        '''Updates the ProbabilityCalculator to include new community_cards.
            Removes newly impossible hands accordingly. Also updates best_hand
            values for each hand in the hands dictionary.
        
        Arguments:
        *new_cards: Any number of Card objects, representing the newly drawn
            community cards.
        
        Output: None
        '''

        self.community_cards.extend(new_cards)
        
        for hand in self.hands:
            c1, c2 = Card(hand[:2]), Card(hand[2:])
            if (c1 in self.community_cards) or (c2 in self.community_cards):
                # Hands that contain a community card are impossible.
                del self.hands[hand]

            full_hand = PokerHand(self.community_cards + [c1, c2])
            self.hands[hand] = full_hand.best_hand()
    
