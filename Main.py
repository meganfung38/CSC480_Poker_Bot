from Deck import Deck, show_hand
from Evaluator import evaluate_hand
from PokerBot import PokerBot


def random_setup():
    """randomly deals"""
    # create an instance of a deck
    deck = Deck()

    # deal cards
    my_hole = deck.draw(2)  # my hole cards
    shared_community_cards = deck.draw(5)  # shared community cards
    opponent_hole = deck.draw(2) # opponent hole cards

    return my_hole, shared_community_cards, opponent_hole


def simulate_game(my_hand, community_cards, opponent_hand):
    """simulates a full texas hold em game"""

    # create bot-- for MCTS
    bot = PokerBot()

    # pre flop
    print("Pre-Flop -> my hand: ", show_hand(my_hand))
    decision = bot.decide(my_hand, [])
    print("Bot Decision: ", decision)
    if decision == "fold":
            return -1

    # pre turn
    print("Pre-Turn -> my hand: ", show_hand(my_hand))
    print("Pre-Turn -> community cards: ", show_hand(community_cards[:3]))
    decision = bot.decide(my_hand, community_cards[:3])
    print("Bot Decision: ", decision)
    if decision == "fold":
        return -1

    # pre river
    print("Pre-River -> my hand: ", show_hand(my_hand))
    print("Pre-River -> community cards: ", show_hand(community_cards[:4]))
    decision = bot.decide(my_hand, community_cards[:4])
    print("Bot Decision: ", decision)
    if decision == "fold":
        return -1

    # river revealing
    print("Final Round -> my hand: ", show_hand(my_hand))
    print("Final Round -> community cards: ", show_hand(community_cards))
    print("Final Round -> opponent's hand: ", show_hand(opponent_hand))
    my_hand_eval = evaluate_hand(my_hand + community_cards)
    opponent_hand_eval = evaluate_hand(opponent_hand + community_cards)
    result = bot.evaluate_hands(my_hand, opponent_hand, community_cards)
    print("Your hand evaluation: ", my_hand_eval)
    print("Opponent's hand evaluation: ", opponent_hand_eval)

    if result == 1:
        print("You won!")
        return 1
    elif result == 0:
        print("You lost!")
        return 0
    else:
        print("It was a draw!")
        return 0.5



if __name__=="__main__":
    my_random_hand, community, random_opponent_hand = random_setup()
    simulate_game(my_random_hand, community, random_opponent_hand)