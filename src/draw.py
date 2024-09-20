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


easy_button_rect = pygame.Rect(200, 200, 300, 50)
medium_button_rect = pygame.Rect(200, 275, 300, 50)
hard_button_rect = pygame.Rect(200, 350, 300, 50)
champ_button_rect = pygame.Rect(200, 425, 300, 50)


def draw_button(text, x, y, w, h, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(
        screen, color, (x, y, w, h), border_radius=10
    )  # Aggiungi angoli arrotondati
    text_surf = font.render(text, True, FONT_COLOR)
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                screen,
                GRID_COLOR,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                2,
            )


def draw_piece(row, col, color):
    pygame.draw.circle(
        screen,
        color,
        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
        CELL_SIZE // 2 - 10,
    )


def draw_cursor(col):
    pygame.draw.rect(
        screen, CURSOR_COLOR, (col * CELL_SIZE, 0, CELL_SIZE, HEIGHT), CURSOR_WIDTH
    )


def display_thinking_message():
    text = small_font.render("Il computer sta pensando...", True, FONT_COLOR)
    text_rect = text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(text, text_rect)


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
        draw_button(
            "Easy",
            200,
            200,
            300,
            50,
            hover=easy_button_rect.collidepoint(mouse_x, mouse_y),
        )
        draw_button(
            "Medium",
            200,
            275,
            300,
            50,
            hover=medium_button_rect.collidepoint(mouse_x, mouse_y),
        )
        draw_button(
            "Hard",
            200,
            350,
            300,
            50,
            hover=hard_button_rect.collidepoint(mouse_x, mouse_y),
        )
        draw_button(
            "Champion",
            200,
            425,
            300,
            50,
            hover=champ_button_rect.collidepoint(mouse_x, mouse_y),
        )

        # Disegna le istruzioni
        instructions_line1 = "ISTRUZIONI PER IL GIOCO: per selezionare la colonna,"
        instructions_line2 = "usare le frecce destra e sinistra."
        instructions_line3 = "Per far cadere la pedina, usare la freccia in giù."

        # Renderizza il testo su più righe
        instruction_text1 = small_font.render(instructions_line1, True, FONT_COLOR)
        instruction_text2 = small_font.render(instructions_line2, True, FONT_COLOR)
        instruction_text3 = small_font.render(instructions_line3, True, FONT_COLOR)

        # Posiziona le righe di testo
        instruction_rect1 = instruction_text1.get_rect(
            center=(WIDTH // 2, HEIGHT - 100)
        )
        instruction_rect2 = instruction_text2.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        instruction_rect3 = instruction_text3.get_rect(center=(WIDTH // 2, HEIGHT - 60))

        screen.blit(instruction_text1, instruction_rect1)
        screen.blit(instruction_text2, instruction_rect2)
        screen.blit(instruction_text3, instruction_rect3)

        pygame.display.flip()


def display_winner(message):
    text = font.render(message, True, FONT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Attendere 3 secondi
