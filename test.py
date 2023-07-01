from Card import Card
from Probabilities import ProbabilityCalculator

calculator = ProbabilityCalculator(Card('AS'), Card('AH'))

calculator.add_community(Card('7D'), Card('5H'), Card('9H'))

print(calculator.estimate())
