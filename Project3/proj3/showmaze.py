#!/usr/bin/python3

import curses
import re
import time
import sys

def ncoins():
    return 10

def readMaze(fname):
    notAllowed = re.compile('[^XO ]')
    width = 0
    maze = []
    coins = set()
    with open(fname) as mapin:
        rowind = 0
        for line in mapin:
            line = line.rstrip()
            s = notAllowed.search(line)
            if s:
                raise ValueError('Illegal character in maze: {}'.format(s.group(0)))
            for colind in range(len(line)):
                if line[colind] == 'O':
                    coins.add((rowind,colind))
            row = list(c == 'X' for c in line)
            wdiff = width - len(row)
            if wdiff > 0:
                row.extend([False] * wdiff)
            elif wdiff < 0:
                for otherRow in maze:
                    otherRow.extend([False] * (-wdiff))
                width = len(row)
            maze.append(row)
            rowind += 1
    assert len(maze) >= 2
    return tuple(tuple(row) for row in maze), coins

def readMoves(fname):
    valid = re.compile('[UDLR]')
    spaces = re.compile('\s')
    moves = []
    with open(fname) as movesin:
        for line in movesin:
            for char in line:
                if valid.match(char):
                    moves.append(char)
                elif not spaces.match(char):
                    raise ValueError("Illegal character in moves: {}".format(char))
    return moves

def initscores(maze):
    h = len(maze) - 2
    w = len(maze[0]) - 2
    initial = 2*w*h
    coin = 2*w*h
    final = 2*w*h
    return (initial, coin, final)

def dispMaze(win, maze, coins, offset=(0,0)):
    # A valid maze is a rectangular array of boolean values, with
    # at least 2 rows and at least 2 columns.
    above = 1
    left = 2
    right = 4
    below = 8

    width = len(maze[0])
    height = len(maze)

    matrix = []
    for row in range(height):
        matrix.append([0] * width)

    # add aboves
    for i in range(height-1):
        for j in range(width):
            if maze[i][j] and maze[i+1][j]:
                matrix[i+1][j] |= above

    # add belows
    for i in range(1, height):
        for j in range(width):
            if maze[i][j] and maze[i-1][j]:
                matrix[i-1][j] |= below

    # add lefts
    for i in range(height):
        for j in range(width-1):
            if maze[i][j] and maze[i][j+1]:
                matrix[i][j+1] |= left

    # add rights
    for i in range(height):
        for j in range(1,width):
            if maze[i][j] and maze[i][j-1]:
                matrix[i][j-1] |= right
    
    mapping = {
        0: curses.ACS_VLINE,
        above: curses.ACS_VLINE,
        below: curses.ACS_VLINE,
        left: curses.ACS_HLINE,
        right: curses.ACS_HLINE,
        above|below: curses.ACS_VLINE,
        left|right: curses.ACS_HLINE,
        above|left: curses.ACS_LRCORNER,
        above|right: curses.ACS_LLCORNER,
        below|left: curses.ACS_URCORNER,
        below|right: curses.ACS_ULCORNER,
        above|left|right: curses.ACS_BTEE,
        below|left|right: curses.ACS_TTEE,
        left|above|below: curses.ACS_RTEE,
        right|above|below: curses.ACS_LTEE,
        left|right|above|below: curses.ACS_PLUS,
    }

    for i in range(height):
        for j in range(width):
            if maze[i][j]:
                disp = mapping[matrix[i][j]]
            elif (i,j) in coins:
                disp = 'O'
            else:
                disp = ' '
            win.addch(i + offset[0], j + offset[1], disp, curses.color_pair(4))

def inbounds(maze, pos):
    h, w = len(maze), len(maze[0])
    return 0 <= pos[0] < h and 0 <= pos[1] < w

def mazeref(maze, pos):
    return maze[pos[0]][pos[1]]

def doMove(win, maze, curpos, nextMove, offset=(0,0)):

    if not inbounds(maze, curpos):
        return (None,0,0)
    elif mazeref(maze, curpos): 
        return (None,0,0)

    nextpos = list(curpos)
    if nextMove == 'L':
        nextpos[1] -= 1
    elif nextMove == 'D':
        nextpos[0] += 1
    elif nextMove == 'U':
        nextpos[0] -= 1
    elif nextMove == 'R':
        nextpos[1] += 1
    else:
        raise ValueError('Illegal move')

    # Drop faint diamond at curpos
    win.addch(curpos[0]+offset[0], curpos[1]+offset[1], curses.ACS_CKBOARD,
        curses.color_pair(3)|curses.A_DIM)

    msg = None
    mv = 0
    status = 0
    if not inbounds(maze, nextpos):
        msg = "Out of bounds!"
        status = 1
    elif mazeref(maze, nextpos):
        msg = "Ran into a wall!"
        # Draw bloody diamond.
        win.addch(nextpos[0]+offset[0], nextpos[1]+offset[1], curses.ACS_DIAMOND,
            curses.color_pair(2)|curses.A_BOLD)
        mv = 1
        status = 1
    else:
        # Draw diamond at nextpos
        win.addch(nextpos[0]+offset[0], nextpos[1]+offset[1], curses.ACS_DIAMOND,
            curses.color_pair(1)|curses.A_BOLD)
        mv = 1

    curpos[:] = nextpos
    return (msg, mv, status)

