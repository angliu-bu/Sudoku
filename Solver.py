from collections import defaultdict
def solveBoard(board):

    rows = defaultdict(set)
    cols = defaultdict(set)
    blocks = defaultdict(set)

    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num != '.':
                rows[r].add(num)
                cols[c].add(num)
                blocks[(r // 3, c // 3)].add(num)


    def getChoices(r, c):
        choices = []
        for d in '123456789':
            if d not in rows[r] and d not in cols[c] and d not in blocks[(r // 3, c // 3)]:
                choices.append(d)

        return choices


    def getEmpty():
        empty = []

        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    choices = getChoices(r, c)
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


    def solve():
        empty = getEmpty()
        if not empty:
            return True
        else:
            r, c, choices = empty
            if not choices:
                return False

            for choice in choices:
                fill(r, c, choice)
                if solve():
                    return True
                else:
                    unfill(r, c, choice)
            return False


    solve()