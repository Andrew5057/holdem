from Card import Card
from Deck import Deck
from PokerHand import PokerHand
from itertools import combinations
from random import choice

class ProbabilityCalculator:

    def __init__(self, player_hand: list[Card]):
        
        self.player: str = f'{str(player_hand[0])}{str(player_hand[1])}'
        self.deck: Deck = Deck()
        self.deck.remove(player_hand[0])
        self.deck.remove(player_hand[1])

        possible_cards: list[str] = ['2H', '2D', '2S', '2C', '3H', '3D', 
                                     '3S', '3C', '4H', '4D', '4S', '4C',
                                     '5H', '5D', '5S', '5C', '6H', '6D', 
                                     '6S', '6C', '7H', '7D', '7S', '7C', 
                                     '8H', '8D', '8S', '8C', '9H', '9D', 
                                     '9S', '9C', 'TH', 'TD', 'TS', 'TC', 
                                     'JH', 'JD', 'JS', 'JC', 'QH', 'QD', 
                                     'QS', 'QC', 'KH', 'KD', 'KS', 'KC', 
                                     'AH', 'AD', 'AS', 'AC']
        possible_cards.remove(str(player_hand[0]))
        possible_cards.remove(str(player_hand[1]))
        self.hands: dict[str: int] = {}
        possible_hands: tuple = combinations(self.possible_cards, 2)
        for hand in possible_hands:
            c1, c2 = hand[0], hand[1]
            self.hands[f'{c1}{c2}'] = PokerHand(Card(c1),
                                                Card(c2)).best_hand()

        self.community_cards: list[Card] = []
        
    def community(self, *new_cards: Card) -> None:
        '''Updates the ProbabilityCalculator to include new community_cards.
            Removes newly impossible hands accordingly. Also updates best_hand
            values for each hand in the hands dictionary.
        
        Arguments:
        *new_cards: Any number of Card objects, representing the newly drawn
            community cards.
        
        Output: None
        '''

        self.community_cards.extend(new_cards)
        
        for hand in self.hands:
            c1, c2 = Card(hand[:2]), Card(hand[2:])
            if (c1 in self.community_cards) or (c2 in self.community_cards):
                # Hands that contain a community card are impossible.
                del self.hands[hand]
                continue

            full_hand = PokerHand(self.community_cards + [c1, c2])
            self.hands[hand] = full_hand.best_hand()
    def estimate(self, opponents:int=8, n:int=1000) -> float:
        '''Estimates the probability that at least one person has a hand
            better than the player's.
        
        Arguments:
        opponents (int): The number of other players in play. Defaults to 8.
        n (int): The number of random samples used for estimation  

        Output: float in [0, 1] representing the estimated probability that
        at least one opponent has a hand better than the player's.
        '''

        possible_hands: list = self.hands.keys()
        sample_maxes: list[int] = []
        for game_sample in range(n):
            game_strengths: list[int] = []
            compatible_hands: list[str] = list(possible_hands)
            for opponent in range(opponents):
                new_hand = choice(compatible_hands)
                compatible_hands: list[str] = [hand for hand in compatible_hands
                                               if (new_hand[:2] not in hand) and
                                               (new_hand[2:] not in hand)]
                game_strengths.append(self.hands[new_hand])
            sample_maxes.append(max(game_strengths))
        num_better = len([game for game in sample_maxes if game > self.hands[self.player]])
        num_games = len(sample_maxes)
        return num_better/num_games