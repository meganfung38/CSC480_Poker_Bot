import random
import math
from itertools import combinations
import time
from Deck import Deck
from Evaluator import evaluate_hand


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

        my_score = evaluate_hand(my_hand + shared_community_cards)
        opponent_score = evaluate_hand(opponent_hand + shared_community_cards)
        if my_score > opponent_score:  # terminal state: win
            return 1
        elif my_score < opponent_score:  # terminal state: loss
            return 0
        else:  # terminal state: draw
            return 0.5

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

        print("win rate: ", win_rate)

        return "stay" if win_rate >= 0.5 else "fold"

