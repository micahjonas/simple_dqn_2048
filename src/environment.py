import sys
import os
from game import Game
import cv2
import logging
logger = logging.getLogger(__name__)

class Environment:
  def __init__(self, rom_file, args):
    self.game = Game()

    #if args.display_screen:

      # DO SOME VISUALISATION

    #if args.random_seed:
      #self.ale.setInt('random_seed', args.random_seed)

    self.actions = self.game.getActionSet()
    logger.info("Using full action set with size %d" % len(self.actions))

    logger.debug("Actions: " + str(self.actions))

    self.dims = (args.screen_height, args.screen_width)

  def numActions(self):
    return len(self.actions)

  def restart(self):
    self.game.reset()

  def act(self, action):
    reward = self.game.move(self.actions[action])

    return reward

  def getScreen(self):
    return self.game.getCellsLog2()

  def isTerminal(self):
    if(self.game.canMove()):
        return False
    else:
        #print "Game ended!"
        #print "Score:"
        #print self.game.score
        #print "Number of moves: "
        #print self.game.nomove
        #print "Cells"
        #print self.game.cellsToString(self.game.getCells())
        return True
