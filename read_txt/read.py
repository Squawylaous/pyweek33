import pygame
#from pygame.locals import *
from pygame.math import Vector2 as vector
import operator as op
import re
import itertools
from itertools import chain
import functools
from functools import partial

with open("maze.txt") as file:
  txt = [i[:-1] for i in filter(lambda x:len(x)>1, file.readlines())]

# splits list_ into a list of slices
# key is called on each item of list_ and any that return true are used as seperators
def splitlist(key, list_, filter_empty=False):
  indexes = (*[i for i in range(len(list_)) if key(list_[i])], len(list_))
  start = 0
  for stop in indexes:
    sublist = list_[start:stop]
    if len(sublist) or not filter_empty:
      yield sublist
    start = stop+1

#calls splitlist(key, list_, filter_empty) for values and uses what it seperated list_ by as keys
def split_to_dict(key, list_, filter_empty=False):
  return dict(zip(filter(key, list_), splitlist(key, list_, filter_empty)))

print(*txt, sep="\n")
print("\n")
txt = split_to_dict(lambda line:line[0] == "#" and line[-1] == ":", txt, 1)
names, levels = map(op.itemgetter(slice(1, -1)), txt.keys()), txt.values()
levels = [split_to_dict(lambda line:line[0] == "#", level, 1) for level in levels]
print(*levels, sep="\n\n")
maze_names = map(partial(map, op.itemgetter(1)), map(op.methodcaller("keys"), levels))
levels = map(op.methodcaller("values"), levels)
levels = [[[(x, y) for y in range(len(maze)) for x in range(len(maze[y]))] for maze in lvl] for lvl in levels]
print("\ne\n")
print(*dict(zip(names, map(dict, map(zip, maze_names, levels)))).items(), sep="\n")
