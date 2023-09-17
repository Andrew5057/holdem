from Card import Card
from Deck import Deck
from PokerHand import PokerHand
from Table import Table
import os
import sys

table = Table()

# New game
table.new_game()
table.analyze_and_display()

# Flop
if input("Hit Enter for the flop or 'x' to exit")=='x': sys.exit()
table.draw_community(num_cards=3)
table.analyze_and_display()

# Turn
input("Any key + Enter for the turn card")
table.draw_community(num_cards=1)
table.analyze_and_display()

# River
input("Any key + Enter for the river card")
table.draw_community(num_cards=1)
table.analyze_and_display()
