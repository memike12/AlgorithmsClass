/* SI 335 Spring 2015
 * Project 1: OMA Service Selection
 *
 * This contains the "simple" algorithm to do the service
 * selection, provided as example/starter code.
 */
 
import java.util.Scanner;
 
class selection {
  public static void main(String[] args) {
    Scanner in = new Scanner(System.in);
 
    // Read in the number of communities
    int k = in.nextInt();
    in.nextLine();
 
    // Read in the community names
    String[] communities = new String[k];
    for (int i=0; i<k; ++i) {
      communities[i] = in.nextLine();
    }
 
    // Read in the number of proles
    int n = in.nextInt();
    
    // Read in the proles' names and rankings
    // Rankings will be stored in an array of arrays.
    // Each array in the array will contain all k rankings for that prole.
    String[] proleNames = new String[n];
    int[][] proleRanks = new int[n][k];
    for (int i=0; i<n; ++i) {
      proleNames[i] = in.next();
 
      // Read in the rankings
      for (int j=0; j<k; ++j) {
        proleRanks[i][j] = in.nextInt();
      }
    }
 
    // This list will hold the names that are already picked
    String[] picked = new String[n];
 
    // Now do the actual selection
    for (int i = 0; i < n; ++i) {
      int comm = i % k; // Which community gets this pick
      int rank = 0; // start with the top-ranked pick
      boolean found = false;
      String nextPick = "";
 
      while(! found) { 
        rank = rank + 1;
 
        for (int j = 0; j < n; ++j) {
          if (proleRanks[j][comm] == rank) {
            nextPick = proleNames[j];
          }
        }
 
        // Now nextPick is the name of the prole with rank "rank"
        // by community "comm". But are they already picked?
 
        found = true;
        for (int j = 0; j < i; ++j) {
          if (picked[j] == nextPick) found = false;
        }
      }
 
      // Now we have the actual pick!
      // Print it and then add to the "picked" list.
      System.out.println(nextPick + " " + communities[comm]);
      picked[i] = nextPick;
    }
 
    System.exit(0);
  }
}
