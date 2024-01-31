import random
from game import Game, Move, Player
from copy import deepcopy
import numpy as np
import struct

class QlearningPlayer(Player):
    def __init__(self, player) -> None:
        super().__init__()
        self.q_table= {}
        self.player=player
        file = "Qtable_Player0.txt" if self.player==0 else "Qtable_Player1.txt"
        print("Charging Q_table...")
        with open(file, 'r') as f:
            for line in f:
                line = line.split(" ")
                self.q_table[(line[0], line[1])] = float(line[2])

    def get_q_table(self):
        return self.q_table

    def compact_string(self, matrix):
        matrix = matrix.flatten()
        compressed_data = struct.pack(f">{len(matrix)}b", *matrix)
              
        return compressed_data
    
    def compact_move(self,t):
        string=str(t[0][0])+str(t[0][1])+str(t[1].value)
        string = string.encode('utf-8')
        return string
    
    def decode_move(self,t):
        t = t.decode('utf-8')
        return (int(t[0]), int(t[1])), Move(int(t[2]))
    
    def get_q_value(self, state, action):
        if (state, action) not in self.q_table:
            self.q_table[(state, action)] = 0
        return self.q_table[(state, action)]
    
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        player = game.get_current_player()
        actions = game.possible_moves(player)
        state = game.get_board()
        state = self.compact_string(state)
        actions = [self.compact_move(action) for action in actions]
        q_values = np.array([self.get_q_value(state, action) for action in actions])
        maximum = np.max(q_values)
        return self.decode_move(actions[np.random.choice(np.where(q_values == maximum)[0])])