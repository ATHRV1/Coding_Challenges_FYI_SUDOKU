import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 540
CELL_SIZE = SCREEN_WIDTH // 9
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
HIGHLIGHT_COLOR = (173, 216, 230)
FIXED_CELL_COLOR = (200, 200, 255)

# Fonts
FONT = pygame.font.Font(None, 36)

# Pre-defined Sudoku board (partially completed)
puzzle = [
    [0, 0, 0, 2, 9, 0, 4, 5, 0],
    [5, 0, 3, 0, 4, 0, 0, 0, 2],
    [6, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 9, 0, 0, 0, 6, 7, 0],
    [0, 7, 0, 6, 8, 1, 0, 2, 9],
    [8, 0, 6, 5, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 2, 9, 8, 6, 5],
    [7, 0, 0, 1, 0, 0, 9, 0, 0],
    [3, 0, 0, 0, 1, 4, 0, 0, 0]
]

# Copy of puzzle to store player entries
board = [row[:] for row in puzzle]

# Functions to draw grid and numbers
def draw_grid(selected_cell):
    screen.fill(WHITE)
    
    # Draw grid lines and numbers
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] != 0:
                # Draw fixed cell value in blue
                value = FONT.render(str(puzzle[row][col]), True, BLUE)
                pygame.draw.rect(screen, FIXED_CELL_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif board[row][col] != 0:
                # Draw player-entered values in black
                value = FONT.render(str(board[row][col]), True, BLACK)
            else:
                value = None

            if value:
                screen.blit(value, (col * CELL_SIZE + 15, row * CELL_SIZE + 10))

            # Highlight selected cell
            if selected_cell == (row, col):
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw thicker lines for 3x3 subgrids
    for x in range(9):
        thickness = 3 if x % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, SCREEN_HEIGHT), thickness)
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE), (SCREEN_WIDTH, x * CELL_SIZE), thickness)

def is_valid_move(row, col, value):
    # Check row and column
    for i in range(9):
        if board[row][i] == value or board[i][col] == value:
            return False

    # Check 3x3 box
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row_start + i][box_col_start + j] == value:
                return False

    return True

def check_win():
    # Check if all cells are filled and each row, column, and 3x3 box is valid
    for row in range(9):
        for col in range(9):
            value = board[row][col]
            if value == 0 or not is_valid_move(row, col, value):
                return False
    return True

def set_cell_value(row, col, value):
    if puzzle[row][col] == 0:  # Allow entry only if the cell was initially empty
        board[row][col] = value

# Main loop
def main():
    selected_cell = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selected_cell = (y // CELL_SIZE, x // CELL_SIZE)
            elif event.type == pygame.KEYDOWN:
                if selected_cell and event.unicode.isdigit() and event.unicode != '0':
                    row, col = selected_cell
                    value = int(event.unicode)
                    if is_valid_move(row, col, value):
                        set_cell_value(row, col, value)
                        if check_win():
                            print("Congratulations! You've solved the puzzle.")
        
        # Draw everything
        draw_grid(selected_cell)
        pygame.display.flip()

main()
