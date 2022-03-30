import operator as op
import re
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
txt = filter(len, map(remove_whitespace, map("".join, splitlist(lambda x:x[0]!="#", txt))))
def lol(x):
  print(x.group())
  return "{}"
txt = map(partial(group_re.sub, lol), txt)
print()
print(dict(zip(names, txt)))
