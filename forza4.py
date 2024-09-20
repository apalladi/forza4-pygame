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
    pass


def ai_move_champion(grid, simulations=1000):
    pass



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
