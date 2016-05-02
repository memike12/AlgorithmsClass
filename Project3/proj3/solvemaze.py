#!/usr/bin/python3

''' SI 335 Spring 2015
    Project 3
    Moore
'''
import time
import re
import random
import sys
import queue
from queue import PriorityQueue
from itertools import combinations
import heapq

class Graph:
    def __init__(self):
        self.verticies = {}

    def getVerticies(self):
        return self.verticies

    def neighbors(self, u):
        return self.verticies[u].adjancent

    def addVertex(self, name):
        newVert = Vertex(name)
        self.verticies[name] = newVert

    def addEdge(self, u, v, dist):
        self.verticies[u].addNeighbor(v, dist)
        self.verticies[v].addNeighbor(u, dist)
        return

    def cost(self):
        return 1

class Vertex:
    def __init__(self, name):
        self.name = name
        self.adjancent = {}

    def addNeighbor(self, v, dist):
        self.adjancent[v] = dist

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, start)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while len(frontier):
        current = heapq.heappop(frontier)
        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, next)
                came_from[next] = current
    
    return came_from, cost_so_far

def calcMoves(maze):
    '''This function takes in a 2D-array that stores a maze description,
       and returns a list of "moves" to make in order to solve the maze.
    '''
    # THIS IS THE FUNCTION YOU NEED TO RE-WRITE
    # Width and height calculated from maze size, minus borders
    w = len(maze) - 2
    h = len(maze[0]) - 2
    startPos = (1, 0)
    endPos = (h, w+1)
    curY, curX = startPos

    gold = []
    mapGraph = Graph()
    
    for x in range(w+1):
        for y in range(h+2):
            if maze[x][y] == "O":
                gold.append((x,y))
                mapGraph.addVertex((x,y))
                if  maze[x-1][y] == " " or maze[x-1][y] == "O" :
                    mapGraph.addEdge((x,y),(x-1,y), 1)
                if  maze[x][y-1] == " " or maze[x][y-1] == "O":
                    mapGraph.addEdge((x,y),(x,y-1), 1)
            if maze[x][y] == " ":
                mapGraph.addVertex((x,y))
                if  maze[x-1][y] == " " or maze[x-1][y] == "O" :
                    mapGraph.addEdge((x,y),(x-1,y), 1)
                if  maze[x][y-1] == " " or maze[x][y-1] == "O":
                    mapGraph.addEdge((x,y),(x,y-1), 1)     

    #gold.append((w,h+1))
    total = 0
    comb = []
    #heapq.heappush(comb, combinations(gold, 2))
    comb = combinations(gold,2)
    min = float("inf")
    routes = {}

    #goes from the start to each individual goal
    for goal in gold:
        came_from, cost_so_far = a_star_search(mapGraph, startPos, goal)
        print(goal[0] - came_from[goal][0], goal[1] - came_from[goal][1])
        x = cost_so_far[goal]
        #print((startPos, goal))
        #print(x)
        routes[(startPos, goal)] = x
        if x < min:
            min = x

    #goes from every goal to all other goals
    for goal in comb:
        #print(goal)
        came_from, cost_so_far = a_star_search(mapGraph, goal[0], goal[1])
        x = cost_so_far[goal[1]]
        #print(x)
        #routes.append((goal, x))
        routes[goal] = x
    
    #goes from every goal to end
    for goal in gold:
        #print((goal, endPos))
        came_from, cost_so_far = a_star_search(mapGraph, startPos, goal)
        x = cost_so_far[goal]
        #print(x)
        routes[(goal, endPos)] = x
    


    #populate the graph with start and rings
    goldGraph = Graph()
    goldGraph.addVertex(startPos)
    for goal in gold:
        goldGraph.addVertex(goal)
        
    #add neighbors
    for goal in gold:
        #print(startPos, goal, routes[startPos, goal])
        goldGraph.addEdge(startPos, goal,routes[startPos, goal])
    for goal in comb:
        if goal in routes:
            #print( goal1, goal2, routes[goal1, goal2])
            goldGraph.addEdge(goal[0], goal[1], routes[goal1, goal2])
            #total=total+1
            
    goldGraph.addVertex(endPos)
    for goal in gold:
        print( goal, endPos, routes[goal, endPos])
        
        goldGraph.addEdge(goal, endPos, routes[goal, endPos])
        #total=total+1

    #print(total)
    print("Time = ", time.time() - startTime)
    exit()
    '''
    # The solution here is terrible: it just randomly mills about until
    # it happens upon the end or it runs out of points.
    moves = []
    while len(moves) < 4*h*w:
        nextY, nextX = curY, curX
        # randomly choose a direction
        if random.randrange(0,2) == 0:
            # go left/right
            if random.randrange(0,2) == 0:
                nextX -= 1
                nextMove = 'L'
            else:
                nextX += 1
                nextMove = 'R'
        else:
            # go up/down
            if random.randrange(0,2) == 0:
                nextY -= 1
                nextMove = 'U'
            else:
                nextY += 1
                nextMove = 'D'
        if nextX < 0 or nextX > w+1 or maze[nextY][nextX] == 'X':
            # illegal move; give up and try another.
            continue
        moves.append(nextMove)
        curY, curX = nextY, nextX

    return moves'''


def readMaze(stream):
    '''This functions reads in a maze description from the given file
       and returns a 2-dimensional array of characters.
       ' ' means a space in the maze,
       'X' means an impenetrable wall, and
       'O' means a lucrative prize.
    '''
    # YOU DON'T NEED TO CHANGE THIS FUNCTION.
    notAllowed = re.compile('[^XO ]')
    width = 0
    maze = []
    prizes = set()
    rowind = 0
    for line in stream:
        line = line.rstrip()
        s = notAllowed.search(line)
        if s:
            raise ValueError('Illegal character in maze: {}'.format(s.group(0)))
        row = list(line)
        wdiff = width - len(row)
        if wdiff > 0:
            row.extend([' '] * wdiff)
        elif wdiff < 0:
            for otherRow in maze:
                otherRow.extend([' '] * (-wdiff))
            width = len(row)
        maze.append(row)
        rowind += 1
    assert len(maze) >= 2
    return tuple(tuple(row) for row in maze)

def writeMoves(moves):
    '''Writes the list of moves to standard out'''
    # YOU DON'T NEED TO CHANGE THIS FUNCTION
    for move in moves:
        print(move)

if __name__ == '__main__':
    # THIS IS THE MAIN METHOD. YOU DON'T NEED TO CHANGE IT.
    startTime = time.time()
    maze = readMaze(sys.stdin)
    moves = calcMoves(maze)
    writeMoves(moves)
