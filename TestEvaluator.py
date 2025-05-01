import unittest
from Evaluator import evaluate_hand, rank, suit


def hand_from_strs(card_strs):
    """Helper to convert human-readable cards to integer values"""
    rank_map = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7,
                'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
    suit_map = {'♣': 0, '♦': 1, '♥': 2, '♠': 3}
    return [13 * suit_map[c[1]] + rank_map[c[0]] for c in card_strs]


class TestEvaluator(unittest.TestCase):

    def test_royal_flush(self):
        hand = hand_from_strs(['T♠', 'J♠', 'Q♠', 'K♠', 'A♠', '2♦', '3♣'])
        self.assertEqual(evaluate_hand(hand), (9, [12]))

    def test_straight_flush(self):
        hand = hand_from_strs(['9♦', 'T♦', 'J♦', 'Q♦', 'K♦', '2♠', '3♣'])
        self.assertEqual(evaluate_hand(hand), (8, [11]))

    def test_four_of_a_kind(self):
        hand = hand_from_strs(['9♣', '9♦', '9♥', '9♠', 'K♦', '2♠', '3♣'])
        self.assertEqual(evaluate_hand(hand), (7, [7, 11]))  # 9s with K kicker

    def test_full_house(self):
        hand = hand_from_strs(['T♣', 'T♦', 'T♠', '3♣', '3♦', '4♠', '7♦'])
        self.assertEqual(evaluate_hand(hand), (6, [8, 1]))  # Tens full of Threes

    def test_flush(self):
        hand = hand_from_strs(['2♠', '5♠', '7♠', 'J♠', 'Q♠', '2♦', '3♣'])
        self.assertEqual(evaluate_hand(hand), (5, [10, 9, 5, 3, 0]))

    def test_straight(self):
        hand = hand_from_strs(['5♣', '6♦', '7♠', '8♥', '9♣', '2♠', 'Q♦'])
        self.assertEqual(evaluate_hand(hand), (4, [7]))

    def test_wheel_straight(self):
        hand = hand_from_strs(['A♣', '2♦', '3♣', '4♠', '5♠', 'K♦', 'Q♣'])
        self.assertEqual(evaluate_hand(hand), (4, [3]))  # 5-high straight

    def test_three_of_a_kind(self):
        hand = hand_from_strs(['J♣', 'J♦', 'J♠', '4♠', '5♦', '9♥', '2♠'])
        self.assertEqual(evaluate_hand(hand), (3, [9, 7, 3]))  # Jacks with 9 and 5

    def test_two_pair(self):
        hand = hand_from_strs(['Q♣', 'Q♦', '8♠', '8♥', '3♦', '5♣', 'K♠'])
        self.assertEqual(evaluate_hand(hand), (2, [10, 6, 11]))  # Queens & Eights with King

    def test_one_pair(self):
        hand = hand_from_strs(['K♣', 'K♦', '7♠', '3♥', '2♦', 'J♠', '9♣'])
        self.assertEqual(evaluate_hand(hand), (1, [11, 9, 7, 5]))  # Kings with Jacks, 9, and 7

    def test_high_card(self):
        hand = hand_from_strs(['2♣', '5♦', '8♥', 'J♠', 'Q♣', '3♠', '9♦'])
        self.assertEqual(evaluate_hand(hand), (0, [10, 9, 7, 6, 3]))  # Queens, Jacks, 9, 8, 5


if __name__ == "__main__":
    unittest.main()
