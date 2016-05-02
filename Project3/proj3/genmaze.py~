#!/usr/bin/python3

import random
import sys
import queue
import copy

from showmaze import mazeref, inbounds

ncoins = 10

def makeEmpty(h, w):
    '''Creates an empty h by w maze'''
    rows = []
    rows.append([True] * (w+2))
    rows.append([False] * (w+1) + [True])
    for i in range(h-2):
        rows.append([True] + [False]*w + [True])
    rows.append([True] + [False]*(w+1))
    rows.append([True] * (w+2))
    return rows

def coinlocs(h, w):
    global ncoins
    cs = set()
    while len(cs) < ncoins:
        cs.add( (random.randrange(1, h+1), random.randrange(1, w+1)) )
    return cs

def below(pos): return (pos[0]+1, pos[1])
def above(pos): return (pos[0]-1, pos[1])
def leftof(pos): return (pos[0], pos[1]-1)
def rightof(pos): return (pos[0], pos[1]+1)

def neighbors(pos):
    return (below(pos), above(pos), leftof(pos), rightof(pos))

def dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def connected(sofar, pos):
    for np in neighbors(pos):
        if np in sofar:
            return True
    return False

def reachable(maze, start, dests):
    mr = copy.deepcopy(maze)
    mr[len(maze)-2][len(maze[0])-1] = True
    ur = set(dests)
    fr = [start]
    while fr:
        p = fr.pop()
        if inbounds(mr,p) and not mazeref(mr,p):
            ur.discard(p)
            mr[p[0]][p[1]] = True
            fr.extend(neighbors(p))
    return not bool(ur)

def fillReachable(h, w, param):
    maze = makeEmpty(h, w)
    coins = coinlocs(h,w)
    start = (1,0)
    end = (h, w+1)
    need = set(coins)
    need.add((h,w))
    assert mazeref(maze,start) is False
    assert mazeref(maze,end) is False

    for i in range(round(h*w*param)):
        y = random.randrange(1, h+1)
        x = random.randrange(1, w+1)
        if not maze[y][x]:
            maze[y][x] = True
            if not reachable(maze, start, need):
                # undo
                maze[y][x] = False

    return maze, coins

def fillFromPath(h, w, param):
    global ncoins

    maze = makeEmpty(h, w)
    end = (h, w+1)

    coins = coinlocs(h,w)
    stops = list(coins)
    stops.append(end)

    path = [(1,0), (1,1)]
    for stop in stops:
        cury, curx = path[-1]
        while (cury,curx) != stop:
            ydif = stop[0] - cury
            xdif = stop[1] - curx
            if random.random() < abs(ydif) / (abs(ydif) + abs(xdif)):
                if ydif < 0:
                    cury -= 1
                else:
                    cury += 1
            else:
                if xdif < 0:
                    curx -= 1
                else:
                    curx += 1
            path.append( (cury,curx) )

    print(path)
    ps = set(path)

    for i in range(round((h*w - len(path)+2)*param)):
        y = random.randrange(1, h+1)
        x = random.randrange(1, w+1)
        if (y,x) not in ps:
            if (y,x) == (1,1):
                print("WTF")
            maze[y][x] = True

    return maze, coins

def rPrims(h, w, param):
    global ncoins

    maze = makeEmpty(h, w)
    
    # divide into cells
    for i in range(2, h, 2):
        for j in range(1, w+1):
            maze[i][j] = True
    for j in range(2, w, 2):
        for i in range(1, h+1):
            maze[i][j] = True

    included = set()
    q = queue.PriorityQueue()

    def addNeighbors(pos):
        nonlocal q, maze, included
        for direction in (above, below, rightof, leftof):
            wp = direction(pos)
            if not mazeref(maze, wp): continue
            other = direction(wp)
            if not inbounds(maze, other): continue
            if other in included: continue
            q.put((random.uniform(0,1), wp, other))

    # choose random starting point
    y = random.randrange(1, h+1, 2)
    x = random.randrange(1, w+1, 2)
    included.add((y,x))
    addNeighbors((y,x))

    while not q.empty():
        (pri, (wy,wx), opp) = q.get()
        if opp in included: continue
        included.add(opp)
        maze[wy][wx] = False
        addNeighbors(opp)

    # randomly remove some walls
    s = 1/8
    scale = (1-param)*s/(s+param)
    for i in range(round(scale*h*w)):
        y = random.randrange(1, h+1)
        x = random.randrange(1, w+1)
        maze[y][x] = False

    # place coins
    coins = set()
    while len(coins) < ncoins:
        coins.add( (random.randrange(1,h+1,2), random.randrange(1,w+1,2)) )

    return maze, coins

def makeCharMaze(maze, coins):
    mz = [['X' if entry else ' ' for entry in row] for row in maze]
    for c in coins:
        mz[c[0]][c[1]] = 'O'
    return mz

def addPrizes(maze, nprizes):
    h, w = len(maze)-2, len(maze[0])-2
    while nprizes > 0:
        y = random.randrange(1,h+1)
        x = random.randrange(1,w+1)
        if maze[y][x] == ' ':
            maze[y][x] = 'O'
            nprizes -= 1

def printMaze(maze):
    for row in maze:
        print(''.join(row))

genmeths = {
    'fillFromPath': 'Creates a path and then fills in around it',
    'fillReachable': "Adds obstacles that don't prevent reaching the finish (slow)",
    'rPrims': "Creates a traditional-looking maze using Prim's MST algorithm"
}
defmeth = 'rPrims'

def usage(exitval=0):
    print("Usage: {} height width [method] [param]".format(sys.argv[0]))
    print("method (optional) is one of:")
    for (meth, desc) in genmeths.items():
        df = " (default)" if meth == defmeth else ""
        print("  {}{}: {}".format(meth, df, desc))
    print('param (optional) indicates how "dense" the output will be.')
    exit(exitval)

if __name__ == '__main__':
    if not 3 <= len(sys.argv) <= 5:
        usage(1)
    h = int(sys.argv[1])
    w = int(sys.argv[2])
    method = defmeth if len(sys.argv) <= 3 else sys.argv[3]
    param = 0.5 if len(sys.argv) <= 4 else float(sys.argv[4])

    if method not in genmeths:
        print("Invalid method number")
        usage(2)

    genfunc = globals()[method]
    maze, coins = genfunc(h, w, param)

    cm = makeCharMaze(maze, coins)
    # addPrizes(cm, 10)
    printMaze(cm)
