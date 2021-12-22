from datetime import datetime
from threading import Timer

def position(v):
    return (v-10) if v>10 else v

transitions_count = 0
transitions = dict()
def add_transition(t):
    global transitions_count
    transitions_count += 1
    if t[0] in transitions:
        positions = transitions[t[0]]
        if t[1] in positions:
            positions[t[1]] += 1
        else:
            positions[t[1]] = 1
    else:
        transitions[t[0]] = dict()
        transitions[t[0]][t[1]] = 1
        
for p in range(1, 11):
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                add_transition((p, position(p + i + j + k)))
                
print(transitions_count)
for k, v in transitions.items():
    print(k, v)


count1 = 0
count2 = 0

def traverse1(p1, s1, c1, p2, s2, c2):
    global count1, count2
    for k, v in transitions[p1].items():
        s = s1 + k
        c = c1*v
        if s >= 21:
            count1 += c
        else:
            traverse2(k, s, c, p2, s2, c2*v)

def traverse2(p1, s1, c1, p2, s2, c2):
    global count1, count2
    for k, v in transitions[p2].items():
        s = s2 + k
        c = c2*v
        if s >= 21:
            count2 += c
        else:
            traverse1(p1, s1, c1*v, k, s, c)


traverse1(4, 0, 1, 8, 0, 1)
print(count1, count2)
