import asyncio
import pygame
import sys


class Game(object):
    def __init__(self, window, glbls, start_state):
        self.done = False
        self.window = window
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.glbls = glbls
        self.state = self.glbls['STATES'][start_state]
        self.state.startup()

    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self):
        self.state.done = False
        self.state = self.glbls['STATES'][self.state.next_state]
        self.state.startup()

    def update(self, dt):
        if self.state.quit:
            self.done = True

        elif self.state.done:
            self.flip_state()

        self.state.update(dt)

    def draw(self):
        self.state.draw(self.window)

    async def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()
            await asyncio.sleep(0)
        # Closing the game
        pygame.quit()
        sys.exit()
