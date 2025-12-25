from src.game_logic import ChessGame

def test_game():
    game = ChessGame()
    print("Initial FEN:", game.get_fen())
    
    # Test valid move (e2e4)
    if game.make_move("e2e4"):
        print("Move e2e4 successful")
    else:
        print("Move e2e4 failed")
        
    print("FEN after e2e4:", game.get_fen())
    
    # Test invalid move
    if not game.make_move("e2e5"): # e2e5 is illegal now (pawn at e4)
        print("Invalid move handled correctly")
    else:
        print("Invalid move failed to be rejected")
        
    # Undo
    game.undo_move()
    print("FEN after undo:", game.get_fen())
    
if __name__ == "__main__":
    test_game()
