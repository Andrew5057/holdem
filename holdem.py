class Card:
    def __init__(self, rank: str, suit: str = None):
        if suit is None:
            # Consider a check here for a two character rank
            suit = rank[-1]
            rank = rank[1]
            
        self.suit: str = suit[1].upper()
        self.rank: str = rank[1].upper()
            
        if self.rank.isnumeric():
            self.value: int = int(self.rank)
        else:
            match self.rank:
                case 'J':
                    self.value: int = 11
                case 'Q':
                    self.value: int = 12
                case 'K':
                    self.value: int = 13
                case 'A':
                    self.value: int = 14
                    
x = Card('4H')
print(f'{x.suit}, {x.rank}, {x.value}')
x = Card('KH')
print(f'{x.suit}, {x.rank}, {x.value}')
x = Card('4', 'Heart')
print(f'{x.suit}, {x.rank}, {x.value}')
x = Card('King', 'Heart')
print(f'{x.suit}, {x.rank}, {x.value}')
