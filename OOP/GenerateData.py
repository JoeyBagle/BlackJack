'''

Generate data for the Machine Learning
model to use for learning and testing.

'''

data_for_learning = [('Player_Hand_Value', 'Player_State', 'Player_Hand_Soft', 'Dealer_Up_Card', 'Game_Win')]

import Main
import numpy as np

def generate_data():
    for i in range(30000):
        game = Main.Game(100, 'strategy_one')
        winLoss = game.run()
        data_for_learning.append((game.player.hand.value(), game.player.state, game.player.hand.soft, game.dealer.hand.cards[0].rank, winLoss > 100))
    np.savetxt('DataForLearning.csv', [p for p in data_for_learning], delimiter=',', fmt='%s')

generate_data()
