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

        self.hearts = tuple([card.value for card in self.cards if card.suit == 'H'])
        self.diamonds = tuple([card.value for card in self.cards if card.suit == 'D'])
        self.clubs = tuple([card.value for card in self.cards if card.suit == 'C'])
        self.spades = tuple([card.value for card in self.cards if card.suit == 'S'])
    
    # The following functions evaluate for the possibility of hands
    # and will return a hexidecimal int under this pattern:
    # Position 1: strength of hand (0=none, 1=pair, ...)
    # Position 2-6: card values in order of importance
    # e.g. a pair of kings with A-J-4 kickers: 1DDEB4
    # e.g. three fives with 10-8 kickers: 555A8 
    # If hand not found, will return 0

    def straight_flush(self) -> int:
        count = 0
        high = None
        
        for i, value in enumerate(self.possible_ranks):
            if value in self.hearts:
                if high is None: high = value
                count += 1
                if count == 5: return int('8'+high+''.join(self.possible_ranks[i-3:i+1]), 16)
            else:
                count = 0
                high = None
        if (count == 4) and (14 in self.hearts): return int('854321', 16)

        count = 0
        high = None
        
        for i, value in enumerate(self.possible_ranks):
            if value in self.diamonds:
                if high is None: high = value
                count += 1
                if count == 5: return int('8'+high+''.join(self.possible_ranks[i-3:i+1]), 16)
            else:
                count = 0
                high = None
        if (count == 4) and (14 in self.diamonds): return int('854321', 16)

        count = 0
        high = None
        
        for i, value in enumerate(self.possible_ranks):
            if value in self.clubs:
                if high is None: high = value
                count += 1
                if count == 5: return int('8'+high+''.join(self.possible_ranks[i-3:i+1]), 16)
            else:
                count = 0
                high = None
        if (count == 4) and (14 in self.clubs): return int('854321', 16)

        count = 0
        high = None
        
        for i, value in enumerate(self.possible_ranks):
            if value in self.spades:
                if high is None: high = value
                count += 1
                if count == 5: return int('8'+high+''.join(self.possible_ranks[i-3:i+1]), 16)
            else:
                count = 0
                high = None
        return int('854321', 16) if (count == 4) and (14 in self.spades) else 0
    
    def four_of_a_kind(self) -> int:
        four_of_a_kind: re.Match = re.search(r'(.)\1\1\1', self.cards_string)
        card = four_of_a_kind.group(1)
        if len(self.cards_string) == 4:
            return int(f'7{card}{card}{card}{card}')
        for char in self.cards_string:
            if not char == card:
                return int(f'7{card}{card}{card}{card}{char}', 16)
        return 0

    def flush(self) -> int:
        if len(self.hearts) >= 5:
            return int('5'+''.join(self.hearts)[:5], 16)
        if len(self.diamonds) >= 5:
            return int('5'+''.join(self.diamonds)[:5], 16)
        if len(self.clubs) >= 5:
            return int('5'+''.join(self.clubs)[:5], 16)
        if len(self.spades) >= 5:
            return int('5'+''.join(self.spades)[:5], 16)
        return 0
    
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
        return int('454321', 16) if (count == 4) and ('E' in self.cards_string) else 0

    def three_of_kind(self) -> int:
        # Split the string with the three of kind as the delimiter
        split = re.split(r'([2-9ABCDE])\1\1', self.cards_string, maxsplit=1)
        if(len(split) < 3): return 0 # No match
        # Three of kind found - result should have 3 elements
        # split[0] = substring before the top three of kind
        # split[1] = rank of the three of kind (single character)
        # split[2] = substring following the three of kind
        threeofkind: str = split[1]*3
        kickers: str = (split[0]+split[2])[0:2]
        return int('1'+threeofkind+kickers, 16)

    def two_pair(self) -> int:
        two_pair: re.Match = re.search(r'(.)\1.*?(.)\2', 
                                       self.cards_string)
        if two_pair is not None:
            highest: str = two_pair.group(1)
            second: str = two_pair.group(2)

            for char in self.cards_string:
                if (not char == two_pair.group(1)) and (not char == two_pair.group(2)):
                    return int(f'2{highest}{highest}{second}{second}{char}', 16)
        
        return 0

    def pair(self) -> int:
        # Split the string with the top pair as the delimiter
        split = re.split(r'([2-9ABCDE])\1', self.cards_string, maxsplit=1)
        if(len(split) < 3): return 0 # No match
        # Pair found - result should have 3 elements
        # split[0] = substring before the top pair
        # split[1] = rank of the pair (single character)
        # split[2] = substring following the top pair
        pair: str = split[1]*2
        kickers: str = (split[0]+split[2])[0:3]
        return int('1'+pair+kickers, 16)

    def high_card(self) -> int:
        return int(self.cards_string[:5], 16)

hand = PokerHand([Card('KH'),Card('KD'),Card('3H'),Card('QS'),Card('3D'),Card('3D'),Card('KS')])
# hand = PokerHand([Card('JH'),Card('2S')])
print(hand.cards)
hand.create_string()
# print(hex(hand.pair()))
print(hex(hand.three_of_kind()))