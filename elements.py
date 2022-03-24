from math import ceil, floor
import pygame
from pygame.math import Vector2 as vector

from misc import *


# class for anything the player can interact with, will be packaged into a maze
# most attributes should be immutable, seve for anything in self.flags
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
  
  def draw(self, surface, size):
    start = to_surface_pos(map(floor, self.pos), size) - vector(self.verti, self.horiz)*26
    stop = to_surface_pos(map(ceil, self.pos), size) + vector(self.verti, self.horiz)*26
    pygame.draw.line(surface, foreground, start, stop, 55)


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
