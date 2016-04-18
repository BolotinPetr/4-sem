import pygame
from pygame import *


class Driver(sprite.Sprite):
    def __init__(self, nerve, reacTime, direction):
        sprite.Sprite.__init__(self)
        self.nerve = nerve
        self.rTime = reacTime
        self.dir = direction    #there is only one direction in oneRoad model.

    def find_the_leader(self):
        x0, y0, a = self.x, self.y, True
        while a:
            if self.y < 0:
                a = False
            self.x += self.dir[0]
            self.y -= self.dir[1]
            self.rect = Rect(self.x, self.y, ROAD_WIDTH+10*self.dir[0], ROAD_WIDTH+10*self.dir[1])
            #driver.leaders.remove(driver)
            for leader in self.leaders:
                if (self.rect.contains(leader.rect))\
                        or (leader.rect.contains(self.rect)):
                    a = False
                    self.leader = leader
        self.x, self.y = x0, y0


