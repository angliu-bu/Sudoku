from collections import defaultdict
import random

# initialized board




def GenerateBoard:
    def __init__(self):
        self.board = [['.']*9]*9

        self.rows = defaultdict(set)
        self.cols = defaultdict(set)
        self.blocks = defaultdict(set)
        self.numList = list('123456789')
        self.indexList = list('02345678')

    def fillBoard(self
    num = random.choice(self.numList)
    r = random.choice(self.indexList)
    c = random.choice(self.indexList)
    if self.board[r][c] == '.':
        if num not in self.rows[r] and d not in self.cols[c] and d not in self.blocks[(r // 3, c // 3)]:
            self.fill(c, r, num)

    def fill(self, c, r, v):
        self.board[r][c] = v
        self.rows[r].add(v)
        self.cols[c].add(v)
        self.blocks[(r // 3, c // 3)].add(v)

    def unfill(self, r, c, v):
        self.board[r][c] = '.'
        self.rows[r].remove(v)
        self.cols[c].remove(v)
        self.blocks[(r // 3, c // 3)].remove(v)






