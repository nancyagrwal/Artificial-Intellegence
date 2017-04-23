# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        
        foodList = currentGameState.getFood().asList()
    

        # the warning that a ghost is near is 'Stop'
        if action == 'Stop':
             return float("-inf")

        # considering the non scared ghosts, if the position of the ghost and pacman is same, that is pacman gets eaten up,
        # then its loses.
        
        for ghost_state in newGhostStates:
             if ghost_state.scaredTimer is 0:
                   if ghost_state.getPosition() == newPos:
                        return float("-inf")

        # else pacman goes for the food.
        # as in the question, receprocating  each manhattan distance.
        distance, food = max ([(-1*util.manhattanDistance(newPos, food), food) for food in foodList])
                
        return distance 
        
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.pacmanIndex = 0

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        # we develop three functions:
        # getValue: that calls the minimumVal and the maximumVal functions.
        # minimumVal and maximumVal find the minimum and the maximum value according to the successors.
        
        action = self.getValue(gameState, 0, 0)
        # action gives a pair  of direction and the score at each state.
        return action[0]

    def getValue(self, gameState,  depth , agent_index):

        agents = gameState.getNumAgents()
        current_depth = self.depth
        pacman_pos = self.pacmanIndex
        
        if agent_index >= agents:
            # increasing the depth one by one 
            depth += 1
            # agent index 0 means pacman
            agent_index = 0
            
        # if all the states are expanded at a given depth, return the score
        if depth == current_depth:
            return self.evaluationFunction(gameState)

        # if the agent indexes >=1 , i.e ghosts , then they will minimize the score
       
        if agent_index != pacman_pos:
            return self.minimumVal(gameState, depth , agent_index)

        else:
            # if pacman is the agent index, then it will maximize its score
            return self.maximumVal(gameState, depth , agent_index)

        
    def minimumVal(self, gameState,  depth , agent_index):

        initialAction = ""
        minVal = float("inf")
        # the initial tuple must consist of these arbitrary values.
        value = (initialAction , minVal)
        
        # if there are no more legal actions for an agent, then the score at that state is returned

        if not gameState.getLegalActions(agent_index):
            
                return self.evaluationFunction(gameState)

        
        for action in gameState.getLegalActions(agent_index):
            # new action and score pair must be returned as:
            # if there is no legal action that can be taken, only the score would be returned,
            # else the action and score pair would be returned.
            
            SuccessorValue = self.getValue(gameState.generateSuccessor(agent_index, action), depth , agent_index + 1 )

            #if only the score is returned:
            if isinstance(SuccessorValue , float):
                finalValue = min(value[1] , SuccessorValue)
                
            # if a pair of action and score is returned:    
            else:
                finalValue = min(value[1] , SuccessorValue[1])
                
        
            if finalValue != value[1]:
                   value = (action, finalValue) 

        return value
    

    def maximumVal(self, gameState, depth , agent_index):
      
        initialAction = ""
        maxVal = float("-inf")
        # the initial tuple must consist of these arbitrary values.
        value = (initialAction , maxVal)
        
        # if there are no more legal actions for an agent, then the score at that state is returned

        if not gameState.getLegalActions(agent_index):
             
            return self.evaluationFunction(gameState)

        for action in gameState.getLegalActions(agent_index):
            
            # new action and score pair must be returned as:
            # if there is no legal action that can be taken, only the score would be returned,
            # else the action and score pair would be returned.
            
            SuccessorValue = self.getValue(gameState.generateSuccessor(agent_index, action), depth , agent_index + 1)

            #if only the score is returned:
            if isinstance(SuccessorValue , float):
                 finalValue = max(value[1] , SuccessorValue)
                 
            # if a pair of action and score is returned:    
            else:
                finalValue = max(value[1] , SuccessorValue[1])

            

            if finalValue != value[1]:
                    value = (action, finalValue) 

        return value



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """


    def getAction(self, gameState):
    
        "*** YOUR CODE HERE ***"

        # initially alpha is -infinity and beta is +infinity
        
        action = self.getValue(gameState, 0, 0 , float("-inf") , float("inf"))
        # action gives a pair  of direction and the score at each state.
        return action[0]

    def getValue(self, gameState,  depth , agent_index , alpha , beta):

        agents = gameState.getNumAgents()
        current_depth = self.depth
        pacman_pos = self.pacmanIndex
        
        if agent_index == agents:
            # increasing the depth one by one 
            depth += 1
            # agent index 0 means pacman
            agent_index = 0
            
        # if all the states are expanded at a given depth, return the score
        if depth >= current_depth:
            
            return self.evaluationFunction(gameState)

        if agent_index != pacman_pos:
            # if the agent indexes >=1 , i.e ghosts , then they will minimize the score
            return self.minimumVal(gameState, depth , agent_index , alpha , beta)

            
        # if pacman is the agent index, then it will maximize its score 
      
        else:
            return self.maximumVal(gameState, depth , agent_index , alpha , beta)
        
    def minimumVal(self, gameState,  depth , agent_index , alpha , beta):

        initialAction = ""
        minVal = float("inf")
        # the initial tuple must consist of these arbitrary values.
        value = (initialAction , minVal)
        
       
        if not gameState.getLegalActions(agent_index):
               # if there are no more legal actions for an agent, then the score at that state is returned

                return self.evaluationFunction(gameState)

        
        for action in gameState.getLegalActions(agent_index):
            # new action and score pair must be returned as:
            # if there is no legal action that can be taken, only the score would be returned,
            # else the action and score pair would be returned.
            
            SuccessorValue = self.getValue(gameState.generateSuccessor(agent_index, action), depth , agent_index + 1  , alpha , beta)

           
            if value[1] == float("inf"):

               if isinstance(SuccessorValue , float):
                   finalValue = SuccessorValue
               else:
                   finalValue = SuccessorValue[1]

            else:
                
               #if only the score is returned:
               if isinstance(SuccessorValue , float):
                   finalValue = min(value[1] , SuccessorValue)
                
               # if a pair of action and score is returned:    
               else:
                 finalValue = min(value[1] , SuccessorValue[1])
                
        
            if finalValue != value[1]:
                   value = (action, finalValue) 

            # choosing the new alpha, always the minimum value is chosen.
            if alpha != float("inf") and value[1] < alpha:
                 return value       

            # choosing the new alpha, always the minimum value is chosen. 
            beta = value[1] if beta is float("inf") else min(beta, value[1]) 
           
            
        return value
    

    def maximumVal(self, gameState, depth , agent_index , alpha , beta):
      
        initialAction = ""
        maxVal = float("-inf")
        # the initial tuple must consist of these arbitrary values.
        value = (initialAction , maxVal)
        
        if not gameState.getLegalActions(agent_index):
            # if there are no more legal actions for an agent, then the score at that state is returned

            return self.evaluationFunction(gameState)

        
        for action in gameState.getLegalActions(agent_index):
            
            # new action and score pair must be returned as:
            # if there is no legal action that can be taken, only the score would be returned,
            # else the action and score pair would be returned.
            
            SuccessorValue = self.getValue(gameState.generateSuccessor(agent_index, action), depth , agent_index + 1, alpha , beta)

            #if only the score is returned:
            if isinstance(SuccessorValue , float):
                 finalValue = max(value[1] , SuccessorValue)
                 
            # if a pair of action and score is returned:    
            else:
                finalValue = max(value[1] , SuccessorValue[1])

                
            if finalValue != value[1]:
                    value = (action, finalValue)
                    
            if beta != float("inf") and value[1] > beta:
                   return value

            alpha = max(alpha, value[1])
           

        return value


       


        
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        action = self.getValue(gameState, 0, 0)
        return action[0]

        # we develop three functions:
        # getValue: that calls the expectedValue and the maximumVal functions.
        # expectedValue and maximumVal find the expected and the maximum value according to the successors.
        
    def getValue(self, gameState, depth , agent_index ):

        agents = gameState.getNumAgents()
        currentDepth = self.depth
        pacman_pos = self.pacmanIndex
        
        if agent_index >= agents:
            depth += 1
            agent_index = 0
            
        # if all the states are expanded at a given depth, return the score
        if depth == currentDepth:
            
            return self.evaluationFunction(gameState)

        if agent_index != pacman_pos:
             # if the agent indexes >=1 , i.e ghosts , then they will give a random result according to the probablity.

             return self.expectedValue(gameState, depth , agent_index)
               
        # if pacman is the agent index, then it will maximize its score
        else:
            
             return self.maximumVal(gameState, depth , agent_index)
        
    def expectedValue(self, gameState, depth , agent_index):

        initialAction = ""
        expVal = 0
        # the initial tuple must consist of these arbitrary values.
        result = [initialAction , expVal]
        
        d= len(gameState.getLegalActions(agent_index))

        # if no legal action is allowed further, return the score
        if not gameState.getLegalActions(agent_index):
            return self.evaluationFunction(gameState)
        
        probability = 1.0/d

        for action in gameState.getLegalActions(agent_index):
                        
            SuccessorValue = self.getValue(gameState.generateSuccessor(agent_index, action), depth , agent_index + 1)

            #if only the score is returned:
            if isinstance(SuccessorValue , float):
                  result[1] += SuccessorValue * probability
                                  
            # if a pair of action and score is returned:    
            else:
                 result[1] +=  SuccessorValue[1]  * probability
                
                   
        return (action,result[1])

    def maximumVal(self, gameState, depth , agent_index):
        
        initialAction = ""
        maxVal = float("-inf")
        # the initial tuple must consist of these arbitrary values.
        result = (initialAction , maxVal)
       

        if not gameState.getLegalActions(agent_index):
            return self.evaluationFunction(gameState)

        for action in gameState.getLegalActions(agent_index):
            # new action and score pair must be returned as:
            # if there is no legal action that can be taken, only the score would be returned,
            # else the action and score pair would be returned.
            
            SuccessorValue = self.getValue(gameState.generateSuccessor(agent_index, action), depth , agent_index + 1)

            #if only the score is returned:
            if isinstance(SuccessorValue , float):
                 finalValue = max(result[1] , SuccessorValue)
                 
            # if a pair of action and score is returned:    
            else:
                finalValue = max(result[1] , SuccessorValue[1])

            

            if finalValue != result[1]:
                    result = (action, finalValue) 

        return result
    

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    def nextCoordinate(point):
         nextCoordinate = []
         nextCoordinate.extend([((point[0]-1,point[1])), ((point[0],point[1]-1)), ((point[0],point[1]+1)) , ((point[0]+1,point[1]))])
         return nextCoordinate

     
    pacman_pos = currentGameState.getPacmanPosition()
    food_pos = currentGameState.getFood()
    distancetoGhosts = []
    foodList = food_pos.asList()
    noFoodPoints = 0
    distanceToFood = []
    score = currentGameState.getScore()
   

    # we initially take the heuristic as 0:
    h = 0

    # ghosts are a minimizer , therefore distance to ghosts need to be taken into account as well.     
    for ghostState in currentGameState.getGhostStates():
         distancetoGhosts .append (util.manhattanDistance(ghostState.getPosition(),pacman_pos))

     
    minDist = (min(distancetoGhosts))     
   
    # eating a capsule is a maximizer, therefore scared times need to be taken into account.
    for scaredTime in [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]:
         h += scaredTime

     
    # eating food is a maximizer, therefore must be added.
    # Similarly, if there is an empty point with no food, its count will have to be deducted.
    
    for food in foodList:
        
                # checking the neighbours of the food coordinate:        
                for foodLoc in nextCoordinate(food):
                    
                   # if the coordinate is not in the foodList, then we
                   #increase the empty space by 1 , else calculate the manhattan distance with the food position
                   if foodLoc not in foodList:
                       
                      noFoodPoints += 1
                      
                distanceToFood.append (util.manhattanDistance(pacman_pos,food))

             
    # reciprocating the food distance values:
    inverse = 0
    if len(distanceToFood) > 0:
         # x is the min food distance
         x= (min(distanceToFood))
         inverse = 1.0/x

    
    h +=  (score- float(noFoodPoints)*7) +  (minDist *((inverse**6))) 
    return h

# Abbreviation
better = betterEvaluationFunction

