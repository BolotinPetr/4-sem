import pygame
from pygame import *

ROAD_WIDTH = 32
ROAD_HEIGHT = 32
ROAD_COLOR = "#FF6262"

level = [
       "-------------------------",
       "-                       -",   # x - light, . - road, s - start, f - finish
       "-           f           -",
       "-           .           -",
       "-           .           -",
       "-           .           -",
       "--          .           -",
       "-           .           -",
       "-           .           -",
       "-           .  x        -",
       "-           .           -",
       "-           .           -",
       "-           .           -",
       "-           .           -",
       "-           .           -",
       "-           .           -",
       "-           s           -",
       "-                       -",
       "-                       -",
       "-------------------------"]

class Level:
       def __init__(self, screen):
              self.screen = screen

       def render(self):
              x = y = 0
              for row in level:
                     for col in row:
                            if col == '.':
                                   road = Surface((ROAD_WIDTH,ROAD_HEIGHT))
                                   road.fill(Color(ROAD_COLOR))
                                   self.screen.blit(road,(x,y))

                            x = x + ROAD_WIDTH
                     y = y + ROAD_HEIGHT
                     x = 0