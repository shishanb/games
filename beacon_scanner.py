orientations = [
    ('x', 'y', 'z'),
    ('x', 'y', '-z'),
    ('x', '-y', 'z'),
    ('x', '-y', '-z'),
    ('x', 'z', 'y'),
    ('x', 'z', '-y'),
    ('x', '-z', 'y'),
    ('x', '-z', '-y'),
    ('-x', 'y', 'z'),
    ('-x', 'y', '-z'),
    ('-x', '-y', 'z'),
    ('-x', '-y', '-z'),
    ('-x', 'z', 'y'),
    ('-x', 'z', '-y'),
    ('-x', '-z', 'y'),
    ('-x', '-z', '-y'),    
    ('y', 'x', 'z'),
    ('y', 'x', '-z'),
    ('y', '-x', 'z'),
    ('y', '-x', '-z'),
    ('y', 'z', 'x'),
    ('y', 'z', '-x'),
    ('y', '-z', 'x'),
    ('y', '-z', '-x'),    
    ('-y', 'x', 'z'),
    ('-y', 'x', '-z'),
    ('-y', '-x', 'z'),
    ('-y', '-x', '-z'),
    ('-y', 'z', 'x'),
    ('-y', 'z', '-x'),
    ('-y', '-z', 'x'),
    ('-y', '-z', '-x'),
    ('z', 'x', 'y'),
    ('z', 'x', '-y'),
    ('z', '-x', 'y'),
    ('z', '-x', '-y'),
    ('z', 'y', 'x'),
    ('z', 'y', '-x'),
    ('z', '-y', 'x'),
    ('z', '-y', '-x'),
    ('-z', 'x', 'y'),
    ('-z', 'x', '-y'),
    ('-z', '-x', 'y'),
    ('-z', '-x', '-y'),
    ('-z', 'y', 'x'),
    ('-z', 'y', '-x'),
    ('-z', '-y', 'x'),
    ('-z', '-y', '-x'),
]

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.magnitude2 = x*x + y*y + z*z
        
    def get_coor(self, c):
        return {'x': self.x, 'y': self.y, 'z': self.z, '-x': -self.x, '-y': -self.y, '-z': -self.z }[c]
            
    def values(self):
        return set([abs(self.x), abs(self.y), abs(self.z)])

    def reorient(self, o):
        x, y, z = o
        return Vector(self.get_coor(x), self.get_coor(y), self.get_coor(z))
    
    def similar(self, other):
        return (self.magnitude2 == other.magnitude2) and (self.values() == other.values())
    
    def minus(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def translate(self, t):
        return Vector(self.x + t.x, self.y + t.y, self.z + t.z)

    def align(self, other):
        if not self.similar(other):
            return None
        for o in orientations:
            if self == other.reorient(o):
                return o
        raise 'not possible'            

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
    
    def __hash__(self):
        return (self.x, self.y, self.z).__hash__()
    
    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)

class Beacon():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def vector(self):
        return Vector(self.x, self.y, self.z)
    
    def to_tuple(self):
        return (self.x, self.y, self.z)

    def relative(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)
    
class Scanner:
    def __init__(self, id, beacons):
        self.id = id
        self.beacons = beacons
        self.beacon_map = dict()
        for i in range(len(beacons) - 1):
            for j in range(i + 1, len(beacons)):
                self.beacon_map[(i, j)] = beacons[i].relative(beacons[j]) 
        self.scanners = [Vector(0, 0, 0)]
        
    def __str__(self):
        return 'scanner-{}\n{}\n{}]'.format(
            self.id,
            '\n'.join([str(b) for b in self.beacons]),
            '\n'.join([(str(k) + '->' + str(v)) for k, v in self.beacon_map.items()])
        )
        
def parse_scanner(id, lines):
    beacons = []
    for line in lines[1:]:        
        if len(line.strip()) == 0:
            break
        p = [int(i) for i in line.strip().split(',')]
        beacons.append(Beacon(p[0], p[1], p[2]))
    scanner = Scanner(id, beacons)
    return scanner, lines[len(beacons)+2:]
    
