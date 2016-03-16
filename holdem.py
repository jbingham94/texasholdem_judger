import sys
import fileinput
from hand_utils import *
from helpers import *
from poker_dicts import *
from tiebreakers import *
from poker_classes import *


def run_game():
    players = process_game_input(fileinput.input())
    if players == 'Only one player':
        print '0'  # ID of lone player
        sys.exit(0)
    else:
        winning_strength = 0
        for player in players:
            player.hand = score_hand(player.hand.cards)
            if player.hand.strength > winning_strength:
                winning_strength = player.hand.strength
        winners = []
        for player in players:  # detect if we need to break a tie
            if player.hand.strength == winning_strength:
                winners.append(player)
        if len(winners) > 1:  # tiebreak
            winning_hands = []
            winning_strength = winners[0].hand.strength
            for winner in winners:
                winning_hands.append(winner.hand)
            winning_hands = break_tie(winning_hands, winning_strength)
            if len(winning_hands) > 1:  # if there's a split pot
                final_winners = []
                for winner in winners:
                    for hand in winning_hands:
                        if winner.hand == hand:
                            final_winners.append(winner)
                print ' '.join(str(winner.id_num) for winner in final_winners)
            else:
                winning_hand = winning_hands.pop()
                for winner in winners:
                    if winner.hand == winning_hand:
                        print str(winner.id_num)
        else:
            winner = winners.pop()
            print str(winner.id_num)

# Main method

if __name__ == '__main__':
    run_game()
