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
