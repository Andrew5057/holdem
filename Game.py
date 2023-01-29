from Card import *
from Deck import *
from holdem import *

class Game:
    def __init__(self, player_count: int):
        self.deck: Deck = Deck()
        self.deck.shuffle()
        self.player_count: int = player_count
        self.players: list[Player] = [Player(self.deck.draw(2)) for player in range(player_count)]
        # 0 = post-deal, 1 = post-flop, 2 = post-turn, 3 = post-river
        self.state: int = 0
        self.community_cards: list[Card] = []
    
    def next(self):
        self.state += 1
        match self.state:
            case 1:
                self.community_cards.extend(self.deck.draw(3))
            case 2:
                self.community_cards.extend(self.deck.draw(1))
            case 3:
                self.community_cards.extend(self.deck.draw(1))
            case 4:
                self.__init__(self.player_count)
