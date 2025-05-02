import unittest
from Main import simulate_game


class TestPokerBot(unittest.TestCase):

    def test_draw(self):
        """draw-- both use all 5 community cards as hand"""
        my_hand = [51, 24]  # A♠ and K♦
        community_cards = [49, 48, 47, 46, 45]  # Q♠, J♠, T♠, 9♠, 8♠
        opponent_hand = [44, 27]  # 7♠ and 2♥
        terminal_state = simulate_game(my_hand, community_cards, opponent_hand)
        self.assertEqual(terminal_state, 0.5)

    def test_win(self):
        """win-- royal flush vs straight flush"""
        my_hand = [51, 50]  # A♠ and K♠
        community_cards = [49, 48, 47, 46, 45]  # Q♠, J♠, T♠, 9♠, 8♠
        opponent_hand = [44, 27]  # 7♠ and 2♥
        terminal_state = simulate_game(my_hand, community_cards, opponent_hand)
        self.assertEqual(terminal_state, 1)

    def test_loss(self):
        """loss-- four of a kind (high 4) vs four of a kind (high 7)"""
        my_hand = [28, 41]  # 4♥ and 4♠
        community_cards = [31, 44, 11, 15, 2]  # 7♥, 7♠, K♣, 4♦, 4♣
        opponent_hand = [5, 18]  # 7♣ and 7♦
        terminal_state = simulate_game(my_hand, community_cards, opponent_hand)
        self.assertEqual(terminal_state, 0)


if __name__ == "__main__":
    unittest.main()