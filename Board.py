from Totem import Totem
import random

class Board:
    def __init__(self,n):
        self.board = [[None for _ in range(n)] for _ in range(n)]
        self.n = n
        self.piecesonboard = []

    def __repr__(self):
        ret = ""
        for x in self.board:
            ret = ret + (str(x) + "\n")
        return ret

    def addPiece(self, totem, x,y):
        if(self.board[x][y]):
            return False
        self.board[x][y] = totem
        self.piecesonboard.append(totem)
        return True

    def adjacent(self,x,y):
        ret = []
        size = len(self.board)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if(i == 0 and j == 0):
                    continue
                idx_x = x + i
                idx_y = y + j
                print(idx_x,idx_y)
                if(idx_x < size and idx_x >= 0 and
                   idx_y < size and idx_y >= 0):
                   ret.append(self.board[idx_x][idx_y])
        return ret

    def diagonalLeft(self):
        ret = []
        for i in range(len(self.board)):
            ret.append(self.board[i][i])
        return ret

    def diagonalRight(self):
        ret = []
        size = len(self.board)
        for i in range(size):
            ret.append(self.board[size-i-1][i])
        return ret

    def columns(self):
        ret = []
        temp = zip(*self.board)
        for row in temp:
            ret.append(row)
        return ret

    def rows(self):
        ret = []
        for i in self.board:
            ret.append(i)
        return ret

    def emptyspaces(self):
        ret = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] is None:
                    ret.append([i,j])
        return ret

    def piecelocation(self,piece):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == piece:
                    return (i,j)
        return False

    def duplicatesexist(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                for k in range(len(self.board)):
                    for l in range(len(self.board)):
                        if (not (i == k)) and (not (j == l)):
                            p = self.board[i][j]
                            q = self.board[k][l]
                            if (p is not None and q is not None and p == q):
                                return True
        return False
