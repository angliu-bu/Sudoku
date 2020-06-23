from collections import defaultdict


class Board:

    def __init__(self, board):
        self.board = board

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

        def unfill(r, c, v):
            self.board[r][c] = '.'
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
