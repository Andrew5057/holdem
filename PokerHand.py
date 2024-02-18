from Card import Card
import re

class PokerHand:
    possible_ranks = 'EDCBA98765432'

    def __init__(self, cards: list[Card]):
        """Represents a hand of Card objects in Texas Holdem.
        
        Should be constructed to include both individual cards and community 
        cards. Also defines methods to determine the strength of the hand.

        Class variables:
        possible_ranks (str): 'EDCBA98765432'. Represents the hexadecimal 
            values of the cards 2-A in descending order.

        Instance variables:
        cards (list[Card]): The cards, represented as Card objects, that make 
            up the hand. Should include community cards.
        cards_string (str): A string containing the hexadecimal values of the
            cards in the hand in descending order.
        hearts (tuple[str]): A list containing the hexadecimal values of the 
            heart cards in the hand in descending order.
        diamonds (tuple[str]): A list containing the hexadecimal values of the 
            diamond cards in the hand in descending order.
        clubs (tuple[str]): A list containing the hexadecimal values of the 
            club cards in the hand in descending order.
        spades (tuple[str]): A list containing the hexadecimal values of the 
            spade cards in the hand in descending order.
        
        Static methods:
        human_readable: Converts an int to _______________

        Instance methods:
        create_string: Initializes or modifies the cards_string, hearts, 
            diamonds, clubs, and spades variables.
        straight_flush: Determines whether a straight flush is present in the 
            hand and, if so, returns a hexadecimal int representing its 
            strength.
        four_of_a_kind: Determines whether a four of a kind is present in the 
            hand and, if so, returns a hexadecimal int representing its 
            strength.
        straight_flush: Determines whether a straight flush is present in the 
            hand and, if so, returns a hexadecimal int representing its 
            strength.
        full_house: Determines whether a full house is present in the hand 
            and, if so, returns a hexadecimal int representing its strength.
        flush: Determines whether a flush is present in the hand and, if so, 
            returns a hexadecimal int representing its strength.
        straight: Determines whether a straight is present in the hand and, 
            if so, returns a hexadecimal int representing its strength.
        three_of_kind: Determines whether a three of a kind is present in the 
            hand and, if so, returns a hexadecimal int representing its 
            strength.
        two_pair: Determines whether a two pair is present in the hand and, 
            if so, returns a hexadecimal int representing its strength.
        pair: Determines whether a pair is present in the hand and, if so, 
            returns a hexadecimal int representing its strength.
        high_card: Determines the strength of the hand, assuming that it 
            contains no special hands.
        best_hand: Determines the strength of the hand as a six-digit
            hexadecimal int. Defined such that higher return values represent 
            stronger hands.
        """
        # Cards as they get introduced, no order
        self.cards: list[Card] = cards
        self.cards.sort(reverse=True)
        self.create_string()
    
    def create_string(self) -> None:
        """Mutates the cards_string, hearts, diamonds, clubs, and spades 
            variables to list the hexadecimal values of each card in 
            descending order of strength.
        
        Example:
            hand = PokerHand([Card('5D'), Card('QH'), Card('6S'), Card('3D')])
            hand.create_string()
            hand.cards_string
                -> 'C653'
            hand.hearts
                -> ('C',)
            hand.diamonds
                -> ('5', '3')
            hand.clubs
                -> ()
            hand.spades
                -> ('6',)

        Arguments: None
        
        Output: None
        """
        self.cards.sort(reverse=True)
        self.cards_string = ''.join([card.value for card in self.cards])

        self.hearts = tuple([card.value for card in self.cards if card.suit == 'H'])
        self.diamonds = tuple([card.value for card in self.cards if card.suit == 'D'])
        self.clubs = tuple([card.value for card in self.cards if card.suit == 'C'])
        self.spades = tuple([card.value for card in self.cards if card.suit == 'S'])
    
    # The following functions evaluate for the possibility of hands
    # and will return a hexadecimal int under this pattern:
    # Position 1: strength of hand (0=none, 1=pair, ...)
    # Position 2-6: card values in order of importance
    # e.g. a pair of kings with A-J-4 kickers: 0x1DDEB4
    # e.g. three fives with 10-8 kickers: 0x555A8 
    # If hand not found, will return 0

    def straight_flush(self) -> int:
        """Determines whether the hand contains a straight flush and, if it 
            does, how strong the straight flush is. Higher-integered values 
            represent stronger hands.

        Arguments: None

        Returns: An int in which each hexadecimal digit represents an aspect 
            of the hand. The first digit is "8". The next five digits are the 
            numeric values of the cards that make up the straight flush, in 
            descending order. If a straight flush is not found, returns 0.
        """

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
        if (count == 4) and ('E' in self.hearts): return int('854321', 16)

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
        if (count == 4) and ('E' in self.diamonds): return int('854321', 16)

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
        if (count == 4) and ('E' in self.clubs): return int('854321', 16)

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
        return int('854321', 16) if (count == 4) and ('E' in self.spades) else 0
    
    def four_of_a_kind(self) -> int:
        """Determines whether the hand contains a four-of-a-kind and, if it 
            does, how strong the four-of-a-kind is. Higher-integered values 
            represent stronger hands.

        Arguments: None

        Returns: An int in which each hexadecimal digit represents an aspect 
            of the hand. The first digit is "7". The next four digits are the 
            numeric values of the cards that make up the four-of-a-kind. The 
            last digit is the numeric value of the kicker. If a 
            four-of-a-kind is not found, returns 0.
        """
        
        four_of_a_kind: re.Match = re.search(r'(.)\1\1\1', self.cards_string)
        if four_of_a_kind is None:
            return 0
        card = four_of_a_kind.group(1)
        if len(self.cards_string) == 4:
            return int(f'7{card}{card}{card}{card}', 16)
        for char in self.cards_string:
            if not char == card:
                return int(f'7{card}{card}{card}{card}{char}', 16)
        return 0

    def full_house(self) -> int:
        """Determines whether the hand contains a full house and, if it does, 
            how strong the full house is. Higher-integered values represent 
            stronger hands.

        Arguments: None

        Returns: An int in which each hexadecimal digit represents an aspect 
            of the hand. The first digit is "6". The next five digits are the 
            numeric values of the cards that make up the full house, in 
            descending order. If a full house is not found, returns 0.
        """

        full_house_2_3: re.Match = re.search(r'(.)\1.*?(.)\2\2', self.cards_string)
        full_house_3_2: re.Match = re.search(r'(.)\1\1.*?(.)\2', self.cards_string)
        if (full_house_2_3 is None) and (full_house_3_2 is None):
            return 0
        if (full_house_2_3 is not None) and (full_house_3_2 is None):
            high = full_house_2_3.group(2)
            low = full_house_2_3.group(1)
        elif (full_house_3_2 is not None) and (full_house_2_3 is None):
            high = full_house_3_2.group(1)
            low = full_house_3_2.group(2)
        elif int(full_house_2_3.group(2), 16) >= int(full_house_3_2.group(1), 16):
            # If the two three-of-a-kinds are equal, we know the first full
            # house is higher because its pair comes before the value while
            # the other's pair comes after the value, and cards earlier in the
            # string are greater.
            high = full_house_2_3.group(2)
            low = full_house_2_3.group(1)
        elif int(full_house_3_2.group(1), 16) > int(full_house_2_3.group(2), 16):
            high = full_house_3_2.group(1)
            low = full_house_3_2.group(2)
        return int(f'6{high}{high}{high}{low}{low}', 16)


    def flush(self) -> int:
        """Determines whether the hand contains a flush and, if it does, how 
            strong the flush is. Higher-integered values represent stronger hands.

        Arguments: None

        Returns: An int in which each hexadecimal digit represents an aspect 
            of the hand. The first digit is "5". The next five digits are the 
            numeric values of the cards that make up the flush, in descending 
            order. If a flush is not found, returns 0.
        """

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
        """Determines whether the hand contains a straight and, if it does, 
            how strong the four of a kind is. Higher-integered values 
            represent stronger hands.

        Arguments: None

        Returns: An int in which each hexadecimal digit represents an aspect 
            of the hand. The first digit is "4". The next five digits are the 
            numeric values of the cards that make up the straight, in 
            descending order. If a straight is not found, returns 0.
        """

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
        """Determines whether the hand contains a three-of-a-kind and, if it 
            does, how strong the three-of-a-kind is. Higher-integered values 
            represent stronger hands.

        Arguments: None

        Returns: An int in which each hexadecimal digit represents an aspect 
            of the hand. The first digit is "3". The next three digits are the 
            numeric values of the cards that make up the three-of-a-kind. The 
            last two digit are the numeric values of the kickers, in 
            descending order. If a three-of-a-kind is not found, returns 0.
        """

        # Split the string with the three of kind as the delimiter
        split = re.split(r'([2-9ABCDE])\1\1', self.cards_string, maxsplit=1)
        if(len(split) < 3): return 0 # No match
        # Three of kind found - result should have 3 elements
        # split[0] = substring before the top three of kind
        # split[1] = rank of the three of kind (single character)
        # split[2] = substring following the three of kind
        threeofkind: str = split[1]*3
        kickers: str = (split[0]+split[2])[0:2]
        return int('3'+threeofkind+kickers, 16)

    def two_pair(self) -> int:
        """Determines whether the hand contains a two-pair and, if it does, 
            how strong the two-pair is. Higher-integered values represent stronger hands.

        Arguments: None

        Returns: An int in which each hexadecimal digit represents an aspect 
            of the hand. The first digit is "2". The next four digits are the 
            numeric values of the cards that make up the two-pair, in 
            descending order. The last digit is the numeric value of 
            the kicker. If a two-pair is not found, returns 0.
        """

        two_pair: re.Match = re.search(r'(.)\1.*?(.)\2', 
                                       self.cards_string)
        if two_pair is not None:
            highest: str = two_pair.group(1)
            second: str = two_pair.group(2)

            for char in self.cards_string:
                if (not char == two_pair.group(1)) and (not char == two_pair.group(2)):
                    return int(f'2{highest}{highest}{second}{second}{char}', 16)
            return int(f'2{highest}{highest}{second}{second}', 16) 
        return 0

    def pair(self) -> int:
        """Determines whether the hand contains a pair and, if it does, how 
            strong the strongest pair is. Higher-integered values represent 
            stronger hands.

        Arguments: None

        Returns: An int in which each hexadecimal digit represents an aspect 
            of the hand. The first digit is "1". The next two digits are the 
            numeric values of the cards that make up the strongest pair, in 
            descending order. The last three digit are the numeric values of 
            the kickers, in descending order. If a pair is not found, returns 
            0.
        """

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
        """Determines the strength of the hand, assuming that it could only 
            be interpreted as a high card.

        Arguments: None

        Returns: An int in which each hexadecimal digit represents an aspect 
            of the hand. The (omitted) first digit is "0". The next five 
            digits are the cards that make up the hand, in descending order.
        """
        return int(self.cards_string[:5], 16)
      
    def best_hand(self) -> dict:
        """Determines the strength of the hand, accounting for both hand type 
            and kickers. This method is constructed such that one hand's 
            best_hand value is greater than another's if and only if it beats 
            that hand, is less than another's if and only if it loses to that 
            hand, and is equal to another's if and only if it draws that hand.
            (That is, higher values represent stronger hands.)
        
        Arguments: None

        Returns: A two-item dictionary:
            "level" (int): A value from 0-8 (inclusive) representing the 
                strength of the hand's type. 0 represents a high card, while 
                8 represents a straight flush.
            "value" (int): An integer with 6 hexadecimal digits, each 
                representing a different aspect of the hand. The first digit 
                represents the level of the hand. The remaining five digits 
                are the numeric values of the cards that make up the hand, in 
                order of their importance in tiebreakers. For example, the 
                second and third digits for a pair will be the values of the paired 
                cards, while the last three digits will be the kickers in 
                decreasing order of strength.
        """

        # Find the strongest hand by testing top-down
        test = self.straight_flush()
        if test != 0: return {"level": 8, "value": test}
        test = self.four_of_a_kind()
        if test != 0: return {"level": 7, "value": test}
        test = self.full_house()
        if test != 0: return {"level": 6, "value": test}
        test = self.flush()
        if test != 0: return {"level": 5, "value": test}
        test = self.straight()
        if test != 0: return {"level": 4, "value": test}
        test = self.three_of_kind()
        if test != 0: return {"level": 3, "value": test}
        test = self.two_pair()
        if test != 0: return {"level": 2, "value": test}
        test = self.pair()
        if test != 0: return {"level": 1, "value": test}
        return {"level": 0, "value": self.high_card()}

    @staticmethod
    def human_readable_level(level: int):
        return ["High Hand",
                "Pair",
                "Two Pair",
                "Three Of Kind",
                "Straight",
                "Full House",
                "Four Of Kind",
                "Straight Flush"][level]

    @staticmethod
    def human_readable_cards(intval: int):
        # Determine number of cards. Only options are 2 or 5
        ncards = 2 if intval < 0x11111 else 5
        cards = ""
        # Look at digits "right-to'left" and convert to cards
        for i in range(ncards):
            cards = '-A23456789TJQKA'[intval % 16] + cards
            intval = int(intval/16)
        # Remaining digit should be the class of hand
        return cards

    def append(self, card: Card) -> None:
        self.cards.append(card)
        self.cards.sort(reverse=True)
        self.create_string()
