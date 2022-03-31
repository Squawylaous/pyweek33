import operator as op
from itertools import starmap
from functools import partial

with open("maze.txt") as file:
  txt = [i[:-1] for i in filter(lambda x:len(x)>1, file.readlines())]

group_dict = lambda dict_:{i:value for key, value in dict_.items() for i in key}
#example: {0:"e", 1:"o", 2:"e", 3:"o"} -> {"e":(0, 2), "o":(1, 3)}
reverse_and_group_dict = lambda dict_:{key:tuple(i for i in dict_.keys() if dict_[i]==key) for key in set(dict_.values())}

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

def process_txt(val, x, y):
  wall_dict = group_dict({"|_":"wall"})
  wall_dict.update(group_dict({key:"one-way "+value for key, value in {"^uU":"u", "vVdD":"d", ">rR":"r", "<lL":"l"}.items()}))
  tile_dict = group_dict({"Ss":"start", "Ff":"finish"})
  try:
    key = (tile_dict if x%2 and y%2 else wall_dict)[val]
  except KeyError:
    return None, None
  key = key.split()
  return ((x, y), tuple(key[1:])), key[0]

print(*txt, sep="\n")
print("\n")
txt = split_to_dict(lambda line:line[0] == "#" and line[-1] == ":", txt, 1)
names, levels = map(op.itemgetter(slice(1, -1)), txt.keys()), txt.values()
levels = [split_to_dict(lambda line:line[0] == "#", level, 1) for level in levels]
print(*levels, sep="\n\n")
maze_names = map(partial(map, op.itemgetter(1)), map(op.methodcaller("keys"), levels))
levels = [[
           [(maze[y][x], (x, y)) for y in range(len(maze)) for x in range(len(maze[y])) if maze[y][x] != " " and (x%2 or y%2)]
           for maze in lvl.values()] for lvl in levels]
print("\ne\n")
print(*dict(zip(names, map(dict, map(zip, maze_names, levels)))).items(), sep="\n")
