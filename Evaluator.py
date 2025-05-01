from collections import Counter


# hand ranking numeric breakdown
# royal flush = 9
# straight flush = 8
# four of a kind = 7
# full house = 6
# flush = 5
# straight = 4
# triple = 3
# two pairs = 2
# single pair = 1
# highest card = 0


# map integers (0-51) to rank and suit
def rank(card):
    """0-12 represents ranks 2 to Ace"""
    return card % 13

def suit(card):
    """0-3 represents clubs, diamonds, hearts, spades respectively"""
    return card // 13


# evaluation function
def evaluate_hand(hand):
    """evaluate a 7 card hand and return its rank
    returns a tuple representing
    (hand rank as an integer, tiebreaker cards)"""

    assert len(hand) == 7, "Must provide exactly 7 cards (2 hole cards, 5 community cards)"

    # list of ranks and suits
    ranks = [rank(card) for card in hand]
    suits = [suit(card) for card in hand]

    # sort cards based on number of occurrences first, then rank (descending)
    rank_count = Counter(ranks)
    rank_sorted = sorted([(count, card_rank) for card_rank, count in rank_count.items()], reverse=True)

    # count number of occurrences of each suit
    suit_count = Counter(suits)

    # straight-- consecutive 5 ranks
    def get_straight(hand_ranks):
        """return highest card in a 5 card straight or none"""
        card_ranks = set(hand_ranks)
        # ace to 5-- 5 is the highest card here not ace
        if {12, 0, 1, 2, 3}.issubset(card_ranks): return 3
        # any other case, check for high = 12 (ace), high = 11 (king), ..., high = 4 (6)
        for high in range(12, 3, -1):
            if all(((high - i) % 13) in card_ranks for i in range(5)):
                return high
        return None

    # flush-- 5 cards of the same suit
    # if count is greater than or equal to 5 we have a flush
    flush_suit = next((card_suit for card_suit, count in suit_count.items() if count >= 5), None)


    # check for straight flush-- straight with all suits being the same
    if flush_suit is not None:  # possible to have a straight flush
        suited_cards = [card for card in hand if suit(card) == flush_suit] # collect cards that have flush suit
        suited_ranks = [rank(card) for card in suited_cards]  # collected ranks that have flush suit
        straight_flush_high = get_straight(suited_ranks)  # collect best consecutive 5 ranks
        if straight_flush_high is not None:  # straight flush exists
            if straight_flush_high == 12:
                return 9, [12]  # royal flush
            else:
                return 8, [straight_flush_high]  # straight flush

    # check for a four of a kind-- 4 cards of the same rank and one random card
    if rank_sorted[0][0] == 4:  # there are 4 cards of the same rank
        four_rank = rank_sorted[0][1]  # get card rank
        last_card = max(card_rank for card_rank in ranks if card_rank != four_rank)
        return 7, [four_rank, last_card]

    # check for full house-- 3 cards of the same rank and a pair
    if rank_sorted[0][0] == 3:  # there are 3 cards of the same rank
        three_rank = rank_sorted[0][1]  # get card rank
        pair_rank = None
        for count, card_rank in rank_sorted[1:]:  # traverse remaining cards
            if count >= 2:  # can collect a pair
                pair_rank = card_rank
                break
        if pair_rank is not None:
            return 6, [three_rank, pair_rank]

    # check for flush-- 5 cards of the same suit
    if flush_suit is not None:  # we have a flush, take top ranked cards that have the flush suit
        flush_hand = sorted([rank(card) for card in hand if suit(card) == flush_suit], reverse=True)[:5]
        return 5, flush_hand

    # check for straight-- 5 consecutive ranks
    straight_high = get_straight(ranks)  # see if straight can be collected
    if straight_high is not None:
        return 4, [straight_high]

    # three of a kind
    if rank_sorted[0][0] == 3:
        triples_rank = rank_sorted[0][1]  # get card rank
        remaining = sorted([card_rank for card_rank in ranks if card_rank != triples_rank], reverse=True)[:2]
        return 3, [triples_rank] + remaining

    # two pairs
    if rank_sorted[0][0] == 2 and rank_sorted[1][0] == 2:  # have two pairs
        high_pair = rank_sorted[0][1]
        low_pair = rank_sorted[1][1]
        remaining = max(card_rank for card_rank in ranks if card_rank != high_pair and card_rank != low_pair)
        return 2, sorted([high_pair, low_pair], reverse=True) + [remaining]

    # single pair
    if rank_sorted[0][0] == 2:  # have single pair
        pair_rank = rank_sorted[0][1]
        remaining = sorted([card_rank for card_rank in ranks if card_rank != pair_rank], reverse=True)[:3]
        return 1, [pair_rank] + remaining

    return 0, sorted(ranks, reverse=True)[:5]








