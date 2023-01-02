class Card:
    def __init__(self, suit: str, rank: str = None):
        if rank is None:
            suit_initial: str = suit[-1]
            rank: str = suit[:-1]
            match suit_initial:
                case 'H':
                    self.suit: str = 'Heart'
                case 'S':
                    self.suit: str = 'Suit'
                case 'D':
                    self.suit: str = 'Diamond'
                case 'C':
                    self.suit: str = 'Club'
            self.rank = rank
            if self.rank.isnumeric():
                self.value = int(self.rank)
            else:
                match self.rank:
                    case 'Jack':
                        self.value: int = 11
                    case 'Queen':
                        self.value: int = 12
                    case 'King':
                        self.value: int = 13
                    case 'Ace':
                        self.value: int = 14

        else:
            self.suit: str = suit
            self.rank: str = str(rank)
            if self.rank.isnumeric():
                self.value: int = int(rank)
            else:
                match self.rank:
                    case 'Jack':
                        self.value: int = 11
                    case 'Queen':
                        self.value: int = 12
                    case 'King':
                        self.value: int = 13
                    case 'Ace':
                        self.value: int = 14
x = Card('4H')
y = Card('4', 'King')