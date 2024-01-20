import random
from game import Game, Move, Player
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import struct

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos, move=random.choice(game.possible_moves(game.get_current_player()))
        return from_pos, move
    

class QlearningPlayer(Player):
    def __init__(self, player) -> None:
        super().__init__()
        self.q_table= {}
        self.player=player
        file = "Quixo\\Q_table_0.txt" if self.player==0 else "Quixo\\Q_table_1.txt"
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
            

class MinMaxPlayer(Player):
    def __init__(self, player: int) -> None:
        super().__init__()
        self.player = player
        self.DEPTH = 4

    def evaluate(self, game: 'Game') -> int:
        evaluation = 0
        if game.check_winner() == 0:
            evaluation= 1000
        elif game.check_winner() == 1:
            evaluation = -1000
        else:
            board = game.get_board()
            number_of_player_0 = 0
            number_of_player_1 = 0
            for i in range(5):
                for j in range(5):
                    if board[i][j] == 0:
                        number_of_player_0 += 1
                    elif board[i][j] == 1:
                        number_of_player_1 += 1
            evaluation = number_of_player_0 - number_of_player_1

            number_of_4_player_0= 0
            number_of_4_player_1= 0
            row_player_0 = [0, 0, 0, 0, 0]
            row_player_1 = [0, 0, 0, 0, 0]
            column_player_0 = [0, 0, 0, 0, 0]
            column_player_1 = [0, 0, 0, 0, 0]
            diag_player_1=0
            diag_player_0=0
            anti_diag_player_0=0
            anti_diag_player_1=0
            for i in range(5):
                for j in range(5):
                    if board[i][j] == 0:
                        row_player_0[i] += 1
                        column_player_0[j] += 1
                    elif board[i][j] == 1:
                        row_player_1[i] += 1
                        column_player_1[j] += 1

                    if i==j:
                        if board[i][j] == 0:
                            diag_player_0 += 1
                        elif board[i][j] == 1:
                            diag_player_1 += 1
                    
                    if i+j==4:
                        if board[i][j] == 0:
                            anti_diag_player_0 += 1
                        elif board[i][j] == 1:
                            anti_diag_player_1 += 1

            for i in range(5):
                if row_player_0[i] == 4:
                    number_of_4_player_0 += 1
                elif row_player_1[i] == 4:
                    number_of_4_player_1 += 1
                if column_player_0[i] == 4:
                    number_of_4_player_0 += 1
                elif column_player_1[i] == 4:
                    number_of_4_player_1 += 1
            
            if diag_player_0 == 4:
                number_of_4_player_0 += 1
            elif diag_player_1 == 4:
                number_of_4_player_1 += 1
            
            if anti_diag_player_0 == 4:
                number_of_4_player_0 += 1
            elif anti_diag_player_1 == 4:
                number_of_4_player_1 += 1

            evaluation += 3* (number_of_4_player_0 - number_of_4_player_1)
        return evaluation if self.player == 0 else -evaluation
        
    def max(self, game: 'Game', depth: int, alpha: int, beta: int):
        if depth == 0 or game.check_winner() != -1:
            return self.evaluate(game)
        max_value = -10000

        for move in game.possible_moves(game.get_current_player()):
            game_copy = deepcopy(game)
            game_copy.move(move[0], move[1], game_copy.get_current_player())
            minimum = self.min(game_copy, depth - 1, alpha, beta)
            if max_value < minimum:
                best_move= (move[0],move[1])
                max_value = minimum
            
            if max_value >= beta:
                break

            if max_value > alpha:
                alpha = max_value
        
        if depth == self.DEPTH:
            return best_move

        return max_value
    
    def min(self, game: 'Game', depth: int, alpha: int, beta: int) -> int:
        if depth == 0 or game.check_winner() != -1:
            return self.evaluate(game)
        min_value = 10000

        for move in game.possible_moves(game.get_current_player()):
            game_copy = deepcopy(game)
            game_copy.move(move[0], move[1],  game_copy.get_current_player())
            min_value = min(min_value, self.max(game_copy, depth - 1, alpha, beta))

            if min_value <= alpha:
                break   

            if min_value < beta:
                beta = min_value

        return min_value

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos, move = self.max(game, self.DEPTH, -10000, 10000)
        return from_pos, move