def valid_pairs(pairs):
    return (len(set([p[0] for p in pairs])) == len(set([p[0] for p in pairs]))) and (len(pairs) == 12)

def find_common_points(s1, s2):
    common_pairs = dict()
    for k1, v1 in s1.beacon_map.items():
        for k2, v2 in s2.beacon_map.items():
            align = v1.align(v2)
            if align:
                if align in common_pairs:
                    common_pairs[align].add((k1[0], k2[0]))
                    common_pairs[align].add((k1[1], k2[1]))
                else:
                    common_pairs[align] = set([(k1[0], k2[0]), (k1[1], k2[1])])
    points = dict()
    for k, v in common_pairs.items():
        if valid_pairs(v):
            points[k] = v
    return points

def transfer_beacons(destination, source, o, t):
    for b in source.beacons:
        p = b.vector().reorient(o).translate(t)
        destination.beacons.append(Beacon(p.x, p.y, p.z))
        
scanners = []
with open('./data/scanners.txt', 'r') as file: 
    lines = file.readlines()
    scanner_count = 0
    while len(lines) > 0:
        scanner, lines = parse_scanner(scanner_count, lines)
        scanners.append(scanner)
        scanner_count += 1


common_points = dict()
for i in range(len(scanners)):
    for j in range(len(scanners)):
        if i != j:
            points = find_common_points(scanners[i], scanners[j])
            if len(points) > 0:
                common_points[(i, j)] = points

transfers = dict()

for k, v in common_points.items():
    s1 = scanners[k[0]]
    s2 = scanners[k[1]]
    for o, pairs in v.items():
        translate = set()
        for p in pairs:
            v1 = s1.beacons[p[0]].vector()
            v2 = s2.beacons[p[1]].vector()
            v2h = v2.reorient(o)
            translate.add(v1.minus(v2h))
        if len(translate) == 1:
            transfers[k] = (o, list(translate)[0])
            

scanner_count = len(scanners)
ordered_transfers = []
scanners_traversed = set()
scanners_to_traverse = set([0])
while (len(scanners_traversed) < scanner_count) and (len(scanners_to_traverse) > 0):    
    new_scanners_to_traverse = set()
    for i in scanners_to_traverse:
        scanners_traversed.add(i)
        for k, v in transfers.items():
            if k[0] == i:
                if (k[1] not in scanners_traversed) and (k[1] not in new_scanners_to_traverse):
                    ordered_transfers.append((k, v[0], v[1]))
                    new_scanners_to_traverse.add(k[1])
    scanners_to_traverse = new_scanners_to_traverse

for t in ordered_transfers:
    print(t)
    

scanner_transfers = []
while len(ordered_transfers) > 0:
    transfer = ordered_transfers.pop()
    scanner_transfers.append(transfer)
    s1, s2 = transfer[0]    
    transfer_beacons(scanners[s1], scanners[s2], transfer[1], transfer[2])
    
print(len(set([b.to_tuple() for b in scanners[0].beacons])))

# part 2

def transfer_scanners(destination, source, o, t):
    print(destination.id, [str(s) for s in destination.scanners], source.id, [str(s) for s in source.scanners])
    for s in source.scanners:
        p = s.reorient(o).translate(t)
        destination.scanners.append(Vector(p.x, p.y, p.z))
    print('\t', destination.id, [str(s) for s in destination.scanners])


for s in scanners:
    s.scanners = [Vector(0, 0, 0)]
    
for t in scanner_transfers:
    print(t)
    
for t in scanner_transfers:
    s1, s2 = t[0]    
    transfer_scanners(scanners[s1], scanners[s2], t[1], t[2])
    
all_scanners = scanners[0].scanners
for s in all_scanners:
    print(s)

max_d = 0
for i in range(len(all_scanners) - 1):
    v1 = all_scanners[i]
    for j in range(i + 1, len(all_scanners)):
        v2 = all_scanners[j]
        d = abs(v2.x - v1.x) + abs(v2.y - v1.y) + abs(v2.z - v1.z)
        if d > max_d:
            max_d = d
            
print(max_d)

