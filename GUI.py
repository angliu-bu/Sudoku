import pygame

pygame.init()
size = w, h = 500, 500
color = (255, 255, 255)

window = pygame.display.set_mode(size)
window.fill(color)
pygame.display.set_caption("Sudoku")
pygame.display.update()

run = True
while run:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False
    pygame.time.delay(100)

pygame.quit()
