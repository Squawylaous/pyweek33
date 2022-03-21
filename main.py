import operator as op
from itertools import chain
import pygame
from pygame.locals import *
from pygame.math import Vector2 as vector

pygame.init()

background = Color(0, 0, 0)
foreground = Color(255, 255, 255)
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
screen_rect = screen.get_rect()
screen.fill(background)

def get_sign(x):
  return 1 if x>0 else -1 if x<0 else 0


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
# most attributes should be immutable, seve for anything ending in self.flags
class wall:
  def __init__(self, a, b=None, **flags):
    if b is None:
      a, b = a
    self.a, self.b = vector(a), vector(b)
    self.collidepoint = (self.a+self.b)/2
    self.horiz = self.a.x == self.b.x
    self.verti = self.a.y == self.b.y
    self.flags = {"active":True}
    self.flags.update(flags)

# splits a wall into walls of length 1
def split_wall(wall):
  a, b = wall
  a = vector(a)
  b = vector(b)
  diff = vector(*map(get_sign, b - a))
  new_a, new_b = a, a+diff
  while True:
    yield new_a, new_b
    if new_b == b:
      return
    new_a, new_b = new_b, new_b+diff


# class for mazes, just a collection for walls
class maze:
  all = {};
  def __init__(self, name, *, walls):
    self.name = name
    self.perm_walls = [*map(wall, chain(*map(split_wall, walls)))]
    if self.name not in maze.all:
      maze.all[self.name] = []
    maze.all[self.name].append(self)

  def __contains__(self, item):
    for wall in self.walls:
      if item == wall.collidepoint:
        return True
    return False
  
  @property
  def walls(self):
    return chain(self.perm_walls, self.temp_walls, self.toggle_walls)


# variables/objects to store constant values
class level_names_class:
  # singleton, esentally a dict w/ some dynamic values
  # keys are level codes (used internally) and values are displayed names
  def __init__(self):
    self.data = {}
  
  def __getitem__(self, key):
    try:
      return self.data[key]
    except KeyError:
      pass
    if key[0] == "l":
      self.data[key] = "Level "+key[1:]
    return self.data[key]


level_names = level_names_class()
print(level_names["l1"])

maze("l1p",
     walls=[
            ((0, 0), (0, 5)), ((0, 5), (3, 5)), ((4, 5), (5, 5)), ((5, 5), (5, 0)), ((5, 0), (2, 0)), ((1, 0), (0, 0)),
            ((2, 0), (2, 1)), ((2, 1), (3, 1)), ((1, 1), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 4)), ((2, 4), (3, 4)),
            ((0, 3), (1, 3)), ((1, 4), (1, 5)), ((4, 4), (5, 4)), ((3, 3), (5, 3)), ((3, 2), (5, 2)), ((4, 1), (4, 2))]
)
maze("l1t",
     walls=[
            ((0, 0), (0, 5)), ((0, 5), (3, 5)), ((4, 5), (5, 5)), ((5, 5), (5, 0)), ((5, 0), (2, 0)), ((1, 0), (0, 0)),
            ((1, 0), (1, 2)), ((0, 3), (2, 3)), ((2, 3), (2, 2)), ((2, 1), (3, 1)), ((3, 1), (3, 3)), ((1, 5), (1, 4)),
            ((1, 4), (3, 4)), ((4, 1), (4, 2)), ((4, 2), (5, 4)), ((4, 3), (4, 5))]
)
