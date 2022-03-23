from pygame.locals import *
from pygame.math import Vector2 as vector

# just some miscellaneous functions grouped togther so they can be imported anywhere

background = Color(0, 0, 0)
foreground = Color(255, 255, 255)
update_rects = []

# variables to store constant values
UI_offset = vector(25, 50) # how much space the UI needs
surface_scale = vector() # size of mazes
surface_padding = vector(10, 10) # empty space around a surface
surface_scale_padded = surface_scale+surface_padding
NEXTLEVEL = USEREVENT + 0
all_levels = ["l1"] # all levels, in order

def get_sign(x):
  return 1 if x>0 else -1 if x<0 else 0

# transforms a vector to position on a surface
def to_surface_pos(pos, size):
  return tuple(map(int, surface_scale.elementwise()*vector(*pos)/size+surface_padding/2))


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
    [setattr(self, key, value) for key, value in kwargs.items()]
  
  def __getattr__(self, name):
    return self._default
