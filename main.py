from Deck import Deck, show_hand
from PokerBot import PokerBot


def main():
    """simulates a full texas hold em game"""

    # create an instance of a deck
    deck = Deck()

    # deal cards
    my_hand = deck.draw(2)  # my hole cards
    community_cards = deck.draw(5)  # shared community cards

    # create both-- for MCTS
    bot = PokerBot()

    # pre flop
    print("Pre-Flop -> my hand: ", show_hand(my_hand))
    decision = bot.decide(my_hand, [])
    print("Bot Decision: ", decision)
    if decision == "fold":
            return

    # pre turn
    print("Pre-Turn -> my hand: ", show_hand(my_hand))
    print("Pre-Turn -> community cards: ", show_hand(community_cards[:3]))
    decision = bot.decide(my_hand, community_cards[:3])
    print("Bot Decision: ", decision)
    if decision == "fold":
        return

    # pre river
    print("Pre-River -> my hand: ", show_hand(my_hand))
    print("Pre-River -> community cards: ", show_hand(community_cards[:4]))
    decision = bot.decide(my_hand, community_cards[:4])
    print("Bot Decision: ", decision)
    if decision == "fold":
        return

    # river revealing
    opponent_hand = deck.draw(2)
    print("Final Round -> my hand: ", show_hand(my_hand))
    print("Final Round -> community cards: ", show_hand(community_cards))
    print("Final Round -> opponent's hand: ", show_hand(opponent_hand))
    result = bot.evaluate_hands(my_hand, opponent_hand, community_cards)
    if result == 1:
        print("You won!")
    elif result == 0:
        print("You lost!")
    else:
        print("It was a draw!")



if __name__=="__main__":
    main()