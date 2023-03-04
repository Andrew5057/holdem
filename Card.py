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
            # Consider a check here for a two character rank
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
            self.value: int = int(self.rank)

            if self.value < 1 or self.value > 14:
                raise ValueError('Numeric ranks must be between 1 and 14 inclusive.')

            match self.value:
                case 1:
                    self.rank: str = 'A'
                    self.value: int = 14
                case 11:
                    self.rank: str = 'J'
                case 12:
                    self.rank: str = 'Q'
                case 13:
                    self.rank: str = 'K'
                case 14:
                    self.rank: str = 'A'
                
        else:
            # Handles face cards' ranks and values.
            self.rank: str = rank[0].upper()
            match self.rank:
                case 'J':
                    self.value: int = 11
                case 'Q':
                    self.value: int = 12
                case 'K':
                    self.value: int = 13
                case 'A':
                    self.value: int = 14
                case _:
                    raise ValueError("Non-numeric ranks must begin with 'J', 'Q', 'K', or 'A'.")
        
        self.str: str = f'{self.rank}{self.suit}'
        self.repr: str = f"Card('{self.rank}{self.suit}')"
    
    def __repr__(self) -> str:
        return self.repr
    
    def __str__(self) -> str:
        return self.str
    
    # ADD: __eq__, __gt__, __lt__, 
    def  __eq__(self, card) -> bool:
        if not isinstance(card, Card):
            return False
        
        same_value: bool = self.value == card.value
        same_suit: bool = self.suit == card.suit
        return same_value and same_suit
    def __lt__(self, card) -> bool:
        return self.value < card.value