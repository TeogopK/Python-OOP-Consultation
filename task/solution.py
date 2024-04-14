import random


class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def get_suit(self):
        return self.suit

    def get_face(self):
        return self.face


class Deck:
    SUITES = ['clubs', 'diamonds', 'hearts', 'spades']
    FACES = ['2', '3', '4', '5', '6', '7',
             '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, face_filter=None):
        faces_to_get = self.FACES if not face_filter else face_filter
        self.cards = [Card(suit, face)
                      for face in faces_to_get for suit in self.SUITES]

    def cut(self):
        index = random.randint(1, len(self.cards))
        self.cards = self.cards[index:] + self.cards[:index]

    def shuffle(self):
        random.shuffle(self.cards)

    def get_cards(self):
        return self.cards

    def deal_cards(self, count):
        cards_to_throw = self.cards[:count]
        self.cards = self.cards[count:]
        return cards_to_throw

    def add_cards(self, cards_to_add):
        self.cards.extend(cards_to_add)


class Player():
    def __init__(self):
        self.cards = []

    def get_cards(self):
        return self.cards

    def add_cards(self, cards_to_add):
        self.cards.extend(cards_to_add)

    def throw_cards(self):
        cards_to_throw = self.cards
        self.cards = []
        return cards_to_throw


class Game():
    def __init__(self, number_of_players, dealing_direction, dealing_instructions):
        self.number_of_players = number_of_players
        self.dealing_direction = dealing_direction
        self.dealing_instructions = dealing_instructions

        self.players = [Player() for _ in range(number_of_players)]
        self.deck = Deck()

    def get_players(self):
        return self.players

    def prepare_deck(self):
        for player in self.players:
            returned_cards = player.throw_cards()
            self.deck.add_cards(returned_cards)

        self.deck.shuffle()
        self.deck.cut()

    def deal(self, player):
        player_order_step = 1 if self.dealing_direction == 'ltr' else -1
        ordered_players = self.players[::player_order_step]
        index = ordered_players.index(player)
        players_final = ordered_players[index:] + ordered_players[:index]

        for deal_instruction in self.dealing_instructions:
            for player in players_final:
                dealed_cards = self.deck.deal_cards(deal_instruction)
                player.add_cards(dealed_cards)

    def get_deck(self):
        return self.deck


class Belot(Game):
    def __init__(self):
        super().__init__(4, 'ltr', (2, 3, 3))
        self.deck = Deck(face_filter=('7', '8', '9', '10',
                                       'J', 'Q', 'K', 'A'))


class Poker(Game):
    def __init__(self):
        super().__init__(9, 'rtl', (1, 1, 1, 1, 1))


def main():
    belot = Belot()
    players = belot.get_players()
    belot.prepare_deck()
    belot.deal(players[0])
    belot.prepare_deck()
    belot.deal(players[1])


if __name__ == '__main__':
    main()
