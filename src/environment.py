import sys
import os
from game import Game
import cv2
import logging
logger = logging.getLogger(__name__)

class Environment:
  def __init__(self, rom_file, args):
    self.game = Game()
    if args.display_screen:
      # DO SOME VISUALISATION

    if args.random_seed:
      self.ale.setInt('random_seed', args.random_seed)

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
    for line in self.game.getCellsLog2()
        line = line.map()
    return

  def isTerminal(self):
    return not self.game.canMove()
