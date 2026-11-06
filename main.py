import os

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

def draw_board(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # Alternate colors based on whether the sum of row and col is even
            is_light_square = (row + col) % 2 == 0
            square_color = LIGHT_RGB if is_light_square else DARK_RGB

            square_rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, square_color, square_rect)


def load_pieces():
    """ Loads the piece textures from the 'images' directory. '"""
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.smoothscale(
            pygame.image.load(f"images/{piece}.svg"), (SQ_SIZE, SQ_SIZE),
        )

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
        ["bP", "bP", "bP", "bP", "bp", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
    ]

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

        draw_board(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()