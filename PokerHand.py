from holdem import *
from Card import *
import re

class PokerHand:
    def __init__(self, cards: list[Card]):
        # Cards as they get introduced, no order
        self.cards: list[Card] = cards
        self.cards.sort(reverse=True)

        # String representations of hand
        self.card_string: str = ""
        self.value_map: dict[str: int] = {'1': 10, '2': 2, '3': 3, '4':4, 
                                         '5':5, '6':6, '7':7, '8': 8, '9': 9, 
                                         '10': 10, 'J': 11, 'Q': 12, 'K': 13, 
                                         'A': 14}
    
    def create_string(self) -> None:
        self.cards.sort(reverse=True)
        self.cards_string = ''.join([card.str for card in self.cards])
    
    def straight_flush(self) -> int:
        flush = self.flush()
        # enumerate(iterable) returns both the index and value for each item.
        for i, value in enumerate(flush[:-1]):
            if not value == flush[i+1] + 1:
                return None
        return flush[0]
    
    def flush(self) -> tuple[int]:
        flush: re.Match = re.search(r'([1-9JQKA])([HDSC]).*([1-9JQKA])\2.*([1-9JQKA])\2.*([1-9JQKA])\2.*([1-9JQKA])\2', self.cards_string)
        if flush is None: return None
        return tuple(self.value_map[value] for value in flush.groups() if not value in ('H', 'D', 'S', 'C'))

    def two_pair(self) -> tuple[int]:
        two_pair: re.Match = re.search(r'([1-9JQKA]).\1.*([1-9JQKA]).\2', 
                                       self.cards_string)
        if two_pair is not None:
            highest: int = self.value_map[two_pair.group(1)]
            second: int = self.value_map[two_pair.group(2)]

            for char in self.cards_string:
                if char in self.value_map and (not char == two_pair.group(1) and 
                                               not char == two_pair.group(2)):
                    kicker: int = self.value_map[char]

            return (highest, second, kicker)
        
        return None