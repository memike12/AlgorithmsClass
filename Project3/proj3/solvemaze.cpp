/* SI 335 Spring 2015
 * Project 3
 * Michael Moore
 */

#include <cassert>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <map>
#include <unordered_map>
using namespace std;

template<typename L>
struct Graph {
  typedef L Location;
  typedef typename vector<Location>::iterator iterator;
  map<Location, vector<Location> > edges;

  inline const vector<Location> neighbors(Location id) {
    return edges[id];
  }
};

template<typename Graph>
void a_star_search
  (Graph graph,
   typename Graph::Location start,
   typename Graph::Location goal,
   unordered_map<typename Graph::Location, typename Graph::Location>& came_from,
   unordered_map<typename Graph::Location, int>& cost_so_far)
{
  typedef typename Graph::Location Location;
  PriorityQueue<Location> frontier;
  frontier.put(start, 0);

  came_from[start] = start;
  cost_so_far[start] = 0;
  
  while (!frontier.empty()) {
    auto current = frontier.get();

    if (current == goal) {
      break;
    }

    for (auto next : graph.neighbors(current)) {
      int new_cost = cost_so_far[current] + graph.cost(current, next);
      if (!cost_so_far.count(next) || new_cost < cost_so_far[next]) {
        cost_so_far[next] = new_cost;
        int priority = new_cost + heuristic(next, goal);
        frontier.put(next, priority);
        came_from[next] = current;
      }
    }
  }
}

inline int heuristic(Graph::Location a, Graph::Location b) {
  int x1, y1, x2, y2;
  tie (x1, y1) = a;
  tie (x2, y2) = b;
  return abs(x1 - x2) + abs(y1 - y2);
}

/* This function takes in a 2D-array that stores a maze description,
   and returns a list of "moves" to make in order to solve the maze.  */
vector<char> calcMoves(vector< vector<char> >& maze) {
  // THIS IS THE FUNCTION YOU NEED TO RE-WRITE!
  // Width and height calculated from maze size, minus borders
  int w = maze.size() - 2;
  int h = maze[0].size() - 2;

  // Start (curY, curX) at the starting position
  int curY = 1;
  int curX = 0;

  // The solution here is terrible: it just randomly mills about until
  // it happens upon the end or it runs out of points.
  vector<char> moves;
  while (moves.size() < 4*h*w) {
    int nextY = curY;
    int nextX = curX;
    char nextMove;
    // randomly choose a direction
    if (rand() % 2 == 0) {
      // go left/right
      if (rand() % 2 == 0) {
        nextX -= 1;
        nextMove = 'L';
      }
      else {
        nextX += 1;
        nextMove = 'R';
      }
    }
    else {
      // go up/down
      if (rand() % 2 == 0) {
        nextY -= 1;
        nextMove = 'U';
      }
      else {
        nextY += 1;
        nextMove = 'D';
      }
    }
    if (nextX < 0 || nextX > w+1 || maze[nextY][nextX] == 'X') {
      // illegal move; give up and try another.
      continue;
    }
    moves.push_back(nextMove);
    curY = nextY;
    curX = nextX;
  }

  return moves;
}

/* Reads in a maze into a double array of chars. */
vector< vector<char> > readMaze(istream& in) {
  // YOU DON'T NEED TO CHANGE THIS FUNCTION.
  int width = 0;
  string line;
  vector<string> rows;
  while (getline(cin, line)) {
    if (line.find_first_not_of(" XO") != string::npos) {
      cerr << "Invalid maze characters in row: " << line << endl;
      exit(2);
    }
    line.erase(line.find_last_not_of(" \n\r\t")+1);
    rows.push_back(line);
    if (line.length() > width) width = line.length();
  }
  int height = rows.size();
  assert (height >= 2);
  assert (width >= 2);
  vector< vector<char> > maze(height);
  for (int i=0; i<height; ++i) {
    maze[i].assign(rows[i].begin(), rows[i].end());
    maze[i].insert(maze[i].end(), width-maze[i].size(), ' ');
  }
  return maze;
}

/* Writes the moves in the list to standard out, one per line. */
void writeMoves(const vector<char>& moves) {
  for (int i=0; i<moves.size(); ++i) {
    cout << moves[i] << endl;
  }
}

int main(int argc, char** argv) {
  // THIS IS THE MAIN METHOD. YOU DON'T NEED TO CHANGE IT.
  vector< vector<char> > maze = readMaze(cin);
  vector<char> moves = calcMoves(maze);
  writeMoves(moves);
  return 0;
}
