/*
	while(dist < min){
	    int y = dist;
	    for(int x = 1; x <= dist; x++){
		curPos.changeLocation(x,y);
		System.out.println("searching " + x + " " + y);
		if(maze[x][y] == 'O' || maze[x][y] == ' '){
		    if(maze[x][y] == 'O'){
			gold.add(curPos);
			//System.out.println("O");
		    }
		    mapGraph.addVertex(curPos);
		    if(maze[x-1][y] == ' ' || maze[x-1][y] == 'O'){
			Pair nextPos = new Pair();
			nextPos.changeLocation(x-1,dist);
			mapGraph.addEdge(curPos,nextPos, 1);}
		    if(maze[x][y-1] == ' ' || maze[x][y-1] == 'O'){
			Pair nextPos = new Pair();
			nextPos.changeLocation(x,dist-1);
			mapGraph.addEdge(curPos,nextPos, 1);}
		}
		y--;
	    }
	    dist++;
	    }

	    if(min == w+1)*/
	/*
	for(dist=1; dist<min; dist++){
	    for(int x=1; x<=dist; x++){
		curPos.changeLocation(x,dist);
		System.out.println("x: " + x + " " + dist);
		if(maze[x][dist] == 'O' || maze[x][dist] == ' '){
		    if(maze[x][dist] == 'O'){
			gold.add(curPos);
			
		    }
		    mapGraph.addVertex(curPos);
		    if(maze[x-1][dist] == ' ' || maze[x-1][dist] == 'O'){
			Pair nextPos = new Pair();
			nextPos.changeLocation(x-1,dist);
			mapGraph.addEdge(curPos,nextPos, 1);}
		    if(maze[x][dist-1] == ' ' || maze[x][dist-1] == 'O'){
			Pair nextPos = new Pair();
			nextPos.changeLocation(x,dist-1);
			mapGraph.addEdge(curPos,nextPos, 1);}
		}
	    }
	    for(int y=1; y<dist; y++){
		System.out.println("y : " + dist + " "  + y);
		curPos.changeLocation(dist,y);
		if(maze[dist][y] == 'O' || maze[dist][y] == ' '){
		    if(maze[dist][y] == 'O'){
			gold.add(curPos);
			System.out.println("O");
		    }
		    mapGraph.addVertex(curPos);
		    if(maze[dist-1][y] == ' ' || maze[dist-1][y] == 'O'){
			Pair nextPos = new Pair();
			nextPos.changeLocation(dist-1,y);
			mapGraph.addEdge(curPos,nextPos, 1);}
		    if(maze[dist][y-1] == ' ' || maze[dist][y-1] == 'O'){
			Pair nextPos = new Pair();
			nextPos.changeLocation(dist,y-1);
			mapGraph.addEdge(curPos,nextPos, 1);}
		}
	    }

	}
	if(min == w+1){
	    for(int travx = dist; travx<h+1; travx++){
		for(int y=0; y<dist; y++){
		    System.out.println("Here");
		    curPos.changeLocation(travx,y);
		    if(maze[travx][y] == 'O' || maze[travx][y] == ' '){
			if(maze[travx][y] == 'O')
			    gold.add(curPos);
			mapGraph.addVertex(curPos);
			if(maze[travx-1][y] == ' ' || maze[travx-1][y] == 'O'){
			    Pair nextPos = new Pair();
			    nextPos.changeLocation(dist-1,y);
			    mapGraph.addEdge(curPos,nextPos, 1);}
			if(maze[travx][y-1] == ' ' || maze[travx][y-1] == 'O'){
			    Pair nextPos = new Pair();
			    nextPos.changeLocation(travx,y-1);
			    mapGraph.addEdge(curPos,nextPos, 1);}
		    }
		}
	    }
	}
	else{
	     for(int travY = dist; travY<h+1; travY++){
		 for(int x=0; x<dist; x++){
		     System.out.println("Here2");
		     curPos.changeLocation(x,travY);
		     if(maze[x][travY] == 'O' || maze[x][travY] == ' '){
			 if(maze[x][travY] == 'O')
			     gold.add(curPos);
			 mapGraph.addVertex(curPos);
			 if(maze[x-1][travY] == ' ' || maze[x-1][travY] == 'O'){
			     Pair nextPos = new Pair();
			     nextPos.changeLocation(x-1,dist);
			     mapGraph.addEdge(curPos,nextPos, 1);}
			 if(maze[x][travY-1] == ' ' || maze[x][travY-1] == 'O'){
			     Pair nextPos = new Pair();
			     nextPos.changeLocation(x,travY-1);
			     mapGraph.addEdge(curPos,nextPos, 1);}
		     }
		 }
	    }
	}
	*/
 static class Graph{
	HashMap<Pair, Vertex> verticies = new HashMap<Pair, Vertex>();

	public void addVertex(Pair loc){
	    Vertex vert = new Vertex();
	    vert.newVertex(loc);
	    verticies.put(loc, vert);}	
	public void addEdge(Pair u, Pair v, int dist){
	    if(!verticies.containsKey(u))
		this.addVertex(u);
	    if(!verticies.containsKey(v))
		this.addVertex(v);
	    verticies.get(u).addNeighbor(v, dist);
	    verticies.get(v).addNeighbor(u, dist);}
	public int size(){
	    return verticies.size();}
	public HashMap neighbors(Pair u ){
	    return verticies.get(u).neighbors;
	}
    }
