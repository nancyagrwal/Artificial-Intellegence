
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """
    "*** YOUR CODE HERE ***"
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
   
    # explored is a set to keep track of the explored nodes
    # dfsfringe is the stack used to push the vertex on being traversed, and popped once expanded.
    # start is the start state of the pacman
    # if the successor results in a goal state, then the action (and the direction) is returned ,
    # else the successor is pushed into the stack.
    # the process is repeated till all the vertices have been explored.
    
    explored = []
    dfsfringe = util.Stack()
    start = problem.getStartState()
    
    if problem.isGoalState(start):
        return []
        
    dfsfringe.push((start,[],[]))
   
    while not dfsfringe.isEmpty():
        vertex,actions,explored = dfsfringe.pop()

        if vertex not in explored:
           explored.append(vertex)
       
           if problem.isGoalState(vertex):
              return actions

           for successor,direction,stepCost in problem.getSuccessors(vertex):
              if successor not in explored:
                dfsfringe.push((successor,actions+[direction],explored+[vertex]))
                
    return False
    util.raiseNotDefined()

                 
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
   
    # explored is a set to keep track of the explored nodes
    # bfsfringe is the first-in first-out queue used to push the vertex on being traversed, and popped once expanded.
    # start is the start state of the pacman
    # if the successor results in a goal state, then the action (and the direction) is returned ,
    # else the successor is pushed into the queue
    # the process is repeated till all the vertices have been explored.
    
   
    bfsfringe = util.Queue()
    explored = []
    start = problem.getStartState()

    if problem.isGoalState(start):
        return []
     
    bfsfringe.push((start,[]))
    while not bfsfringe.isEmpty():
        vertex,actions = bfsfringe.pop()

        if  vertex not in explored:
            explored.append(vertex)

            if problem.isGoalState(vertex):
                 return actions
               
            for successor,direction,stepCost in problem.getSuccessors(vertex):
                if successor not in explored:
                     bfsfringe.push((successor,actions + [direction]))
                  
    return []
    util.raiseNotDefined()

    
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    # explored is a set to keep track of the explored nodes
    # ucsfringe is the priority queue used to push the vertex on being traversed, and popped once expanded.
    # start is the start state of the pacman
    # if the successor results in a goal state, then the action (and the direction) is returned ,
    # else the successor is pushed into the queue
    # the process is repeated till all the vertices have been explored.
    
                 
    ucsfringe = util.PriorityQueue()
    explored = []
    start = problem.getStartState()

    if problem.isGoalState(start):
        return []
    
    ucsfringe.push((start,[]),0)
    
    while not ucsfringe.isEmpty():
        vertex,actions = ucsfringe.pop()

        if vertex not in explored:
           explored.append(vertex)

           if problem.isGoalState(vertex):
              return actions
        
           for successor,direction,stepCosts in problem.getSuccessors(vertex):
               if successor not in explored:
                   ucsfringe.push((successor , actions + [direction]), problem.getCostOfActions(actions + [direction]))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    # explored is a set to keep track of the explored nodes
    # AStarfringe is the priority queue used to push the vertex on being traversed, and popped once expanded.
    # start is the start state of the pacman
    # the heuristic can be passed as nullHeuristic,manhattanHeuristic, EuclidianHeusristic etc.
    # if the successor results in a goal state, then the action (and the direction) is returned , along with the heuristic
    # else the successor is pushed into the queue
    # the process is repeated till all the vertices have been explored.

    explored = []
    aStarfringe = util.PriorityQueue()
    start = problem.getStartState()
    cost_heuristic = heuristic(start, problem)

    if problem.isGoalState(start):
       return []
       
    aStarfringe.push((start,[]), cost_heuristic)

    while not aStarfringe.isEmpty():
        vertex,actions = aStarfringe.pop()

        if vertex not in explored:
            explored.append(vertex)

            if problem.isGoalState(vertex):
                 return actions
                  
            for successor,direction,stepCost in problem.getSuccessors(vertex):
                if not successor in explored:
                    score = problem.getCostOfActions(actions + [direction]) + heuristic(successor,problem)
                    aStarfringe.push((successor, actions + [direction]),score)

    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
