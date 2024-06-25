import pygame
import sys
import os
from board.chess_board import Chess  # Import your Chess class

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800  # Width and height of the window
ROWS, COLS = 8, 8  # Number of rows and columns on the chess board
SQUARE_SIZE = HEIGHT // ROWS  # Size of each square

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BROWN = (127, 51, 0)
LIGHT_BROWN = (198, 163, 97)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Paths
IMAGE_PATH = "images/"

# Create the Pygame window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Board')

# Load piece images
piece_images = {}
for filename in os.listdir(IMAGE_PATH):
    name, extension = os.path.splitext(filename)
    if extension == '.png':
        image = pygame.image.load(os.path.join(IMAGE_PATH, filename))
        piece_images[name] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(board, possible_positions):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if (row, col) in possible_positions:
                color = GREEN
            elif (row + col) % 2 == 0:
                color = LIGHT_BROWN
            else:
                color = BROWN
            
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if piece is not None:
                filename = f'{piece.name}' + '_' + f'{piece.color}'
                image = piece_images[filename]
                win.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_board_position(mouse_pos):
    x, y = mouse_pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def draw_start_screen():
    win.fill(GREY)
    font = pygame.font.SysFont(None, 74)
    text_white = font.render('Play as White', True, WHITE)
    text_black = font.render('Play as Black', True, BLACK)
    
    white_button = pygame.Rect(200, 300, 400, 100)
    black_button = pygame.Rect(200, 450, 400, 100)
    
    pygame.draw.rect(win, BLUE, white_button)
    pygame.draw.rect(win, BLUE, black_button)
    
    win.blit(text_white, (250, 320))
    win.blit(text_black, (250, 470))
    
    pygame.display.flip()
    
    return white_button, black_button

def main():
    run = True
    chess = Chess()  # Initialize your Chess game
    board = chess.board  # Get the board configuration

    selected_piece = None  # Variable to store the selected piece
    possible_positions = []  # List to store the possible moves
    player_color = None  # Variable to store the player's color

    while run:
        if player_color is None:
            white_button, black_button = draw_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if white_button.collidepoint(mouse_pos):
                        player_color = 'white'
                        chess.current_turn = 'white'
                    elif black_button.collidepoint(mouse_pos):
                        player_color = 'black'
                        chess.current_turn = 'white'
        else:
            current_turn = chess.current_turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = get_board_position(mouse_pos)
                    
                    if selected_piece is None:
                        piece = board[row][col]
                        if piece is not None and piece.color == current_turn:
                            selected_piece = (row, col)
                            possible_positions = piece.get_possible_moves((row, col), chess)
                    else:
                        if (row, col) in possible_positions:
                            chess.make_move(selected_piece, (row, col))
                            selected_piece = None
                            possible_positions = []
                        else:
                            selected_piece = None
                            possible_positions = []

            if current_turn != player_color:
                chess.make_ai_move(depth=3)
            
            win.fill(GREY)  # Fill the background with grey
            draw_board(chess.board, possible_positions)  # Draw the chess board with possible positions
            
            pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
