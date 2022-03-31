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

#process txt
