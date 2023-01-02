class Card:
    def __init__(self, suit: str, rank: str):
        if suit in ('heart', 'diamond', 'spade', 'club'):
            self.suit: str = suit
        self.rank: str = str(rank)
        if self.rank.isnumeric():
            self.value: int = int(rank)
        else:
            match self.rank:
                case 'jack':
                    self.value: int = 11
                case 'queen':
                    self.value: int = 12
                case 'king':
                    self.value: int = 13
                case 'ace':
                    self.value: int = 14
x = Card('heart', 'ace')

print(x.suit)
print(x.rank)
print(x.value)