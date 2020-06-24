import random
from collections import defaultdict

import Game
board = [[".",".","9","7","4","8",".",".","."],
         ["7",".",".",".",".",".",".",".","."],
         [".","2",".","1",".","9",".",".","."],
         [".",".","7",".",".",".","2","4","."],
         [".","6","4",".","1",".","5","9","."],
         [".","9","8",".",".",".","3",".","."],
         [".",".",".","8",".","3",".","2","."],
         [".",".",".",".",".",".",".",".","6"],
         [".",".",".","2","7","5","9",".","."]]

def GeneratedBoard(k):
    board = [['.'for _ in range(9)] for _ in range(9)]
    rows = defaultdict(set)
    cols = defaultdict(set)
    blocks = defaultdict(set)
    numList = list('123456789')
    indexList = list('02345678')

    def fill(c, r, v):
        board[r][c] = v
        rows[r].add(v)
        cols[c].add(v)
        blocks[(r // 3, c // 3)].add(v)


    while k >0:
        num = random.choice(numList)
        r = int(random.choice(indexList))
        c = int(random.choice(indexList))
        if board[r][c] == '.':
            if num not in rows[r] and num not in cols[c] and num not in blocks[(r // 3, c // 3)] and len(blocks[(r // 3, c // 3)]) <= 5:
                fill(c, r, num)
                k -= 1
    return board

game = Game.Board(board)

