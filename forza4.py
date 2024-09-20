import pygame
import sys
import random
import numpy as np

# Costanti
WIDTH, HEIGHT = 700, 600
BACKGROUND_COLOR = (30, 30, 30)  # Colore di sfondo scuro
GRID_COLOR = (200, 200, 200)  # Colore della griglia più chiaro
CELL_SIZE = 100
ROWS, COLS = 6, 7
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PLAYER1_COLOR = RED
PLAYER2_COLOR = YELLOW
CURSOR_COLOR = (0, 255, 0)
CURSOR_WIDTH = 8
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 72
SMALL_FONT_SIZE = 24
BUTTON_COLOR = (70, 130, 180)  # Colore blu
BUTTON_HOVER_COLOR = (100, 149, 237)  # Colore blu chiaro

# Inizializzazione di PyGame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forza 4")
font = pygame.font.Font(None, FONT_SIZE)
small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

def draw_button(text, x, y, w, h, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)  # Aggiungi angoli arrotondati
    text_surf = font.render(text, True, FONT_COLOR)
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)

def show_difficulty_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if easy_button_rect.collidepoint(x, y):
                    return "easy"
                if medium_button_rect.collidepoint(x, y):
                    return "medium"
                if hard_button_rect.collidepoint(x, y):
                    return "hard"
                if champ_button_rect.collidepoint(x, y):
                    return "champion"
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill(BACKGROUND_COLOR)
        
        # Disegna i pulsanti
        draw_button("Easy", 200, 200, 300, 50, hover=easy_button_rect.collidepoint(mouse_x, mouse_y))
        draw_button("Medium", 200, 275, 300, 50, hover=medium_button_rect.collidepoint(mouse_x, mouse_y))
        draw_button("Hard", 200, 350, 300, 50, hover=hard_button_rect.collidepoint(mouse_x, mouse_y))
        draw_button("Champion", 200, 425, 300, 50, hover=champ_button_rect.collidepoint(mouse_x, mouse_y))
        
        # Disegna le istruzioni
        instructions_line1 = "ISTRUZIONI PER IL GIOCO: per selezionare la colonna,"
        instructions_line2 = "usare le frecce destra e sinistra."
        instructions_line3 = "Per far cadere la pedina, usare la freccia in giù."
        
        # Renderizza il testo su più righe
        instruction_text1 = small_font.render(instructions_line1, True, FONT_COLOR)
        instruction_text2 = small_font.render(instructions_line2, True, FONT_COLOR)
        instruction_text3 = small_font.render(instructions_line3, True, FONT_COLOR)

        # Posiziona le righe di testo
        instruction_rect1 = instruction_text1.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        instruction_rect2 = instruction_text2.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        instruction_rect3 = instruction_text3.get_rect(center=(WIDTH // 2, HEIGHT - 60))

        screen.blit(instruction_text1, instruction_rect1)
        screen.blit(instruction_text2, instruction_rect2)
        screen.blit(instruction_text3, instruction_rect3)

        pygame.display.flip()


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, GRID_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

def draw_piece(row, col, color):
    pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 10)

def draw_cursor(col):
    pygame.draw.rect(screen, CURSOR_COLOR, (col * CELL_SIZE, 0, CELL_SIZE, HEIGHT), CURSOR_WIDTH)

def display_thinking_message():
    text = small_font.render("Il computer sta pensando...", True, FONT_COLOR)
    text_rect = text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(text, text_rect)

def drop_piece(grid, col, color):
    for row in range(ROWS - 1, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = color
            return row
    return -1

def check_win(grid, color):
    # Verifica orizzontale
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(grid[row][col + i] == color for i in range(4)):
                return True
    # Verifica verticale
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(grid[row + i][col] == color for i in range(4)):
                return True
    # Verifica diagonale /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(grid[row - i][col + i] == color for i in range(4)):
                return True
    # Verifica diagonale \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(grid[row + i][col + i] == color for i in range(4)):
                return True
    return False

def display_winner(message):
    text = font.render(message, True, FONT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Attendere 3 secondi

def ai_move_easy(grid):
    available_columns = [c for c in range(COLS) if grid[0][c] == 0]
    if available_columns:
        col = random.choice(available_columns)
        drop_piece(grid, col, PLAYER2_COLOR)

def ai_move_medium(grid):
    def can_win(grid, color, col):
        temp_grid = [row[:] for row in grid]
        row = drop_piece(temp_grid, col, color)
        if row != -1 and check_win(temp_grid, color):
            return True
        return False

    for col in range(COLS):
        if grid[0][col] == 0:
            if can_win(grid, PLAYER1_COLOR, col):
                drop_piece(grid, col, PLAYER2_COLOR)
                return

    available_columns = [c for c in range(COLS) if grid[0][c] == 0]
    if available_columns:
        col = random.choice(available_columns)
        drop_piece(grid, col, PLAYER2_COLOR)
        

def ai_move_hard(grid):
    def evaluate_board(board):
        if check_win(board, PLAYER2_COLOR):
            return 1000
        if check_win(board, PLAYER1_COLOR):
            return -1000
        return 0

    def minimax(board, depth, is_maximizing):
        if depth == 0 or check_win(board, PLAYER1_COLOR) or check_win(board, PLAYER2_COLOR):
            return evaluate_board(board)

        if is_maximizing:
            max_eval = -float('inf')
            available_columns = [c for c in range(COLS) if board[0][c] == 0]
            random.shuffle(available_columns)  # Introduce randomness
            for col in available_columns:
                row = drop_piece(board, col, PLAYER2_COLOR)
                eval = minimax(board, depth - 1, False)
                board[row][col] = 0
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            available_columns = [c for c in range(COLS) if board[0][c] == 0]
            random.shuffle(available_columns)  # Introduce randomness
            for col in available_columns:
                row = drop_piece(board, col, PLAYER1_COLOR)
                eval = minimax(board, depth - 1, True)
                board[row][col] = 0
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(board):
        best_move = None
        best_value = -float('inf')
        available_columns = [c for c in range(COLS) if board[0][c] == 0]
        random.shuffle(available_columns)  # Introduce randomness
        for col in available_columns:
            temp_board = [row[:] for row in board]
            row = drop_piece(temp_board, col, PLAYER2_COLOR)
            move_value = minimax(temp_board, 4, False)
            board[row][col] = 0
            if move_value > best_value:
                best_value = move_value
                best_move = col
        return best_move

    best_col = find_best_move(grid)
    if best_col is not None:
        drop_piece(grid, best_col, PLAYER2_COLOR)


def ai_move_champion(grid, simulations=1000):
    def is_forced_move(board, color):
        def can_win_with_move(temp_board, color, col):
            row = drop_piece(temp_board, col, color)
            win = check_win(temp_board, color)
            temp_board[row][col] = 0
            return win

        def find_forced_move(color):
            # Controlla le mosse che vincono per il giocatore
            for col in range(COLS):
                if board[0][col] == 0:
                    temp_board = [row[:] for row in board]
                    if can_win_with_move(temp_board, color, col):
                        return col
            return None

        # Verifica se c'è una mossa forzata per il giocatore
        move = find_forced_move(PLAYER2_COLOR)
        if move is not None:
            return move

        # Verifica se c'è una mossa forzata per l'avversario e blocca
        move = find_forced_move(PLAYER1_COLOR)
        if move is not None:
            return move

        return None

    def simulate_game(board, player_color):
        available_columns = [c for c in range(COLS) if board[0][c] == 0]
        if not available_columns:
            return 0  # Pareggio

        while True:
            col = random.choice(available_columns)
            row = drop_piece(board, col, player_color)

            if check_win(board, player_color):
                return 1
            if all(board[0][c] != 0 for c in range(COLS)):
                return 0

            player_color = PLAYER1_COLOR if player_color == PLAYER2_COLOR else PLAYER2_COLOR
            available_columns = [c for c in range(COLS) if board[0][c] == 0]

    def get_best_move(board):
        move_scores = np.zeros(COLS)

        # Controlla se c'è una mossa forzata
        forced_move = is_forced_move(board, PLAYER2_COLOR)
        if forced_move is not None:
            return forced_move

        remaining_moves = sum(board[0][c] == 0 for c in range(COLS))
        num_simulations = 1000 if remaining_moves > 20 else 500 if remaining_moves > 10 else 100

        for col in range(COLS):
            if board[0][col] == 0:
                temp_board = [row[:] for row in board]
                row = drop_piece(temp_board, col, PLAYER2_COLOR)

                wins = sum(simulate_game([row[:] for row in temp_board], PLAYER1_COLOR) for _ in range(num_simulations))
                move_scores[col] = wins

                temp_board[row][col] = 0

        return np.argmax(move_scores) if np.any(move_scores) else None

    best_col = get_best_move(grid)
    if best_col is not None:
        drop_piece(grid, best_col, PLAYER2_COLOR)



def main():
    global grid
    difficulty_level = show_difficulty_screen()
    
    grid = [[0] * COLS for _ in range(ROWS)]
    clock = pygame.time.Clock()
    turn = 0
    column = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    column = max(column - 1, 0)
                if event.key == pygame.K_RIGHT:
                    column = min(column + 1, COLS - 1)
                if event.key == pygame.K_DOWN:
                    if turn == 0:
                        row = drop_piece(grid, column, PLAYER1_COLOR)
                        if row != -1:
                            screen.fill(BACKGROUND_COLOR)
                            draw_grid()
                            for r in range(ROWS):
                                for c in range(COLS):
                                    if grid[r][c] != 0:
                                        draw_piece(r, c, grid[r][c])
                            draw_cursor(column)
                            pygame.display.flip()

                            if check_win(grid, PLAYER1_COLOR):
                                display_winner("Player 1 Wins!")
                                return
                            
                            turn = 1
                            pygame.time.wait(100)
                            
                            screen.fill(BACKGROUND_COLOR)
                            draw_grid()
                            for r in range(ROWS):
                                for c in range(COLS):
                                    if grid[r][c] != 0:
                                        draw_piece(r, c, grid[r][c])
                            draw_cursor(column)
                            display_thinking_message()
                            pygame.display.flip()
                            
                            pygame.time.wait(500)

                            if difficulty_level == "easy":
                                ai_move_easy(grid)
                            elif difficulty_level == "medium":
                                ai_move_medium(grid)
                            elif difficulty_level == "hard":
                                ai_move_hard(grid)
                            elif difficulty_level == "champion":
                                ai_move_champion(grid)
                            
                            screen.fill(BACKGROUND_COLOR)
                            draw_grid()
                            for r in range(ROWS):
                                for c in range(COLS):
                                    if grid[r][c] != 0:
                                        draw_piece(r, c, grid[r][c])
                            draw_cursor(column)
                            pygame.display.flip()
                            
                            if check_win(grid, PLAYER2_COLOR):
                                display_winner("Computer Wins!")
                                return
                            
                            turn = 0

        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        for row in range(ROWS):
            for col in range(COLS):
                if grid[row][col] != 0:
                    draw_piece(row, col, grid[row][col])
        draw_cursor(column)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    easy_button_rect = pygame.Rect(200, 200, 300, 50)
    medium_button_rect = pygame.Rect(200, 275, 300, 50)
    hard_button_rect = pygame.Rect(200, 350, 300, 50)
    champ_button_rect = pygame.Rect(200, 425, 300, 50)
    main()
