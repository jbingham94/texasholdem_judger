from helpers import generate_histogram


# Tiebreaker functions


def break_tie(hands, strength):
    winners = []
    if strength == 9:
        winners = compare_straights(hands)
    elif strength == 8:
        winners = compare_four_of_kinds(hands)
    elif strength == 7:
        winners = compare_full_houses(hands)
    elif strength == 6:
        winners = compare_flushes(hands)
    elif strength == 5:
        winners = compare_straights(hands)
    elif strength == 4:
        winners = compare_three_of_kinds(hands)
    elif strength == 3:
        winners = compare_two_pairs(hands)
    elif strength == 2:
        winners = compare_pairs(hands)
    else:
        winners = compare_high_cards(hands)
    return winners


def compare_straights(hands):
    best_top = 0
    winners = []
    for hand in hands:  # first find high card
        top = 0
        if hand.cards[4].rank == 14:  # deal with A-5 straight
            top = 5
        else:
            top = hand.cards[4].rank
        if top > best_top:
            best_top = top
    for hand in hands:  # check if more than one person has the high card
        top = 0
        if hand.cards[4].rank == 14:  # deal with A-5 straight
            top = 5
        else:
            top = hand.cards[4].rank
        if top == best_top:
            winners.append(hand)
    return winners


def compare_flushes(hands):
    winners = list(hands)
    index = 4  # start by comparing highest cards
    while index >= 0:
        top_card = 0
        for hand in winners:  # first determine highest card at index
            if hand.cards[index].rank > top_card:
                top_card = hand.cards[index].rank
        for hand in winners[:]:  # weed out, if possible
            if hand.cards[index].rank < top_card:
                winners.remove(hand)
        if len(winners) == 1:  # we're done
            return winners
        else:
            index -= 1
    return winners


def compare_four_of_kinds(hands):
    winners = list(hands)
    best_quad = 0
    for hand in winners:  # first determine best quad
        for rank, freq in hand.histogram.items():
            if freq == 4 and rank > best_quad:
                best_quad = rank
    for hand in winners[:]:  # weed out hands with quad < best quad
        for rank, freq in hand.histogram.items():
            if freq == 4:
                if rank < best_quad:
                    winners.remove(hand)
    if len(winners) > 1:  # need to compare kickers
        best_kicker = 0
        for hand in winners:  # first determine best kicker
            for rank, freq in hand.histogram.items():
                if freq == 1:
                    if rank > best_kicker:
                        best_kicker = rank
        for hand in winners[:]:  # weed out hands with kicker < best kicker
            for rank, freq in hand.histogram.items():
                if freq == 1:
                    if rank < best_kicker:
                        winners.remove(hand)
    return winners


def compare_full_houses(hands):
    winners = list(hands)
    best_triple = 0
    for hand in winners:  # first determine best triples
        for rank, freq in hand.histogram.items():
            if freq == 3 and rank > best_triple:
                best_triple = rank
    for hand in winners[:]:  # weed out hands with triple < best triple
        for rank, freq in hand.histogram.items():
            if freq == 3 and rank < best_triple:
                winners.remove(hand)
    if len(winners) > 1:  # need to compare doubles
        best_double = 0
        for hand in winners:  # first determine best double
            for rank, freq in hand.histogram.items():
                if freq == 2 and rank > best_double:
                    best_double = rank
        for hand in winners[:]:  # weed out hands with double < best double
            for rank, freq in hand.histogram.items():
                if freq == 2 and rank < best_double:
                    winners.remove(hand)
    return winners


