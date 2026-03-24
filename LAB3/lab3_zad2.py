import pygame
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
BG_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (250, 245, 0)
GREEN = (0, 255, 0)
BLUE = (20, 20, 245)
RED = (255, 20, 20)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAB3 - Zadanie 2")


def square_surface(size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (0, 0, size, size))
    return surf


def circle_surface(size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (size // 2, size // 2), size // 2)
    return surf


def triangle_surface(size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    points = [(size // 2, 0), (0, size), (size, size)]
    pygame.draw.polygon(surf, color, points)
    return surf


base_square = square_surface(100, BLUE)
base_triangle = triangle_surface(100, BLUE)
base_circle = circle_surface(100, BLACK)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill(BG_COLOR)

    pygame.draw.rect(win, BLACK, (15, 15, 470, 470), 3)

    # Lewy gorny
    big_circle = pygame.transform.scale(base_circle, (155, 155))
    win.blit(big_circle, (55, 70))

    yellow_square = square_surface(80, YELLOW)
    win.blit(yellow_square, (93, 108))

    # Prawy gorny
    green_square = square_surface(155, GREEN)
    win.blit(green_square, (285, 70))

    cut_triangle = triangle_surface(100, BG_COLOR)
    cut_triangle = pygame.transform.scale(cut_triangle, (155, 78))
    win.blit(cut_triangle, (285, 147))

    # Lewy dolny
    top_triangle = pygame.transform.scale(base_triangle, (60, 60))
    top_triangle = pygame.transform.flip(top_triangle, False, True)
    win.blit(top_triangle, (105, 300))

    mid_rect = pygame.transform.scale(base_square, (120, 60))
    win.blit(mid_rect, (75, 360))

    bottom_triangle = pygame.transform.scale(base_triangle, (60, 60))
    win.blit(bottom_triangle, (105, 420))

    # Prawy dolny
    base_square_red = square_surface(100, RED)
    z_width = 160
    z_height = 120
    thickness = 8

    top_bar = pygame.transform.scale(base_square_red, (z_width, thickness))
    win.blit(top_bar, (285, 308))

    bottom_bar = pygame.transform.scale(base_square_red, (z_width, thickness))
    win.blit(bottom_bar, (285, 428))

    diag_len = int(math.hypot(z_width, z_height))
    diag_surf = pygame.transform.scale(base_square_red, (diag_len, thickness))
    angle = math.degrees(math.atan2(z_height, z_width))
    diag_rot = pygame.transform.rotate(diag_surf, angle)
    
    center_x = 285 + z_width // 2
    center_y = 308 + z_height // 2 + thickness // 2
    diag_rect = diag_rot.get_rect(center=(center_x, center_y))
    win.blit(diag_rot, diag_rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
