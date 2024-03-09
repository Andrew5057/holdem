from Card import Card
from Deck import Deck
from PokerHand import PokerHand
from Table import Table

def random_game():
    table: Table = Table()
    
    # Initial draw
    print("Analyzing the starting hands...")
    table.new_game()
    table.analyze_and_display(opponents=[7, 5, 3, 1])

    # Flop
    input("Hit Enter for the flop")
    print("Analyzing...")
    table.draw_community(num_cards = 3)
    table.analyze_and_display(opponents=[7, 5, 3, 1])

    # Turn
    input("Hit Enter for the turn")
    print("Analyzing...")
    table.draw_community(num_cards = 1)
    table.analyze_and_display(opponents=[7, 5, 3, 1])

    # River
    input("Hit Enter for the river")
    print("Analyzing...")
    table.draw_community(num_cards = 1)
    table.analyze_and_display(opponents=[7, 5, 3, 1])

def manual_game():
    card1 = input("Enter your first pocket card: ")
    try:
        card1: Card = Card(card1)
    except ValueError:
        while (isinstance(card1, str)):
            card1 = input(f"{card1} is not a card. Enter your first pocket card: ")
            try:
                card1: Card = Card(card1)
            except ValueError:
                pass
    
    card2 = input("Enter your second pocket card: ")
    try:
        card2: Card = Card(card2)
    except ValueError:
        while (isinstance(card2, str)):
            card2 = input(f"{card2} is not a card. Enter your second pocket card: ")
            try:
                card2: Card = Card(card2)
            except ValueError:
                pass
    while (card1 == card2):
        card2 = input("Your pocket cards can't be identical. Enter your second pocket card: ")
        try:
            card2: Card = Card(card2)
        except ValueError:
            while (isinstance(card2, str)):
                card2 = input(f"{card2} is not a card. Enter your second pocket card: ")
                try:
                    card2: Card = Card(card2)
                except ValueError:
                    pass

    table: Table = Table()
    
    # Initial draw
    print("Analyzing the starting hands...")
    table.manual_game(card1, card2)
    table.analyze_and_display(opponents=[7, 5, 3, 1])

    # Flop
    input("Hit Enter for the flop")
    print("Analyzing...")
    table.draw_community(num_cards = 3)
    table.analyze_and_display(opponents=[7, 5, 3, 1])

    # Turn
    input("Hit Enter for the turn")
    print("Analyzing...")
    table.draw_community(num_cards = 1)
    table.analyze_and_display(opponents=[7, 5, 3, 1])

    # River
    input("Hit Enter for the river")
    print("Analyzing...")
    table.draw_community(num_cards = 1)
    table.analyze_and_display(opponents=[7, 5, 3, 1])

def play_game():
    play_mode = input("/Manual/ game or /Random/ game? ").lower()
    
    match play_mode:
        case "random":
            random_game()
        case "manual":
            manual_game()
        case _:
            play_mode = input("I couldn't understand that. /Manual/ game or /Random/ game? ").lower()
            while play_mode not in ("manual", "lower"):
                play_mode = input("I couldn't understand that. /Manual/ game or /Random/ game? ").lower()
            match play_mode:
                case "random":
                    random_game()
                case "manual":
                    manual_game()

if __name__ == "__main__":
    play_game()

    while input("\nPlay again? (y/n) ").lower()[0] == "y":
        print()
        play_game()

