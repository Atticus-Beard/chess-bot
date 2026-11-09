from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
DIMENSION = 8  # 8x8 chessboard
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15

# Colors (RGB)
DARK_RGB = (118, 150, 86)
LIGHT_RGB = (238, 238, 210)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess game")

# Global dictionary for piece textures
IMAGES = {}

def draw_board(screen, selected_piece, valid_moves):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # Alternate colors based on whether the sum of row and col is even
            is_light_square = (row + col) % 2 == 0
            square_color = LIGHT_RGB if is_light_square else DARK_RGB

            square_rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, square_color, square_rect)

            # Highlight the selected piece
            if selected_piece == (row, col):
                highlight_surface = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                highlight_surface.fill((255, 255, 0, 120))  # Translucent yellow
                screen.blit(highlight_surface, square_rect.topleft)
                pygame.draw.rect(screen, (255, 215, 0), square_rect, 4)

            if (row, col) in valid_moves:
                center_x = col * SQ_SIZE + SQ_SIZE // 2
                center_y = row * SQ_SIZE + SQ_SIZE // 2

                pygame.draw.circle(screen, (202, 203, 179), (center_x, center_y), SQ_SIZE // 6)



def load_pieces():
    """ Loads the piece textures from the 'images' directory. '"""
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.smoothscale(
            pygame.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE),
        )

def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def is_valid_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end

    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    if start == end:
        return False

    # Makes sure the piece is not capturing its own color.
    if target != "--" and piece[0] == target[0]:
        return False

    piece_color = piece[0]
    piece_type = piece[1]

    row_diff  = end_row - start_row
    col_diff = end_col - start_col

    # --- ROOK RULES ---
    if piece_type == 'R':
        if row_diff != 0 and col_diff != 0:
            return False

        # Check for path blocking.
        if piece_type == 'R':
            if row_diff != 0 and col_diff != 0:
                return False

            # Check for path blocking.
            if row_diff == 0:
                # Horizontal movement (FIXED: changed > 1 to > 0)
                step = 1 if col_diff > 0 else -1

                for c in range(start_col + step, end_col, step):
                    # FIXED: corrected board indices to [start_row][c]
                    if board[start_row][c] != "--":
                        return False

            elif col_diff == 0:
                # Vertical movement (FIXED: changed > 1 to > 0)
                step = 1 if row_diff > 0 else -1

                for r in range(start_row + step, end_row, step):
                    if board[r][start_col] != "--":
                        return False


    if piece_type == "B":
        # Checks that the bishop is moving only diagonally
        if abs(col_diff) != abs(row_diff):
            return False

    return True

def main():
    clock = pygame.time.Clock()
    load_pieces()

    # 2D array for the chess board
    # The first character is what color the piece is w = white and b = black.
    # The second character is what piece it is.
    # R = rook
    # N = knight
    # B = bishop
    # Q = queen
    # K = King
    # P = Pawn
    # -- means there is no piece at that location.
    board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
    ]

    selected_piece = () # Keeps track of the (row, col) of the selected piece
    turn = 'w' # 'w' for white who goes first and 'b' for black
    valid_moves = []

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos() # Gets the X,Y coords.
                col = pos[0] // SQ_SIZE
                row = pos[1] // SQ_SIZE

                print(f"Clicked on row {row} and col {col}.")

                if selected_piece == (row, col):
                    # Clicked the piece so deselect
                    valid_moves = []
                    selected_piece = ()
                elif not selected_piece:
                    # First click. Select the piece.
                    if board[row][col] != "--":
                        if board[row][col][0] == turn:
                            # Only selects the piece of the player whose turn it is.
                            selected_piece = (row, col)
                            valid_moves = []

                            # Get a list of valid moves.
                            for r in range(DIMENSION):
                                for c in range(DIMENSION):
                                    if is_valid_move(board, selected_piece,(r, c)):
                                        valid_moves.append((r,c))

                else:
                    start_row, start_col = selected_piece

                    # Moves the piece in the 2d array.
                    if is_valid_move(board, (start_row, start_col), (row, col)):
                        board[row][col] = board[start_row][start_col]
                        board[start_row][start_col] = "--"

                        # Switches the turn value to the other player.
                        turn = 'b' if turn == 'w' else 'w'

                    selected_piece = ()
                    valid_moves = []
        draw_board(screen, selected_piece, valid_moves)
        draw_pieces(screen, board)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()