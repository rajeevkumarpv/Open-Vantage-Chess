import chess
import chess.engine
import os

class StockfishEngine:
    def __init__(self, engine_path="stockfish"):
        self.engine_path = engine_path
        self.engine = None
        self.limit = chess.engine.Limit(time=0.1) # Fast move for GUI responsiveness

    def start(self):
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
            # Try to verify by pinging or setting option
            # self.engine.configure({"Threads": 2})
            print(f"Engine started: {self.engine_path}")
            return True
        except Exception as e:
            print(f"Failed to start engine: {e}")
            self.engine = None
            return False

    def get_best_move(self, board):
        if not self.engine:
            return None
        try:
            result = self.engine.play(board, self.limit)
            return result.move
        except Exception as e:
            print(f"Engine error: {e}")
            return None

    def quit(self):
        if self.engine:
            self.engine.quit()

