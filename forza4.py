import pygame
import sys
import random
import numpy as np
from src.difficulty import *
from src.draw import *
from src.game import *

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
