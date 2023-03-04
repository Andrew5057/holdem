from Card import *

class Player:
    def __init__(self, *args):
        if len(args) == 1:
            self.hand: tuple[Card] = args[0]
        else:
            self.hand: tuple[Card] = tuple([card for card in args])
    
    def __repr__(self) -> str:
        return f'Player({self.hand[0]}, {self.hand[1]})'

