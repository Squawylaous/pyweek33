import pygame
from pygame.locals import *
from pygame.math import Vector2 as vector

# just some miscellaneous functions grouped togther so they can be imported anywhere

background = Color(0, 0, 0)
foreground = Color(255, 255, 255)
update_rects = []

get_sign = lambda x: 1 if x>0 else -1 if x<0 else 0
int_vector = lambda x:(int(round(x.x)), int(round(x.y)))
ratio_vector = lambda x:vector(x)/max(x)
group_dict = lambda dict_: {i:dict_[key] for key in dict_ for i in key}
post_event = lambda event: pygame.event.post(pygame.event.Event(event))

# variables to store constant values
UI_offset = vector(0, 50) # how much space the UI needs
surface_scale_real = vector() # size of mazes scaled to fit screen
surface_scale = vector(1000, 1000) # size of mazes
surface_padding = vector(100, 100) # empty space around a surface
MAINMENU = USEREVENT + 0
LEVELSELECT = USEREVENT + 1
NEXTLEVEL = USEREVENT + 2
LOSE = USEREVENT + 3
WIN = USEREVENT + 4
direction_keys = group_dict({(K_UP, K_w):(0, -1), (K_DOWN, K_s):(0, 1), (K_LEFT, K_a):(-1, 0), (K_RIGHT, K_d):(1, 0)})
all_levels = [f"l{i}" for i in range(1, 7)] # all levels, in order

# transforms a vector to position on a surface
to_surface_pos = lambda pos, size: int_vector(surface_scale.elementwise()*vector(*pos)+surface_padding/2)


# singleton, esentally a dict w/ some dynamic values
class level_names_class:
  # keys are level codes (used internally) and values are displayed names
  def __init__(self, start=0):
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
  
  @property
  def current(self):
    return self[all_levels[self.current_level]]


# basically a mix of javasctipt objects and default dicts, just for convience
class container:
  def __init__(self, default=None, **kwargs):
    self._default = default
    for key, value in kwargs.items():
      setattr(self, key, value)
  
  def __getattr__(self, name):
    return self._default
  
  def __repr__(self):
    return f"container<{self.dict}>"
  
  @property
  def dict(self):
    return self.__dict__
  
  def update(self, other=None, override=False, **kwargs):
    if other is None:
      other = {}
    elif isinstance(other, container):
      other = other.dict
    kwargs.update(other)
    for key, value in kwargs.items():
      if override or (key != "_default" and key not in self.dict):
        setattr(self, key, value)


# class for UI buttons the user can select. instances are groups
class button:
  def __init__(self, screen, func, init_func, amount, size, center, **options):
    self.func = func
    self.size = vector(size)
    self.amount = vector(amount)
    self.rect = pygame.rect.Rect((0,0), self.size.elementwise()*(self.amount))
    self.rect.center = center
    self.surface = screen.subsurface(self.rect)
    self.options = {value.pos:init_func(self, container(name=key, **value.dict)) for key, value in options.items()}
    self.highlighted = None
  
  def select(self, choice=None):
    if choice is None:
      choice = self.highlighted
    self.func(self, self.options[tuple(choice)])
  
  def move(self, direction):
    if self.highlighted is None:
      self.highlighted = vector()
    else:
      self.highlighted += direction
      self.highlighted = vector([(h+a)%a for h, a in zip(self.highlighted, self.amount)])
  
  def draw(self):
    for option in self.options.values():
      option.surface.blit(option.background, (0,0))
    if self.highlighted is not None:
      pygame.draw.rect(self.surface, foreground, self.options[tuple(self.highlighted)].rect, 5)
    pygame.display.flip() # temporary workaround
    update_rects.append(self.rect)
