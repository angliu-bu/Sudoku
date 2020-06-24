import random
from collections import defaultdict
from copy import deepcopy
import pygame

class Board:

    def __init__(self, board=None):
        if board:
            self.board = board
        else:
            self.board = GeneratedBoard(40)

        for row in self.board:
            print(row)

        self.temp = deepcopy(self.board)
        self.solution = deepcopy(self.board)

        self.solve(self.solution)

        print('\n')
        for row in self.solution:
            print(row)

        self.launchGUI()

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

    def launchGUI(self):

        # Start the game
        pygame.init()

        # Fonts
        font26 = pygame.font.Font(None, 26)
        font20 = pygame.font.Font(None, 20)

        # Colors
        black = (0, 0, 0)
        white = (211, 211, 211)
        red = (255, 0, 0)
        green = (21, 119, 40)

        # Create Window
        size = 550, 550
        window = pygame.display.set_mode(size)
        window.fill(white)
        pygame.display.set_caption("Sudoku")
        pygame.display.flip()
        # Place numbers
        for x, row in enumerate(self.board):
            for y, value in enumerate(row):
                if value != '.':
                    text = font26.render(self.board[x][y], True, black, white)
                    textRect = text.get_rect(center=((y * 50) + 75, (x * 50) + 75))
                    window.blit(text, textRect)

        def drawGrid():
            for i, offset in enumerate(range(0, 500, 50)):
                if i == 3 or i == 6:
                    thickness = 4
                else:
                    thickness = 2
                pygame.draw.line(window, black, (50 + offset, 50), (50 + offset, 500), thickness)
                pygame.draw.line(window, black, (50, 50 + offset), (500, 50 + offset), thickness)

        def select(x, y):
            pygame.draw.rect(window, red, ((y + 1) * 50 + 2, (x + 1) * 50 + 2, 47, 47), 2)

        def deselect(x, y):
            pygame.draw.rect(window, white, ((y + 1) * 50 + 2, (x + 1) * 50 + 2, 48, 48), 4)
            drawGrid()  # CleanUp any problems with the border

        def clearCell(x, y):
            pygame.draw.rect(window, white, ((y + 1) * 50 + 2, (x + 1) * 50 + 2, 48, 48))
            drawGrid()  # CleanUp any problems with the border

        def pencil(val, x, y):
            self.temp[x][y] = str(num + 1)

            clearCell(x, y)
            select(x, y)

            text = font20.render(self.temp[x][y], True, black, white)
            textRect = text.get_rect(center=((y * 50) + 63, (x * 50) + 64))
            window.blit(text, textRect)

        def write(val, x, y, color=black):
            clearCell(x, y)
            self.board[x][y] = val

            text = font26.render(val, True, color, white)
            textRect = text.get_rect(center=((y * 50) + 75, (x * 50) + 75))
            window.blit(text, textRect)

        def showSolution():
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

                write(v, r, c, green)
                pygame.display.update()
                pygame.time.wait(50)

            def unfill(r, c, v):
                self.board[r][c] = '.'
                rows[r].remove(v)
                cols[c].remove(v)
                blocks[(r // 3, c // 3)].remove(v)

                clearCell(r, c)
                pygame.display.update()
                pygame.time.wait(50)

            def solve_board():
                events = pygame.event.get()
                keys = pygame.key.get_pressed()

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

        drawGrid()

        selected = False
        run = True
        while run:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:

                    # remove previous selection
                    if selected:
                        deselect(x, y)

                    # get new selection
                    y, x = pygame.mouse.get_pos()
                    x, y = x // 50 - 1, y // 50 - 1

                    # display selection
                    if 0 <= x < 9 and 0 <= y < 9 and self.board[x][y] == '.':
                        select(x, y)
                        selected = True

            if selected:
                # Check for user input
                for num, pressed in enumerate(keys[49:58]):
                    if pressed:
                        pencil(num + 1, x, y)

                # Check for delete
                if keys[pygame.K_DELETE] and self.temp[x][y] != '.':
                    clearCell(x, y)
                    select(x, y)

                # Confirm selection
                if keys[pygame.K_RETURN] and self.temp[x][y] == self.solution[x][y]:
                    write(self.temp[x][y], x, y)
                    selected = False

            if keys[pygame.K_SPACE]:
                if selected:
                    clearCell(x, y)
                showSolution()

            pygame.display.update()
            if keys[pygame.K_ESCAPE]:
                run = False

        pygame.quit()


    def solve(self, board):
        rows = defaultdict(set)
        cols = defaultdict(set)
        blocks = defaultdict(set)

        for r in range(9):
            for c in range(9):
                val = board[r][c]
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
                    if board[r][c] == '.':
                        choices = get_choices(r, c)
                        empty.append((r, c, choices))

            return min(empty, key=lambda x: len(x[2])) if empty else None

        def fill(r, c, v):
            board[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            blocks[(r // 3, c // 3)].add(v)



        def unfill(r, c, v):
            board[r][c] = '.'
            rows[r].remove(v)
            cols[c].remove(v)
            blocks[(r // 3, c // 3)].remove(v)

        def solve_board():
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

def generateBoard(ratio):
    board = [['.' for _ in range(9)] for _ in range(9)]

    count = (81 * ratio) // 100
    numList = '123456789'
    indexList = '012345678'

    rows = defaultdict(set)
    cols = defaultdict(set)
    blocks = defaultdict(set)

    def fill(r, c, v):
        board[r][c] = v
        rows[r].add(v)
        cols[c].add(v)
        blocks[(r // 3, c // 3)].add(v)

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val != '.':
                rows[r].add(val)
                cols[c].add(val)
                blocks[(r // 3, c // 3)].add(val)

    while count > 0:
        num = random.choice(numList)
        r = int(random.choice(indexList))
        c = int(random.choice(indexList))

        if board[r][c] == '.':
            if num not in rows[r] and num not in cols[c] and num not in blocks[(r // 3, c // 3)] and len(blocks[(r // 3, c // 3)]) <= 5:
                fill(c, r, num)
                count -= 1

    return board

