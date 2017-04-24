import java.awt.Point;

public class BacktrackCrosswordSolver {

    private char[][] initpuzzle;
    private CollectionOfSpaces[] slots;
    private CollectionOfWords[] words;
    private int[][] fillLetters;
    private int countOfBacktracks;
    public static final char Empty = ' ';
    public static final char Filled = '#';

    public BacktrackCrosswordSolver(char[][] initpuzzle, CollectionOfSpaces[] slots,CollectionOfWords[] words)
     {
          this.initpuzzle = initpuzzle;
          this.words = words;
          this.slots = slots;

    }

    private void reinitialize() {
        fillLetters = new int[initpuzzle.length][initpuzzle[0].length];
        countOfBacktracks = 0;
    }
    

    public void solve() {
        reinitialize();
        
        if   (fillPuzzleSlots(0) ) {
              System.out.println("Solution exists!");
              System.out.println("Backtracks: " + countOfBacktracks);
        }
        else {
              System.out.println("No solution exist!");
        }
    }
    

    private boolean fillPuzzleSlots (int slot) {
    
        if (slot == slots.length) {
            printSolution();
            return true;
        }
        for (CollectionOfWords word : words)
        {
           if (FitWordInSlot(word, slots[slot]) )
            {       putInSlot(word, slots[slot]);
                    if (fillPuzzleSlots(slot + 1))
                     {
                       return true;
                     }
                     removeWordFromSlot(word, slots[slot]);
            }
        }
        countOfBacktracks++;
        return false;
    }

    private boolean FitWordInSlot (CollectionOfWords w, CollectionOfSpaces slot)
    {
       if ( w.getWord().length() != slot.getLength() || w.isUsed())
         {
            return false;
         }
         Point pos = new Point(slot.getStart());
         for ( int i = 0; i < slot.getLength(); i++ )
          {
            if (initpuzzle[pos.x][pos.y] != Empty &&
                initpuzzle[pos.x][pos.y] != w.getWord().charAt(i))
            {
                return false;    
            }
            pos.x += slot.findDirection().x;
            pos.y += slot.findDirection().y;
        }
        return true;
    }
    

    private void putInSlot (CollectionOfWords w, CollectionOfSpaces slot)
     {
        Point pos = new Point(slot.getStart());
        for ( int i = 0; i < slot.getLength(); i++ )
        {
            initpuzzle[pos.x][pos.y] = w.getWord().charAt(i);
            fillLetters[pos.x][pos.y]++;
            pos.x += slot.findDirection().x;
            pos.y += slot.findDirection().y;
        }
        w.setUsed(true);
    }
    

    private void removeWordFromSlot (CollectionOfWords w, CollectionOfSpaces slot)
    {
        Point pos = new Point(slot.getStart());
        for ( int i = 0; i < slot.getLength(); i++ )
        {
            fillLetters[pos.x][pos.y]--;
            if (fillLetters[pos.x][pos.y] == 0)
            {
                initpuzzle[pos.x][pos.y] = Empty;
            }
            pos.x += slot.findDirection().x;
            pos.y += slot.findDirection().y;
        }
         w.setUsed(false);
    }
    

    public void printSolution() {
        printBorder();
        
        for (int r = 0; r < initpuzzle.length; r++ ) {
            System.out.print("|");
            for (int c = 0; c < initpuzzle[r].length; c++) {
                System.out.print(initpuzzle[r][c] + "|");
            }
            System.out.println();
        }
        printBorder();
        System.out.println();
    }

    private void printBorder() {
          for ( int i = 0; i < initpuzzle[0].length * 2 + 1; i++ )
          {
              System.out.print("-");
          }
        System.out.println();    
    }