class MinMaxPlayerGA(Player):
    def __init__(self, player: int) -> None:
        super().__init__()
        self.player = player
        self.DEPTH= 4

    def evaluate(self, game: 'Game') -> int:
        evaluation = 0
        if game.check_winner() == 0:
            evaluation= 1000
        elif game.check_winner() == 1:
            evaluation = -1000
        else:
            board = game.get_board()
            number_of_player_0 = 0
            number_of_player_1 = 0
            for i in range(5):
                for j in range(5):
                    if board[i][j] == 0:
                        number_of_player_0 += 1
                    elif board[i][j] == 1:
                        number_of_player_1 += 1
            evaluation = 13.29*(number_of_player_0 - number_of_player_1)

            number_of_4_player_0= 0
            number_of_4_player_1= 0
            row_player_0 = [0, 0, 0, 0, 0]
            row_player_1 = [0, 0, 0, 0, 0]
            column_player_0 = [0, 0, 0, 0, 0]
            column_player_1 = [0, 0, 0, 0, 0]
            diag_player_1=0
            diag_player_0=0
            anti_diag_player_0=0
            anti_diag_player_1=0
            for i in range(5):
                for j in range(5):
                    if board[i][j] == 0:
                        row_player_0[i] += 1
                        column_player_0[j] += 1
                    elif board[i][j] == 1:
                        row_player_1[i] += 1
                        column_player_1[j] += 1

                    if i==j:
                        if board[i][j] == 0:
                            diag_player_0 += 1
                        elif board[i][j] == 1:
                            diag_player_1 += 1
                    
                    if i+j==4:
                        if board[i][j] == 0:
                            anti_diag_player_0 += 1
                        elif board[i][j] == 1:
                            anti_diag_player_1 += 1

            number_of_3_player_0=0
            number_of_3_player_1=0

            for i in range(5):
                if row_player_0[i] == 4:
                    number_of_4_player_0 += 1
                elif row_player_1[i] == 4:
                    number_of_4_player_1 += 1
                if column_player_0[i] == 4:
                    number_of_4_player_0 += 1
                elif column_player_1[i] == 4:
                    number_of_4_player_1 += 1
            
            if diag_player_0 == 4:
                number_of_4_player_0 += 1
            elif diag_player_1 == 4:
                number_of_4_player_1 += 1
            
            if anti_diag_player_0 == 4:
                number_of_4_player_0 += 1
            elif anti_diag_player_1 == 4:
                number_of_4_player_1 += 1

            for i in range(5):
                if row_player_0[i] == 3:
                    number_of_3_player_0 += 1
                elif row_player_1[i] == 3:
                    number_of_3_player_1 += 1
                if column_player_0[i] == 3:
                    number_of_3_player_0 += 1
                elif column_player_1[i] == 3:
                    number_of_3_player_1 += 1
            
            if diag_player_0 == 3:
                number_of_3_player_0 += 1
            elif diag_player_1 == 3:
                number_of_3_player_1 += 1
            
            if anti_diag_player_0 == 3:
                number_of_3_player_0 += 1
            elif anti_diag_player_1 == 3:
                number_of_3_player_1 += 1

            evaluation += 3.98* (number_of_4_player_0 - number_of_4_player_1) + 0.58*(number_of_3_player_0 - number_of_3_player_1)
        return evaluation if self.player == 0 else -evaluation
        
    def max(self, game: 'Game', depth: int, alpha: int, beta: int):
        if depth == 0 or game.check_winner() != -1:
            return self.evaluate(game)
        max_value = -10000

        for move in game.possible_moves(game.get_current_player()):
            game_copy = deepcopy(game)
            game_copy.move(move[0], move[1], game_copy.get_current_player())
            minimum = self.min(game_copy, depth - 1, alpha, beta)
            if max_value < minimum:
                best_move= (move[0],move[1])
                max_value = minimum
            
            if max_value >= beta:
                break

            if max_value > alpha:
                alpha = max_value
        
        if depth == self.DEPTH:
            return best_move

        return max_value
    
    def min(self, game: 'Game', depth: int, alpha: int, beta: int) -> int:
        if depth == 0 or game.check_winner() != -1:
            return self.evaluate(game)
        min_value = 10000

        for move in game.possible_moves(game.get_current_player()):
            game_copy = deepcopy(game)
            game_copy.move(move[0], move[1],  game_copy.get_current_player())
            min_value = min(min_value, self.max(game_copy, depth - 1, alpha, beta))

            if min_value <= alpha:
                break   

            if min_value < beta:
                beta = min_value

        return min_value

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos, move = self.max(game, self.DEPTH, -10000, 10000)
        return from_pos, move



def test():
    players_0 =  [RandomPlayer(0), QlearningPlayer(0),MinMaxPlayer(0), MinMaxPlayerGA(0)]
    players_1 =  [RandomPlayer(1), QlearningPlayer(1),MinMaxPlayer(1), MinMaxPlayerGA(1)] 

    names= ["RandomPlayer", "Qlearning","MinMax", "MinMaxGA"] 

    for player_0 in range(len(players_0)):
        for player_1 in range(len(players_1)):
            if player_0 != player_1:
                win = 0
                loss = 0
                tie = 0
                g = Game()
                g.play(players_0[player_0], players_1[player_1])
                check = g.check_winner()
                if check == 0:
                    win += 1
                elif check == 1:
                    loss += 1
                else:
                    tie += 1
                print("Player 0:", names[player_0], "Vs Player 1:", names[player_1], "Win:", win, "Loss:", loss, "Tie:", tie)  

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
        print("Player 0:", names[player_0], "Vs Player 1:", "Random", "Win:", win, "Loss:", loss, "Tie:", tie)  
    

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
        print("Player 0:", "Random", "Vs Player 1:", names[player_1], "Win:", win, "Loss:", loss, "Tie:", tie) 
        
if __name__ == '__main__':
    test()