from game import Game
import numpy as np
import random

def cellsToString(cells):
    res = ""
    for line in cells:
        res += " ".join(map(str, line))
        res += "\n"
    return res

def transform(number):
    if number == 0:
        return 0
    else:
        return int(np.log2(number))

def log2(cells):
    return [[transform(x) for x in line] for line in cells]

game = Game()

print cellsToString(game.getCells())

while game.canMove():
    #move = raw_input("Enter move [0-3]: ")
    move = random.choice([0,1,2,3])
    print "-------"
    print "Move: " + str(move)
    reward = game.move(int(move))
    print "Reward: " + str(reward)
    print ""
    print cellsToString(game.getCells())
    print ""
    print cellsToString(game.getCellsLog2())
    print ""
    print "Score: " + str(game.score)

print "Game ended"
print game.score
print cellsToString(game.getCells())

print "Test Reset"
game.reset()
print game.score
print cellsToString(game.getCells())
