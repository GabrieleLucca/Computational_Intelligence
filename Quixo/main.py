import random
from MinMaxPlayer import MinMaxPlayer
from RandomPlayer import RandomPlayer
from QPlayer import QlearningPlayer
from game import Game 
from copy import deepcopy
from tqdm import tqdm

"""
    This file contains all the requirements that the final project requires. I have also created a Jupyter Notebook
    that is easier to manage, so I encourage to visit that instead.
"""

def test():
    players_0 =  [QlearningPlayer(0), MinMaxPlayer(0)]
    players_1 =  [QlearningPlayer(1), MinMaxPlayer(1)]

    names= ["Q-Learning", "MinMax"] 

    for player_0 in range(len(players_0)):
        for player_1 in range(len(players_1)):
            if player_0 != player_1:
                g = Game()
                g.play(players_0[player_0], players_1[player_1])
                check = g.check_winner()
                if check == 0:
                    print("Player 0:", names[player_0], "won against player 1:", names[player_1])
                elif check == 1:
                    print("Player 1:", names[player_1], "won against player 0:", names[player_1])
                else:
                    print("Player 0:", names[player_0], "and player 1:", names[player_1], "tied")

    for player_0 in range(len(players_0)):
        win = 0
        loss = 0
        tie = 0
        for _ in tqdm(range(1000)):
            
            g = Game()
            g.play(players_0[player_0], RandomPlayer())
            check = g.check_winner()
            if check == 0:
                win += 1
            elif check == 1:
                loss += 1
            else:
                tie += 1
        print("Player 0:", names[player_0], "Vs Player 1:", "Random", "\nWin:", win, "Loss:", loss, "Tie:", tie)  
    

    for player_1 in range(len(players_1)):
        win = 0
        loss = 0
        tie = 0
        for _ in tqdm(range(1000)):
            
            g = Game()
            g.play(RandomPlayer(), players_1[player_1])
            check = g.check_winner()
            if check == 1:
                win += 1
            elif check == 0:
                loss += 1
            else:
                tie += 1
        print("Player 0:", "Random", "Vs Player 1:", names[player_1], "\nWin:", win, "Loss:", loss, "Tie:", tie) 
        
if __name__ == '__main__':
    test()