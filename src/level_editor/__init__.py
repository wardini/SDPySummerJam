import asyncio
import pygame

from level_editor.constants import glbls

# importing the game states
from level_editor.game import Game
from level_editor.editor import Editor

# initializing pygame and setting the screen resolution
pygame.init()
screen = pygame.display.set_mode((glbls['WIDTH'], glbls['HEIGHT']))
pygame.display.set_caption(f"Constellation Editor")

# Game states
glbls['STATES'] = {
    "EDITOR"     : Editor(glbls),
}
glbls["GAME"] = Game(screen, glbls, glbls["start_state"])

# Game class instance
asyncio.run(glbls["GAME"].run())
