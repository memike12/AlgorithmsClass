/* SI 335 Spring 2015
 * Project 1: OMA Service Selection
 *
 * This contains the "simple" algorithm to do the service
 * selection, provided as example/starter code.
 */
 
import java.util.Scanner;
import java.util.HashMap;
 
class ImprovedSelection {

    public class communityRankings{
        String community;
        String[] rankings;
        int nextIndex = 0;

        public communityRankings(String communityName){
            this.community = communityName;
        }

        public communityRankings(){
        }

        public void communityRankingName(String communityName){
            this.community = communityName;
        }

        public void setSize(int num){
            this.rankings = new String[num];
        }

        public void add(int index, String Prole){
            rankings[index] = Prole;
        }

        public String getName(int index){
            return rankings[index];
        }
        public int getNextIndex(){
            nextIndex++;
            return nextIndex-1;
        }
    }

    public static void main(String[] args) {
    Scanner in = new Scanner(System.in);
 
    // Read in the number of communities
    int k = in.nextInt();
    in.nextLine();
 
    // Read in the community names
    communityRankings[] communities = new communityRankings[k];
    for (int i=0; i<k; ++i) {
        String name = (String)in.nextLine();
        communities[i] = new communityRankings(name);
    }
 
    // Read in the number of proles
    int n = in.nextInt();
    for (int i=0; i<k; ++i) {
        communities[i].setSize(n);
    }
    HashMap<String, Boolean> proleFoundMap = new HashMap<String, Boolean>(n);

    // Read in the proles' names and rankings

    String proleName;
    int rank;
    for (int i=0; i<n; ++i) {
        proleName = in.next();
        proleFoundMap.put(proleName, false);
        for(int jj=0; jj<k; jj++){
            rank = in.nextInt();
            communities[jj].add(rank, proleName);
        }
        
    }

    // Now do the actual selection
    String nextPick;
    int comm, nextRankToChoose;
    for (int i = 0; i < n; ++i) {
        comm = i % k;
        nextRankToChoose = communities[comm].getNextIndex();
        nextPick = communities[comm].getName(nextRankToChoose);
        while(proleFoundMap.get(nextPick)){
            nextRankToChoose = communities[comm].getNextIndex();
            nextPick = communities[comm].getName(nextRankToChoose);
        }
        proleFoundMap.put(nextPick, true);
    }
    


    System.exit(0);
  }
}
