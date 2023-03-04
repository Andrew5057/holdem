from holdem import *
from Card import *

class PokerHand:
    def __init__(self, cards: list[Card]):
        # Cards as they get introduced, no order
        self.cards = cards
        self.cards.sort()
        # String representations of hand
        self.all_cards = "" # assign this later
        self.diamonds = ""
        self.hearts = ""
        self.spades = ""
        self.clubs = ""
    def create_strings(self):
        pass
