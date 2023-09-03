from Card import Card
from PokerHand import PokerHand
from Deck import Deck
from itertools import combinations
import random
import pandas as pd

# human_readable returns [(pair, two_pair, ...), (card ranks)]

class Table:
    # For sorting pandas dataframes in the estimate_chart() method
    hand_type_indexes = {
        "High Card": 8,
        "Pair": 7,
        "Two Pair": 6,
        "Three of a Kind": 5,
        "Straight": 4,
        "Flush": 3,
        "Full House": 2,
        "Four of a Kind": 1,
        "Straight Flush": 0
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
        '''Draws cards from the deck and adds them to the community cards. Drawn cards are removed from the deck.

        Positional arguments:
        num_cards(int): The number of cards to draw.

        Output: None
        '''

        cards_to_add: tuple[Card] = self.deck.draw(num_cards)
        self.community_cards.extend(cards_to_add)
    
    def probabilities(self, n:int=10000) -> dict:
        """Estimates the probability that each type of the hand is the 
            strongest at the table, excluding the player's.
        
        Positional arguments:
        n (int): The number of simulations to use in the estimate. Defaults to
            10000.
        
        Output: Dictionary in which the name of each type of hand is the key 
            and the probability of it being the strongest at the table is the 
            value. Also includes key/value pairs for "the player"s hand but 
            stronger" and "the player"s hand but weaker".
        """
        
        # Caclulates the strength of every single hand that could be 
        # construcuted out of cards in the deck, storing them in a 
        # dictionary for quick access
        hands: dict[str: int] = {}
        possible_hands: tuple = combinations(self.deck, 2)
        for hand in possible_hands:
            c1, c2 = hand[0], hand[1]
            full_hand: list = list(hand) + self.community_cards
            # eg: hands["KHQS"] = strength
            hands[f"{str(c1)}{str(c2)}"] = PokerHand(full_hand).best_hand()["value"]
        
        # Samples n possible table setups and sorts them by how strong each 
        # one's strongest hand was.
        hand_levels = {
            "Straight Flush": [],
            "Four of a Kind": [],
            "Full House": [],
            "Flush": [],
            "Straight": [],
            "Three of a Kind": [],
            "Two Pair": [],
            "Pair": [],
            "High Card": []
        }
        possible_hands: list = hands.keys()
        for game_sample in range(n):
            game_strengths: list[int] = []
            compatible_hands: list[str] = list(possible_hands)
            for opponent in range(self.opponents):
                new_hand = random.choice(compatible_hands)
                compatible_hands: list[str] = [hand for hand in compatible_hands
                                               if (new_hand[:2] not in hand) and
                                               (new_hand[2:] not in hand)]
                game_strengths.append(hands[new_hand])
            top = max(game_strengths)
            # Gets the first digit of the best hand
            # Either it has two cards or five; there can't be an in-between
            if len(self.community_cards) == 0:
                hand_type = top // 256
            else:
                hand_type = top // 1048576
            match hand_type:
                case 0: hand_levels["High Card"].append(top)
                case 1: hand_levels["Pair"].append(top)
                case 2: hand_levels["Two Pair"].append(top)
                case 3: hand_levels["Three of a Kind"].append(top)
                case 4: hand_levels["Straight"].append(top)
                case 5: hand_levels["Flush"].append(top)
                case 6: hand_levels["Full House"].append(top)
                case 7: hand_levels["Four of a Kind"].append(top)
                case 8: hand_levels["Straight Flush"].append(top)
        
        # Creates a pandas DataFrame that matches each hand level to the 
        # number of tables with that level as the strongest opponent.
        hand_counts = {hand_name: len(hand_levels[hand_name]) for hand_name in hand_levels}
        types_frame: pd.DataFrame = pd.DataFrame.from_dict(hand_counts, orient="index")
        types_frame.reset_index(inplace=True)
        types_frame.columns = "Hand", "Count"

        # Creates categories for "player's level but lower" and "player's 
        # level but higher" for the DataFrame
        full_player: PokerHand = PokerHand(self.player+self.community_cards)
        player_strength: int = full_player.best_hand()["value"]
        # Grabs the first digit of the player's hand strength
        if len(self.community_cards) == 0:
            player_hand_level = player_strength // 256
        else:
            player_hand_level = player_strength // 1048576
        match player_hand_level:
            case 0: player_hand_level = "High Card"
            case 1: player_hand_level = "Pair"
            case 2: player_hand_level = "Two Pair"
            case 3: player_hand_level = "Three of a Kind"
            case 4: player_hand_level = "Straight"
            case 5: player_hand_level = "Flush"
            case 6: player_hand_level = "Full House"
            case 7: player_hand_level = "Four of a Kind"
            case 8: player_hand_level = "Straight Flush"
        # Ensures the two new rows go into the right part of the table
        index_high: int = self.hand_type_indexes[player_hand_level]-0.5
        index_low: int = self.hand_type_indexes[player_hand_level]+0.5
        types_frame.sort_index(axis=0, inplace=True, ignore_index=True)
        types_frame.loc[index_high] = f"{player_hand_level} (High)", 0
        types_frame.loc[index_low] = f"{player_hand_level} (Low)", 0
        for hand_strength in hand_levels[player_hand_level]:
            if hand_strength > player_strength:
                types_frame.at[index_high, "Count"] += 1
            elif hand_strength < player_strength:
                types_frame.at[index_low, "Count"] += 1
        # We don't need the combined row anymore - the two new ones suffice
        types_frame.drop(self.hand_type_indexes[player_hand_level], axis=0, inplace=True)

        # Final dataframe cleaning
        types_frame["Probability"] = types_frame["Count"].map(lambda count: count/n)
        types_frame.drop("Count", axis=1, inplace=True)
        types_frame["Percent Chance"] = types_frame["Probability"].map(lambda prob: prob*100)
        types_frame.sort_index(inplace=True, ignore_index=True)

        return types_frame
