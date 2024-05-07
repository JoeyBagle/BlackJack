'''

Generate data for the Machine Learning
model to use for learning and testing.

'''

data_for_learning = [('Player Hand Value', 'Player State', 'Player Hand Soft', 'Dealer Up Card', 'Game Win')]

import Main
import numpy as np

def generate_data():
    for i in range(3000):
        game = Main.Game(100, 'random')
        game.run()
        data_for_learning.append((game.player.hand.value(), game.player.state, game.player.hand.soft, game.dealer.hand.cards[0].rank, game.check_win()))
    np.savetxt('DataForLearning.csv', [p for p in data_for_learning], delimiter=',', fmt='%s')