import random
from game import Game, Move, Player

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos, move=random.choice(game.possible_moves(game.get_current_player()))
        return from_pos, move
    