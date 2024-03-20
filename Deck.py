from random import shuffle
from Card import Card

class Deck:
    def __init__(self):
        self.cards: list[Card] = [Card(str(rank), suit) for rank in range(1, 14) for suit in ('C', 'S', 'D', 'H')]

    def shuffle(self) -> None:
        shuffle(self.cards)

    def draw(self, count: int = 1) -> tuple[Card]:
        if not isinstance(count, int):
            return TypeError(f"Default argument count must be of type int.")
        if count > len(self):
            raise ValueError(f"Cannot draw {count} cards from a Deck of length {len(self)}.")
        return tuple([self.cards.pop() for i in range(count)])
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __iter__(self):
        yield from self.cards
    
    def remove(self, card: Card) -> None:
        if not (card in self.cards):
            raise ValueError(f"Card {card} not in deck.")
        self.cards.remove(card)