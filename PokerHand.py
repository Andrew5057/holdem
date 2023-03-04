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
    def create_string(self):
        self.cards.sort()
        self.cards_string = ''.join([card.str for card in self.cards])
