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
font = pygame.font.SysFont("", 75)
screen.blit(font.render("Loading...", 1, foreground), (0, screen_rect.h-font.size("Loading...")[1]))
pygame.display.flip()
current_state = container(screen="menu")


# surface to draw mazes on
main_surface_rect = pygame.rect.Rect(UI_offset, vector(screen_rect.size)-UI_offset)
main_surface = screen.subsurface(main_surface_rect)

# variables to store constant values
surface_scale_real.x = min(main_surface_rect.w/2, main_surface_rect.h)
surface_scale_real.y = surface_scale_real.x
twin_pos = -(surface_scale_real-(main_surface_rect.w/2, main_surface_rect.h))/2
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
    self.pos = vector(self.maze.start)
    self.maze.player = self
    entity.all.append(self)
    self.surface = pygame.Surface(surface_scale*0.75)
    self.rect = self.surface.get_rect()

  def move(self, direction):
    direction = vector(direction)/2
    do = container(check_ifs=[])
    for dist in range(self.maze.size*2):
      self.pos += direction
      if self.maze[self.pos]:
        do = entity.act(self.maze[self.pos], getattr(self.maze[self.pos], "action", {"stop":"before"}),
                        check_ifs=do.check_ifs, direction=direction)
        self.pos += do.move
      if do.stop:
        break
    if do.finish:
      post_event((LOSE, WIN)[self.isPlayer])
  
  def draw(self):
    self._draw(self)
    self.maze.surface.blit(self.surface, to_surface_pos(self.pos-(0.375, 0.375), self.maze.size))
  
  @staticmethod
  def act(element, action, *, check_ifs=[], direction=vector(), do=None):
    if action is None:
      action = {}
    if do is None:
      do = container(move=vector(), check_ifs=[])
    for i in action:
      if i in ["stop", "finish"]:
        setattr(do, i, True)
      if i == "stop":
        if action[i] == "before":
          do.move = -direction
      elif i == "is":
        if action[i]["?"] == "direction":
          entity.act(element, action[i]["T" if vector(*map(get_sign, direction)) == element.direction else "F"],
                     direction=direction, do=do)
      elif i == "if":
        do.check_ifs.append((element, action[i]))
    
    for element, check_if in check_ifs:
      if check_if["?"] == "landed":
        #TODO: fix
        entity.act(element, check_if["T" if do.stop else "F"], direction=direction, do=do)
    
    return do


# class for mazes, just a collection for walls
class Maze_class:
  all = {};
  def __init__(self, name, pos, size=None, start=(0,0), finish=(0,0), *, walls, one_way_walls=[]):
    self.name = name
    self.start, self.finish = vector(start), elements.Finish(finish)
    walls = chain(*[zip(wall, wall[1:]) for wall in walls])
    self.perm_walls = [*map(elements.Wall, chain(*map(split_wall, walls)))]
    self.one_way_walls = [*map(elements.OneWayWall, one_way_walls)]
    self.toggle_walls = []
    self.plates = [self.finish]
    if size is None:
      all_pos = {*chain(*map(op.attrgetter("pos"), self.elements))}
      size = max(all_pos) - min(all_pos)
    self.size = size
    self.background = pygame.Surface(surface_scale*self.size+surface_padding)
    for element in self.still_elements:
      element.draw(self.background, self.size)
    self.surface = pygame.Surface(surface_scale*self.size+surface_padding)
    self.rect = pygame.rect.Rect(pos, surface_scale_real)
    self.scaled_surface = main_surface.subsurface(self.rect)

  def __getitem__(self, item):
    item = vector(item)
    for element in self.elements:
      if item == element.pos:
        return element
  
  @property
  def elements(self):
    return chain(self.still_elements, self.anim_elements)
  
  @property
  def still_elements(self):
    return chain(self.plates, self.perm_walls, self.one_way_walls)
  
  @property
  def anim_elements(self):
    return chain(self.toggle_walls)

  def draw(self):
    self.surface.blit(self.background, (0,0))
    for element in self.anim_elements:
      element.draw(self.surface, self.size)
    self.player.draw()
    pygame.transform.scale(self.surface, self.rect.size, self.scaled_surface)


