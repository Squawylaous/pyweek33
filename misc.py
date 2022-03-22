from pygame.locals import *
from pygame.math import Vector2 as vector

# just some miscellaneous functions grouped togther so they can be imported anywhere

background = Color(0, 0, 0)
foreground = Color(255, 255, 255)
update_rects = []

# variables to store constant values
surface_scale = 300
NEXTLEVEL = USEREVENT + 0
all_levels = ["l1"] # all levels, in order

# variables for storing references to data, can be updated
current_level = -1
player = None
twin = None
current_level_p = None
current_level_t = None

def get_sign(x):
  return 1 if x>0 else -1 if x<0 else 0

# transforms a vector to position on a surface
def to_surface_pos(pos, size):
  return tuple(map(int, vector(*pos)/size*surface_scale+(5,5)))


# singleton, esentally a dict w/ some dynamic values
class level_names_class:
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
  
  def __next__(self):
    global current_level
    current_level += 1
    return all_levels[current_level]
