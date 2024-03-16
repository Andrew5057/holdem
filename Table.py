from Card import Card
from PokerHand import PokerHand
from Deck import Deck
import itertools
import pandas as pd
import random
from tabulate import tabulate

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

    def __init__(self):
        """Defines a class that simulates & analyzes games of Texas
            Holdem
        
        After instantiation, this class's instance variables should not be 
            altered or deleted, and new instance variables should not be 
            declared.

        Optional arguments:
            None
        
        Instance variables:
        player (list): A list object representing the player's  hand, not 
            including community cards.
        community_cards (list): A continuously updated list representing 
            community cards.
        deck (Deck): A Deck object representing the cards in the gmae that 
            are neither part of the player's hand nor the community cards.
        n (int): The number of random samples used for estimation. Defaults to
            10,000.

        Methods:
        new_game: Re-initializes the table with random cards.
        add_community: Adds cards to the instance's community cards.
        estimate: Uses random sampling to estimate the probability of at 
            least one player at the table beating the player's hand.
        """

        self.deck: Deck = Deck()
        self.deck.shuffle()
        self.player: list[Card] = list(self.deck.draw(2))
        self.community_cards: list[Card] = []

    def new_game(self):
        '''Re-initizalizes the table. Uses an alternative name for user 
            friendliness.
               
        Returns: None
        '''
        self.__init__()

    def manual_game(self, card1: Card, card2: Card):
        '''Re-initializes the table with a user-defined player hand.
        
        Positional arguments:
        card1 (Card): One card in the player's hand.
        card2 (Card): Another card in the player's hand.
 
        Returns: None
        '''
        # Sanity checks
        if not isinstance(card1, Card):
            raise TypeError("Positional variable card1 must be of type Card.")
        if not isinstance(card2, Card):
            raise TypeError("Positional variable card2 must be of type Card.")
        if (card1 == card2):
            raise ValueError("Positional variables card1 and card2 cannot be identical")

        self.player: list[Card] = [card1, card2]
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
        
        Returns: None
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

        Returns: None
        """

        cards_to_add: tuple[Card] = self.deck.draw(num_cards)
        self.community_cards.extend(cards_to_add)
    


    def probabilities(self, opponents, n_samples:int=10000) -> pd.DataFrame:
        """Estimates the probability that each type of the hand is the 
            strongest at the table, excluding the player's.
        
        Positional arguments:
        n_samples (int): The number of simulations to use in the estimate. 
            Defaults to 10000.
        
        Returns: List of three pandas DataFrames. Each contains two columns, 
            called "Level" and "Percentage" respectively. The Level 
            is a string representing the name of the hand, such as "Pair". 
            The Percentage is a string representing the percentage that 
            any other player at the table has that level of hand, followed by 
            the percentage sign %. The first DataFrame contains only the 
            levels stronger than the player's, the second DataFrame contains 
            the levels equal to the players, and the third DataFrame contains 
            the levels weaker than the player's. The second is further 
            subdivided into "Level (High)", "Level", and "Level (Weak)", 
            which represent hands that beat, draw, and lose to the player, 
            respectively.
        """

        # Find the player's hand strength
        player_full_hand: PokerHand = PokerHand(self.player + self.community_cards)
        player_strength: dict = player_full_hand.best_hand()
        player_level: int = player_strength["level"]

        # Dictionary that will store the number of opponents with each hand level. Indexes are the numeric 
        # representations of each level, as per PokerHand.best_hand()
        hand_level_counts = {level: 0 for level in range(9)}
        # These two represent "player's level but weaker" and "player's level 
        # but stronger," respectively
        hand_level_counts[player_level-0.25] = 0
        hand_level_counts[player_level+0.25] = 0

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
            reasonable = False
            while not reasonable:
                reasonable = True
                # This is the fastest way I can think of to set up all the the 
                # hands.
                chosen_cards = random.sample(self.deck.cards, opponents*2)
                opponents_hands = [(chosen_cards[2*n], chosen_cards[2*n+1]) for n in range(opponents)]
                for hand in opponents_hands:
                    """
                    Reasonability check. Keep if:
                    - At least 1 King/Ace
                    - Both > 10
                    - Consecutive cards
                    - Suited
                    - Pair
                    Otherwise draw a new set
                    """
                    card1, card2 = hand
                    if ((int(card1.value, 16) < 13) and (int(card2.value, 16) < 13)) and \
                            ((int(card1.value, 16)) < 10 or (int(card2.value, 16) < 10)) and \
                            ((abs(int(card1.value, 16)-int(card2.value, 16))) > 1) and \
                                (card1.suit != card2.suit):
                        reasonable = False
                        break

            opponents_hands = [str(hand[0]) + str(hand[1]) for hand in opponents_hands]
            opponents_strengths = [hand_strengths[hand] for hand in opponents_hands]
            
            # Finds the best hand. Can't use max() because that wouldn't store the level.
            best_hand = {"level": 0, "value": 0}
            for strength in opponents_strengths:
                if strength["value"] > best_hand["value"]:
                    best_hand = strength
            # Increments the correct value in the levels dictionary
            if best_hand["level"] != player_level:
                hand_level_counts[best_hand["level"]] += 1
            else:
                if best_hand["value"] > player_strength["value"]:
                    hand_level_counts[best_hand["level"]+0.25] += 1
                elif best_hand["value"] == player_strength["value"]:
                    hand_level_counts[best_hand["level"]] += 1
                else:
                    hand_level_counts[best_hand["level"]-0.25] += 1
        
        # Splitting the dictionary into same-level, higher-level, and lower-level dicts.
        # Could be made more efficient by doing this during the loop, but that takes refactoring.
        higher_level_counts: dict = {}
        lower_level_counts: dict = {}
        same_level_counts: dict = {}

        for level, count in hand_level_counts.items():
            if level >= player_level + 1:
                higher_level_counts[level] = count
            elif level <= player_level - 1:
                lower_level_counts[level] = count
            else:
                same_level_counts[level] = count

        # Pretty-printing as DataFrames
        hand_dataframes: list[pd.DataFrame] = []
        for hand_dict in (higher_level_counts, same_level_counts, lower_level_counts):
            df: pd.DataFrame = pd.DataFrame.from_dict(hand_dict, orient="index", columns = ["Count"])
            df["Level"] = df.index.map(Table.index_to_level)
            df["Percentage"] = df["Count"].map(lambda x: f"{round(x*100/n_samples, 2)}%")
            df = df[["Level", "Percentage"]]
            df.sort_index(ascending=False, inplace=True, ignore_index=True)
            hand_dataframes.append(df.copy())
        return hand_dataframes

    def analyze_and_display(self, opponents: list[int]):
        # Get results for each opponents input
        results = []
        for n in opponents:
            result_n = self.probabilities(n)
            result_n[0] = result_n[0].rename(columns={'Percentage': n})
            result_n[1] = result_n[1].rename(columns={'Percentage': n})
            result_n[2] = result_n[2].rename(columns={'Percentage': n})
            results.append(result_n)
            # print(result_n[0].columns)
            # print(result_n[1].columns)
            # print(result_n[2].columns)

        # Right now results is a list of list of pandas tables
        stronger_hand = results[0][0]
        same_hand = results[0][1]
        weaker_hand = results[0][2]
        for i in range(1, len(opponents)):
            stronger_hand = stronger_hand.merge(results[i][0], how='outer', on='Level')
            same_hand = same_hand.merge(results[i][1], how='outer', on='Level')
            weaker_hand = weaker_hand.merge(results[i][2], how='outer', on='Level')

        # Reorder and standardize columns
        stronger_hand = stronger_hand[["Level"]+opponents]
        same_hand = same_hand[["Level"]+opponents]
        weaker_hand = weaker_hand[["Level"]+opponents]
        # print(stronger_hand.columns)
        # print(same_hand.columns)
        # print(weaker_hand.columns)
  
        # Display
        import os
        os.system("cls")
        # Print cards
        Card.print_cards(self.player + [Card()] + self.community_cards)
        # Card.print_cards(self.community_cards)

        # tablefmt options: psql(preferred), plain, simple, grid, pipe, html, outline, etc
        print(tabulate(stronger_hand, headers=['Hand']+opponents, tablefmt='psql', showindex=False))
        print(tabulate(same_hand, tablefmt='psql', showindex=False))
        print(tabulate(weaker_hand, tablefmt='psql', showindex=False))
        return
    
    @staticmethod
    def index_to_level(index: float) -> str:
        """Converts a numeric hand representation to a string representing 
            its level, as per Table.probabilities().
        
        Poisitional arguments:
        index (float): The index to be converted to a string level.

        Returns: A string representing the index's level, such as "Pair". If 
            index is a decimal, the method infers that it is a stronger 
            or weaker version of the player's hand (for example, both are 
            Pairs but the player has a stronger kicker) and append "(Low)" or
            "(High)" to the string accordingly.
        """

        match index % 1:
            case 0:
                return Table.index_level_pairs[index]
            case 0.75:
                base_level: int = index+0.25
                return f"{Table.index_level_pairs[base_level]} (Low)"
            case 0.25:
                base_level: int = index-0.25
                return f"{Table.index_level_pairs[base_level]} (High)"
