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
        
        if rank.isnumeric():
            # Handles numeric cards' ranks and values, with 1's being handled
            # later.
            self.rank: str = rank
            self.value: int = int(self.rank)
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
        
        # Allows the user to input either '1' for 'Ace'.
        if self.rank == '1':
            self.rank: str = 'A'
            self.value: int = 14

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
