import pygame
from pygame import *


class Driver(sprite.Sprite):
    def __init__(self, nerve, reacTime, direction):
        sprite.Sprite.__init__(self)
        self.nerve = nerve
        self.rTime = reacTime
        self.dir = direction    #there is only one direction in oneRoad model.
    def check (self):
        print ''