def runMaze(stdscr, maze, coins, moves):
    def showMessage(text):
        stdscr.move(msgline, 0)
        stdscr.clrtoeol()
        stdscr.addstr(text, curses.color_pair(2)|curses.A_BOLD)

    def showScore(curscore):
        stdscr.move(*scorePos)
        stdscr.clrtoeol()
        stdscr.addstr(str(curscore), curses.color_pair(1))

    curses.curs_set(0)
    curses.use_default_colors()
    stdscr.nodelay(1)

    curses.init_pair(1, curses.COLOR_BLUE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_CYAN, -1)
    curses.init_pair(4, -1, -1)

    mazedims = len(maze), len(maze[0])
    dispMaze(stdscr, maze, coins)

    scoreline = mazedims[0] + 1
    stdscr.move(scoreline, 0)
    stdscr.addstr("Score: ", curses.color_pair(1))
    scorePos = stdscr.getyx()

    curscore, coinBonus, finishBonus = initscores(maze)
    showScore(curscore)

    infoline = mazedims[0] + 4
    stdscr.move(infoline,0)
    stdscr.addstr("UP/DOWN keys change speed, P pauses/resumes, and Q quits.\n")
    if moves is None:
        stdscr.addstr("To move, h/j/k/l are left/down/up/right.\n")
    stdscr.addstr("Bonus for picking up a coin is {} points.\n".format(coinBonus))
    stdscr.addstr("Bonus for reaching the finish is {} points.\n".format(finishBonus))

    msgline = mazedims[0] + 2

    startpos = [1,0]
    endpos = [len(maze)-2, len(maze[0])-1]
    assert mazeref(maze,startpos) is False
    assert mazeref(maze,endpos) is False
    curpos = list(startpos)

    # Draw diamond at curpos
    stdscr.addch(curpos[0], curpos[1], curses.ACS_DIAMOND,
        curses.color_pair(1)|curses.A_BOLD)
    mv = 1

    stdscr.refresh()

    speed = 5 if moves else 1
    count = 0

    if moves:
        movesIter = iter(moves)
        nextMove = next(movesIter)
    else:
        movesIter = None
        nextMove = None

    active = True

    while True:
        time.sleep(.1)
        if speed > 0 and count < speed: count += 1

        c = stdscr.getch()
        badch = False
        if c == curses.KEY_UP:
            speed = max(1, speed-1)
            count = min(speed, count)
        elif c == curses.KEY_DOWN:
            speed = max(speed*-1, speed+1)
            count = 0
        elif c == ord('p') or c == ord('P'):
            speed *= -1
            count = 0
        elif c == ord('q') or c == ord('Q'):
            break
        elif moves is None and c > 0:
            if c == ord('h'):
                nextMove = 'L'
            elif c == ord('j'):
                nextMove = 'D'
            elif c == ord('k'):
                nextMove = 'U'
            elif c == ord('l'):
                nextMove = 'R'
            elif c >= 0:
                badch = True
        elif c >= 0:
            badch = True

        if badch:
            showMessage("Unrecognized command")
            
        if active and count == speed and nextMove:
            (msg, mv, status) = doMove(stdscr, maze, curpos, nextMove)
            nextMove = None
            if msg:
                showMessage(msg)
            else:
                showMessage('')
            if mv > 0:
                curscore -= mv
                showScore(curscore)
            if status == 1:
                # bad ending
                curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
                active = False
            elif curpos == endpos and bool(coins):
                # bad ending
                showMessage("You missed some coins!")
                curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
                active = False
            elif curpos == endpos:
                # good ending
                showMessage("You reached the finish!")
                curscore += finishBonus
                showScore(curscore)
                curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
                active = False
            elif tuple(curpos) in coins:
                # good news
                coins.discard(tuple(curpos))
                showMessage("You found a coin!")
                curscore += coinBonus
                showScore(curscore)
            elif curscore == 0:
                # bad ending
                showMessage("You ran out of points!")
                curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
                active = False
            stdscr.refresh()
            if movesIter:
                try:
                    nextMove = next(movesIter)
                except StopIteration:
                    movesIter = None
            count = 0


def usage(exitval = 0):
    print("Usage: {} maze_file [moves_file]".format(sys.argv[0]))
    exit(exitval)

if __name__ == '__main__':
    if not 2 <= len(sys.argv) <= 3:
        usage(1)
    mazefn = sys.argv[1]
    if mazefn.startswith('-'):
        usage(2)
    maze, coins = readMaze(mazefn)
    if len(sys.argv) >= 3:
        moves = readMoves(sys.argv[2])
    else:
        moves = None
    try:
        curses.wrapper(runMaze, maze, coins, moves)
    except curses.error:
        print("There was an error displaying the maze.")
        print("Check that your window is large enough.")
        exit(3)
