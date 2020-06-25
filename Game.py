import random
from collections import defaultdict
from copy import deepcopy
import time
import pygame

black = (0, 0, 0)
white = (211, 211, 211)
red = (255, 0, 0)
green = (21, 119, 40)



class Game:

    def __init__(self, diff='medium'):

        # self.board = [[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
        # self.solution = [["5","1","9","7","4","8","6","3","2"],["7","8","3","6","5","2","4","1","9"],["4","2","6","1","3","9","8","7","5"],["3","5","7","9","8","6","2","4","1"],["2","6","4","3","1","7","5","9","8"],["1","9","8","5","2","4","3","6","7"],["9","7","5","8","6","3","1","2","4"],["8","3","2","4","9","1","7","5","6"],["6","4","1","2","7","5","9","8","3"]]
        self.board, self.solution = self.GeneratedBoard(diff)
        self.temp = deepcopy(self.board)

        # Start the game
        pygame.init()

        # Fonts
        self.font26 = pygame.font.Font(None, 26)
        self.font20 = pygame.font.Font(None, 20)

        # Create window
        self.window = pygame.display.set_mode(size=(750, 550))
        self.window.fill(white)
        pygame.display.set_caption("Sudoku")
        pygame.display.flip()

        # Place numbers
        for x, row in enumerate(self.board):
            for y, value in enumerate(row):
                if value != '.':
                    text = self.font26.render(self.board[x][y], True, black, white)
                    textRect = text.get_rect(center=((y * 50) + 75, (x * 50) + 75))
                    self.window.blit(text, textRect)

        self.drawGrid()
        self.run()

    def __str__(self):

        res = ''
        for i, row in enumerate(self.board):
            for j, value in enumerate(row):
                res += value + "  "
                if j == 2 or j == 5:
                    res += "| "
            if i == 2 or i == 5:
                res += "\n- - - - - - - - - - - - - - - -"

            res += '\n'
        return res


    def run(self):
        clock = pygame.time.Clock()
        button1 = pygame.Rect(600, 200, 100, 50)
        button2 = pygame.Rect(600, 400, 100, 50)
        selected = False
        run = True
        click = False
        while run:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            # x, y = pygame.mouse.get_pos()
            #
            # # check for clinking bottoms
            # if button1.collidepoint((x, y)):
            #     if click:
            #         pass
            # if button2.collidepoint((x, y)):
            #     if click:
            #         pass
            pygame.draw.rect(self.window, (200, 0, 0), button1)
            pygame.draw.rect(self.window, (200, 100, 0), button2)

            text1 = self.font26.render('Level', True, black, white)
            textRect1 = text1.get_rect(center=(600 + 50, 200 + 25))
            self.window.blit(text1, textRect1)

            text2 = self.font26.render('Restart', True, black, white)
            textRect2 = text1.get_rect(center=(600 + 50, 400 + 25))
            self.window.blit(text2, textRect2)

            # click = False


            for event in events:
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:

                    # remove previous selection
                    if selected:
                        self.deselect(x, y)

                    # get new selection
                    y, x = pygame.mouse.get_pos()

                    # display selection
                    x, y = x // 50 - 1, y // 50 - 1
                    if 0 <= x < 9 and 0 <= y < 9 and self.board[x][y] == '.':
                        self.select(x, y)
                        selected = True

            if selected:
                # Check for user input
                for num, pressed in enumerate(keys[49:58]):
                    if pressed:
                        self.pencil(num + 1, x, y)

                # Check for delete
                if keys[pygame.K_DELETE] and self.temp[x][y] != '.':
                    self.clearCell(x, y)
                    self.select(x, y)

                # Confirm selection
                if keys[pygame.K_RETURN] and self.temp[x][y] == self.solution[x][y]:
                    self.write(self.temp[x][y], x, y)
                    selected = False

                if keys[pygame.K_LEFT] and y > 0:
                    i = y - 1
                    while i > 0 and self.board[x][i] != '.':
                        i -= 1

                    if self.board[x][i] == '.':
                        self.deselect(x, y)
                        self.select(x, i)
                        y = i
                    pygame.time.wait(150)

                if keys[pygame.K_RIGHT] and y < 8:
                    i = y + 1
                    while i < 8 and self.board[x][i] != '.':
                        i += 1

                    if self.board[x][i] == '.':
                        self.deselect(x, y)
                        self.select(x, i)
                        y = i
                    pygame.time.wait(150)

                if keys[pygame.K_DOWN] and x < 8:
                    i = x + 1
                    while i < 8 and self.board[i][y] != '.':
                        i += 1

                    if self.board[i][y] == '.':
                        self.deselect(x, y)
                        self.select(i, y)
                        x = i
                    pygame.time.wait(150)

                if keys[pygame.K_UP] and x > 0:
                    i = x - 1
                    while i > 0 and self.board[i][y] != '.':
                        i -= 1

                    if self.board[i][y] == '.':
                        self.deselect(x, y)
                        self.select(i, y)
                        x = i
                    pygame.time.wait(150)

            if keys[pygame.K_SPACE]:
                if selected:
                    self.clearCell(x, y)
                self.solve()

            pygame.display.update()
            if keys[pygame.K_ESCAPE]:
                run = False
        # pygame.time.wait(5)
        # Render the current text.
        # pygame.display.flip()
        # txt_surface = self.font26.render('closing the game', True, (200, 0, 0), white)
        # self.window.blit(txt_surface, (100, 100))
        # clock.tick(3000)

        pygame.display.quit()
        pygame.quit()


    def drawGrid(self):
        for i, offset in enumerate(range(0, 500, 50)):
            if i == 3 or i == 6:
                thickness = 4
            else:
                thickness = 2
            pygame.draw.line(self.window, black, (50 + offset, 50), (50 + offset, 500), thickness)
            pygame.draw.line(self.window, black, (50, 50 + offset), (500, 50 + offset), thickness)

    def select(self, x, y):
        pygame.draw.rect(self.window, red, ((y + 1) * 50 + 2, (x + 1) * 50 + 2, 47, 47), 2)

    def deselect(self, x, y):
        pygame.draw.rect(self.window, white, ((y + 1) * 50 + 2, (x + 1) * 50 + 2, 48, 48), 4)
        self.drawGrid()  # CleanUp any problems with the border

    def clearCell(self, x, y):
        pygame.draw.rect(self.window, white, ((y + 1) * 50 + 2, (x + 1) * 50 + 2, 48, 48))
        self.drawGrid()  # CleanUp any problems with the border

    def pencil(self, val, x, y):
        self.temp[x][y] = str(val)

        self.clearCell(x, y)
        self.select(x, y)

        text = self.font20.render(self.temp[x][y], True, black, white)
        textRect = text.get_rect(center=((y * 50) + 63, (x * 50) + 64))
        self.window.blit(text, textRect)

    def write(self, val, x, y, color=black):
        self.clearCell(x, y)
        self.board[x][y] = val

        text = self.font26.render(val, True, color, white)
        textRect = text.get_rect(center=((y * 50) + 75, (x * 50) + 75))
        self.window.blit(text, textRect)

    def solve(self):
        rows = defaultdict(set)
        cols = defaultdict(set)
        blocks = defaultdict(set)

        for r in range(9):
            for c in range(9):
                val = self.board[r][c]
                if val != '.':
                    rows[r].add(val)
                    cols[c].add(val)
                    blocks[(r // 3, c // 3)].add(val)

        def get_choices(r, c):
            choices = []
            for d in '123456789':
                if d not in rows[r] and d not in cols[c] and d not in blocks[(r // 3, c // 3)]:
                    choices.append(d)

            return choices

        def get_empty_cell():
            empty = []
            for r in range(9):
                for c in range(9):
                    if self.board[r][c] == '.':
                        choices = get_choices(r, c)
                        empty.append((r, c, choices))

            return min(empty, key=lambda x: len(x[2])) if empty else None

        def fill(r, c, v):
            self.board[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            blocks[(r // 3, c // 3)].add(v)

            self.write(v, r, c, green)
            pygame.display.update()
            pygame.time.wait(50)

        def unfill(r, c, v):
            self.board[r][c] = '.'
            rows[r].remove(v)
            cols[c].remove(v)
            blocks[(r // 3, c // 3)].remove(v)

            self.clearCell(r, c)
            pygame.display.update()
            pygame.time.wait(50)

        def solve_board():
            # if events are not read, pygame will crash
            events = pygame.event.get()

            empty = get_empty_cell()
            if not empty:
                return True

            else:
                r, c, choices = empty
                if not choices:
                    return False

                for choice in choices:
                    fill(r, c, choice)
                    if solve_board():
                        return True
                    else:
                        unfill(r, c, choice)
                return False

        solve_board()

    def GeneratedBoard(self, d='medium'):

        difficulty = {'easy': 4, 'medium': 5, 'hard': 7}

        count = 81
        board = [['.' for _ in range(9)] for _ in range(9)]
        rows = defaultdict(set)
        cols = defaultdict(set)
        blocks = defaultdict(set)

        def get_choices(r, c):
            choices = []
            for d in '123456789':
                if d not in rows[r] and d not in cols[c] and d not in blocks[(r // 3, c // 3)]:
                    choices.append(d)
            return choices

        def get_empty_cell():
            empty = []
            for r in range(9):
                for c in range(9):
                    if board[r][c] == '.':
                        choices = get_choices(r, c)
                        empty.append((r, c, choices))

            return min(empty, key=lambda x: len(x[2])) if empty else None

        while count > 0:
            empty = get_empty_cell()
            if empty:
                r, c, choices = empty
                if choices:
                    v = random.choice(choices)
                    board[r][c] = v
                    rows[r].add(v)
                    cols[c].add(v)
                    blocks[(r // 3, c // 3)].add(v)
                    count -= 1

                else:
                    count = 81
                    board = [['.' for _ in range(9)] for _ in range(9)]
                    rows = defaultdict(set)
                    cols = defaultdict(set)
                    blocks = defaultdict(set)

        solution = deepcopy(board)

        for r in range(9):
            columns = random.sample(list(range(9)), difficulty[d])
            for c in columns:
                board[r][c] = '.'
        return board, solution


if __name__ == '__main__':
    game = Game('hard')



