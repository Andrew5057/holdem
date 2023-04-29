from holdem import *
from Card import *
import re

class PokerHand:
    possible_ranks = 'EDCBA98765432'

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
        four_of_a_kind: re.Match = re.search(r'(.)\1\1\1', self.cards_string)
        card = four_of_a_kind.group(1)
        if len(self.cards_string) == 4:
            return f'6{card}{card}{card}{card}'
        for char in self.cards_string:
            if not char == card:
                return f'6{card}{card}{card}{card}{char}'
        return None

    def flush(self) -> tuple[int]:
        #rewrite
        pass
    
    
    def straight(self) -> int:
        count = 0
        high = None

        for i, rank in enumerate(self.possible_ranks):
            if rank in self.cards_string:
                if high is None: high = rank
                count += 1
                if count == 5: return int('4'+high+''.join(self.possible_ranks[i-3:i+1]), 16)
            else:
                count = 0
                high = None
            
        # The for loop misses bottom ace, so this checks for it.
        return int('454321', 16) if (count == 4) and ('E' in self.cards_string) else None

    def two_pair(self) -> int:
        two_pair: re.Match = re.search(r'(.)\1.*?(.)\2', 
                                       self.cards_string)
        if two_pair is not None:
            highest: str = two_pair.group(1)
            second: str = two_pair.group(2)

            for char in self.cards_string:
                if (not char == two_pair.group(1)) and (not char == two_pair.group(2)):
                    return int(f'2{highest}{highest}{second}{second}{char}', 16)
        
        return None
