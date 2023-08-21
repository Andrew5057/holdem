from Card import Card
from PokerHand import PokerHand

class Player:
    def __init__(self, *args):
        if len(args) == 1:
            self.hand: tuple[Card] = args[0]
        else:
            self.hand: tuple[Card] = tuple([card for card in args])
    
    def __repr__(self) -> str:
        return f'Player({self.hand[0]}, {self.hand[1]})'

if __name__ == '__main__':
    while True:
        try:
            cards = []
            x = input('Enter a card name: ')
            while x != '':
                cards.append(Card(x))
                x = input('Enter a card name: ')
            hand = PokerHand(cards)
            print()
            function_name = input('Enter a function name: ')
            print()
            print(str(hex(eval(f'hand.{function_name}()')))[2:])
            print('\n-----\n')
        except Exception:
            print('\nYour input raised an error. Please try again.\n-----\n')