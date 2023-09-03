class Card:
    def __init__(self, rank: str, suit: str = None):
        '''A class that represents a standard playing card.
        
        Argument pattern 1:
        rank: A 2-character string containing the rank (first letter for
            faces) and first letter of the suit, in that order.
        
        Argument pattern 2:
        rank: A string containing the rank
        suit: A string containing the suit
        
        Instance variables:
        rank: A string containing the rank
        suit: A string containing the first letter of the suit (capitalized)
        value: An integer containing the value of the card, with Jack,
            Queen, King, and Ace as 11, 12, 13, and 14 respectively.
        '''

        # Handles pattern 1.
        if suit is None:
            suit: str = rank[-1]
            rank: str = rank[:-1]
        
        # Allows most representations of the suit to be handled with the same
        # code.
        self.suit: str = suit[0].upper()
        if not self.suit in ('H', 'D', 'S', 'C'):
            raise ValueError("Suit must begin with 'H', 'D', 'S', or 'C'")
        
        if isinstance(rank, int):
            rank: str = str(rank)

        if rank.isnumeric():
            # Handles numeric cards' ranks and values
            self.rank: str = rank
            self.value: str = rank

            match self.value:
                case '1':
                    self.rank: str = 'A'
                    self.value: int = 'E'
                case '10':
                    self.rank: str = 'T'
                    self.value = 'A'
                case '11':
                    self.rank: str = 'J'
                    self.value = 'B'
                case '12':
                    self.rank: str = 'Q'
                    self.value = 'C'
                case '13':
                    self.rank: str = 'K'
                    self.value = 'D'
                case '14':
                    self.rank: str = 'A'
                    self.value = 'E'
                
        else:
            # Handles face cards' ranks and values.
            self.rank: str = rank[0].upper()
            match self.rank:
                case 'T':
                    self.value: int = 'A'
                case 'J':
                    self.value: int = 'B'
                case 'Q':
                    self.value: int = 'C'
                case 'K':
                    self.value: int = 'D'
                case 'A':
                    self.value: int = 'E'
                case _:
                    raise ValueError("Non-numeric ranks must begin with 'T', 'J', 'Q', 'K', or 'A'.")
        
        self.str: str = f'{self.rank[0]}{self.suit}'
        self.repr: str = f"Card('{self.rank}{self.suit}')"
<<<<<<< Updated upstream
        self.hash: int = hash(self.repr)
    
=======

>>>>>>> Stashed changes
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
        return int(self.value, 16) < int(card.value, 16)
    
    @staticmethod
    def ascii_art(card):
        if card.rank == "T":
            upper_left = lower_right = "10"
        else:
            upper_left = card.rank + " "
            lower_right = " " + card.rank
        match card.suit:
            case 'C':
                return [" ______________ ",
                        "| {}           |".format(upper_left),
                        "|      __      |",
                        "|     /  \     |",
                        "|    _\  /_    |",
                        "|   /      \   |",
                        "|   \__/\__/   |",
                        "|      ||      |",
                        "|           {} |".format(lower_right),
                        "|______________|"]
            case 'S':
                return [" ______________ ",
                        "| {}           |".format(upper_left),
                        "|              |",
                        "|      /\      |",
                        "|     /  \     |",
                        "|    /    \    |",
                        "|    \____/    |",
                        "|      ||      |",
                        "|           {} |".format(lower_right),
                        "|______________|"]
            case 'D':
                return [" ______________ ",
                        "| {}           |".format(upper_left),
                        "|      /\      |",
                        "|     /  \     |",
                        "|    /    \    |",
                        "|    \    /    |",
                        "|     \  /     |",
                        "|      \/      |",
                        "|           {} |".format(lower_right),
                        "|______________|"]
            case 'H':
                return [" ______________ ",
                        "| {}           |".format(upper_left),
                        "|    __  __    |",
                        "|   /  \/  \   |",
                        "|   \      /   |",
                        "|    \    /    |",
                        "|     \  /     |",
                        "|      \/      |",
                        "|           {} |".format(lower_right),
                        "|______________|"]
            case _:
                return [""]*10

    @staticmethod
    def print_cards(cards: list):
        # Convert cards to ascii art
        ascii_cards = [Card.ascii_art(i) for i in cards]
        # Line up cards horizontally
        ascii_cards = [" ".join(row) for row in zip(*ascii_cards)]
        # Add line breaks and print
        print("\n".join(ascii_cards))
        # Print one more line break to finish
        print("")

