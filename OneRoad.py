import Space
import pygame

class Model:
    def __init__(self):
        self._running = True
        self.space = Space.Space()

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            self.exit()
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                self.exit()

    def calculate(self):
        self.space.calculate()

    def render(self):
        self.space.render()
        pygame.display.flip()

    def exit(self):
        self._running = False

    def cleanup(self):
        pygame.quit()

    def execute(self):
        while(self._running):
            for event in pygame.event.get():
                self.event_handler(event)
            #self.calculate()
            self.render()
        self.cleanup()

if __name__ == "__main__":
    model = Model()
    model.execute()
