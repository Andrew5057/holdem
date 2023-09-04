from Card import Card
from PokerHand import PokerHand
from Deck import Deck
import itertools
import random
import pandas as pd

# human_readable returns [(pair, two_pair, ...), (card ranks)]

class Table:
    # Used in index_to_level()
    index_level_pairs: dict[int: str] = {
        0: "High Card",
        1: "Pair",
        2: "Two Pair",
        3: "Three of a Kind",
        4: "Straight",
        5: "Flush",
        6: "Full House",
        7: "Four of a Kind",
        8: "Straight Flush",
    }

    def __init__(self, opponents:int=8):
        """Defines a class that simulates & analyzes games of Texas
            Holdem
        
        After instantiation, this class's instance variables should not be 
            altered or deleted, and new instance variables should not be 
            declared.

        Optional arguments:
        opponents (int): The number of opponents at the table. Does not 
            include the player. Defaults to 8.
        
        Instance variables:
        player (list): A list object representing the player's  hand, not 
            including community cards.
        community_cards (list): A continuously updated list representing 
            community cards.
        deck (Deck): A Deck object representing the cards in the gmae that 
            are neither part of the player's hand nor the community cards.
        opponents (int): The number of other players in play. Defaults to 8.
        n (int): The number of random samples used for estimation. Defaults to
            10,000.

        Methods:
        new_game: Re-initializes the table with random cards.
        add_community: Adds cards to the instance's community cards.
        estimate: Uses random sampling to estimate the probability of at 
            least one player at the table beating the player's hand.
        """
        # Sanity check
        if not isinstance(opponents, int):
            raise TypeError("opponents must be of type int.")
        if opponents < 1:
            raise ValueError("opponents must be greater than 1.")

        self.deck: Deck = Deck()
        self.deck.shuffle()
        self.player: list[Card] = list(self.deck.draw(2))
        self.opponents: int = opponents
        self.community_cards: list[Card] = []

    def new_game(self, opponents: int = 8):
        '''Re-initizalizes the table. Uses an alternative name for user 
            friendliness.
        
        Positional arguments:
        opponents (int): The number of opponents at the table. Defaults to 8.
        '''
        self.__init__(opponents)

    def manual_game(self, card1: Card, card2: Card, opponents: int = 8):
        '''Re-initializes the table with a user-defined player hand.
        
        Positional arguments:
        card1 (Card): One card in the player's hand.
        card2 (Card): Another card in the player's hand.
        opponents (int): The number of opponents at the table. Defaults to 8.

        Output: None
        '''
        # Sanity checks
        if not isinstance(card1, Card):
            raise TypeError("Positional variable card1 must be of type Card.")
        if not isinstance(card2, Card):
            raise TypeError("Positional variable card2 must be of type Card.")
        if not isinstance(opponents, int):
            raise TypeError("Optional variable opponents must be of type int.")

        self.player: list[Card] = [card1, card2]
        self.opponents = opponents
        self.deck: Deck = Deck()
        self.deck.shuffle()
        self.deck.remove(card1)
        self.deck.remove(card2)
        self.community_cards: list[Card] = []

        
    def add_community(self, *new_cards: Card) -> None:
        """Updates the ProbabilityCalculator to include new community_cards.
            Removes newly impossible hands accordingly. Also updates best_hand
            values for each hand in the hands dictionary.
        
        Arguments:
        *new_cards: Any number of Card objects, representing the newly drawn
            community cards.
        
        Output: None
        """

        # Sanity checks
        for card in new_cards:
            if not isinstance(card, Card):
                raise TypeError("All arguments must be of type Card.")
            if card in self.community_cards:
                raise ValueError("No arguments can already exist in \
                                 community_cards.")
        if len(set(new_cards)) != len(new_cards):
            raise ValueError("All arguments must be unique.")

        self.community_cards.extend(new_cards)
        for card in new_cards:
            self.deck.remove(card)
    
    def draw_community(self, num_cards: int):
        """Draws cards from the deck and adds them to the community cards. 
            Drawn cards are removed from the deck.

        Positional arguments:
        num_cards(int): The number of cards to draw.

        Output: None
        """

        cards_to_add: tuple[Card] = self.deck.draw(num_cards)
        self.community_cards.extend(cards_to_add)

    def probabilities(self, n_samples:int=10000) -> pd.DataFrame:
        """Estimates the probability that each type of the hand is the 
            strongest at the table, excluding the player's.
        
        Positional arguments:
        n_samples (int): The number of simulations to use in the estimate. 
            Defaults to 10000.
        
        Output: Dictionary in which the name of each type of hand is the key 
            and the probability of it being the strongest at the table is the 
            value. Also includes key/value pairs for "the player"s hand but 
            stronger" and "the player"s hand but weaker", as well as win/loss.
        """
        
        # Find the player's hand strength
        player_full_hand: PokerHand = PokerHand(self.player + self.community_cards)
        player_strength: dict = player_full_hand.best_hand()

        # Dictionary that will store the number of opponents with each hand level. Indexes are the numeric 
        # representations of each level, as per PokerHand.best_hand()
        hand_level_counts = {level: 0 for level in range(9)}
        # These two represent "player's level but weaker" and "player's level 
        # but stronger," respectively
        hand_level_counts[player_strength["level"]-0.25] = 0
        hand_level_counts[player_strength["level"]+0.25] = 0

        # Stores the strength of every possible opponent hand in a dict. Doing this now saves a lot of computation time 
        # later. Keys are the string representations of the two cards in each starting hand.
        hand_strengths = {}
        
        for opponent_hand in itertools.combinations(self.deck, 2):
            card1, card2 = opponent_hand
            full_opponent_hand: PokerHand = PokerHand(self.community_cards + list(opponent_hand))
            opponent_hand_strength = full_opponent_hand.best_hand()
            hand_strengths[f"{str(card1)}{str(card2)}"] = opponent_hand_strength
            hand_strengths[f"{str(card2)}{str(card1)}"] = opponent_hand_strength
        
        # Random sampling
        for sample in range(n_samples):
            # This is the fastest way I can think of to set up all the the 
            # hands.
            chosen_cards = random.sample(self.deck.cards, self.opponents*2)
            opponents_hands = [f"{chosen_cards[2*n]}{chosen_cards[2*n+1]}" for n in range(self.opponents)]
            opponents_strengths = [hand_strengths[hand] for hand in opponents_hands]
            # Finds the best hand. Can't use max because that wouldn't store the level.
            best_hand = {"level": 0, "value": 0}
            for strength in opponents_strengths:
                if strength["value"] > best_hand["value"]:
                    best_hand = strength
            # Increments the correct value in the levels dictionary
            if best_hand["level"] != player_strength["level"]:
                hand_level_counts[best_hand["level"]] += 1
            else:
                if best_hand["value"] > player_strength["value"]:
                    hand_level_counts[best_hand["level"]+0.25] += 1
                elif best_hand["value"] == player_strength["value"]:
                    hand_level_counts[best_hand["level"]] += 1
                else:
                    hand_level_counts[best_hand["level"]-0.25] += 1
        
        # Pretty-printing
        hand_level_df: pd.DataFrame = pd.DataFrame.from_dict(hand_level_counts, orient="index", columns = ["Count"])
        hand_level_df["Level"] = hand_level_df.index.map(Table.index_to_level)
        hand_level_df["Percentage"] = hand_level_df["Count"].map(lambda x: f"{round(x*100/n_samples, 2)}%")
        hand_level_df = hand_level_df[["Level", "Percentage"]]
        hand_level_df.sort_index(ascending=False, inplace=True)

        return hand_level_df

    @staticmethod
    def index_to_level(index: float) -> str:
        match index % 1:
            case 0:
                return Table.index_level_pairs[index]
            case 0.75:
                base_level: int = index+0.25
                return f"{Table.index_level_pairs[base_level]} (Low)"
            case 0.25:
                base_level: int = index-0.25
                return f"{Table.index_level_pairs[base_level]} (High)"
