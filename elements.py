from math import ceil, floor
import operator as op
import pygame
from pygame.math import Vector2 as vector

from misc import *


# class for anything the player can interact with, will be packaged into a maze
# most attributes should be immutable, save for anything in self.flags
class element:
  def __init__(self, pos, **flags):
    self.pos = vector(pos)
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
  
  def draw(self, surface, size):
    pass


# class for walls, subclasses element
class Wall(element):
  def __init__(self, pos, **flags):
    super().__init__(pos, **flags)
    self.horiz = not self.pos.x%1
    self.verti = not self.pos.y%1
    self.rotation = vector(self.verti, self.horiz)
  
  def draw(self, surface, size):
    start = to_surface_pos(map(floor, self.pos), size) - self.rotation*26
    stop = to_surface_pos(map(ceil, self.pos), size) + self.rotation*26
    pygame.draw.line(surface, foreground, start, stop, 55)


# class for one-way walls, subclasses Wall
class OneWayWall(Wall):
  action = {"is":{"?":"direction", "T":None, "F":{"stop":"before"}}}
  
  def __init__(self, pos, **flags):
    pos, self.direction = (vector(pos[0])+vector(pos[1]))/2, vector(pos[2])
    super().__init__(pos, **flags)
  
  def draw(self, surface, size):
    start = to_surface_pos(map(floor, self.pos), size) - self.rotation*26
    stop = to_surface_pos(map(ceil, self.pos), size) + self.rotation*26
    # 0 1 2 3 4 5 6 7 8 9 a b c d e f g h i
    # -----------   ---------   -----------
    midpoints = [0, 5, 7, 11, 13, 18]
    midpoints = zip(*[iter([int_vector(start.lerp(stop, i/max(midpoints))) for i in midpoints])]*2)
    for a, b in midpoints:
      pygame.draw.line(surface, foreground, a, b, 55)
    arrow = map(op.add, [start.lerp(stop, i) for i in (2/5, 0.5, 3/5)], [i*self.direction*100 for i in (-2.5, 0, -2.5)])
    pygame.draw.lines(surface, foreground, 0, [*map(int_vector, arrow)], 40)


# decorator for creating element subclasses for tiles that activate when landed on
def Plate(subcls):
  subcls.action = {"if":{"?":"landed", "T":subcls.action, "F":None}}
  return subcls


# class for finish tile, subclasses element
@Plate
class Finish(element):
  action = {"finish":None}
  
  def __init__(self, pos, **flags):
    super().__init__(pos, **flags)
  
  def draw(self, surface, size):
    draw_rect = pygame.rect.Rect((0,0), surface_scale*0.75)
    draw_rect.center = to_surface_pos(self.pos, size)
    pygame.draw.rect(surface, foreground, draw_rect)
