import itertools
from itertools import chain

class splitlist:
  def __init__(key, _iter):
    self._iter = iter(_iter)
  
  def __iter__(self):
    len_ = 100
    for i in range(len_):
      yield [*itertools.takewhile(key, list_)]


def splitlist(key, list_):
  indexes = (i for i in range(len(list_)) if not key(list_[i]))
  start = 0
  for stop in indexes:
    yield list_[start:stop]
    start = stop+1
  yield list_[start:]

with open("mazes.txt") as file:
  txt = file.readlines()

print(*splitlist(lambda x:x[0]!="#", txt), sep="\n")
