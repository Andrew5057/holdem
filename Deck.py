from random import shuffle
from Card import *

class Deck:
    def __init__(self):
        self.cards: list[Card] = [Card(str(rank), suit) for rank in range(1, 14) for suit in ('C', 'S', 'D', 'H')]

    def shuffle(self):
        shuffle(self.cards)

    def draw(self, count=1) -> tuple[Card]:
        return tuple([self.cards.pop() for i in range(count)])
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __iter__(self):
        yield from self.cards