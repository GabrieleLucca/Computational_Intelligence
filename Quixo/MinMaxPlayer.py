import random
from game import Game, Move, Player
from copy import deepcopy

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
