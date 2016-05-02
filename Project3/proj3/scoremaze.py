#!/usr/bin/python3

import sys
from showmaze import readMaze, readMoves, initscores, inbounds, mazeref

def usage(exitval = 0):
    print("Usage: {} maze_file moves_file".format(sys.argv[0]))
    exit(exitval)

def updatepos(pos, move):
    py, px = pos
    if move == 'L':
        return (py, px-1)
    elif move == 'R':
        return (py, px+1)
    elif move == 'U':
        return (py-1, px)
    elif move == 'D':
        return (py+1, px)

def calcScore(maze, coins, moves):
    curscore, percoin, finish = initscores(maze)
    h = len(maze)-2
    w = len(maze[0])-2
    pos = (1,0)
    end = (h, w+1)
    for move in moves:
        pos = updatepos(pos, move)
        if not inbounds(maze, pos):
            print("Went out of bounds", file=sys.stderr)
            return curscore
        curscore -= 1
        if mazeref(maze, pos) or (pos == end and bool(coins)):
            print("Ran into a wall", file=sys.stderr)
            return curscore
        if pos in coins:
            print("Found a coin", file=sys.stderr)
            coins.discard(pos)
            curscore += percoin
        if pos == end and not bool(coins):
            print("Found the finish", file=sys.stderr)
            curscore += finish
            return curscore
        if curscore == 0:
            print("Ran out of points", file=sys.stderr)
            return curscore
    print("Ran out of moves", file=sys.stderr)
    return curscore

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(1)
    mazefn = sys.argv[1]
    if mazefn.startswith('-'):
        usage(2)
    maze, coins = readMaze(mazefn)
    moves = readMoves(sys.argv[2])
    score = calcScore(maze, coins, moves)
    print(score)