    public static void main (String[] args) {
        char[][] smallPuzzle = {
           { Empty, Empty, Empty, Filled, Empty, Empty, Empty, Empty, Empty },
           { Empty, Empty, Empty, Empty, Empty, Empty, Empty, Filled, Empty },
           { Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty },
           { Empty, Empty, Empty, Empty, Empty, Filled, Empty, Empty, Empty },
           { Filled, Empty, Empty, Empty, Filled, Empty, Empty, Empty, Filled },
           { Empty, Empty, Empty, Filled, Empty, Empty, Empty, Empty, Empty },
           { Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty },
           { Empty, Filled, Empty, Empty, Empty, Empty, Empty, Empty, Empty },
           { Empty, Empty, Empty, Empty, Empty, Filled, Empty, Empty, Empty }
        };
        

        CollectionOfSpaces[] slots = {
            new CollectionOfSpaces(new Point(0, 0), new Point(1, 0), 4),
            new CollectionOfSpaces(new Point(0, 6), new Point(1, 0), 9),
            new CollectionOfSpaces(new Point(0, 4), new Point(0, 1), 5),
            new CollectionOfSpaces(new Point(4, 1), new Point(0, 1), 3),
            new CollectionOfSpaces(new Point(3, 6), new Point(0, 1), 3),
            new CollectionOfSpaces(new Point(0, 4), new Point(1, 0), 4),
            new CollectionOfSpaces(new Point(0, 5), new Point(1, 0), 3),
            new CollectionOfSpaces(new Point(1, 0), new Point(0, 1), 7),
            new CollectionOfSpaces(new Point(1, 3), new Point(1, 0), 4),
            new CollectionOfSpaces(new Point(2, 7), new Point(1, 0), 7),
            new CollectionOfSpaces(new Point(5, 4), new Point(0, 1), 5),
            new CollectionOfSpaces(new Point(7, 2), new Point(0, 1), 7),
            new CollectionOfSpaces(new Point(5, 8), new Point(1, 0), 4),
            new CollectionOfSpaces(new Point(5, 0), new Point(0, 1), 3),
            new CollectionOfSpaces(new Point(0, 2), new Point(1, 0), 9),
            new CollectionOfSpaces(new Point(3, 0), new Point(0, 1), 5),
            new CollectionOfSpaces(new Point(4, 5), new Point(0, 1), 3),
            new CollectionOfSpaces(new Point(5, 4), new Point(1, 0), 4),
            new CollectionOfSpaces(new Point(2, 0), new Point(0, 1), 9),
            new CollectionOfSpaces(new Point(0, 1), new Point(1, 0), 7),
            new CollectionOfSpaces(new Point(6, 3), new Point(1, 0), 3),
            new CollectionOfSpaces(new Point(8, 6), new Point(0, 1), 3),
            new CollectionOfSpaces(new Point(4, 5), new Point(1, 0), 4),
            new CollectionOfSpaces(new Point(0, 8), new Point(1, 0), 4),
            new CollectionOfSpaces(new Point(5, 0), new Point(1, 0), 4),
            new CollectionOfSpaces(new Point(0, 0), new Point(0, 1), 3),
            new CollectionOfSpaces(new Point(8, 0), new Point(0, 1), 5),
            new CollectionOfSpaces(new Point(6, 0), new Point(0, 1), 9)
        };
        
           CollectionOfWords[] words = {
            new CollectionOfWords("AEROSPACE"),
            new CollectionOfWords("ALCHEMY"),
            new CollectionOfWords("AYATOLLAH"),
            new CollectionOfWords("BAA"),
            new CollectionOfWords("BALD"),
            new CollectionOfWords("BEFIT"),
            new CollectionOfWords("BEST"),
            new CollectionOfWords("BMP"),
            new CollectionOfWords("BOMB"),
            new CollectionOfWords("COMPOTE"),
            new CollectionOfWords("DWEEB"),
            new CollectionOfWords("ELEGIAC"),
            new CollectionOfWords("EST"),
            new CollectionOfWords("GIST"),
            new CollectionOfWords("GOLIATH"),
            new CollectionOfWords("HAL"),
            new CollectionOfWords("HELP"),
            new CollectionOfWords("NEED"),
            new CollectionOfWords("POD"),
            new CollectionOfWords("SCAPAFLOW"),
            new CollectionOfWords("SCRIMMAGE"),
            new CollectionOfWords("THEY"),
            new CollectionOfWords("THOSE"),
            new CollectionOfWords("TIME"),
            new CollectionOfWords("TOE"),
            new CollectionOfWords("TYSON"),
            new CollectionOfWords("WHY"),
            new CollectionOfWords("YAM")
        };
        
       BacktrackCrosswordSolver s = new BacktrackCrosswordSolver(smallPuzzle, slots, words);
       System.out.println("The solution is as:");
       s.printSolution();
       s.solve();
    }
}


class CollectionOfSpaces {
    private Point start;
    private Point direction;
    private int length;
        
    public CollectionOfSpaces ( Point start, Point direction, int length ) {
        this.start = start;
        this.direction = direction;
        this.length = length;
    }
    
    public Point getStart() {
        return start;
    }
    
    public Point findDirection() {
        return direction;
    }
    
    public int getLength() {
        return length;
    }
}


class CollectionOfWords {
    private String word;
    private boolean used;
        
    public CollectionOfWords ( String word ) {
        this.word = word;
        used = false;
    }
    
    public String getWord() {
        return word;
    }
    
    public boolean isUsed() {
        return used;
    }
    
    public void setUsed ( boolean isUsed ) {
        used = isUsed;
    }
}