# functions for drawing entities
def draw_entity(color):
  color = Color(*color)
  
  def draw_square(self):
    draw_rect = pygame.rect.Rect((0,0), vector(self.rect.size))
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


level_names = level_names_class()
def goto_level(level=None):
  if level is None:
    level = level_names.current_level
  level_names.current_level = level-1
  return level_names.current_level

# decorator function for button_init functions
def button_init(func):
  def init_func(self, choice):
    choice = func(self, choice)
    choice.rect = pygame.rect.Rect(self.size.elementwise()*choice.pos, self.size)
    choice.surface = self.surface.subsurface(choice.rect)
    choice.background = pygame.Surface(self.size)
    choice.text = pygame.transform.scale(font.render(choice.text, 1, foreground),
                                         int_vector(ratio_vector(font.size(choice.text))*max(self.size*0.75)))
    choice.background.blit(choice.text, (self.size-choice.text.get_rect().size)/2)
    return choice
  return init_func

# initalizes each menu button
@button_init
def menu_button_init(self, choice):
  return choice

# initalizes each level select button
@button_init
def select_button_init(self, choice):
  choice.text = level_names[choice.name]
  choice.event = NEXTLEVEL
  return choice

# decorator function for button functions
def button_func(func):
  def _func(self, choice):
    func(self, choice)
    post_event(choice.event)
  return _func

# called when a menu button is selected
@button_func
def menu_button_func(self, choice):
  if choice.event == NEXTLEVEL:
    goto_level({"start":0, "cont":level_names.current_level}[choice.name])

# called when a level select button is selected
@button_func
def select_button_func(self, choice):
  goto_level(all_levels.index(choice.name))

menu_buttons = button(screen, menu_button_func, menu_button_init, (1, 4), (300, 100), screen_rect.center,
                      start=container(text="Start New Game", pos=(0, 0), event=NEXTLEVEL),
                      cont=container(text="Continue Game", pos=(0, 1), event=NEXTLEVEL),
                      select=container(text="Level Select", pos=(0, 2), event=LEVELSELECT),
                      exit=container(text="Exit Game", pos=(0, 3), event=QUIT)
)

