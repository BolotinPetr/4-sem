import pygame
import Road
import Driver as Driver
import random
from pygame import *

bg_color = "#FF6262"
ROAD_WIDTH = 44
ROAD_HEIGHT = 44
ROAD_COLOR = "GREY"
BG_COLOR = (0, 0, 0)
level = [
       "-------------------------",
       "-           f           -",   # 'l' - light, '.' - road, 's' - start, 'f' - finish, 'b' - branch
       "-           .           -",
       "-           .           -",
       "-      W...S.           -",
       "-      .   ..           -",
       "--     .   ..           -",
       "-      .   S.           -",
       "-      s   ..           -",
       "-          l.           -",
       "-   f......32k.......E  -",
       "-   W.....k41.....f  .  -",
       "-   .      .l        .  -",
       "-   .      ..        s  -",
       "-   s      ..           -",
       "-          ..           -",
       "-          f.           -",
       "-           s           -",
       "-------------------------"]


class Space:
    def __init__(self):
        self.size = self.width, self.height = 1000, 800
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        pygame.display.set_caption('Model')
        self.bg = Surface((self.width, self.height))
        self.objects = pygame.sprite.Group()  # need to draw all objects.
        self.branchBlocks = pygame.sprite.Group() # need for easy linking with drivers.
        self.leaders = pygame.sprite.Group() # we need to find leader.
        self.drivers = pygame.sprite.Group()
        self.finishPoints = pygame.sprite.Group()
        x = y = 0
        for row in level:
            for col in row:
                if col == '.':
                    road = Road.RoadBlock(x, y)
                    self.objects.add(road)
                if col == 'l':
                    light = Road.Light(x, y, (0,1), "WHITE")
                    self.objects.add(light)
                    self.branchBlocks.add(light)
                    self.leaders.add(light)
                if col == 'k':
                    light = Road.Light(x, y, (0,1), "RED")
                    self.objects.add(light)
                    self.branchBlocks.add(light)
                    self.leaders.add(light)
                """if col == 's':
                    driver = Driver.Driver(0, 0.1, (0, 1), x, y, self.branchBlocks, self.leaders, self.drivers)
                    self.drivers.add(driver)
                    self.leaders.add(driver)"""
                if col == 'f':
                    finish = Road.FinishPoint(x, y)
                    self.objects.add(finish)
                    self.branchBlocks.add(finish)
                    self.leaders.add(finish)
                    self.finishPoints.add(finish)
                if col == '1':
                    branches = ((0, -1), (1, 0))
                if col == '2':
                    branches = ((0, -1), (-1, 0))
                if col == '3':
                    branches = ((-1, 0), (0, 1))
                if col == '4':
                    branches = ((1, 0), (0, 1))
                if (col == '1') or (col == '2') or (col == '3') or (col == '4'):
                    light = Road.BranchPoint(x, y, branches)
                    self.leaders.add(light)
                    self.branchBlocks.add(light)
                    self.objects.add(light)
                if col == 'W':
                    branches = ((1, 0), (1, 0))
                if col == 'E':
                    branches = ((-1, 0), (-1, 0))
                if col == 'N':
                    branches = ((0, -1), (0, -1))
                if col == 'S':
                    branches = ((0, 1), (0, 1))
                if (col == 'W') or (col =='E') or (col == 'N') or (col == 'S'):
                    branch = Road.BranchPoint(x, y, branches)
                    self.leaders.add(branch)
                    self.branchBlocks.add(branch)
                    self.objects.add(branch)
                x += ROAD_WIDTH
            y += ROAD_HEIGHT
            x = 0

    def calculate(self, change_light):
        def generate_driver():
            if random.randint(1, 10000) < 20:
                x = y = 0
                for row in level:
                    for col in row:
                        if col == 's':
                            driver = Driver.Driver(0, 0.4, (0, -1), x, y, self.branchBlocks, self.leaders, self.drivers)
                            if sprite.spritecollideany(driver, self.drivers) is None:
                                self.drivers.add(driver)
                                self.leaders.add(driver)
                                for d in self.drivers:
                                    d.driver_add(driver)
                        x += ROAD_WIDTH
                    y += ROAD_HEIGHT
                    x = 0
        # delete driver when he reaches finish
        for finish in self.finishPoints:
            for driver in self.drivers:
                if sprite.collide_rect(driver, finish):
                    self.drivers.remove(driver)
                    self.leaders.remove(driver)
                    for dr in self.drivers:
                        dr.delete(driver)
        generate_driver()
        self.objects.update(change_light)
        self.drivers.update()

    def render(self, change_light):
        self.bg.fill((0, 133, 0))
        self.screen.blit(self.bg, (0,0))
        self.objects.draw(self.screen)
        self.drivers.draw(self.screen)

