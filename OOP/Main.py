'''

Basic Blackjack program

Follows all rules as provided on Wikipedia

'''

from random import shuffle, randint
from typing import Literal, Union
import matplotlib.pyplot as plt
data = []



class Card():

    '''

    Creating the 'Card' class

    this is used simply to evaluate information about a singular card instead of an entire deck

    '''

    def __init__(self, rank: tuple , suit: tuple) -> str:
        self.rank = rank
        self.suit = suit


    def card_value(self) -> int:

        '''

        Evaluate the value of a card

        in blackjack if cards are any of the royals
        they are just a ten

        and if they are an Ace, they are either 1 or 11
        depending on if that would cause you to bust.
        which is checked for in the hand class

        '''

        # if the rank is is a king, queen, or jack, return 10 as the value of the card.
        if self.rank in ['J', 'Q', 'K']:
            return 10
        # if the rank is an ace return 1 and 11. This will later
        # let us choose whether we want the ace to be a one or eleven
        if self.rank == 'A':
            return 1, 11
        # if it's nothing special just return the number.
        return int(self.rank)


    def __str__(self):
        return f"{self.rank}-{self.suit}"


class Deck():

    '''

    Creating our deck class

    mostly, this will be used for drawing cards,
    setting up a deck so we don't just draw cards at random
    resulting in us having 2 aces of spades, which is illegal in blackjack.

    '''

    def __init__(self):
        # Create a deck, suit first then rank.
        # This makes the deck follow what a brand new pack of cards looks like.
        self.generate_deck()
        shuffle(self.cards)

    def generate_deck(self):
        ''' Initializes the deck '''
        self.cards = [Card(rank, suit) for suit in ('Spades', 'Hearts', 'Diamonds', 'Clubs') for rank in ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')]



    def deal_card(self) -> classmethod:

        '''

        simply deals a card by popping one
        from the first spot in the deck array

        '''

        # Check if there are no cards left in the deck
        if not self.cards:
            self.generate_deck()
        # As long as there are cards left in the deck, pop one from the top of the deck out.
        # return the drawn card so it can be added to the hand
        return self.cards.pop(0)


    def __str__(self):
        return f"{', '.join(map(str, self.cards))}"



class Hand:

    '''

    creating the 'Hand' class

    this is used simply to store each players hand
    give the value of the two hands
    show if either hand is soft
    and also to make it easier to draw cards

    '''


    def __init__(self, deck: classmethod):
        # start with two cards in hand.
        self.cards = []
        self.draw()
        self.draw()
        self.soft = any(c.rank == 'A' for c in self.cards)


    def value(self) -> int:

        '''

        The method 'Value', is used to check the value
        of the players hand, this will allow us to check
        to see if the player has busted, has an ace, or
        just has a regular old hand

        '''

        total = 0
        ace_count = 0

        # Calculate the total value of the hand
        for card in self.cards:
            if card.rank == 'A':
                ace_count += 1
            else:
                total += card.card_value()

        # Determine the value of aces
        for _ in range(ace_count):
            if total + 11 <= 21:
                total += 11
                self.soft = True
            else:
                total += 1

        return total


    def draw(self):

        '''

        draw method, simply exists to make it easier
        for a player to draw cards

        '''

        self.cards.append(Partecipant.deck.deal_card())



    def __str__(self):
        return str([str(c) for c in self.cards])


class Partecipant():

    deck = Deck()

    def __init__(self, budget: int, strategy: str, name: str):
        self.name, self.budget, self.strategy = name, budget, strategy

        self.hand = Hand(self.deck)

        self.state, self.broke = 'play', False
        self.bid_amount = 0
        self.starting_bid = 10
        self.current_simulated_bid = self.starting_bid

    # player action
    def hit(self):

        '''

        Makes the player draw a card, and makes sure the player state
        is set to 'play' so that the player can keep playing

        '''

        self.hand.draw()

        self.check_broke()

    def stay(self):

        '''

        Changes the player state to 'stay', which changes anything
        that runs based on the 'play' state and causes
        it to stop working.

        '''

        self.state = 'stay'



    #status ceck point
    def check_bust(self) -> bool:

        '''

        Check if the player busted by seeing if the hand
        value is above 21

        '''

        if self.hand.value() > 21:
            self.state = 'bust'
            return True
        return False


    def check_broke(self) -> bool:

        ''' check if the player is broke '''

        if self.budget < 1:
            self.state = 'broke'
            return True
        return False

    def bid(self, amount = 0) ->int :

        '''

        Get a bid from the player if the player is actually a player,
        otherwise automate the bid

        '''

        if self.strategy is None or amount == 0 :
            if self.check_broke():
                print('You are out of money and cannot bid anymore')
            else:
                self.bid_amount = int(input('How much?\n'))
                while self.bid_amount > self.budget:
                    self.bid_amount = int(input('How much?\n'))
                    print(f'You don\'t have that much. You have: ${self.budget}')
        else:
            self.bid_amount = amount

        self.budget -= amount
        return self.bid_amount




class Player(Partecipant):

    '''

    creating the 'Player' class

    this will have a multitude of select-able values
    a strategy, a name, and a budget
    this will all be managed by the player throughout the game
    whether it's a bot or a person.

    '''

    def __init__(self, budget: int = 100, strategy: str = None, name: str = 'Player'):
        super().__init__(budget, strategy, name)



    # strategies
    def strategy_player(self, strdealer_up_card: classmethod):

        '''

        A random very basic strategy, generated by chatGPT
        and implemented, by no means is it great. but
        it gets the job done for now.

        '''
        dealer_up_card = strdealer_up_card
        player_hand_value = self.hand.value()
        if self.strategy == "strategy_one":
            # Define the basic strategy decisions based
            # on the player's hand value and the dealer's up card
            if self.hand.soft:
                if player_hand_value <= 17:
                    self.hit()
                elif player_hand_value == 18 and dealer_up_card.rank in [9, 10, 'J', 'Q', 'K', 'A']:
                    self.hit()
                else:
                    self.stay()
            else:
                if player_hand_value <= 11:
                    self.hit()
                elif player_hand_value == 12:
                    if dealer_up_card.rank in [2, 3, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']:
                        self.hit()
                    else:
                        self.stay()
                elif 13 <= player_hand_value <= 16:
                    if dealer_up_card.rank in [2, 3, 4, 5, 6]:
                        self.stay()
                    else:
                        self.hit()
                else:
                    self.stay()

        elif self.strategy == "strategy_one":

        # A completely random strategy to test the game

          if self.state == 'play' and randint((True, False)):
              self.hit()
          else:
              self.stay()


    def __str__(self):
        return f"Name: {str(self.name)}; Budget: {str(self.budget)};\nHand: {str(self.hand)};\nHand Value: {str(self.hand.value())}\n"



class Dealer(Partecipant):

    '''

    A dealer is another player where
    his strategy is automatic

    '''

    # initialize the dealer as a player
    def __init__(self):
        super().__init__(float('inf'), 'dealer', 'Dealer')

    def dealer_strategy(self):

        '''

        the dealers strategy is always:
        hit below 17 and on soft 17
        stay on hard 17 or above 17

        '''

        if self.hand.value() < 17 or (
            self.hand.value() == 17 and self.hand.soft):
            self.hit()
        else:
            self.stay()

    def __str__(self):
        return f"Name: {self.name}; up_card: [{str(self.hand.cards[0])}]\n"



class Game():

    game_count = 0

    '''

    Create the 'Game' class

    This will be used to create and run the game as well as
    log it within a variable which we have set to 'data'


    '''

    

    def __init__(self,  budget: int =100, strategy: Union[None, Literal['strategy_one', 'random']] = None , name: str ='Player'):

        self.dealer = Dealer()
        self.player = Player(budget, strategy, name)
        self.pot = 0
        self.simulated = False
        self.game_count += 1


    def log_game(self):

        '''

        as mentioned above,
        the game class is in charge
        of logging the game.
        which is what this method does

        '''

        data.append((Game.game_count, self.player.budget))


    def player_turn(self):

        ''' player's turn function '''
        if self.player.strategy == 'random':
            self.pot += self.player.bid(10)

        if self.player.strategy is None:

            self.player.budget -= 10
            self.pot += 10
            option = ('1', 'HIT', '2', 'STAY','3', 'BID')
            question = "What would you like to do? \n1) Hit \n2) Stay \n3) Bid\n"
            player_move = input(question).upper()
            while player_move not in option:
                print('Not a valid move')
                player_move = input(question).upper()

            # execute that move
            if player_move in option[:2]:
                self.player.hit()
            elif player_move in option[2:4]:
                self.player.stay()
            elif player_move in option[4:]:
                self.pot += self.player.bid()

            print(f"Hand: {self.player.hand}")
            print(f"Hand Value: {self.player.hand.value()} \n")

            # Check if the player busted
            if self.player.check_bust():
                print('Sorry, you busted.')


        # get the move that the player wants to do
        elif self.player.strategy == 'strategy_one':
            self.player.strategy_player(self.dealer.hand.cards[0])

            self.player.check_bust()

            # in this version we are using the 2 - 1 - 2 bidding strategy
            # which increments by 1 every win, then resets to 1 at a loss

            self.pot += self.player.bid(self.player.current_simulated_bid)
        else:
            self.player.strategy_random()
            self.player.check_bust()


    def check_win(self) -> bool:

        '''

        Check if the player has won the round
        this will be if the hand value is higher
        than the dealers
        and the hand has not busted
        or if the dealer has busted
        and the player hasn't

        '''

        if  self.player.state != 'bust' and (self.player.hand.value() > self.dealer.hand.value() or self.dealer.state == 'bust'):
            self.player.budget += self.pot
            return True
        return False



    def change_bid(self):

        '''

        change the amount of the
        simulated bid depending on win/loss

        '''

        if self.check_win():
            self.player.current_simulated_bid += self.player.starting_bid
            self.player.budget += self.pot
        else:
            self.player.current_simulated_bid = self.player.starting_bid


    def run(self):

        '''

        this function actually runs the game,
        letting the player make their moves first
        then the dealer making theirs.

        '''

        self.pot = 0
        self.player.state = 'play'

        if self.player.strategy is None:
            print('Buy in is 10 bucks.')
            print(self.dealer)
            print(self.player)


        # while the player and is not staying, busted or out of budget
        while 'play' in (self.player.state, self.dealer.state):
            if self.player.state == 'play':
                self.player_turn()
            if self.dealer.state == 'play':
                self.dealer.dealer_strategy()

        # add the dealers bet to the pot, which will always be equal to the pot.
        self.pot += self.dealer.bid(self.pot)

        # Check bust for both
        self.dealer.check_bust()
        self.player.check_bust()

        # Check win and lost
        if self.player.strategy is None:
            if self.check_win():
                print('You won this round.')
            else:
                print('You lost this round.')
        elif self.player.strategy == "strategy_one":
            self.change_bid()
        else:
            self.check_win()

        self.log_game()
        # print(data[-1])
        return self.player.budget


#    <------------- TESTS ------------->

class Test():

    def card_test():
        ''' manually create 4 cards to make sure all the special things work '''
        card1 = Card('9', 'Spades')
        card2 = Card('3', 'Hearts')
        card3 = Card('K', 'Clubs')
        card4 = Card('A', 'Diamonds')
        print(card1, card2, card3, card4)


    def deck_test():
        '''

        create a deck, display the deck to test the str
        then shuffle and re-display to test the shuffle method

        '''
        deck = Deck()
        deck.generate_deck()
        print('<----------- Before Shuffle ----------->')
        print(deck)
        deck = Deck()
        print('<----------- After Shuffle ----------->')
        print(deck)


    def hand_test():
        ''' make a new hand and print it and its value. '''

        deck = Deck()
        hand = Hand(deck)
        print(hand)
        print(hand.value())
        print(hand.soft)


    def player_test():
        ''' make sure the player class and each of there moves are working. '''
        player1 = Player(200, None, 'Andrea')
        player2 = Player(100)
        player3 = Player(100, None, 'Rob')
        player4 = Player(300, None, 'Tara')
        print(player1, '\n' + str(player2), '\n' + str(player3), '\n' + str(player4))
        player4.hit()
        print(player4)


    def dealer_test():

        ''' simply test a dealer by creating and printing '''

        dealer = Dealer()
        print(dealer)
        while dealer.state not in ['stay', 'bust']:
            dealer.dealer_strategy()
            print(dealer.state, [ str(card) for card in dealer.hand.cards], dealer.hand.value())


    def simulate_game():

        ''' Run a game, based on the provided strategy. '''
        next_game_budget = 0
        number_of_games = 0
        print('<--------------------------------------- GAME --------------------------------------->')
        while next_game_budget <= 0:
            next_game_budget = int(input("How much money? \n"))
        while number_of_games <= 0:
            number_of_games = int(input("How many games would you like to simulate? \n"))
        for _ in range(number_of_games):
            game = Game(next_game_budget, "strategy_one")
            next_game_budget = game.run()


        # <--- Pyplot stuff --->
        # plt.pcolor(250,250,250)
        plt.plot(range(number_of_games), data)
        plt.grid(True)
        plt.title("Simulated game")
        plt.tight_layout()
        plt.xlabel('Games')
        plt.ylabel('Money')
        plt.show()

    def play_game():

        ''' Run a game, with the player playing '''
        money = 1000
        continue_playing = 'Y'
        print('<--------------------------------------- GAME --------------------------------------->')
        while continue_playing not in ['N', 'NO']:
            game = Game(money, None)
            money = game.run()
            continue_playing = input('Want to keep playing? Y/N\n').upper()




def run():

    ''' Run the program '''

    done = False
    while not done:
        which = input('\nWhat would you like to run?\n 1) Test Card\n 2) Test Deck'+
            '\n 3) Test Player\n 4) Test Dealer\n 5) Simulate Game\n 6) Play Game\n 7) End \n').upper()
        if which in ['1', 'TEST CARD', 'CARD']:
            Test.card_test()
        elif which in ['2', 'TEST DECK', 'DECK']:
            Test.deck_test()
        elif which in ['3', 'TEST PLAYER', 'PLAYER']:
            Test.player_test()
        elif which in ['4', 'TEST DEALER', 'DEALER']:
            Test.dealer_test()
        elif which in ['5', 'SIMULATE']:
            Test.simulate_game()
            done = True
        elif which in ['6', 'PLAY GAME', 'PLAY']:
            Test.play_game()
        elif which in ['7', 'END']:
            done = True
            exit()
        else:
            print('Invalid input.')


if __name__ == "__main__":
    run()
