from poker_classes import *
from poker_dicts import *

# Helper/Setup Functions


def process_game_input(input_str):
    '''
    Generates key game information/data structures based on input.
    '''
    line_track = 1
    comm_cards = []
    player_list = []
    for line in input_str:
        if line_track == 1:  # don't care about # of players unless 1
            if int(line) == 1:
                return 'Only one player'
            else:
                line_track = line_track + 1
                continue
        elif line_track == 2:  # process the community cards
            raw_comm_cards = line.split()
            for card in raw_comm_cards:
                rank = convert_rank(card[0])
                suit = card[1]
                new_card = Card(rank, suit)
                comm_cards.append(new_card)
            line_track = line_track + 1
        else:  # process the players
            player_info = line.split()
            is_id = True
            player_hand = Hand([], 0)
            player = Player(0, player_hand)
            for entry in player_info:
                if is_id:
                    player.id_num = int(entry)
                    is_id = False
                else:
                    card_rank = convert_rank(entry[0])
                    card_suit = entry[1]
                    new_card = Card(card_rank, card_suit)
                    player.hand.cards.append(new_card)
            for card in comm_cards:
                player.hand.cards.append(card)
            player_list.append(player)
    return player_list


def convert_rank(rank):
    if rank in rank_equivs:
        return rank_equivs.get(rank)
    else:
        return int(rank)


def generate_histogram(hand):
    histogram = {}
    for card in hand:
        if card.rank not in histogram:
            histogram.update({
                card.rank: 1
            })
        else:
            histogram[card.rank] += 1
    return histogram
