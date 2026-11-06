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

def draw_board(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # Alternate colors based on whether the sum of row and col is even
            is_light_square = (row + col) % 2 == 0
            square_color = LIGHT_RGB if is_light_square else DARK_RGB

            square_rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, square_color, square_rect)

def main():
    clock = pygame.time.Clock()

    board = [[]]

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