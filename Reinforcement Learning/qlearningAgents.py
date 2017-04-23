# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qvalues = {}


    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"

        if not (state,action) in self.qvalues:
             return 0.0
        else:
             return self.qvalues[(state, action)]
        util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"

        legalActions = self.getLegalActions(state)
        value = None
        nextAction = None
       
        # checking if no legal actions are possible,
        if len(legalActions) == 0:
             return 0.0

        for action in legalActions:
             # checking for legal actions, to return the maximum QValue  
             qVal = self.getQValue(state, action)
             if qVal > value:
                 nextAction = action
                 value = qVal
       
        return value
        util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"

        legalActions = self.getLegalActions(state)
        value = None
        nextAction = None
        
        # checking if no legal actions are possible,
        if len(legalActions) == 0:
             return None
       
        for action in legalActions:
             # checking for legal actions, to return the best action
             qVal = self.getQValue(state, action)
             if qVal > value:
                nextAction = action
                value = qVal
           
        return nextAction
        util.raiseNotDefined()

        
    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        prob = self.epsilon
        # checking if there is no legal action possible
        if len(legalActions) == 0:
              return None
        
        # taking a random action with probability self.epsilon
        if util.flipCoin(prob):
              action =  random.choice(legalActions)
        else:     
              action =  self.computeActionFromQValues(state)

        return action
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        discountRate = self.discount
        learningRate = self.alpha
       
        #updating the Q(state, action) as 0.0 if we have not seen the state(as previously)
        if not (state, action) in self.qvalues:
              self.qvalues[(state, action)] = 0.0

        #updating the Q-Value:
        curQVal = self.qvalues[(state, action)]
        nextQVal = self.computeValueFromQValues(nextState)
        changeInQVal =  (discountRate * nextQVal) - curQVal
        value = changeInQVal + reward
        self.qvalues[(state, action)] = curQVal + (learningRate * value)
               

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()
        

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"

        qValue = 0.0
        feature = self.featExtractor.getFeatures(state, action)
        
        # calculating the weighted combination of features.
        for key in feature.keys():
    	       qValue += (self.weights[key] * feature[key])
        return qValue
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        discountRate = self.discount
        learningRate = self.alpha
        currQVal = self.getQValue(state , action)
        nextQVal = self.computeValueFromQValues(nextState)
        features = self.featExtractor.getFeatures(state, action)
        
        #computing the updated Q-Value:        
        changeInQVal =  (discountRate * nextQVal) - currQVal
        value = changeInQVal + reward
              
        for key in features.keys():
              val = features[key]*value*learningRate
    	      self.weights[key] += val

                
    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
