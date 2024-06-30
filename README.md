# San Diego Python Pygame Summer Jam contest entry.
## June 29, 2024
The theme of this game jam is "Interstellar".
Our brainstorming session led us toward a game about visualizing
and tracing constellations in the night sky.

A typical game loop in pygame looks like this:

```
    async def run(self):
        pgclk = pygame.time.Clock()

        while not self.done:
            for event in pygame.event.get():
                self.state.process_event(event)
            dt = pgclk.tick(60)
            self.update(dt)
            self.state.draw(self.window)
            pygame.display.update()

        # Closing the game
        pygame.quit()
```

## These things happen over and over in the game loop
- Process events (mouse clicks, keyboard presses etc)
- get the time passed since the last loop and limit frame rate
- Update all the game states (run game logic, move players, play sounds, etc.)
- Draw all the graphics
- Update the screen

A typical element in the game has these methods

- Initialization
  - Location of the item
  - whatever is unique about this element
- reset (for replay of the level)
- update(dt)  Update movement or states (dt is in milliseconds)
- render(window)  Draw the item to the graphics window
