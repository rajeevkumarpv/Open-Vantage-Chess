import chess

class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move_uci):
        """Attempts to make a move. Returns True if successful, False if illegal."""
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            else:
                return False
        except ValueError:
            return False

    def get_legal_moves(self):
        """Returns a list of legal moves in UCI format."""
        return [move.uci() for move in self.board.legal_moves]

    def is_game_over(self):
        return self.board.is_game_over()

    def get_fen(self):
        return self.board.fen()

    def undo_move(self):
        if len(self.board.move_stack) > 0:
            self.board.pop()
            return True
        return False

    def reset(self):
        self.board.reset()
