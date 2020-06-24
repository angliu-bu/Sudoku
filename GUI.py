import pygame

pygame.init()
size = w, h = 550, 550
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

window = pygame.display.set_mode(size)
window.fill(white)
pygame.display.set_caption("Sudoku")
# pygame.draw.rect(window, black,(50,50,450,450), 2)

board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
font = pygame.font.Font('freesansbold.ttf', 20)

for x, row in enumerate(board):
    for y, value in enumerate(row):
        if value != '.':
            text = font.render(board[x][y], True, black, white)
            textRect = text.get_rect()
            textRect.center = ((y * 50) + 75, (x * 50) + 75)
            window.blit(text, textRect)

for i, offset in enumerate(range(0, 500, 50)):
    if i == 3 or i == 6:
        thickness = 4
    else:
        thickness = 2
    pygame.draw.line(window, black, (50 + offset, 50), (50 + offset, 500), thickness)
    pygame.draw.line(window, black, (50, 50 + offset), (500, 50 + offset), thickness)

# pygame.draw.line(window, black, (400,100), (400,400),5)
pygame.display.update()

run = True
while run:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            y, x = pygame.mouse.get_pos()
            x, y = x // 50 - 1, y // 50 - 1

            if board[x][y] == '.':
                pygame.draw.rect(window, red, ((y + 1) * 50, (x + 1) * 50, 50, 50), 5)
                pygame.display.update()

                print("you clicked an empty slot")
            else:
                print(board[x][y])


            print("you clicked ", (x, y))

    if keys[pygame.K_ESCAPE]:
        run = False
    pygame.time.delay(100)

pygame.quit()

