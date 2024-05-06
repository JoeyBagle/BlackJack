import unittest
from Main import Card, Deck, Hand, Player, Dealer, Game

class TestCard(unittest.TestCase):
    def test_card_value(self):
        card1 = Card('9', 'Spades')
        card2 = Card('3', 'Hearts')
        card3 = Card('K', 'Clubs')
        card4 = Card('A', 'Diamonds')
        
        self.assertEqual(card1.card_value(), 9)
        self.assertEqual(card2.card_value(), 3)
        self.assertEqual(card3.card_value(), 10)
        self.assertEqual(card4.card_value(), (1, 11))

class TestDeck(unittest.TestCase):
    def test_generate_deck(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deal_card(self):
        deck = Deck()
        card = deck.deal_card()
        self.assertIsInstance(card, Card)

class TestHand(unittest.TestCase):
    def test_value(self):
        hand = Hand()
        hand.cards = [Card('A', 'Spades'), Card('9', 'Hearts')]
        self.assertEqual(hand.value(), 20)

class TestPlayer(unittest.TestCase):
    def test_hit(self):
        player = Player()
        player.hit()
        self.assertEqual(len(player.hand.cards), 3)

    def test_stay(self):
        player = Player()
        player.stay()
        self.assertEqual(player.state, 'stay')

    def test_bid(self):
        player = Player(budget=100)
        bid_amount = player.bid(50)
        self.assertEqual(bid_amount, 50)
        self.assertEqual(player.budget, 50)

class TestDealer(unittest.TestCase):
    def test_dealer_strategy(self):
        dealer = Dealer()
        dealer.hand.cards = [Card('10', 'Spades'), Card('6', 'Hearts'), Card('5', 'Clubs')]
        dealer.dealer_strategy()
        self.assertEqual(dealer.state, 'stay')

class TestGame(unittest.TestCase):
    def test_check_win(self):
        game = Game()
        game.player.hand.cards = [Card('A', 'Spades'), Card('9', 'Hearts')]
        game.dealer.hand.cards = [Card('K', 'Clubs'), Card('6', 'Diamonds')]
        self.assertTrue(game.check_win())

if __name__ == '__main__':
    unittest.main()