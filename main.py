import operator as op
import pygame
from pygame.locals import *
from pygame import Vector2 as vector

pygame.init()

background = Color(0, 0, 0)
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
screen_rect = screen.get_rect()
screen.fill(background)


# class for entities that can move and stuff
class entity:
    def __init__(self, pos, maze=None):
        self.pos = vector(pos)
        self.maze = maze

    def move(self, direction):
        if direction == "up":
            direction = vector(0, -1)
        elif direction == "down":
            direction = vector(0, 1)
        elif direction == "left":
            direction = vector(1, 0)
        elif direction == "right":
            direction = vector(-1, 0)
        self.pos += direction/2
        for i in range(self.maze.size):
            if self.pos in maze:
                break
            self.pos += direction
        self.pos -= direction/2


# class for walls, will be packaged into a maze
class wall:
    def __init__(self, a, b=None):
        if b is None:
            a, b = a
        self.a, self.b = vector(a), vector(b)
        self.midpoints = self._midpoints()

    # returns a list of midpoints that the player can collide with
    def _midpoints(self):
        diff = self.b - self.a
        return [self.a+(i+0.5 if diff.x else 0, i+0.5 if diff.y else 0) for i in range(int(diff.x+diff.y))]

    def __contains__(self, item):
        return vector(item) in self.midpoints


# class for mazes, just a collection for walls
class maze:
    def __init__(self, *walls, size):
        self.walls = [*map(wall, walls)]
        self.size = size

    def __contains__(self, item):
        for wall in self.walls:
            if item in wall:
                return True
        return False


lvl1p = maze(((0, 0), (0, 5)), ((0, 5), (3, 5)), ((4, 5), (5, 5)), ((5, 5), (5, 0)), ((5, 0), (2, 0)), ((1, 0), (0, 0)),
             ((2, 0), (2, 1)), ((2, 1), (3, 1)), ((1, 1), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 4)), ((2, 4), (3, 4)),
             ((0, 3), (1, 3)), ((1, 4), (1, 5)), ((4, 4), (5, 4)), ((3, 3), (5, 3)), ((3, 2), (5, 2)), ((4, 1), (4, 2)),
             size=5)
lvl1t = maze(((0, 0), (0, 5)), ((0, 5), (3, 5)), ((4, 5), (5, 5)), ((5, 5), (5, 0)), ((5, 0), (2, 0)), ((1, 0), (0, 0)),
             ((1, 0), (1, 2)), ((0, 3), (2, 3)), ((2, 3), (2, 2)), ((2, 1), (3, 1)), ((3, 1), (3, 3)), ((1, 5), (1, 4)),
             ((1, 4), (3, 4)), ((4, 1), (4, 2)), ((4, 2), (5, 4)), ((4, 3), (4, 5)), size=5)
print((2.5, 1) in lvl1p)
