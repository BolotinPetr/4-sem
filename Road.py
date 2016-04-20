from pygame import *
ROAD_WIDTH = 44
ROAD_HEIGHT = 44
ROAD_COLOR = "GREY"
BRANCH_COLOR = "RED"
max_velocity = 10


class RoadBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((ROAD_WIDTH, ROAD_HEIGHT))
        self.image.fill(Color(ROAD_COLOR))
        self.rect = Rect(x, y, ROAD_WIDTH, ROAD_HEIGHT)


class BranchPoint(RoadBlock):
    def __init__(self, x, y, branches):
        RoadBlock.__init__(self, x, y)
        self.image.fill(Color(BRANCH_COLOR))
        self.branches = branches
        self.color = ROAD_COLOR
        self.vx = 0
        self.vy = 0
        self.x = x
        self.y = y
        self.type = 'branch'

    def update(self, change_light):
        self.image.fill(Color(self.color))


class FinishPoint(BranchPoint):
    def __init__(self, x, y):
        BranchPoint.__init__(self, x, y, (1, 1))
        self.color = "BLUE"
        self.x = x
        self.y = y
        self.vx = max_velocity
        self.vy = max_velocity
        self.type = 'finish'

    def update(self, change_light):
        self.image.fill(Color(self.color))


class Light(BranchPoint):
    def __init__(self, x, y, branches, color):
        BranchPoint.__init__(self, x, y, branches)
        self.color = color
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.type = 'light'
        self.rect = Rect(x, y, ROAD_WIDTH, ROAD_HEIGHT)

    def update(self, change_light):
        if change_light:
            if self.color == "WHITE":
                self.color = "RED"
                self.vx = 0
                self.vy = 0
            else:
                if self.color == "RED":
                    self.color = "WHITE"
                    self.vx = max_velocity
                    self.vy = max_velocity
        self.image.fill(Color(self.color))