row_size = 3
select_buttons = button(screen, select_button_func, select_button_init, (row_size, len(all_levels)/row_size),
                        vector(screen_rect.size)*0.875/max(len(all_levels)//row_size, row_size),
                        screen_rect.center, **{all_levels[i]:container(pos=(i%row_size, i//row_size)) for i in range(len(all_levels))})

# returns decorator function
def load_screen(current_screen):
  # decorator function, updates current_state
  def load_decorator(func):
    def load_func(*args, **kwargs):
      current_state.screen=current_screen
      screen.fill(background)
      func(*args, **kwargs)
      update_rects.append(screen_rect)
    return load_func
  return load_decorator

# loads the menu screen
@load_screen("menu")
def load_menu():
  menu_buttons.draw()

# loads the level select screen
@load_screen("select")
def load_select():
  select_buttons.draw()

# loads and initalizes a level
@load_screen("level")
def load_level(level):
  global player, twin, current_level_p, current_level_t
  current_level_p = Maze_class.all[level]["p"]()
  current_level_t = Maze_class.all[level]["t"]()
  player = entity(current_level_p, True, draw_entity((161, 161, 161)).square)
  twin = entity(current_level_t, False, draw_entity((161, 130, 130)).square)
  level_text = level_names.current
  screen.blit(font.render(level_text, 1, foreground), (screen_rect.w/2 - font.size(level_text)[0]/2, UI_offset.y))
  update_level()

# updates the current level display
def update_level():
  current_level_p.draw()
  current_level_t.draw()
  update_rects.append(main_surface_rect)

# creates a function that creates and returns a new maze object when called
def maze(name, *args, **kwargs):
  name = name.split("_")
  if name[0] not in Maze_class.all:
    Maze_class.all[name[0]] = {}
  Maze_class.all[name[0]][name[1]] = lambda:Maze_class(name, *args, **kwargs)

# all of the mazes for each level (didn't have time to put this in a .txt file or something so it's here)
#level 1
maze("l1_p", player_pos, size=7, start=(3.5, 5.5), finish=(5.5, 1.5),
     walls=[((1, 1), (1, 6), (6, 6), (6, 1), (1, 1)),
            ((1, 3), (2, 3)), ((3, 3), (4, 3), (4, 4), (3, 4), (3, 3)), ((5, 3), (6, 3)), ((2, 2), (5, 2))]
)
maze("l1_t", twin_pos, size=7, start=(3.5, 5.5), finish=(5.5, 1.5),
     walls=[((1, 1), (1, 6), (6, 6), (6, 1), (1, 1)),
            ((1, 3), (2, 3)), ((3, 3), (4, 3), (4, 4), (3, 4), (3, 3)), ((5, 3), (6, 3)), ((2, 2), (6, 2)), ((5, 1), (5, 2))]
)
#level 2
maze("l2_p", twin_pos, size=7, start=(3.5, 5.5), finish=(5.5, 1.5),
     walls=[((1, 1), (1, 6), (6, 6), (6, 1), (1, 1)),
            ((1, 3), (2, 3)), ((3, 3), (4, 3), (4, 4), (3, 4), (3, 3)), ((5, 3), (6, 3)), ((2, 2), (5, 2))]
)
maze("l2_t", twin_pos, size=7, start=(3.5, 5.5), finish=(5.5, 1.5),
     walls=[((1, 1), (1, 6), (6, 6), (6, 1), (1, 1)),
            ((1, 3), (2, 3)), ((3, 5), (3, 3), (4, 3), (4, 5)), ((5, 3), (6, 3)), ((1, 5), (2, 5), (2, 6)), ((5, 6), (5, 5), (6, 5))]
)
#level 3
maze("l3_p", player_pos, size=7, start=(4.5, 6.5), finish=(2.5, 0.5),
     walls=[((1, 1), (1, 6), (4, 6), (4, 7), (5, 7), (5, 6), (6, 6), (6, 1), (3, 1), (3, 0), (2, 0), (2, 1), (1, 1)),
            ((3, 2), (4, 2)), ((2, 2), (2, 3), (3, 3), (3, 5), (4, 5)), ((1, 4), (2, 4)),
            ((2, 5), (2, 6)), ((5, 5), (6, 5)), ((4, 4), (6, 4)), ((4, 3), (6, 3)), ((5, 2), (5, 3))],
     one_way_walls=[((3,1), (3,2), (-1, 0))]
)
maze("l3_t", twin_pos, size=7, start=(4.5, 6.5), finish=(2.5, 0.5),
     walls=[((1, 1), (1, 6), (4, 6), (4, 7), (5, 7), (5, 6), (6, 6), (6, 1), (3, 1), (3, 0), (2, 0), (2, 1), (1, 1)),
            ((2, 1), (2, 3)), ((1, 4), (3, 4), (3, 3)), ((3, 2), (4, 2), (4, 4)), ((2, 6), (2, 5), (4, 5)),
            ((5, 2), (5, 3), (6, 3)), ((5, 4), (5, 6))]
)
#level 4
maze("l4_p", player_pos, size=7, start=(1.5, 0.5), finish=(5.5, 6.5),
     walls=[((2, 1), (6, 1), (6, 7), (5, 7), (5, 6), (1, 6), (1, 0), (2, 0), (2, 2)),
            ((1, 3), (2, 3)), ((2, 5), (2, 6)), ((3, 5), (3, 4), (4, 4)), ((5, 4), (5 ,6)),
            ((4, 2), (4, 3), (5, 3), (5, 1))]
)
maze("l4_t", twin_pos, size=7, start=(1.5, 0.5), finish=(5.5, 6.5),
     walls=[((2, 1), (6, 1), (6, 7), (5, 7), (5, 6), (1, 6), (1, 0), (2, 0), (2, 3)),
            ((3, 1), (3, 2)), ((1, 5), (2, 5)), ((3, 4), (3, 3), (4, 3)), ((4 ,2), (5 ,2), (5, 4)),
            ((3, 6), (3, 5), (5, 5))]
)
#level 5
maze("l5_p", player_pos, size=7, start=(3.5, 3.5), finish=(5.5, 6.5),
     walls=[((1, 1), (6, 1), (6, 7), (5, 7), (5, 6), (1, 6), (1, 1)),
            ((4, 3), (4, 5)), ((5, 4), (3, 4), (3, 3), (2, 3)), ((2, 2), (4, 2)), ((5, 1), (5, 3)),
            ((3, 5), (3, 6)), ((2, 4), (2, 5), (1, 5))]
)
maze("l5_t", twin_pos, size=7, start=(3.5, 3.5), finish=(5.5, 6.5),
     walls=[((1, 1), (6, 1), (6, 7), (5, 7), (5, 6), (1, 6), (1, 1)),
            ((4, 3), (4, 4), (2, 4)), ((3, 3), (3, 4)), ((5, 2), (5, 6)), ((3, 5), (4, 5), (4, 6)),
            ((1, 2), (2, 2), (2, 3)), ((3, 2), (5, 2), (5, 3)), ((5, 5), (5, 4), (6, 4))]
)
#level 6
maze("l6_p", player_pos, size=10, start=(4.5, 6.5), finish=(2.5, 0.5),
     walls=[((1, 1), (1, 6), (4, 6), (4, 7), (5, 7), (5, 6), (6, 6), (6, 1), (3, 1), (3, 0), (2, 0), (2, 1), (1, 1)),
            ((3, 2), (4, 2)), ((2, 2), (2, 3), (3, 3), (3, 5), (4, 5)), ((1, 4), (2, 4)),
            ((2, 5), (2, 6)), ((5, 5), (6, 5)), ((4, 4), (6, 4)), ((4, 3), (6, 3)), ((5, 2), (5, 3))]
)
maze("l6_t", twin_pos, size=10, start=(4.5, 6.5), finish=(2.5, 0.5),
     walls=[((1, 1), (1, 6), (4, 6), (4, 7), (5, 7), (5, 6), (6, 6), (6, 1), (3, 1), (3, 0), (2, 0), (2, 1), (1, 1)),
            ((2, 1), (2, 3)), ((1, 4), (3, 4), (3, 3)), ((3, 2), (4, 2), (4, 4)), ((2, 6), (2, 5), (4, 5)),
            ((5, 2), (5, 3), (6, 3)), ((5, 4), (5, 6))]
)

post_event(MAINMENU)

while True:
  if pygame.event.get(QUIT):
    break
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        post_event(QUIT if current_state.screen == "menu" else MAINMENU)
      elif event.key in direction_keys:
        direction = direction_keys[event.key]
        if current_state.screen == "menu":
          menu_buttons.move(direction)
          menu_buttons.draw()
        elif current_state.screen == "select":
          select_buttons.move(direction)
          select_buttons.draw()
        elif current_state.screen == "level":
          twin.move(direction)
          player.move(direction)
          update_level()
      elif event.key == K_r:
        goto_level()
        post_event(NEXTLEVEL)
      elif event.key in (K_RETURN, K_SPACE):
        if current_state.screen == "menu":
          menu_buttons.select()
        elif current_state.screen == "select":
          select_buttons.select()
    elif event.type == MAINMENU:
      load_menu()
    elif event.type == LEVELSELECT:
      load_select()
    elif event.type == NEXTLEVEL:
      try:
        load_level(next(level_names))
      except KeyError:
        post_event(MAINMENU)
    elif event.type in (LOSE, WIN):
      text = {LOSE:'Lose', WIN:'Win'}[event.type]
      text = f"You {text}!"
      screen.blit(font.render(text, 1, foreground, background), (screen_rect.w/2 - font.size(text)[0]/2, UI_offset.y))
      pygame.display.flip()
      pygame.time.wait(1500)
      if event.type == LOSE:
          goto_level()
          pygame.event.clear(LOSE)
      post_event(NEXTLEVEL)
  
  pygame.display.update(update_rects)
  del update_rects[:]
pygame.quit()
