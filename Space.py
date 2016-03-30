import pygame
import Level
#import Light
from pygame import *

class Space:
    def __init__(self):
        self.size = self.width, self.height = 800, 640
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        pygame.display.set_caption('Game')
        self.level = Level.Level(self.screen)
        #self.light = Light(self.screen)

    def render(self):
        self.level.render()