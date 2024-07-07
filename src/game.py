import asyncio
import pygame

class Game:
    def __init__(self, glbls):
        self.done = False
        self.glbls = glbls
        self.glbls['frame_rate']="0"
        self.state = self.glbls['STATES'][self.glbls['start_state']]
        self.state.startup()

    def update(self,dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.state.done = False
            self.state = self.glbls['STATES'][self.state.next_state]
            self.state.startup()
        self.state.update(dt)

    async def run(self,window):
        pgclk = pygame.time.Clock()

        while not self.done:
            for event in pygame.event.get():
                self.state.process_event(event)
            dt = pgclk.tick(60)
            self.update(dt)
            self.state.draw(window)
            self.glbls['frame_rate']=f"{pgclk.get_fps():4.1f}"
            pygame.display.update()
            await asyncio.sleep(0)

        # Closing the game
        pygame.quit()
