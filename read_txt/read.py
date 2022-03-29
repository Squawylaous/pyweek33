import itertools


class splitlist:
  def __init__(key, _iter):
    self._iter = iter(_iter)
  
  def __iter__(self):
    len_ = 100
    for i in range(len_):
      yield [*itertools.takewhile(key, list_)]

def splitlist(key, list_):
  list_ = iter(list_)
  sublist = []
  while True:
    next_ = next(list_)
    if key(next_):
      sublist.append(next_)
      continue
    yield sublist
    sublist = []

print(splitlist(lambda x:x%3, [1,2,3,4,5,6,7,8,9,10]))
print(*splitlist(lambda x:x%3, [1,2,3,4,5,6,7,8,9,10]))

with open("mazes.txt") as file:
  txt = file.readlines()

print(itertools.takewhile(lambda x:x[0]!="#", txt))
