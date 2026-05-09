from game.board import Board
from game.rules import check_winner, is_draw
import copy


class GameState:
    def __init__(self):
        # initialize game
        self.board = Board()
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.move_history = []

    def reset(self):
        # restart the game
        self.__init__()

    def switch_turn(self):
        # toggle between player 1 and 2
        self.current_player = 2 if self.current_player == 1 else 1

    def is_valid_move(self, col):
        return self.board.is_valid_column(col)

    def get_valid_moves(self):
        return self.board.get_valid_moves()

    def make_move(self, col):
        # can't play if game ended
        if self.game_over:
            return False

        # invalid column
        if not self.is_valid_move(col):
            return False

        # place piece
        self.board.drop_piece(col, self.current_player)

        # save move
        self.move_history.append((self.current_player, col))

        # check game status
        self.update_status()

        # switch turn only if game continues
        if not self.game_over:
            self.switch_turn()

        return True

    def update_status(self):
        # check win
        if check_winner(self.board, self.current_player):
            self.game_over = True
            self.winner = self.current_player
            return

        # check draw
        if is_draw(self.board):
            self.game_over = True
            self.winner = None

    def clone(self):
        return copy.deepcopy(self) 