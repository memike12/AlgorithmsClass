/* SI 335 Spring 2015
 * Project 3
 * YOUR NAME HERE
 */

import java.util.*;
import java.io.*;

public class solvemaze {

    static class Pair implements Comparable<Pair>{
	int x;
	int y;
	int pri;
	public void changeLocation(int x, int y){
	    this.x = x;
	    this.y = y;}
	public int getX(){
	    return this.x;}
	public int getY(){
	    return this.y;}
	public void addPri(int x){
	    this.pri = x;
	}
	public int compareTo(Pair other){
	    if(this.pri > other.pri)
		return 1;
	    else
		return -1;
	}
    }

    static class ArrayPair {
	HashMap<Pair, Pair> first;
	HashMap<Pair, Integer> second;
	
	public void save(HashMap<Pair, Pair> x, HashMap<Pair, Integer> y){
	    this.first = x;
	    this.second = y;}
    }
    
    static class Graph{
	HashMap<Pair, Vertex> verticies = new HashMap<Pair, Vertex>();

	public void addVertex(Pair loc){
	    System.out.print("Making : " + loc.getX() + " " + loc.getY());
	    Vertex vert = new Vertex();
	    vert.newVertex(loc);
	    verticies.put(loc, vert);}	
	public void addEdge(Pair u, Pair v, int dist){
	    //System.out.println("Adding " + u.getX() + " " + u.getY() + " and " + v.getX() + " " + v.getY());
	    if(!verticies.containsKey(u))
		System.out.print("re  asdf  asdf  Making : " + u.getX() + " " + u.getY());
		this.addVertex(u);
	    if(!verticies.containsKey(v))
		this.addVertex(v);
	    verticies.get(u).addNeighbor(v, dist);
	    verticies.get(v).addNeighbor(u, dist);}
	public int size(){
	    return verticies.size();}
	public HashMap neighbors(Pair u){
	    Vertex vert = verticies.get(u);
	    vert.print();
	    HashMap<Pair, Integer> neighbo = vert.get();
	    return neighbo;
	}
    }

    static class Vertex{
	public HashMap<Pair, Integer> neighbors = new HashMap<Pair, Integer>();
	String path = "";
	public Pair location;

	public void newVertex(Pair loc){
	    this.location = loc;}
	public void addNeighbor(Pair loc, int dist){
	    System.out.print("$Adding " + location.getX() + " " + location.getY() + " and " + loc.getX() + " " + loc.getY());
	    this.neighbors.put(loc, dist);
	    System.out.println(" size = " + neighbors.size());
	    return;
	}
	public void print(){
	    System.out.println("GOTHERERJL:EJELRJ");
	}
	public HashMap<Pair, Integer> get(){
	    System.out.println("GOTHERERJL:EJELRJ");
	    return neighbors;
	}
    }
    

    static int heuristic(Pair a, Pair b){
	int x1 = a.getX();
	int y1 = a.getY();
	int x2 = b.getX();
	int y2 =  b.getY();
	return Math.abs(x1 - x2) + Math.abs(y1 - y2);
    }

