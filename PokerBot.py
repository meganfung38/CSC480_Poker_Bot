import random
import math
from itertools import combinations
import time
from Evaluator import evaluate_hand
from Deck import Deck, show_hand


class GameStateStat:
    def __init__(self):
        self.wins = 0  # number of wins through this game state
        self.visits = 0  # number of visits to this game state during simulation phase

    def update(self, result):
        """updates stat of game state"""
        self.visits += 1
        self.wins += result

    def win_rate(self):
        """calculates win rate for current game state"""
        return self.wins / self.visits if self.visits > 0 else 0

    def ucb1(self, total_simulations):
        """calculates the game state's ucb1 value"""
        if self.visits == 0:
            return float('inf')
        return self.win_rate() + math.sqrt(2) * math.sqrt(math.log(total_simulations) / self.visits)


class PokerBot:
    def __init__(self):
        self.simulation_time_limit = 10  # 10 second thinking time

    def evaluate_hands(self, my_hand, opponent_hand, shared_community_cards):
        """evaluates your hand with opponents hand and determines the terminal state"""

        my_score, my_tiebreakers = evaluate_hand(my_hand + shared_community_cards)
        opponent_score, opponent_tiebreakers = evaluate_hand(opponent_hand + shared_community_cards)
        if my_score > opponent_score:  # terminal state: win
            return 1
        elif my_score < opponent_score:  # terminal state: loss
            return 0
        else:  # compare tiebreaker cards
            for my_tb, opponent_tb in zip(my_tiebreakers, opponent_tiebreakers):
                if my_tb > opponent_tb:
                    return 1  # win by highest card
                elif my_tb < opponent_tb:
                    return 0  # loss by highest card
        return 0.5  # full tie if tiebreakers don't break ties

    def decide(self, my_hand, revealed_cards):
        """computes a win rate using MCTS for the current game state-- current hand--
        and determines whether to stay or fold"""

        start = time.time()  # record start time
        total_simulations = 0  # number of simulated rollouts completed within time limit per decision point
        node_stats = {}  # maps opponent hands to NodeStats

        # set up game state
        full_deck = set(range(52))
        known_cards = set(my_hand + revealed_cards)  # flipped cards at decision point
        remaining_cards = list(full_deck - known_cards)  #  # cards that can still be flipped
        possible_opponent_hand = list(combinations(remaining_cards, 2))  # list of all the possible opponent hands

        # simulate rollouts within time limit (thinking time for decision-making)
        while time.time() - start < self.simulation_time_limit:

            # SELECTION
            best_ucb1 = float('-inf')  # by default
            choose = None  # node/ game state to choose in MCTS traversal

            # randomly sample a possible opponent hand
            for opponent_hand in random.sample(possible_opponent_hand, k=min(len(possible_opponent_hand), 100)):
                opponent_key = tuple(sorted(opponent_hand))
                curr_stats = node_stats.get(opponent_key, GameStateStat())  # get current game state stat
                ucb1_value = curr_stats.ucb1(total_simulations + 1)  # evaluate ucb1 value for current game state
                if ucb1_value > best_ucb1:  # determine best game state from root
                    best_ucb1 = ucb1_value
                    choose = opponent_key

            if not choose:  # in case no assignment is made (failed to determine which game state from root is best)
                continue

            # EXPANSION + SIMULATION
            deck = Deck()
            deck.remove_cards(my_hand + revealed_cards + list(choose))  # create an instance of the current deck updated with current game state

            to_reveal = 5 - len(revealed_cards)  # number of cards to still be flipped in shared community cards
            complete_community_cards = deck.sample(to_reveal)  # randomly sample cards that need to flipped in shared community cards
            shared_community_cards = revealed_cards + complete_community_cards  # full set of community cards

            # determine terminal state: win/ loss/ draw
            terminal_state = self.evaluate_hands(my_hand, list(choose), shared_community_cards)

            # update game state's stat for opponent hand
            if choose not in node_stats:  # create key and stat structure
                node_stats[choose] = GameStateStat()
            node_stats[choose].update(terminal_state)  # update wins and visits
            total_simulations += 1  # simulated rollout completed -> increment value

        # BACKPROPAGATION
        total_wins = sum(game_states.wins for game_states in node_stats.values())  # calculate total number of wins during simulation phase
        win_rate = total_wins / total_simulations if total_simulations > 0 else 0  # calculate average win rate over completed simulations

        print("simulations ran: ", total_simulations)
        print("win rate: ", win_rate)

        return "stay" if win_rate >= 0.5 else "fold"


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
    print("Bot computing win rate...")
    decision = bot.decide(my_hand, [])
    print("Bot Decision: ", decision)
    user_decision = input("Do you want to stay or fold? (stay/fold): ").strip().lower()
    if user_decision == "fold":
        print("You folded.")
        return -1

    # pre turn
    print("Pre-Turn -> my hand: ", show_hand(my_hand))
    print("Pre-Turn -> community cards: ", show_hand(community_cards[:3]))
    print("Bot computing win rate...")
    decision = bot.decide(my_hand, community_cards[:3])
    print("Bot Decision: ", decision)
    user_decision = input("Do you want to stay or fold? (stay/fold): ").strip().lower()
    if user_decision == "fold":
        print("You folded.")
        return -1

    # pre river
    print("Pre-River -> my hand: ", show_hand(my_hand))
    print("Pre-River -> community cards: ", show_hand(community_cards[:4]))
    print("Bot computing win rate...")
    decision = bot.decide(my_hand, community_cards[:4])
    print("Bot Decision: ", decision)
    user_decision = input("Do you want to stay or fold? (stay/fold): ").strip().lower()
    if user_decision == "fold":
        print("You folded.")
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
    continue_game = True
    while continue_game:
        my_random_hand, community, random_opponent_hand = random_setup()
        simulate_game(my_random_hand, community, random_opponent_hand)
        user_response = input("Do you want to play again? (yes/ no): ").strip().lower()
        if user_response == "no":
            continue_game = False
    print("Thanks for playing!")
