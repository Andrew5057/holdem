from holdem import *
from Card import *
import re

class PokerHand:
    def __init__(self, cards: list[Card]):
        # Cards as they get introduced, no order
        self.cards = cards
        self.cards.sort()
        # String representations of hand
        self.card_string = ""
        self.value_map = {'1': 10, '2': 2, '3': 3, '4':4, '5':5, '6':6, '7':7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    
    def create_string(self):
        self.cards.sort()
        self.cards_string = ''.join([card.str for card in self.cards])
    def two_pair(self):
        reversed_string = self.cards_string[::-1]

        two_pair = re.search(r'([1-9JQKA]).\1.*([1-9JQKA]).\2', reversed_string)
        if two_pair is not None:
            highest = self.value_map[two_pair.group(1)]
            second = self.value_map[two_pair.group(2)]



            return (highest, second)
        
        return None
    
hand = PokerHand([Card('KH'),Card('KD'),Card('QH'),Card('JS'),Card('JD')])
hand.create_string()
hand.two_pair()