def compare_three_of_kinds(hands):
    winners = list(hands)
    best_triple = 0
    for hand in winners:  # first determine best triples
        for rank, freq in hand.histogram.items():
            if freq == 3 and rank > best_triple:
                best_triple = rank
    for hand in winners[:]:  # weed out hands with triple < best triple
        for rank, freq in hand.histogram.items():
            if freq == 3 and rank < best_triple:
                winners.remove(hand)
    if len(winners) > 1:
        repeat = 1  # may need to repeat to compare next-best kicker
        while repeat >= 0:
            best_kicker = 0
            for hand in winners:
                best_kicker_in_hand = 0  # need to find best kicker each time
                for rank, freq in hand.histogram.items():
                    if freq == 1 and rank > best_kicker_in_hand:
                        best_kicker_in_hand = rank
                if best_kicker_in_hand > best_kicker:
                    best_kicker = best_kicker_in_hand
            for hand in winners[:]:
                best_kicker_in_hand = 0
                for rank, freq in hand.histogram.items():
                    if freq == 1 and rank > best_kicker_in_hand:
                        best_kicker_in_hand = rank
                if best_kicker_in_hand < best_kicker:
                    winners.remove(hand)
                else:  # remove best kicker entry to compare next-best
                    del hand.histogram[best_kicker_in_hand]
            if len(winners) == 1:  # we're done
                repeat = -1
            else:
                repeat -= 1
    for hand in winners:  # refresh histograms
        hand.histogram = generate_histogram(hand.cards)
    return winners


def compare_two_pairs(hands):
    winners = list(hands)
    repeat = 1  # may need to repeat once to check second pair
    while repeat >= 0:
        best_pair = 0
        for hand in winners:
            best_pair_in_hand = 0  # need to find best pair each time
            for rank, freq in hand.histogram.items():
                if freq == 2 and rank > best_pair_in_hand:
                    best_pair_in_hand = rank
            if best_pair_in_hand > best_pair:
                best_pair = best_pair_in_hand
        for hand in winners[:]:
            best_pair_in_hand = 0
            for rank, freq in hand.histogram.items():
                if freq == 2 and rank > best_pair_in_hand:
                    best_pair_in_hand = rank
            if best_pair_in_hand < best_pair:
                winners.remove(hand)
            else:  # temporarily remove best pair to compare next-best
                del hand.histogram[best_pair_in_hand]
        if len(winners) == 1:  # we're done
            repeat = -1
        else:
            repeat -= 1
    if len(winners) > 1:  # must compare kickers
        best_kicker = 0
        for hand in winners:
            for rank, freq in hand.histogram.items():
                if freq == 1 and rank > best_kicker:
                    best_kicker = rank
        for hand in winners[:]:
            for rank, freq in hand.histogram.items():
                if freq == 1 and rank < best_kicker:
                    winners.remove(hand)
    for hand in winners:  # refresh histograms
        hand.histogram = generate_histogram(hand.cards)
    return winners


def compare_pairs(hands):
    winners = list(hands)
    best_pair = 0
    for hand in hands:  # first determine best pairs
        for rank, freq in hand.histogram.items():
            if freq == 2 and rank > best_pair:
                best_pair = rank
    for hand in winners[:]:  # weed out hands with pair < best pair
        for rank, freq in hand.histogram.items():
            if freq == 2 and rank < best_pair:
                winners.remove(hand)
    if len(winners) > 1:
        repeat = 2  # may need to repeat twice to compare next-best kickers
        while repeat >= 0:
            best_kicker = 0
            for hand in winners:
                best_kicker_in_hand = 0  # need to find best kicker each time
                for rank, freq in hand.histogram.items():
                    if freq == 1 and rank > best_kicker_in_hand:
                        best_kicker_in_hand = rank
                if best_kicker_in_hand > best_kicker:
                    best_kicker = best_kicker_in_hand
            for hand in winners[:]:
                best_kicker_in_hand = 0
                for rank, freq in hand.histogram.items():
                    if freq == 1 and rank > best_kicker_in_hand:
                        best_kicker_in_hand = rank
                if best_kicker_in_hand < best_kicker:
                    winners.remove(hand)
                else:  # temporarily remove best kicker to compare next-best
                    del hand.histogram[best_kicker_in_hand]
            if len(winners) == 1:  # we're done
                repeat = -1
            else:
                repeat -= 1
    for hand in winners:  # refresh histograms
        hand.histogram = generate_histogram(hand.cards)  # refresh histograms
    return winners


def compare_high_cards(hands):
    winners = list(hands)
    index = 4  # start by comparing highest cards
    while index >= 0:
        top_card = 0
        for hand in winners[:]:
            if hand.cards[index].rank > top_card:
                top_card = hand.cards[index].rank
            elif hand.cards[index].rank == top_card:
                continue
            else:
                winners.remove(hand)
        if len(winners) == 1:  # we're done
            return winners
        else:
            index -= 1
    return winners
