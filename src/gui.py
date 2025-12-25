import pygame
import chess
from src.game_logic import ChessGame

# Constants
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8
OFFSET_X = (WIDTH - BOARD_SIZE) // 2
OFFSET_Y = (HEIGHT - BOARD_SIZE) // 2
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
TEXT_COLOR = (0, 0, 0)

class ChessGUI:
    def __init__(self, game, engine=None):
        self.game = game
        self.engine = engine
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Python Chess")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("segoeuisymbol", 50) # Use a font with chess symbols
        self.selected_square = None
        self.running = True
        self.player_color = chess.WHITE # Player starts as White
        
        # Feature Toggles
        self.show_lines = False
        self.show_heat = False
        
        # UI Elements
        self.ui_font = pygame.font.SysFont("Arial", 20)
        self.chk_lines_rect = pygame.Rect(20, 20, 150, 30)
        self.chk_heat_rect = pygame.Rect(180, 20, 150, 30)
        
        # History
        self.redo_stack = []

        # Audio
        self.move_sound = self.generate_move_sound()
    
    def undo_move(self):
        # Go back in history
        if self.game.board.move_stack:
            move = self.game.board.pop()
            self.redo_stack.append(move)
            
            # If we are in engine mode (and stack was empty), pop again to skip engine move?
            # User wants to review "forward backward", so 1 step at a time is more precise.
            # We just need to make sure engine DOES NOT think while we are in history.
            
    def redo_move(self):
        # Go forward in history
        if self.redo_stack:
            move = self.redo_stack.pop()
            self.game.board.push(move)
            self.play_move_sound()
    
    def generate_move_sound(self):
        # Generate a simple synthetic click sound
        # 44100Hz, 16bit, 2 channels
        # A short decay noise or sine wave
        sound_length = 2000 # samples
        sampling_rate = 44100
        buffer = []
        import math
        import array
        
        # Simple click/thud: fast decay sine wave
        for i in range(sound_length):
            t = float(i) / sampling_rate
            # 200Hz frequency with expo decay
            val = 32000 * math.sin(2.0 * math.pi * 200.0 * t) * math.exp(-15.0 * t)
            val = int(val)
            # Stereo
            buffer.append(val)
            buffer.append(val)
        
        # Convert to bytes for pygame mixer
        sound_array = array.array('h', buffer)
        try:
            return pygame.mixer.Sound(buffer=sound_array)
        except Exception as e:
            print(f"Audio init failed: {e}")
            return None

    def play_move_sound(self):
        if self.move_sound:
            self.move_sound.play()

    def draw_board(self):
        self.screen.fill((30, 30, 30)) # Clear screen
        
        # Explicit colors to ensure they aren't lost
        color_white = (240, 217, 181)
        color_black = (181, 136, 99)
        color_highlight = (186, 202, 68)
        color_last_move = (205, 210, 106)

        for row in range(8):
            for col in range(8):
                # Calculate correct square index
                # Visual row 0 is rank 7, row 7 is rank 0
                rank = 7 - row
                square_idx = chess.square(col, rank)
                
                # Draw Base Square
                is_light_square = (row + col) % 2 == 0
                bg_color = color_white if is_light_square else color_black
                
                x = OFFSET_X + col * SQUARE_SIZE
                y = OFFSET_Y + row * SQUARE_SIZE
                rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
                
                pygame.draw.rect(self.screen, bg_color, rect)

                # Overlays (Highlight/Last Move)
                # Draw these directly on top if needed
                if self.selected_square == (col, rank):
                    # Highlight selected
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    s.set_alpha(180)
                    s.fill(color_highlight)
                    self.screen.blit(s, (x, y))
                elif self.game.board.move_stack:
                    last_move = self.game.board.peek()
                    if square_idx == last_move.from_square or square_idx == last_move.to_square:
                        # Highlight last move
                        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                        s.set_alpha(180)
                        s.fill(color_last_move)
                        self.screen.blit(s, (x, y))

    def draw_pieces(self):
        board = self.game.board
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square) 
                
                symbol = piece.unicode_symbol()
                
                # Determine piece color
                if piece.color == chess.WHITE:
                    text_color = (255, 255, 255) # White
                    # Optional: Add a black outline for visibility on white squares
                    # For simple text rendering, we can render slightly larger black text behind
                    outline_color = (0, 0, 0)
                else:
                    text_color = (0, 0, 0) # Black
                    outline_color = (255, 255, 255) # White outline for contrast (optional, mostly for black on black)

                center_x = OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2

                # Draw Outline (Simple shadow/stroke effect)
                for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 2)]: # Shadow/Stroke
                    outline_surface = self.font.render(symbol, True, outline_color)
                    outline_rect = outline_surface.get_rect(center=(center_x + dx, center_y + dy))
                    self.screen.blit(outline_surface, outline_rect)

                # Draw Main Piece
                text_surface = self.font.render(symbol, True, text_color)
                text_rect = text_surface.get_rect(center=(center_x, center_y))
                self.screen.blit(text_surface, text_rect)

    def get_square_under_mouse(self, pos):
        x, y = pos
        if OFFSET_X <= x < OFFSET_X + BOARD_SIZE and OFFSET_Y <= y < OFFSET_Y + BOARD_SIZE:
            col = (x - OFFSET_X) // SQUARE_SIZE
            row = (y - OFFSET_Y) // SQUARE_SIZE
            return col, 7 - row
        return None

    def main_loop(self):
        while self.running:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.undo_move()
                    elif event.key == pygame.K_RIGHT:
                        self.redo_move()

            # Engine Move Logic
            # Only run engine if we are at the LIVE game tip (redo_stack empty)
            if self.engine and not self.redo_stack and not self.game.is_game_over() and self.game.board.turn != self.player_color:
                # Let user see the player's move before engine blocks
                # We can do this by handling the engine move AFTER a draw cycle
                # But since we are simple:
                
                # Draw current state (Player just moved)
                self.draw_game()
                pygame.display.flip()
                
                # Yield to OS/Pump events
                pygame.event.pump()
                
                # Get engine move
                best_move = self.engine.get_best_move(self.game.board)
                if best_move:
                    self.game.board.push(best_move)
                    self.play_move_sound() # Sound
                else:
                    print("Engine failed to return move.")
                
            # Standard Draw
            self.draw_game()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_click(self, pos):
        # UI Clicks
        if self.chk_lines_rect.collidepoint(pos):
             self.show_lines = not self.show_lines
             return
        if self.chk_heat_rect.collidepoint(pos):
             self.show_heat = not self.show_heat
             return
             
        # New Game Button Check (only if game is over)
        if self.game.is_game_over():
            if hasattr(self, 'new_game_rect') and self.new_game_rect.collidepoint(pos):
                self.reset_game()
                return

        square = self.get_square_under_mouse(pos)
        if square:
            col, rank = square
            sq_idx = chess.square(col, rank)
            
            if self.selected_square:
                prev_col, prev_rank = self.selected_square
                prev_sq = chess.square(prev_col, prev_rank)
                move = chess.Move(prev_sq, sq_idx)
                
                # Auto-promote to Queen
                if chess.Move(prev_sq, sq_idx, promotion=chess.QUEEN) in self.game.board.legal_moves:
                    move.promotion = chess.QUEEN

                if move in self.game.board.legal_moves:
                    self.game.board.push(move)
                    self.play_move_sound() # Sound
                    self.selected_square = None
                    self.redo_stack.clear() # Clear future history on new branch
                else:
                    if self.game.board.piece_at(sq_idx) and self.game.board.piece_at(sq_idx).color == self.game.board.turn:
                        self.selected_square = square
                    else:
                        self.selected_square = None
            else:
                if self.game.board.piece_at(sq_idx) and self.game.board.piece_at(sq_idx).color == self.game.board.turn:
                    self.selected_square = square

    def draw_overlays(self):
        # 1. Heatmap (Colored Transparent Overlays)
        if self.show_heat:
            # Reuse surface
            if not hasattr(self, 'heat_surface'):
                 self.heat_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))

            # Calculate attack counts for White and Black separately
            white_attacks = [0] * 64
            black_attacks = [0] * 64
            
            for sq in chess.SQUARES:
                piece = self.game.board.piece_at(sq)
                if piece:
                    attacks = self.game.board.attacks(sq)
                    target_list = attacks # Bitboard to list iteration happens implicity or we iterate
                    # Actually board.attacks returns a Bitboard, we need to iterate squares
                    # Bitboard is iterable yielding square indices? Yes in python-chess it behaves like set of squares
                    
                    if piece.color == chess.WHITE:
                        for target in attacks:
                            white_attacks[target] += 1
                    else:
                        for target in attacks:
                            black_attacks[target] += 1
            
            # Draw overlays
            for sq in chess.SQUARES:
                w_count = white_attacks[sq]
                b_count = black_attacks[sq]
                
                if w_count > 0 or b_count > 0:
                    c = chess.square_file(sq)
                    r = 7 - chess.square_rank(sq)
                    x = OFFSET_X + c * SQUARE_SIZE
                    y = OFFSET_Y + r * SQUARE_SIZE
                    
                    # Logic: 
                    # If only White attacks -> Blue
                    # If only Black attacks -> Red
                    # If both -> Purple/Mixed? Or Dominant?
                    # Let's mix colors.
                    
                    # Base colors
                    # Blue: (100, 100, 255) | Red: (255, 100, 100)
                    
                    # Calculate net intensity
                    # We can simply draw Red then Blue on top with additive blending or just calculate final color
                    
                    total_attacks = w_count + b_count
                    intensity = min(200, 40 + total_attacks * 30)
                    
                    # Mix Color
                    # Simple lerp based on ratio
                    if total_attacks > 0:
                        r_ratio = b_count / total_attacks # Black is Red
                        b_ratio = w_count / total_attacks # White is Blue
                        
                        color_r = int(255 * r_ratio)
                        color_b = int(255 * b_ratio)
                        color_g = 0 
                        
                        # Fix for purely blue or red to look nice
                        if b_count == 0: color_b = 50 # slight tint
                        if w_count == 0: color_r = 50
                    
                    else:
                        continue # Should not happen inside this if

                    self.heat_surface.fill((color_r, color_g, color_b))
                    self.heat_surface.set_alpha(intensity)
                    self.screen.blit(self.heat_surface, (x, y))

        # 2. Scope Lines
        if self.show_lines:
            if not hasattr(self, 'line_surface'):
                self.line_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            
            self.line_surface.fill((0, 0, 0, 0)) # Clear
            
            for sq in chess.SQUARES:
                piece = self.game.board.piece_at(sq)
                if piece:
                    start_col = chess.square_file(sq)
                    start_row = 7 - chess.square_rank(sq)
                    start_pos = (
                        OFFSET_X + start_col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        OFFSET_Y + start_row * SQUARE_SIZE + SQUARE_SIZE // 2
                    )
                    
                    # Line Color based on piece color
                    if piece.color == chess.WHITE:
                        line_color = (100, 100, 255, 80) # Blue, semi-transparent
                    else:
                        line_color = (255, 100, 100, 80) # Red, semi-transparent

                    attacks = self.game.board.attacks(sq)
                    for target in attacks:
                        t_col = chess.square_file(target)
                        t_row = 7 - chess.square_rank(target)
                        end_pos = (
                            OFFSET_X + t_col * SQUARE_SIZE + SQUARE_SIZE // 2,
                            OFFSET_Y + t_row * SQUARE_SIZE + SQUARE_SIZE // 2
                        )
                        
                        pygame.draw.line(self.line_surface, line_color, start_pos, end_pos, 2)
            
            self.screen.blit(self.line_surface, (0, 0))

    def draw_ui(self):
        # Draw Checkboxes
        # Lines
        color_lines = (100, 200, 100) if self.show_lines else (100, 100, 100)
        pygame.draw.rect(self.screen, color_lines, self.chk_lines_rect)
        pygame.draw.rect(self.screen, (255,255,255), self.chk_lines_rect, 2)
        text_lines = self.ui_font.render("Show Lines", True, (0,0,0))
        self.screen.blit(text_lines, (self.chk_lines_rect.x + 10, self.chk_lines_rect.y + 5))

        # Heat
        color_heat = (100, 200, 100) if self.show_heat else (100, 100, 100)
        pygame.draw.rect(self.screen, color_heat, self.chk_heat_rect)
        pygame.draw.rect(self.screen, (255,255,255), self.chk_heat_rect, 2)
        text_heat = self.ui_font.render("Show Scope", True, (0,0,0))
        self.screen.blit(text_heat, (self.chk_heat_rect.x + 10, self.chk_heat_rect.y + 5))

        # Game Status Message
        status_text = ""
        is_game_over = False
        
        if self.game.board.is_checkmate():
            status_text = "CHECKMATE!"
            is_game_over = True
        elif self.game.board.is_stalemate():
            status_text = "STALEMATE"
            is_game_over = True
        elif self.game.board.is_check():
            status_text = "CHECK!"
            # Check is NOT game over, just a warning
        
        if status_text:
            if is_game_over:
                # Draw semi-transparent background for text (Blocking)
                s = pygame.Surface((WIDTH, 200), pygame.SRCALPHA)
                s.fill((0, 0, 0, 150))
                self.screen.blit(s, (0, HEIGHT//2 - 100))
                
                text_surf = self.font.render(status_text, True, (255, 50, 50))
                rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
                self.screen.blit(text_surf, rect)
                
                # Show New Game Button in center
                self.new_game_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50)
                pygame.draw.rect(self.screen, (50, 150, 50), self.new_game_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), self.new_game_rect, 2)
                
                new_game_text = self.ui_font.render("New Game", True, (255, 255, 255))
                text_rect = new_game_text.get_rect(center=self.new_game_rect.center)
                self.screen.blit(new_game_text, text_rect)
            else:
                # Just show "CHECK!" text somewhere non-intrusive (e.g. top or bottom overlay)
                # Or just below board
                text_surf = self.font.render(status_text, True, (255, 50, 50))
                rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT - 50))
                self.screen.blit(text_surf, rect)
    
    def reset_game(self):
        self.game.reset()
        self.selected_square = None
        self.running = True # Should already be true if we are clicking
        # Clear/Reset engine if needed (usually just board reset is enough)

    def draw_game(self):
        self.draw_board()
        self.draw_overlays() # New Overlay Layer
        self.draw_pieces()
        self.draw_ui() # New UI Layer

if __name__ == "__main__":
    game = ChessGame()
    gui = ChessGUI(game)
    gui.main_loop()
