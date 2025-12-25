import sys
import os
from src.game_logic import ChessGame
from src.gui import ChessGUI
from src.engine_wrapper import StockfishEngine

def main():
    # Try to find stockfish path
    # For now, we assume it's in the PATH or same directory
    # You can change this path to point to your stockfish executable
    stockfish_path = "stockfish" 
    
    # Check if a local stockfish executable exists
    potential_paths = [
        "stockfish/stockfish-windows-x86-64-avx2.exe",
        "stockfish.exe", 
        "stockfish_15_x64_avx2.exe",
        "stockfish_20011801_x64.exe",
        r"C:\stockfish\stockfish_14_x64_avx2.exe" # Example common path
    ]
    
    for path in potential_paths:
        if os.path.exists(path):
            stockfish_path = path
            break

    print(f"Using Stockfish path: {stockfish_path}")

    game = ChessGame()
    engine = StockfishEngine(stockfish_path)
    
    # Start engine
    if not engine.start():
        print("WARNING: Stockfish engine not found or failed to start.")
        print("Game will be Player vs Player (Hotseat).")
        engine = None

    gui = ChessGUI(game, engine)
    try:
        gui.main_loop()
    finally:
        if engine:
            engine.quit()

if __name__ == "__main__":
    main()
