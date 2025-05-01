import random


# constants
NUM_CARDS = 52
RANKS = list(range(13)) # 0 = 2, 1 = 3, ... 9 = Jake, 10 = Queen, 11 = King, 12 = Ace
SUITS = list(range(4)) # 0 = clubs, 1 = diamonds, 2 = hearts, 3 = spades


# visualize cards
def show_card(card):
    """convert integer card (0-51) to its card (rank and suit)"""
    rank = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suit = ['♣', '♦', '♥', '♠']
    return rank[card % 13] + suit[card // 13]


def show_hand(hand):
    """takes a list of integer cards and converts them into its cards (rank and suit)"""
    return [show_card(card) for card in hand]


# deck representation
class Deck:
    def __init__(self):
        """initializes and shuffles a 52 card deck using integers to represent cards (0-51)"""
        self.cards = list(range(NUM_CARDS))
        random.shuffle(self.cards)

    def draw(self, n = 1):
        """draws n cards from the top of the deck.
        returns a list of n cards (represented as integers)"""
        drawn = self.cards[:n]  # drawn cards to return
        self.cards = self.cards[n:]  # remaining cards in deck
        return drawn

    def remove_cards(self, cards_to_remove):
        """removes a list of known cards from deck:
        known hole cards or community cards"""
        to_remove = set(cards_to_remove) # for faster lookup
        self.cards = [card for card in self.cards if card not in to_remove]

    def copy(self):
        """creates a copy of the deck for simulated rollouts"""
        temp = Deck()
        temp.cards = self.cards[:]
        return temp

    def sample(self, n):
        """randomly sample n cards from current deck (simulate unknown opponent's hand or unrevealed community cards)"""
        return random.sample(self.cards, n)