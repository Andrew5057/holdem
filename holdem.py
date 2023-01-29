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
    
    def __repr__(self) -> str:
        return f"Card('{self.rank}{self.suit}')"
    
    def __str__(self) -> str:
        return f'{self.rank}{self.suit}'
    
    # ADD: __eq__, __gt__, __lt__, 
    def  __eq__(self, card) -> bool:
        if not isinstance(card, Card):
            return False
        
        same_value: bool = self.value == card.value
        same_suit: bool = self.suit == card.suit
        return same_value and same_suit
    def __lt__(self, card) -> bool:
        return self.value < card.value

class Deck:
    def __init__(self):
        self.cards: list[Card] = [Card(str(rank), suit) for rank in range(1, 14) for suit in ('C', 'S', 'D', 'H')]

    def shuffle(self):
        shuffle(self.cards)

    def draw(self, count=1) -> tuple[Card]:
        return tuple([self.cards.pop() for i in range(count)])
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __iter__(self):
        yield from self.cards

class Player:
    def __init__(self, *args):
        if len(args) == 1:
            self.hand: tuple[Card] = args[0]
        else:
            self.hand: tuple[Card] = tuple([card for card in args])
    
    def __repr__(self) -> str:
        return f'Player({self.hand[0]}, {self.hand[1]})'

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
