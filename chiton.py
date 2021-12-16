from datetime import datetime

max_int = 99999999999

def incr_value(v, i):
    v = v + i
    if v > 9:
        v = v - 9
    return v

def incr_tile(t, i):    
    new_t = []
    length = len(t)
    width = len(t[0])
    for y in range(length):
        new_t.append([incr_value(t[y][x], i) for x in range(width)])
    return new_t

def add_tile_h(t1, t2):
    new_t = []
    for y in range(len(t1)):
        new_t.append(t1[y] + t2[y])
    return new_t

def add_tile_v(t1, t2):
    return t1 + t2

def print_tile(t):
    for y in range(len(t)):
        for x in range(len(t[0])):
            print(t[y][x], end='')
        print()


tile = []
with open('./data/cave.txt', 'r') as file:
    for line in file.readlines():
        tile.append([int(c) for c in line.strip()])        

t = tile
t = add_tile_h(t, incr_tile(tile, 1))
t = add_tile_h(t, incr_tile(tile, 2))
t = add_tile_h(t, incr_tile(tile, 3))
t = add_tile_h(t, incr_tile(tile, 4))

tile = t
t = add_tile_v(t, incr_tile(tile, 1))
t = add_tile_v(t, incr_tile(tile, 2))
t = add_tile_v(t, incr_tile(tile, 3))
t = add_tile_v(t, incr_tile(tile, 4))
        
cave = t

length = len(cave)
width = len(cave[0])

nodes = dict()
for y in range(length):
    for x in range(width):
        nodes[(y, x)] = (cave[y][x], max_int)        
nodes[(0, 0)] = (0, 0)

visited = dict()
distanced = set()
distanced.add((0, 0))

def set_distance(y, x, d):
    if (y, x) in nodes:
        value, distance = nodes[(y, x)]
        new_distance = d + value
        if new_distance < distance:
            nodes[(y, x)] = (value, new_distance)
            distanced.add((y, x))
        
def smallest_node():
    s_node = None
    s_distance = max_int
    for k in distanced:
        value, distance = nodes[k]
        if distance < s_distance:
            s_distance = distance
            s_node = k
    return s_node
        
    
def traverse(y, x):
    value, distance = nodes[(y, x)]
    set_distance(y - 1, x, distance)
    set_distance(y + 1, x, distance)
    set_distance(y, x - 1, distance)
    set_distance(y, x + 1, distance)
    visited[(y, x)] = nodes.pop((y, x))
    distanced.discard((y, x))
    
print(datetime.now())
while len(nodes) > 0:
    y, x = smallest_node()
    traverse(y, x)
    

print(visited[(length - 1, width - 1)])
print(datetime.now())

