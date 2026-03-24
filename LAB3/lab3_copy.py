import pygame

pygame.init()
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("First Game")

# deklarowanie kolorów
CZERWONY = (255, 0, 0)
ZIELONY = (0, 255, 0)
ZOLTY = (255, 255, 0)
FIOLETOWY = (128, 0, 128)
JASNY_NIEBIESKI = (0, 255, 255)
POMARANCZOWY = (255, 165, 0)
NIEBIESKI = (0, 0, 255)
SZARY = (128, 128, 128)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # rysowanie kwadratów
    pygame.draw.rect(win, CZERWONY , (10, 30, 100, 100))
    pygame.draw.rect(win, ZOLTY, (160, 30, 100, 100))
    pygame.draw.rect(win, ZIELONY, (310, 30, 100, 100))
    # rysowanie kół
    pygame.draw.circle(win, FIOLETOWY, (60, 200), 50, 0)
    pygame.draw.circle(win, JASNY_NIEBIESKI, (210, 200), 50, 25)
    pygame.draw.circle(win, POMARANCZOWY, (360, 200), 50, 5)
    # linia pozioma
    pygame.draw.line(win, NIEBIESKI, (10, 325), (110, 325), 15)
    # linia pionowa
    pygame.draw.line(win, SZARY, (210, 275), (210, 375), 5)
    # rysowanie plusa
    pygame.draw.line(win, NIEBIESKI, (310, 325), (410, 325), 10)
    pygame.draw.line(win, SZARY, (360, 275), (360, 375), 10)
    # wypisywanie tekstu
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Tekst do wyświetlania ', 1, (255, 255, 255))
    win.blit(label, (100, 425))

    pygame.display.update()