    static ArrayPair a_star(Graph graph, Pair start, Pair goal){
	PriorityQueue<Pair> frontier = new PriorityQueue< Pair>();
	HashMap<Pair, Pair> came_from = new HashMap<Pair, Pair>();
	HashMap<Pair, Integer> cost_so_far = new HashMap<Pair, Integer>();
	came_from.put(start, null);
	cost_so_far.put(start, 0);
	start.addPri(0);
	frontier.add(start);

	while(frontier.size()>0){
	    Pair current = frontier.poll();
	    if( current == goal){
		break;
	    }

	    //graph.neighbors(current).keySet.iterator;
	    System.out.println("at " + current.getX() + " " + current.getY());
	    Iterator<Pair> itr = graph.neighbors(current).keySet().iterator();
	    while(itr.hasNext()){
		Pair next = itr.next();
		int new_cost = cost_so_far.get(current) + 1;
		if(!cost_so_far.containsKey(next) || new_cost < cost_so_far.get(next)){
		    cost_so_far.put(next, new_cost);
		    next.addPri(new_cost + heuristic(goal, next));
		    frontier.add(next);
		    came_from.put(next, current);
		}
	    }
	}
	ArrayPair findings = new ArrayPair();
	findings.save(came_from, cost_so_far);
	return findings;

    }
    /* This function takes in a 2D-array that stores a maze description,
       and returns a list of "moves" to make in order to solve the maze.
    */
    static List<Character> calcMoves(char[][] maze) {
	// THIS IS THE FUNCTION YOU NEED TO RE-WRITE!
	// Width and height calculated from maze size, minus borders
	int w = maze.length - 2;
	int h = maze[0].length - 2;
	
	// Start (curY, curX) at the starting position
	int curY = 1;
	int curX = 0;
	ArrayList<Character> movesIfind = new ArrayList<Character>();    

	HashMap dict = new HashMap();
	Pair startPos = new Pair();
	Pair curPos = new Pair();
	Graph Goals = new Graph();
	Graph mapGraph = new Graph();
	ArrayList<Pair> gold = new ArrayList<Pair>();    
	startPos.changeLocation(curX,curY);
	
	Goals.addVertex(startPos);
	
	//radiate search out from start
	int min = Math.min(w+1, h+2);
	int dist = 1;
	
	
	for(int x=0; x<w+2; x++){
	    for(int y=1; y<h+2; y++){
		curPos.changeLocation(x,y);
		if(maze[x][y] == 'O' || maze[x][y] == ' '){
		    if(maze[x][y] == 'O'){
			Pair goldPos = new Pair();
			goldPos.changeLocation(x,y);
			gold.add(goldPos);
		    }
		    Pair thisPos = new Pair();
		    thisPos.changeLocation(x,y);
		    mapGraph.addVertex(thisPos);
		    if(maze[x-1][y] == ' ' || maze[x-1][y] == 'O'){
			Pair nextPos = new Pair();
			nextPos.changeLocation(x-1,y);
			mapGraph.addEdge(thisPos,nextPos, 1);}
		    if(maze[x][y-1] == ' ' || maze[x][y-1] == 'O'){
			Pair nextPos = new Pair();
			nextPos.changeLocation(x,y-1);
			mapGraph.addEdge(thisPos,nextPos, 1);}
		}
	    }
	}
	System.out.println(startPos.getX() + " " + startPos.getY());
	HashMap<Pair, Integer> neigh = mapGraph.neighbors(startPos);
	/*Iterator itr = mapGraph.verticies.keySet().iterator();
	while(itr.hasNext())
	System.out.println(itr.next().neigh);*/
	//System.out.println(mapGraph.verticies.get(startPos).neighbors.iterate());

	/*
	Pair last = startPos;
	while(gold.size()>0){
	    PriorityQueue<Pair> closestNode = new PriorityQueue<Pair>();
	    Iterator<Pair> itr = gold.iterator();
	    while(itr.hasNext()){
		Pair next = itr.next();
		int pri = heuristic(last, next);
		next.addPri(pri);
		closestNode.add(next);
	    }
	    Pair visit = closestNode.poll();
	    a_star(mapGraph, last, visit);
	    System.out.println("Going to " + visit.getX() + " " + visit.getY() + " next");
	    gold.remove(visit);
	    last = visit;
	    }*/

	//dict.put(startPos, 0);
	//System.out.println("Found " + gold.size());
	return movesIfind;

	/*



	// The solution here is terrible: it just randomly mills about until
	// it happens upon the end or it runs out of points.
	ArrayList<Character> moves = new ArrayList<Character>();
	Random rgen = new Random();
	while (moves.size() < 4*h*w) {
	int nextY = curY;
	int nextX = curX;
	char nextMove;
	// randomly choose a direction
	if (rgen.nextBoolean()) {
        // go left/right
        if (rgen.nextBoolean()) {
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
        if (rgen.nextBoolean()) {
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
	moves.add(nextMove);
	curY = nextY;
	curX = nextX;
	}

	// a better way is to utilize FloydWarshall's algorithm to compute the shortest distance between all rings. I have to figure out how to convert the character array into somthing I can use. X's are bad O's are coins. need to have the O's be verticies and the space between be the edges.Graphs store the verticies in a map in a hashMap and an adjacency List or adjacency matrix. 
	return moves;*/
    }

    /* Checks whether a row of text contains only valid maze characters */
    static boolean validRow(String row) {
	// YOU DON'T NEED TO CHANGE THIS FUNCTION.
	for (int i=0; i < row.length(); ++i) {
	    if (" OX".indexOf(row.charAt(i)) < 0) return false;
	}
	return true;
    }

    /* Reads in a maze into a double array of chars. */
    static char[][] readMaze(InputStream in) throws IOException {
	// YOU DON'T NEED TO CHANGE THIS FUNCTION.
	BufferedReader bin = new BufferedReader(new InputStreamReader(in));
	int width = 0;
	String line;
	ArrayList<String> rows = new ArrayList<String>();
	while ((line = bin.readLine()) != null) {
	    if (! validRow(line)) {
		throw new IOException("Invalid maze characters in row: " + line);
	    }
	    // dirty rtrim
	    line = ("!" + line).trim().substring(1);
	    rows.add(line);
	    if (line.length() > width) width = line.length();
	}
	int height = rows.size();
	assert height >= 2;
	assert width >= 2;
	char[][] maze = new char[height][width];
	for (int i=0; i<height; ++i) {
	    Arrays.fill(maze[i], ' ');
	    String row = rows.get(i);
	    row.getChars(0, row.length(), maze[i], 0);
	}
	return maze;
    }

    /* Writes the moves in the list to standard out, one per line. */
    static void writeMoves(List<Character> moves) {
	for (char m : moves) {
	    System.out.println(m);
	}
    }

    public static void main(String[] args) {
	// THIS IS THE MAIN METHOD. YOU DON'T NEED TO CHANGE IT.
	char[][] maze = null;
	try{ maze = readMaze(System.in); }
	catch(IOException e) { e.printStackTrace(); System.exit(1); }
	List<Character> moves = calcMoves(maze);
	writeMoves(moves);
    }
}
