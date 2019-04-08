from random import shuffle
from sushipy.cards import SushiCard

class BaseDeck:
    def __len__(self):
        return len(self.deck)

    # TODO Probably superfluous?
    def __getitem__(self, position):
        return self.deck[position]

    def shuffle_deck(self):
        shuffle(self.deck)

    def deal(self, hands, num_cards=8):
        for _ in range(num_cards):
            for hand in hands:
                card = self.deck.pop()
                hand.take_card(card)

    def make_deck(self):
        pass


class MyFirstMealDeck(BaseDeck):
    def __init__(self):
        self.name = 'My First Meal'
        self.deck = self.make_deck()

    def make_deck(self):
        deck = []
        for _ in range(3):
            deck.append(SushiCard("Squid Nigiri"))
            deck.append(SushiCard("Maki Rolls", makival=3))
            deck.append(SushiCard("Wasabi"))
            deck.append(SushiCard("Tea"))

        for _ in range(4):
            deck.append(SushiCard("Egg Nigiri"))
            deck.append(SushiCard("Maki Rolls", makival=1))

        for _ in range(5):
            deck.append(SushiCard("Salmon Nigiri"))
            deck.append(SushiCard("Maki Rolls", makival=2))

        for _ in range(8):
            deck.append(SushiCard("Tempura"))
            deck.append(SushiCard("Sashimi"))
            deck.append(SushiCard("Miso Soup"))
        return deck
