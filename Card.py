class Card:
    def __init__(self, rank: str = None, suit: str = None):
        '''A class that represents a standard playing card.
        
        Argument pattern 1:
        rank: A string containing the rank (first letter for
            faces) and first letter of the suit, in that order.
        
        Argument pattern 2:
        rank: A string or int containing the rank
        suit: A string containing the suit
        
        Instance variables:
        rank: A string containing the rank
        suit: A string containing the first letter of the suit (capitalized)
        value: A string containing the hexadecimal value of the card, with Jack,
            Queen, King, and Ace as 11, 12, 13, and 14 respectively.
        '''

        if (suit is None) and (rank is None):
            self.suit = ""
            self.rank = ""
            return
        
        # Handles pattern 1.
        if suit is None:
            suit: str = rank[-1]
            rank: str = rank[:-1]
        
        if not isinstance(suit, str):
            raise TypeError(f"Optional argument suit must be of type str, not {type(suit)}")

        # Allows most representations of the suit to be handled with the same
        # code.
        self.suit: str = suit[0].upper()
        if not self.suit in ('H', 'D', 'S', 'C'):
            raise ValueError(f"Suit {self.suit} does not match 'H', 'D', 'S', or 'C'")
        
        if isinstance(rank, int):
            if (rank < 1 or rank > 14):
                raise ValueError(f"Positinoal argument rank must be between 1 and 14 inclusive, not {rank}")
            rank: str = str(rank)

        if not isinstance(rank, str):
            raise TypeError(f"Optional argument rank must be of type str, not {type(rank)}")

        if rank.isnumeric():
            # Handles numeric cards' ranks and values
            self.rank: str = rank
            self.value: str = rank

            if (int(rank) < 1 or int(rank) > 14):
                raise ValueError(f"Optional argument rank must be between 1 and 14 inclusive, not {self.rank}")

            match self.value:
                case '1':
                    self.rank: str = 'A'
                    self.value: str = 'E'
                case '10':
                    self.rank: str = 'T'
                    self.value: str = 'A'
                case '11':
                    self.rank: str = 'J'
                    self.value: str = 'B'
                case '12':
                    self.rank: str = 'Q'
                    self.value: str = 'C'
                case '13':
                    self.rank: str = 'K'
                    self.value: str = 'D'
                case '14':
                    self.rank: str = 'A'
                    self.value: str = 'E'
                
        else:
            # Handles face cards' ranks and values.
            self.rank: str = rank[0].upper()
            match self.rank:
                case 'T':
                    self.value: str = 'A'
                case 'J':
                    self.value: str = 'B'
                case 'Q':
                    self.value: str = 'C'
                case 'K':
                    self.value: str = 'D'
                case 'A':
                    self.value: str = 'E'
                case _:
                    raise ValueError(f"Positional argument rank must match 'T', 'J', 'Q', 'K', or 'A', not {self.rank}")
        
        self.str: str = f'{self.rank[0]}{self.suit}'
        self.repr: str = f"Card('{self.rank}{self.suit}')"
        self.hash: int = hash(self.repr)
    
    def __repr__(self) -> str:
        return self.repr
    
    def __str__(self) -> str:
        return self.str
    
    def __hash__(self) -> int:
        return self.hash
    
    # ADD: __eq__, __gt__, __lt__, 
    def  __eq__(self, card) -> bool:
        if not isinstance(card, Card):
            return False
        same_value: bool = self.value == card.value
        same_suit: bool = self.suit == card.suit
        return same_value and same_suit
    def __lt__(self, card) -> bool:
        if not isinstance(card, Card):
            return TypeError(f"Cannot compare Card to type {type(card)}")
        return int(self.value, 16) < int(card.value, 16)
    def __gt__(self, card) -> bool:
        return not (self.__eq__(card) or self.__lt(card))
    
    @staticmethod
    def ascii_art(card):
        if not isinstance(card, Card):
            raise TypeError(f"Positional argument card must be of type Card, not {type(card)}")
        if card.rank == "T":
            upper_left = lower_right = "10"
        else:
            upper_left = card.rank + " "
            lower_right = " " + card.rank
        match card.suit:
            case 'C':
                return [r" ______________ ",
                        r"| {}           |".format(upper_left),
                        r"|      __      |",
                        r"|     /  \     |",
                        r"|    _\  /_    |",
                        r"|   /      \   |",
                        r"|   \__/\__/   |",
                        r"|      ||      |",
                        r"|           {} |".format(lower_right),
                        r"|______________|"]
            case 'S':
                return [r" ______________ ",
                        r"| {}           |".format(upper_left),
                        r"|              |",
                        r"|      /\      |",
                        r"|     /  \     |",
                        r"|    /    \    |",
                        r"|    \____/    |",
                        r"|      ||      |",
                        r"|           {} |".format(lower_right),
                        r"|______________|"]
            case 'D':
                return [r" ______________ ",
                        r"| {}           |".format(upper_left),
                        r"|      /\      |",
                        r"|     /  \     |",
                        r"|    /    \    |",
                        r"|    \    /    |",
                        r"|     \  /     |",
                        r"|      \/      |",
                        r"|           {} |".format(lower_right),
                        r"|______________|"]
            case 'H':
                return [r" ______________ ",
                        r"| {}           |".format(upper_left),
                        r"|    __  __    |",
                        r"|   /  \/  \   |",
                        r"|   \      /   |",
                        r"|    \    /    |",
                        r"|     \  /     |",
                        r"|      \/      |",
                        r"|           {} |".format(lower_right),
                        r"|______________|"]
            case _:
                return ["       "]*10

    @staticmethod
    def print_cards(cards: list):
        if not isinstance(cards, list):
            raise TypeError(f"Positional argument cards must be of type list, not {type(cards)}")
        # Convert cards to ascii art
        ascii_cards = [Card.ascii_art(i) for i in cards]
        # Line up cards horizontally
        ascii_cards = [" ".join(row) for row in zip(*ascii_cards)]
        # Add line breaks and print
        print("\n".join(ascii_cards))
        # Print one more line break to finish
        print("")

