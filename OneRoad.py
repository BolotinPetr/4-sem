import Space
import pygame


class Model:
    def __init__(self, N):
        self._running = True
        self.clock = pygame.time.Clock()
        self.space = Space.Space()
        self.N = N

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            self.exit()
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                self.exit()

    def calculate(self, change_light):
        self.space.calculate(change_light)

    def render(self, change_light):
        self.space.render(change_light)
        pygame.display.flip()

    def exit(self):
        self._running = False

    def cleanup(self):
        pygame.quit()

    def execute(self):
        time = 0
        change_light = False
        while self._running:
            for event in pygame.event.get():
                self.event_handler(event)
            current_time = pygame.time.get_ticks()/1000
            # we need this because our light mustn't change colour every cycle, only every N seconds
            if current_time - time == self.N:
                time = current_time
                change_light = True
            self.calculate(change_light)
            self.render(change_light)
            change_light = False
        self.cleanup()

if __name__ == "__main__":
    model = Model(20)
    model.execute()
