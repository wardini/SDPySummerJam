# Pygame Summer Jam 2024

import asyncio
from global_dict import glbls
import pygame
import sys

glbls['Full Screen'] = False
if len(sys.argv) > 1:
    glbls['Full Screen'] = (sys.argv[1] == 'full')

from game import Game
from gameplay import Gameplay

pygame.init()

glbls['STATES'] = {
    "Gameplay": Gameplay(glbls),
}

game = Game(glbls)
asyncio.run(game.run())
