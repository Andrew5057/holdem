from random import shuffle

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
            rank = str(rank)

        if rank.isnumeric():
            # Handles numeric cards' ranks and values
            self.rank: str = rank
            self.value: int = int(self.rank)

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
    
    def __repr__(self) -> str:
        return f"Card('{self.rank}{self.suit}')"
    
    # ADD: __eq__, __gt__, __lt__, 
    def  __eq__(self, card) -> bool:
        same_value = self.value == card.value
        same_suit = self.suit == card.suit
        return same_value and same_suit

class Deck:
    def __init__(self):
        self.cards = [Card(str(rank), suit) for rank in range(1, 14) for suit in ('C', 'S', 'D', 'H')]

    def shuffle(self):
        shuffle(self.cards)
    
    def draw(self, count=1):
        return tuple([self.cards.pop() for i in range(count)])
    
    def __len__(self):
        return len(self.cards)
    
    def __iter__(self):
        yield from self.cards

# Runs if and only if this is run as a script
if __name__ == '__main__':
    # Tests various cards.
    x = Card('4H')
    print(f'{x.suit}, {x.rank}, {x.value}')
    x = Card('KH')
    print(f'{x.suit}, {x.rank}, {x.value}')
    x = Card('10H')
    print(f'{x.suit}, {x.rank}, {x.value}')
    x = Card('1H')
    print(f'{x.suit}, {x.rank}, {x.value}')


    x = Card('4', 'Heart')
    print(f'{x.suit}, {x.rank}, {x.value}')
    x = Card('King', 'Heart')
    print(f'{x.suit}, {x.rank}, {x.value}')
    x = Card('10', 'Heart')
    print(f'{x.suit}, {x.rank}, {x.value}')
    x = Card('1', 'Heart')
    print(f'{x.suit}, {x.rank}, {x.value}')

