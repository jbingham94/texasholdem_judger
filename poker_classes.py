# Core Classes
# Note: I included str methods for debugging purposes.


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return str(self.rank) + ' of ' + self.suit


class Hand:
    def __init__(self, cards, strength):
        self.cards = cards
        self.strength = strength
        self.histogram = {}

    def __str__(self):
        ret = ', '.join(str(card) for card in self.cards)
        return ret + '; Strength: ' + str(self.strength)


class Player:
    def __init__(self, id_num, hand):
        self.id_num = id_num
        self.hand = hand

    def __str__(self):
        return 'Player ' + str(self.id_num) + ': ' + str(self.hand)
