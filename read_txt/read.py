import pygame
#from pygame.locals import *
from pygame.math import Vector2 as vector
import operator as op
import re
import itertools
from itertools import chain
import functools
from functools import partial

def splitlist(key, list_):
  indexes = (*[i for i in range(len(list_)) if not key(list_[i])], len(list_))
  start = 0
  for stop in indexes:
    yield list_[start:stop]
    start = stop+1

remove_whitespace = lambda s:"".join(s.split())
group_re = re.compile("\\([^()\\[\\]]*\\)|\\[[^()\\[\\]]*\\]")

with open("maze.txt") as file:
  txt = [i[:-1] for i in filter(lambda x:len(x)>1, file.readlines())]

names = [i[1:] for i in filter(lambda x:x[0]=="#", txt)]
names = chain(*[[f"{lvl[0]}{lvl[-1]}_{i}" for i in "pt"] for lvl in names])
txt = chain(*map(eval, filter(len, map("".join, splitlist(lambda x:x[0]!="#", txt)))))
txt = [*map(dict, map(partial(zip, ["size", "start", "finish", "walls", "one_way_walls"]), txt))]

# splits a wall into walls of length 1
def split_wall(wall):
  a, b = wall
  a = vector(a)
  b = vector(b)
  diff = vector(*map(lambda x:1 if x>0 else -1 if x<0 else 0, b - a))
  new_a, new_b = a, a+diff
  for i in range(int(abs(sum(b-a)))):
    yield (new_a + new_b)
    if new_b == b:
      return
    new_a, new_b = new_b, new_b+diff

for level in txt:
  level["size"] *= 2
  level["start"], level["finish"] = vector(level["start"])*2, vector(level["finish"])*2
  level["walls"] = [*chain(*map(split_wall, chain(*[zip(wall, wall[1:]) for wall in level["walls"]])))]
  if "one_way_walls" in level:
    level["one_way_walls"] = [*map(lambda wall:(vector(wall[0])+wall[1], wall[2]), level["one_way_walls"])]
  else:
    level["one_way_walls"] = []

print(dict(zip(names, txt)))
