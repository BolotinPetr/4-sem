from numpy import random
from pygame import *
import math
from timeit import Timer
DRIVER_WIDTH = 44
DRIVER_HEIGHT = 44
DRIVER_COLOR = "BLACK"
ROAD_WIDTH = 44
max_velocity = 4
dt = 0.1


class Driver(sprite.Sprite):
    def __init__(self, nerve, reac_time, direction, x, y, branches, leaders, drivers):
        sprite.Sprite.__init__(self)
        self.nerve, self.rTime, self.dir, self.color = nerve, reac_time, direction, DRIVER_COLOR
        self.x, self.y, self.vx, self.vy, self.ax, self.ay = x, y, 0, 0, 0, 0
        self.acceleration = 1
        self.image = Surface((DRIVER_WIDTH, DRIVER_HEIGHT))
        self.image.fill(Color(DRIVER_COLOR))
        self.rect = Rect(self.x, self.y, DRIVER_WIDTH, DRIVER_HEIGHT)
        self.leaders = leaders.copy()
        self.leader = None
        self.branch_points = branches.copy()
        self.unchangeable_branch_points = branches.copy()
        self.drivers = drivers.copy()
        self.type = 'driver'
        self.drivers.remove(self)
        self.dir_light = None

    def driver_add(self, driver):
        self.drivers.add(driver)

    def save_dir_light(self):
        if sprite.spritecollideany(self, self.unchangeable_branch_points) is None:
            self.dir_light = self.dir

    def choose_direction(self):
        a = True
        for b in self.branch_points:
            if (b.rect.contains(self)) or ((b.type == 'light') and (sprite.collide_rect(self, b))):
                if b.type == 'light':
                    self.dir = self.dir
                else:
                    if self.dir_light == self.dir:
                        self.dir = b.branches[random.randint(0, 2)]
                    else:
                        while a:
                            rand = random.randint(0, 2)
                            if b.branches[rand] != (-1*self.dir_light[0], -1*self.dir_light[1]):
                                a = False
                                self.dir = b.branches[rand]
                self.branch_points.remove(b)
                self.leaders.remove(b)

    def find_the_leader(self):
        x0, y0, a = self.x, self.y, True
        while a:
            if self.y < 0:
                a = False
            self.x += self.dir[0] * 5
            self.y += self.dir[1] * 5
            self.rect = Rect(self.x, self.y, ROAD_WIDTH, ROAD_WIDTH)
            # driver.leaders.remove(driver)
            for leader in self.leaders:
                if (self.rect.contains(leader.rect))\
                        or (leader.rect.contains(self.rect)) or sprite.collide_rect(self, leader):
                    a = False
                    self.leader = leader
        self.x, self.y = x0, y0

    def check_next_driver(self):
        def two_directions(direction):
            if direction[0] == 0:
                x_1, x_2 = 1, -1
            else:
                x_1 = x_2 = 0
            if direction[1] == 0:
                y_1, y_2 = 1, -1
            else:
                y_1 = y_2 = 0
            return (x_1, y_1), (x_2, y_2)
        if (self.leader is not None) and (self.leader.type != 'driver'):
            x0, y0, a = self.leader.x, self.leader.y, True
            x1 = x2 = x0
            y1 = y2 = y0
            while a:
                if (abs(x1 - x0) > DRIVER_WIDTH*2)\
                        or (abs(y1 - y0) > DRIVER_WIDTH*2):
                    return self.leader
                else:
                    dir1, dir2 = two_directions(self.dir)
                    x1 += dir1[0]
                    y1 -= dir1[1]
                    x2 += dir2[0]
                    y2 -= dir2[1]
                    rect1 = Rect(x1, y1, DRIVER_WIDTH*2, DRIVER_HEIGHT*2)
                    rect2 = Rect(x1, y1, DRIVER_WIDTH*2, DRIVER_HEIGHT*2)
                    for dr in self.drivers:
                        if (dr.rect.contains(rect1) or dr.rect.contains(rect2))\
                                and ((abs(self.dir[0] * (dr.vx - self.vx)) < 0)
                                     or (abs(self.dir[1] * (dr.vy - self.vy)) < 0)):
                            return dr
            return self.leader
        else:
            return self.leader

    def distance (self, leader):
            d = math.sqrt((self.x - leader.x)**2 + (self.y - leader.y)**2)
            return d

    def calculate_acceleration(self):
            lead = self.leader
            if abs(self.vx) < 0.01:
                self.vx = 0
            if abs(self.vy) < 0.01:
                self.vy = 0
            if abs(self.vx) > max_velocity:
                self.vx = max_velocity
            if abs(self.vy) > max_velocity:
                self.vy = max_velocity
            if (lead is None) or (lead.color == "WHITE") or (lead.color  == "BLUE")\
                    or (lead.color == "GREY"):
                dx = dy = 0
            else:
                dx = DRIVER_WIDTH * 1.5 + self.rTime * abs(self.vx) + \
                     abs(self.vx * (abs(self.vx) - abs(lead.vx))) / (2 * self.acceleration)
                dy = DRIVER_WIDTH * 1.5 + self.rTime * abs(self.vy) + \
                     abs(self.vy * (abs(self.vy) - abs(lead.vy))) / (2 * self.acceleration)
            if self.x != lead.x:
                self.ax = self.acceleration * (1 - abs(self.vx / max_velocity) \
                                               - (dx / abs(abs(self.x) - abs(lead.x))) ** 2)
            if self.y != lead.y:
                self.ay = self.acceleration * (1 - abs(self.vy / max_velocity) \
                                               - (dy / abs(abs(self.y) - abs(lead.y))) ** 2)
            if abs(self.ay) > 3:
                self.ay = 3
            if abs(self.ax) > 3:
                self.ax = 3
            self.ax, self.ay = self.dir[0] * self.ax, self.dir[1] * self.ay

    def road_empty(self):
        def distance (a, b, p1, p2):
            d = math.sqrt((p1 * (a.x - b.x))**2 + (p2 * (a.y - b.y))**2)
            return d

        def near_branch():
            nearest = self
            if self.dir[0] == 0:
                for area in self.branch_points:
                    if (0 < distance(self.leader, area, 1, 1) < distance(self.leader, nearest, 1, 1))\
                            and (self.leader.y == area.y):
                        nearest = area
                    else:
                        nearest = nearest
            else:
                for area in self.branch_points:
                    if (0 < distance(self.leader, area, 1, 1) < distance(self.leader, nearest, 1, 1))\
                            and (self.leader.x == area.x):
                        nearest = area
                    else:
                        nearest = nearest
            if nearest is self:
                return self.leader
            else:
                return nearest
        # near_branch_point = near_branch()
        d = self.distance(self.leader)
        if (self.leader.type != 'driver') and (0 <= d < DRIVER_HEIGHT * 2):
            main_collide = sprite.spritecollideany(self.leader, self.drivers)
            # near_collide = sprite.spritecollideany(near_branch_point, self.drivers)
            if main_collide is None:
                return True
            else:
                return False
        else:
            return True

    def crossroad(self):
        if (self.leader.type == 'light') or (self.leader.type == 'branch'):
            return True
        else:
            return False

    def move(self, a):
        if a is False:
            self.ax = self.vx = 0
        else:
            if self.dir[0] == 0:
                self.vx = 0
                self.x += 0
            else:
                self.vx += self.ax * dt
                if abs(self.vx) > 0:
                    self.x += self.vx * dt
            if self.dir[1] == 0:
                self.vy = 0
                self.y += 0
            else:
                self.vy += self.ay * dt
                if abs(self.vy) > 0:
                    self.y += self.vy * dt

    # interface method

    def update(self):
        self.save_dir_light()
        self.drivers.remove(self)
        # t1 = Timer(lambda : self.choose_direction())
        # t2 = Timer(lambda : self.find_the_leader())
        # t3 = Timer(lambda : self.check_next_driver())
        # t4 = Timer(lambda : self.calculate_acceleration())
        # print t1.timeit(number=1), t2.timeit(number=1), t4.timeit(number=1)
        self.choose_direction()
        self.find_the_leader()
        # self.leader = self.check_next_driver()
        self.calculate_acceleration()
        # print self.dir, self.dir_light
        if self.crossroad():
            if self.road_empty():
                self.move(True)
            else:
                self.move(False)
        else:
            self.move(True)

        self.rect = Rect(self.x, self.y, DRIVER_WIDTH, DRIVER_HEIGHT)
        self.image.fill(Color(self.color))    # main #

    def delete(self, driver):
        self.drivers.remove(driver)
        self.leaders.remove(driver)
        driver.drivers.empty()
        driver.leaders.empty()
        driver.branch_points.empty()
