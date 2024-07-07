# Pygame Summer Jam 2024

import pygame
import asyncio
from global_dict import glbls
import sys

glbls['Full Screen'] = False
if len(sys.argv) > 1:
    glbls['Full Screen'] = (sys.argv[1] == 'full')

from game import Game
from gameplay import Gameplay

pygame.init()
pygame.display.set_caption(f"San Diego Python:  Pygame Summer Game Jam")
if glbls['Full Screen']:
    window = pygame.display.set_mode((glbls['WIDTH'], glbls['HEIGHT']), flags=pygame.SCALED)
else:
    window = pygame.display.set_mode((glbls['WIDTH'], glbls['HEIGHT']))

glbls['STATES'] = {
    "Gameplay": Gameplay(glbls),
}

game = Game(glbls)
asyncio.run(game.run(window))
