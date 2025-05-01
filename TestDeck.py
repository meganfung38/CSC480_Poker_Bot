import unittest
from Deck import Deck, show_card, show_hand

class TestDeck(unittest.TestCase):

    def test_deck_initialization(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(len(set(deck.cards)), 52)  # all cards unique
        for card in deck.cards:
            self.assertTrue(0 <= card < 52)

    def test_draw_cards(self):
        deck = Deck()
        drawn = deck.draw(5)
        self.assertEqual(len(drawn), 5)
        self.assertEqual(len(deck.cards), 47)
        self.assertFalse(any(card in deck.cards for card in drawn))  # drawn cards removed

    def test_remove_cards(self):
        deck = Deck()
        cards_to_remove = deck.cards[:5]
        deck.remove_cards(cards_to_remove)
        self.assertEqual(len(deck.cards), 47)
        for card in cards_to_remove:
            self.assertNotIn(card, deck.cards)

    def test_copy_deck(self):
        deck = Deck()
        deck_copy = deck.copy()
        self.assertEqual(deck.cards, deck_copy.cards)
        deck.draw(1)
        self.assertNotEqual(deck.cards, deck_copy.cards)  # ensure it's a copy, not reference

    def test_sample(self):
        deck = Deck()
        sample = deck.sample(5)
        self.assertEqual(len(sample), 5)
        self.assertTrue(all(card in deck.cards for card in sample))
        self.assertEqual(len(deck.cards), 52)  # sampling shouldn't remove

    def test_show_card(self):
        # 0 = 2♣, 12 = A♣, 13 = 2♦, 51 = A♠
        self.assertEqual(show_card(0), "2♣")
        self.assertEqual(show_card(12), "A♣")
        self.assertEqual(show_card(13), "2♦")
        self.assertEqual(show_card(51), "A♠")

    def test_show_hand(self):
        hand = [0, 12, 25, 38, 51]  # 2♣, A♣, A♦, A♥, A♠
        expected = ["2♣", "A♣", "A♦", "A♥", "A♠"]
        self.assertEqual(show_hand(hand), expected)


if __name__ == "__main__":
    unittest.main()
