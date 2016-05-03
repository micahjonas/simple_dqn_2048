# -*- coding: UTF-8 -*-
import random
import numpy as np

# PY3 compat
try:
    xrange
except NameError:
    xrange = range


class Game(object):
    """
    A 2048 board
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    SIZE = 4

    def __init__(self, size=SIZE, **kws):
        self.__size = size
        self.__size_range = xrange(0, self.__size)
        self.cells = [[0]*self.__size for _ in xrange(self.__size)]
        self.addTile()
        self.addTile()
        self.score = 0
        self.nomove = 0
        self.games = 0
        self.isLogging = False
        self.__statsfile = None

    def size(self):
        """return the board size"""
        return self.__size

    def score(self):
        """return the score"""
        return self.score

    def nomove(self):
        """return the score"""
        return self.nomove

    def canMove(self):
        """
        test if a move is possible
        """
        if not self.filled():
            return True

        for y in self.__size_range:
            for x in self.__size_range:
                c = self.getCell(x, y)
                if (x < self.__size-1 and c == self.getCell(x+1, y)) \
                   or (y < self.__size-1 and c == self.getCell(x, y+1)):
                    return True
        if(self.isLogging):
            self.games += 1
            self.__statsfile.write("Runs: {}\n".format(self.games))
            self.__statsfile.write("Score: {}\n".format(self.score))
            self.__statsfile.write("Moves: {}\n".format(self.nomove))
            self.__statsfile.write("Cells:\n")
            self.__statsfile.write(self.cellsToString(self.getCells()))
            self.__statsfile.write("\n")

        return False

    def filled(self):
        """
        return true if the game is filled
        """
        return len(self.getEmptyCells()) == 0

    def addTile(self, value=None, choices=([2]*9+[4])):
        """
        add a random tile in an empty cell
          value: value of the tile to add.
          choices: a list of possible choices for the value of the tile.
                   default is [2, 2, 2, 2, 2, 2, 2, 2, 2, 4].
        """
        if value:
            choices = [value]

        v = random.choice(choices)
        empty = self.getEmptyCells()
        if empty:
            x, y = random.choice(empty)
            self.setCell(x, y, v)

    def getCells(self):
        """return all the cells"""
        return self.cells

    def __transform(self, number):
        if number == 0:
            return 0
        else:
            return int(np.log2(number))

    def getCellsLog2(self):
        nparr = np.array(self.cells)
        nparr = np.log2(nparr)
        nparr[np.isneginf(nparr)] = 0
        return nparr.astype("uint8")
        #return [[self.__transform(x) for x in line] for line in self.cells]

    def getCell(self, x, y):
        """return the cell value at x,y"""
        return self.cells[y][x]

    def setCell(self, x, y, v):
        """set the cell value at x,y"""
        self.cells[y][x] = v

    def getLine(self, y):
        """return the y-th line, starting at 0"""
        return self.cells[y]

    def getCol(self, x):
        """return the x-th column, starting at 0"""
        return [self.getCell(x, i) for i in self.__size_range]

    def setLine(self, y, l):
        """set the y-th line, starting at 0"""
        self.cells[y] = l[:]

    def setCol(self, x, l):
        """set the x-th column, starting at 0"""
        for i in xrange(0, self.__size):
            self.setCell(x, i, l[i])

    def getEmptyCells(self):
        """return a (x, y) pair for each empty cell"""
        return [(x, y)
                for x in self.__size_range
                for y in self.__size_range if self.getCell(x, y) == 0]

    def __collapseLineOrCol(self, line, d):
        """
        Merge tiles in a line or column according to a direction and return a
        tuple with the new line and the score for the move on this line
        """
        if (d == Game.LEFT or d == Game.UP):
            inc = 1
            rg = xrange(0, self.__size-1, inc)
        else:
            inc = -1
            rg = xrange(self.__size-1, 0, inc)

        pts = 0
        for i in rg:
            if line[i] == 0:
                continue
            if line[i] == line[i+inc]:
                v = line[i]*2
                line[i] = v
                line[i+inc] = 0
                pts += v

        return (line, pts)

    def __moveLineOrCol(self, line, d):
        """
        Move a line or column to a given direction (d)
        """
        nl = [c for c in line if c != 0]
        if d == Game.UP or d == Game.LEFT:
            return nl + [0] * (self.__size - len(nl))
        return [0] * (self.__size - len(nl)) + nl

    def getGrid(self):
        """
        Returns the grid
        """
        return sefl.cells

    def getActionSet(self):
        return [0,1,2,3]

    def reset(self):
        self.__size = Game.SIZE
        self.__size_range = xrange(0, self.__size)
        self.cells = [[0]*self.__size for _ in xrange(self.__size)]
        self.addTile()
        self.addTile()
        self.score = 0
        self.nomove = 0

    def startLogging(self, filename):
        self.games = 0
        self.__statsfile = open(filename, 'w')
        self.isLogging = True

    def stopLogging(self):
        self.isLogging = False
        self.__statsfile.close

    def move(self, d, add_tile=True):
        """
        move and return the grid
        """
        if d == Game.LEFT or d == Game.RIGHT:
            chg, get = self.setLine, self.getLine
        elif d == Game.UP or d == Game.DOWN:
            chg, get = self.setCol, self.getCol
        else:
            return self.cells

        moved = False
        scoreOfRound = 0

        for i in self.__size_range:
            # save the original line/col
            origin = get(i)
            # move it
            line = self.__moveLineOrCol(origin, d)
            # merge adjacent tiles
            collapsed, pts = self.__collapseLineOrCol(line, d)
            # move it again (for when tiles are merged, because empty cells are
            # inserted in the middle of the line/col)
            new = self.__moveLineOrCol(collapsed, d)
            # set it back in the board
            chg(i, new)
            # did it change?
            if origin != new:
                moved = True
                self.nomove += 1
            scoreOfRound += pts

        self.score += scoreOfRound

        # don't add a new tile if nothing changed
        if moved and add_tile:
            self.addTile()
            #print self.cellsToString(self.getCells())

        return scoreOfRound

    def cellsToString(self, cells):
        res = ""
        for line in cells:
            res += " ".join(map(str, line))
            res += "\n"

        return res
