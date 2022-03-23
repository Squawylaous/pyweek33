import pygame
from pygame.locals import *
from pygame.math import Vector2 as vector

# just some miscellaneous functions grouped togther so they can be imported anywhere

background = Color(0, 0, 0)
foreground = Color(255, 255, 255)
update_rects = []

group_dict = lambda dict_: {i:dict_[key] for key in dict_ for i in key}
post_event = lambda event: pygame.event.post(pygame.event.Event(event))

# variables to store constant values
UI_offset = vector(25, 50) # how much space the UI needs
surface_scale_real = vector() # size of mazes scaled to fit screen
surface_scale = vector(1000, 1000) # size of mazes
surface_padding = vector(100, 100) # empty space around a surface
NEXTLEVEL = USEREVENT + 0
direction_keys = group_dict({(K_UP, K_w):"up", (K_DOWN, K_s):"down", (K_LEFT, K_a):"left", (K_RIGHT, K_d):"right"})
all_levels = ["l1"] # all levels, in order

def get_sign(x):
  return 1 if x>0 else -1 if x<0 else 0

# transforms a vector to position on a surface
def to_surface_pos(pos, size):
  return tuple(map(int, surface_scale.elementwise()*vector(*pos)+surface_padding/2))


# singleton, esentally a dict w/ some dynamic values
class level_names_class:
  # keys are level codes (used internally) and values are displayed names
  def __init__(self, start=-1):
    self.data = {}
    self.current_level = start
  
  def __getitem__(self, key):
    try:
      return self.data[key]
    except KeyError:
      pass
    if key[0] == "l":
      self.data[key] = "Level "+key[1:]
    return self.data[key]
  
  def __next__(self):
    self.current_level += 1
    return all_levels[self.current_level]


# basically a mix of javasctipt objects and default dicts, just for convience
class container:
  def __init__(self, default=None, **kwargs):
    self._default = default
    for key, value in kwargs.items():
      setattr(self, key, value)
  
  def __getattr__(self, name):
    return self._default
  
  def update(self, other):
    for key, value in other.__dict__.items():
      if key != "_default" and key not in self.__dict__:
        setattr(self, key, value)
