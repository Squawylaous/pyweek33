import operator as op
from itertools import chain
from math import ceil, floor
import pygame
from pygame.locals import *
from pygame.math import Vector2 as vector

import elements
import misc
from misc import *

pygame.init()
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
screen_rect = screen.get_rect()

# surfaces to draw mazes on
main_surface_rect = pygame.rect.Rect(UI_offset, vector(screen_rect.size)-UI_offset)
main_surface = screen.subsurface(main_surface_rect)

# variables to store constant values
surface_scale.x = min(main_surface_rect.w/2, main_surface_rect.h)
surface_scale.y = surface_scale.x
surface_scale_padded += surface_scale
twin_pos = -(surface_scale_padded-(main_surface_rect.w/2, main_surface_rect.h))/2
player_pos = twin_pos + (main_surface_rect.w/2, 0)

# variables for storing references to data, can be updated
player = None
twin = None
current_level_p = None
current_level_t = None

# class for entities that can move and stuff
class entity:
  all = []
  
  def __init__(self, maze, isPlayer, draw):
    self.maze, self.isPlayer, self._draw = maze, isPlayer, draw
    self.pos = self.maze.start
    entity.all.append(self)
    self.surface = pygame.Surface(surface_scale/self.maze.size)
    self.rect = self.surface.get_rect()

  def move(self, direction):
    dir_dict = {"up":vector(0, -1), "down":vector(0, 1), "left":vector(1, 0), "right":vector(-1, 0)}
    direction = dir_dict[direction]/2
    do = container(check_ifs=[])
    for dist in range(self.maze.size):
      self.pos += direction
      if maze[self.pos]:
        do = entity.act(getattr(maze[self.pos], "action", {"stop":"before"}), check_ifs=do.check_ifs)
        self.pos += do.move
      if do.stop:
        break
    if do.finish:
      print("win" if self.isPlayer else "lose")
  
  def draw(self):
    self._draw(self)
    self.maze.blit(self.surface, to_surface_pos(self.pos-(0.5, 0.5), self.maze.size))
  
  @staticmethod
  def act(action, *, check_ifs=None):
    if action is None:
      action = {}
    do = container(move=vector(), check_ifs=[])
    for i in action:
      if i in ["stop", "finish"]:
        setattr(do, i, True)
      if i == "stop":
        if action[i] == "before":
          do.move = -direction
        elif action[i] == "return":
          do.move = -direction*dist
      elif i == "if":
        do.check_ifs.append(action[i])
    
    for check_if in check_ifs:
      if check_if["?"] == "landed":
        entity.act(check_if["T" if do.stop else "F"])
    
    return do


# class for mazes, just a collection for walls
class maze:
  all = {};
  def __init__(self, name, size=None, start=(0,0), finish=(0,0), *, walls):
    self.name = name.split("_")
    walls = chain(*[zip(wall, wall[1:]) for wall in walls])
    self.perm_walls = [*map(elements.Wall, chain(*map(split_wall, walls)))]
    self.toggle_walls = []
    if size is None:
      all_pos = {*chain(*map(op.attrgetter("pos"), self.elements))}
      size = max(all_pos) - min(all_pos)
    self.size = size
    self.start, self.finish = vector(start), elements.Finish(finish)
    
    if self.name[0] not in maze.all:
      maze.all[self.name[0]] = {}
    maze.all[self.name[0]][self.name[1]] = self
    self.background = pygame.Surface(surface_scale_padded)
    for element in self.still_elements:
      element.draw(self.background, self.size)
    self.surface = pygame.Surface(surface_scale_padded)
    self.rect = self.surface.get_rect()

  def __getitem__(self, item):
    for element in self.elements:
      if item == element.pos:
        return elements
  
  @property
  def elements(self):
    return chain(self.perm_walls, self.toggle_walls)
  
  @property
  def still_elements(self):
    return chain(self.perm_walls)
  
  @property
  def anim_elements(self):
    return chain(self.toggle_walls)

  def draw(self):
    self.surface.blit(self.background, (0,0))
    for element in self.anim_elements:
      element.draw(self.surface, self.size)


# functions for drawing entities
def draw_entity(color):
  color = Color(color)
  
  def draw_square(self):
    draw_rect = pygame.rect.Rect((0,0), vector(self.rect.size)*0.75)
    draw_rect.center = self.rect.center
    pygame.draw.rect(self.surface, color, draw_rect)
  
  return container(square=draw_square)


# splits a wall into walls of length 1
def split_wall(wall):
  a, b = wall
  a = vector(a)
  b = vector(b)
  diff = vector(*map(get_sign, b - a))
  new_a, new_b = a, a+diff
  for i in range(int(abs(sum(b-a)))):
    yield (new_a + new_b)/2
    if new_b == b:
      return
    new_a, new_b = new_b, new_b+diff


# loads and initalizes a level
def load_level(level):
  global player, twin, current_level_p, current_level_t
  screen.fill(background)
  current_level_p = maze.all[level]["p"]
  current_level_t = maze.all[level]["t"]
  player = entity(current_level_p, True, draw_entity((161,161,161)).square)
  twin = entity(current_level_t, False)
  current_level_p.draw()
  current_level_t.draw()
  player.draw()
  twin.draw()
  main_surface.blit(current_level_p.surface, player_pos)
  main_surface.blit(current_level_t.surface, twin_pos)
  update_rects.append(main_surface_rect)

level_names = level_names_class()

maze("l1_p", size=7, start=(4.5, 6.5), finish=(2.5,0.5),
     walls=[((1, 1), (1, 6), (4, 6), (4, 7), (5, 7), (5, 6), (6, 6), (6, 1), (3, 1), (3, 0), (2, 0), (2, 1), (1, 1)),
            ((3, 1), (3, 2), (4, 2)), ((2, 2), (2, 3), (3, 3), (3, 5), (4, 5)), ((1, 4), (2, 4)),
            ((2, 5), (2, 6)), ((5, 5), (6, 5)), ((4, 4), (6, 4)), ((4, 3), (6, 3)), ((5, 2), (5, 3))]
)
maze("l1_t", size=7, start=(4.5, 6.5), finish=(2.5,0.5),
     walls=[((1, 1), (1, 6), (4, 6), (4, 7), (5, 7), (5, 6), (6, 6), (6, 1), (3, 1), (3, 0), (2, 0), (2, 1), (1, 1)),
            ((2, 1), (2, 3)), ((1, 4), (3, 4), (3, 3)), ((3, 2), (4, 2), (4, 4)), ((2, 6), (2, 5), (4, 5)),
            ((5, 2), (5, 3), (6, 3)), ((5, 4), (5, 6))]
)

pygame.event.post(pygame.event.Event(NEXTLEVEL))

while True:
  if pygame.event.get(QUIT):
    break
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_RETURN:
        pygame.event.post(pygame.event.Event(NEXTLEVEL))
      elif event.key == K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))
    elif event.type == NEXTLEVEL:
      load_level(next(level_names))
  
  pygame.display.update(update_rects)
  update_rects = []
pygame.quit()
