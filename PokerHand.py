from holdem import *
from Card import *
import re

class PokerHand:
    def __init__(self, cards: list[Card]):
        # Cards as they get introduced, no order
        self.cards: list[Card] = cards
        self.cards.sort(reverse=True)
        self.create_string()
    
    def create_string(self) -> None:
        self.cards.sort(reverse=True)
        self.cards_string = ''.join([card.value for card in self.cards])
    
    def straight_flush(self) -> int:
        count = 0
        high = None

        for value in range(14, 1, -1):
            if value in self.hearts:
                if high is None: high = value
                count += 1
                if count == 5: return high
            else:
                count = 0
                high = None
        if (count == 4) and (14 in self.hearts): return 5

        count = 0
        high = None
        
        for value in range(14, 1, -1):
            if value in self.diamonds:
                if high is None: high = value
                count += 1
                if count == 5: return high
            else:
                count = 0
                high = None
        if (count == 4) and (14 in self.diamonds): return 5

        count = 0
        high = None
        
        for value in range(14, 1, -1):
            if value in self.clubs:
                if high is None: high = value
                count += 1
                if count == 5: return high
            else:
                count = 0
                high = None
        if (count == 4) and (14 in self.clubs): return 5

        count = 0
        high = None
        
        for value in range(14, 1, -1):
            if value in self.spades:
                if high is None: high = value
                count += 1
                if count == 5: return high
            else:
                count = 0
                high = None
        return 5 if (count == 4) and (14 in self.spades) else None
    
    def four_of_a_kind(self) -> int:
        four_of_a_kind: re.Match = re.search(r'([2-9TJQKA]).\1.\1.\1', self.cards_string)
        return self.value_map[four_of_a_kind.group(1)] if four_of_a_kind is not None else None

    def flush(self) -> tuple[int]:
        flush: re.Match = re.search(r'([2-9TJQKA])([HDSC]).*?([2-9TJQKA])\2.*?([2-9TJQKA])\2.*?([2-9TJQKA])\2.*?([2-9TJQKA])\2',
                                    self.cards_string)
        return tuple([self.value_map[rank] for rank in flush.groups() if rank not in 'HDSC']) if flush is not None else None
    
    
    def straight(self) -> int:
        count = 0
        high = None

        for rank in self.value_map:
            if rank in self.cards_string:
                if high is None: high = rank
                count += 1
                if count == 5: return self.value_map[high]
            else:
                count = 0
                high = None
            
        # The for loop misses bottom ace, so this checks for it.
        return 5 if (count == 4) and ('A' in self.cards_string) else None

    def two_pair(self) -> int:
        two_pair: re.Match = re.search(r'([2-9TJQKA])\1.*([2-9TJQKA])\2', 
                                       self.cards_string)
        if two_pair is not None:
            highest: str = two_pair.group(1)
            second: str = two_pair.group(2)

            for char in self.cards_string:
                if (not char == two_pair.group(1)) and (not char == two_pair.group(2)):
                    return int('2'+highest+second+char)
        
        return None
