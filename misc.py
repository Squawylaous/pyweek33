from pygame.math import Vector2 as vector

# just some miscellaneous functions grouped togther so they can be imported anywhere

surface_scale = 300

def get_sign(x):
  return 1 if x>0 else -1 if x<0 else 0

# transforms a vector to position on a surface
def to_surface_pos(pos, size):
  return tuple(map(int, vector(*pos)/size*surface_scale))
