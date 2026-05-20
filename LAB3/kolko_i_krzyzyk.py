"""
Zasady:
  - Gracz X zaczyna zawsze pierwszy.
  - Wygrywa ten, kto jako pierwszy ustawi trzy swoje znaki w rzędzie
    (poziomo, pionowo lub po przekątnej).
  - Jeśli wszystkie pola zostaną zajęte bez zwycięzcy - remis.
"""

import sys
import pygame

# --- Wymiary okna i siatki ---
WIDTH, HEIGHT = 450, 540  # szerokość i wysokość okna w pikselach
GRID_TOP = 70             # odległość górnej krawędzi siatki od góry okna
CELL     = 150            # rozmiar jednej komórki w pikselach
LINE_W   = 4              # grubość linii siatki
MARK_W   = 8              # grubość linii znaku X lub O
MARGIN   = 30             # wewnętrzny margines znaku od krawędzi komórki

# --- Kolory (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
GRAY  = (180, 180, 180)

# --- Inicjalizacja pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kółko i Krzyżyk")
clock = pygame.time.Clock()

# --- Czcionki ---
font_title  = pygame.font.SysFont("segoeui", 30, bold=True)
font_status = pygame.font.SysFont("segoeui", 22)
font_btn    = pygame.font.SysFont("segoeui", 20, bold=True)

def new_board():
    # Tworzy pustą planszę 3x3 (każde pole to pusty string)
    return [["" for _ in range(3)] for _ in range(3)]

# --- Stan gry ---
board     = new_board()
current   = "X"   # aktualnie ruszający się gracz
winner    = None   # zwycięzca ("X", "O") lub "remis", albo None gdy gra trwa
win_cells = []     # komórki tworzące wygrywającą linię
game_over = False  # czy gra się już skończyła

# Wszystkie możliwe linie wygrywające: 3 poziome, 3 pionowe, 2 przekątne
LINES = [
    [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],  # poziome
    [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],  # pionowe
    [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)],                        # przekątne
]

def check_winner(b):
    # Sprawdza, czy któryś gracz wygrał; zwraca (zwycięzca, komórki linii)
    for line in LINES:
        vals = [b[r][c] for r, c in line]
        if vals[0] and vals[0] == vals[1] == vals[2]:
            return vals[0], list(line)
    return None, []

def is_draw(b):
    # Zwraca True, gdy wszystkie pola są zajęte (remis)
    return all(b[r][c] for r in range(3) for c in range(3))

def cell_rect(row, col):
    # Zwraca prostokąt pygame.Rect odpowiadający komórce (row, col)
    return pygame.Rect(col * CELL, GRID_TOP + row * CELL, CELL, CELL)

def pixel_to_cell(px, py):
    # Przelicza współrzędne piksela na indeks komórki (row, col) lub None poza siatką
    if py < GRID_TOP or py > GRID_TOP + 3 * CELL:
        return None
    col, row = px // CELL, (py - GRID_TOP) // CELL
    if 0 <= row < 3 and 0 <= col < 3:
        return row, col
    return None

# --- Przycisk "Zagraj ponownie" ---
BTN_W, BTN_H = 200, 42
btn_rect = pygame.Rect((WIDTH - BTN_W) // 2, HEIGHT - 58, BTN_W, BTN_H)

def draw_button(hovered):
    # Rysuje przycisk restartu; zmienia kolor tła gdy kursor jest nad nim
    pygame.draw.rect(screen, GRAY if hovered else WHITE, btn_rect)
    pygame.draw.rect(screen, BLACK, btn_rect, 2)
    label = font_btn.render("Zagraj ponownie", True, BLACK)
    screen.blit(label, label.get_rect(center=btn_rect.center))

def draw_grid():
    # Rysuje siatkę 3x3 (linie wewnętrzne + obramowanie)
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, GRID_TOP + i * CELL), (WIDTH, GRID_TOP + i * CELL), LINE_W)
        pygame.draw.line(screen, BLACK, (i * CELL, GRID_TOP), (i * CELL, GRID_TOP + 3 * CELL), LINE_W)
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, GRID_TOP, 3 * CELL, 3 * CELL), LINE_W)

def draw_x(row, col):
    # Rysuje znak X w komórce (row, col) jako dwie skrzyżowane linie
    r = cell_rect(row, col)
    pygame.draw.line(screen, BLACK, (r.left + MARGIN, r.top + MARGIN), (r.right - MARGIN, r.bottom - MARGIN), MARK_W)
    pygame.draw.line(screen, BLACK, (r.right - MARGIN, r.top + MARGIN), (r.left + MARGIN, r.bottom - MARGIN), MARK_W)

def draw_o(row, col):
    # Rysuje znak O w komórce (row, col) jako okrąg
    r = cell_rect(row, col)
    pygame.draw.circle(screen, BLACK, r.center, CELL // 2 - MARGIN, MARK_W)

def draw_marks():
    # Rysuje wszystkie znaki X i O aktualnie obecne na planszy
    for r in range(3):
        for c in range(3):
            if board[r][c] == "X":
                draw_x(r, c)
            elif board[r][c] == "O":
                draw_o(r, c)

def draw_win_line():
    # Rysuje szarą linię przez wygrywającą trójkę komórek
    if len(win_cells) == 3:
        start = cell_rect(*win_cells[0]).center
        end   = cell_rect(*win_cells[2]).center
        pygame.draw.line(screen, GRAY, start, end, LINE_W + 4)

def draw_status():
    # Rysuje tytuł gry oraz informację o aktualnym stanie (czyj ruch / wynik)
    title = font_title.render("Kółko i Krzyżyk", True, BLACK)
    screen.blit(title, title.get_rect(centerx=WIDTH // 2, y=8))

    if winner == "remis":
        msg = "Remis!"
    elif winner:
        msg = f"Wygrał gracz {winner}!"
    else:
        msg = f"Ruch gracza: {current}"

    status = font_status.render(msg, True, BLACK)
    screen.blit(status, status.get_rect(centerx=WIDTH // 2, y=44))

def reset():
    # Resetuje wszystkie zmienne stanu do wartości początkowych
    global board, current, winner, win_cells, game_over
    board, current, winner, win_cells, game_over = new_board(), "X", None, [], False

def main():
    global board, current, winner, win_cells, game_over

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Kliknięcie przycisku restartu po zakończeniu gry
                if game_over and btn_rect.collidepoint(mouse_pos):
                    reset(); continue

                if not game_over:
                    cell = pixel_to_cell(*mouse_pos)
                    if cell:
                        r, c = cell
                        if board[r][c] == "":  # pole musi być puste
                            board[r][c] = current
                            winner, win_cells = check_winner(board)
                            if winner:
                                game_over = True
                            elif is_draw(board):
                                winner, game_over = "remis", True
                            else:
                                # Zmiana tury na drugiego gracza
                                current = "O" if current == "X" else "X"

        # --- Rysowanie klatki ---
        screen.fill(WHITE)
        draw_status()
        draw_grid()
        draw_marks()
        if game_over and win_cells:
            draw_win_line()
        if game_over:
            draw_button(btn_rect.collidepoint(mouse_pos))

        pygame.display.flip()
        clock.tick(60)  # ograniczenie do 60 klatek na sekundę

if __name__ == "__main__":
    main()