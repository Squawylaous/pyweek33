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

# transforms a vector to position on a surface
def to_surface_pos(pos):
  return tuple(map(int, pos*20+10))


# class for entities that can move and stuff
class entity:
  def __init__(self, pos, maze=None):
    self.pos = vector(pos)
    self.maze = maze

  def move(self, direction):
    dir_dict = {"up":vector(0, -1), "down":vector(0, 1), "left":vector(1, 0), "right":vector(-1, 0)}
    direction = dir_dict[direction]/2
    stop = False
    for dist in range(self.maze.size):
      self.pos += direction
      if maze[self.pos]:
        action = getattr(maze[self.pos], "action", {"stop":"before"})
        for i in action:
          if i == "stop":
            stop = True
            if action[i] == "before":
              self.pos -= direction
            elif action[i] == "return":
              self.pos -= direction*dist
      if stop:
        break


# class for anything the player can interact with, will be packaged into a maze
# most attributes should be immutable, seve for anything in self.flags
class element:
  def __init__(self, pos, **flags):
    self.pos = pos
    self.flags = {"active":True}
    self.flags.update(flags)
  
  def __str__(self):
    return f"element@({self.x}, {self.y})"
  
  @property
  def x(self):
    return self.pos.x
  
  @property
  def y(self):
    return self.pos.y
  
  def draw(self, surface):
    pass


# class for walls, subclasses element
class wall(element):
  def __init__(self, pos, **flags):
    super().__init__(pos, **flags)
    self.horiz = not self.pos.x%1
    self.verti = not self.pos.y%1
  
  def draw(self, surface):
    pass


# splits a wall into walls of length 1
def split_wall(wall):
  a, b = wall
  a = vector(a)
  b = vector(b)
  diff = vector(*map(get_sign, b - a))
  new_a, new_b = a, a+diff
  while True:
    yield (new_a + new_b)/2
    if new_b == b:
      return
    new_a, new_b = new_b, new_b+diff


# class for mazes, just a collection for walls
class maze:
  all = {};
  def __init__(self, name, size=None, *, walls):
    self.name = name.split("_")
    self.perm_walls = [*map(wall, chain(*chain(*[map(split_wall, [wall[i:i+2] for i in range(len(wall)-1)]) for wall in walls])))]
    self.perm_walls = [*map(wall, chain(*map(split_wall, chain(*[[wall[i:i+2] for i in range(len(wall)-1)] for wall in walls]))))]
    self.toggle_walls = []
    if self.name[0] not in maze.all:
      maze.all[self.name[0]] = {}
    if size is None:
      all_pos = [*map(op.attrgetter("pos"), self.elements)]
      chain(map(op.attrgetter("x"), all_pos), map(op.attrgetter("y"), all_pos))
    maze.all[self.name[0]][self.name[1]] = self
    self.surface = pygame.Surface()

  def __getitem__(self, item):
    for element in self.elements:
      if item == element.pos:
        return elements
  
  @property
  def elements(self):
    return chain(self.perm_walls, self.toggle_walls)
  
  def draw(self):
    for element in self.elements:
      element.draw(self.surface)


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

maze("l1_p", size=7,
     walls=[((1, 1), (1, 6), (4, 6), (4, 7), (5, 7), (5, 6), (6, 6), (6, 1), (3, 1), (3, 0), (2, 0), (2, 1), (1, 1)),
            ((3, 1), (3, 2), (4, 2)), ((2, 2), (2, 3), (3, 3), (3, 5), (4, 5)), ((1, 4), (2, 4)),
            ((2, 5), (2, 6)), ((5, 5), (6, 5)), ((4, 4), (6, 4)), ((4, 3), (6, 3)), ((5, 2), (5, 3))]
)
maze("l1_t", size=7,
     walls=[((1, 1), (1, 6), (4, 6), (4, 7), (5, 7), (5, 6), (6, 6), (6, 1), (3, 1), (3, 0), (2, 0), (2, 1), (1, 1)),
            ((2, 1), (2, 3)), ((1, 4), (3, 4), (3, 3)), ((3, 2), (4, 2), (4, 4)), ((2, 6), (2, 5), (4, 5)),
            ((5, 2), (5, 3), (6, 5)), ((5, 4), (5, 6))]
)
