import itertools
from poker_classes import *
from helpers import *
from tiebreakers import *


def score_hand(hand):
    '''
    Score all possible 5-card combinations in 7-card hand, then return best
    combination and its score.
    '''
    if len(hand) == 7:  # first run through - generate 5-card combos
        top_strength = 0
        top_hand = Hand([], 0)
        pairs = itertools.combinations(hand, 2)
        for pair in pairs:
            five_card_hand = list(hand)
            for card in pair:
                five_card_hand.remove(card)
            five_card_hand.sort(key=lambda x: x.rank)
            strength = score_hand(five_card_hand)
            if strength > top_strength:
                top_strength = strength
                top_hand.cards = five_card_hand
                top_hand.strength = strength
                top_hand.histogram = generate_histogram(top_hand.cards)
            elif strength == top_strength:  # need to pick better of same hands
                hands_to_compare = []
                five_card_hand = Hand(five_card_hand, strength)
                five_card_hand.histogram = generate_histogram(
                    five_card_hand.cards)
                hands_to_compare.append(top_hand)
                hands_to_compare.append(five_card_hand)
                top_hand = break_tie(hands_to_compare, top_strength).pop()
            else:
                continue
        return top_hand
    else:
        histogram = generate_histogram(hand)
        if is_straight_flush(hand):
            return hand_strengths.get('straight flush')
        elif is_four_of_kind(histogram):
            return hand_strengths.get('four of a kind')
        elif is_full_house(histogram):
            return hand_strengths.get('full house')
        elif is_flush(hand):
            return hand_strengths.get('flush')
        elif is_straight(hand):
            return hand_strengths.get('straight')
        elif is_three_of_kind(histogram):
            return hand_strengths.get('three of a kind')
        elif is_two_pair(histogram):
            return hand_strengths.get('two pair')
        elif is_pair(histogram):
            return hand_strengths.get('one pair')
        else:
            return hand_strengths.get('high card')


def is_flush(hand):
    suit = ''
    for card in hand:
        if not suit:
            suit = card.suit
        else:
            if card.suit != suit:
                return False
    return True


def is_straight(hand):
    # otherwise do normal checking
    for index, card in enumerate(hand):
        # look for wheel
        if index == 3 and card.rank == 5:
            if hand[4].rank == 14:
                return True
        if index == 4:
            return True
        else:
            if card.rank + 1 != hand[index+1].rank:
                return False


def is_straight_flush(hand):
    if is_flush(hand) and is_straight(hand):
        return True
    return False


def is_four_of_kind(histogram):
    if 4 in histogram.values():
        return True
    return False


def is_full_house(histogram):
    if 3 in histogram.values() and 2 in histogram.values():
        return True
    return False


def is_three_of_kind(histogram):
    if 3 in histogram.values():
        return True
    return False


def is_two_pair(histogram):
    pairs = 0
    for value in histogram.values():
        if value == 2:
            pairs += 1
    if pairs != 2:
        return False
    return True


def is_pair(histogram):
    if 2 in histogram.values():
        return True
    return False
