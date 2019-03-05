# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        ghosts_pos=currentGameState.getGhostPositions()
        mah_list=[]
        for i in range(0,len(ghosts_pos)):
            mah_dis=abs(newPos[0]-ghosts_pos[i][0])+abs(newPos[1]-ghosts_pos[i][1])
            mah_list.append(mah_dis)
        #print("we have ",len(ghosts_pos),"ghosts")
        min_ghost=min(mah_list)
    #    print("the min distance is ",min_ghost)
        if(min_ghost<=3):
            return min_ghost
        rewards=99999
        if(min_ghost>3):#when the ghost is far away, it need to consider the food distance, choose an action closer to the food
            food_list=newFood.asList()
            food_dis=[]
            for i in range(0,len(food_list)):
                food_dis.append(abs(food_list[i][0]-newPos[0])+abs(food_list[i][1]-newPos[1]))
            if(len(food_dis)!=0):
                min_food_dis=min(food_dis)
                #print("the min food is ",min_food_dis)
                rewards=99999-min_food_dis
            if(currentGameState.hasFood(newPos[0],newPos[1])):
                #print("the action is ",action,"has food!! 99999")
                return 99999
            if(action=='Stop'):
                #print("why does pacman stop???")
                return 0
        #print("the action is ",action,"reward is ",rewards)
        return rewards
        food_num=successorGameState.getNumFood()
        rewards=food_num
        rewards=rewards+min_ghost
    #    print("current rewards ",rewards)
        return rewards

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def value(agentIndex,depth,gameState,evaluate_func):
            #print("for now, the depth is: ",depth)
            #print("player: ",agentIndex)
            if(gameState.isWin() or gameState.isLose()):
                return evaluate_func(gameState)
            if(depth==0):
                #print("depth==0!")
                return evaluate_func(gameState)
            elif(agentIndex==0):
                #print("pacman going")
                return max_value(agentIndex,depth,gameState,evaluate_func)
            elif(agentIndex>0):
                #print("ghost going: ",agentIndex)
                if(agentIndex==gameState.getNumAgents()-1):
                    depth-=1
                return min_value(agentIndex,depth,gameState,evaluate_func)
        def max_value(agentIndex,depth,gameState,evaluate_func):
            value_=-99999
            legal_action=gameState.getLegalActions(agentIndex)
            for action in legal_action:
                nextState=gameState.generateSuccessor(0,action)
                value_=max(value_,value(agentIndex+1,depth,nextState,evaluate_func))
            return value_
        def min_value(agentIndex,depth,gameState,evaluate_func):
            value_=99999
            legal_action=gameState.getLegalActions(agentIndex)
            #print("the len of legal_action is: ",len(legal_action))
            for action in legal_action:
                next_state=gameState.generateSuccessor(agentIndex,action)
                if(agentIndex==gameState.getNumAgents()-1):
                    new_value=value(0,depth,next_state,evaluate_func)
                    #print("next to run pacman, the new value is: ",new_value)
                    value_=min(value_,new_value)
                else:
                    new_value=value(agentIndex+1,depth,next_state,evaluate_func)
                    #print("next to run ghost, the new value is: ",new_value)
                    value_=min(value_,new_value)
            #print("now the ghost is: ",agentIndex," the value_ is:",value_)
            return value_
        next_action=gameState.getLegalActions(0)
        scores=[]
        action_take=[]
        for action in next_action:
            next_state=gameState.generateSuccessor(0,action)
            scores.append(value(1,self.depth,next_state,self.evaluationFunction))
            action_take.append(action)
        max_score=max(scores)
        for i in range(0,len(scores)):
            if(max_score==scores[i]):
                return action_take[i]
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def value(agentIndex,depth,gameState,evaluate_func,alpha,beta):
            #print("for now, the depth is: ",depth)
            #print("player: ",agentIndex)
            if(gameState.isWin() or gameState.isLose()):
                list=[evaluate_func(gameState),0]
                return list
            if(depth==0):
                #print("depth==0!")
                list=[evaluate_func(gameState),0]
                return list
            elif(agentIndex==0):
                #print("pacman going")
                return max_value(agentIndex,depth,gameState,evaluate_func,alpha,beta)
            elif(agentIndex>0):
                #print("ghost going: ",agentIndex)
                if(agentIndex==gameState.getNumAgents()-1):
                    depth-=1
                return min_value(agentIndex,depth,gameState,evaluate_func,alpha,beta)
        def max_value(agentIndex,depth,gameState,evaluate_func,alpha,beta):
            value_=-9999
            legal_action=gameState.getLegalActions(agentIndex)
            new_action=legal_action[0]
            for action in legal_action:
                nextState=gameState.generateSuccessor(0,action)
                new_result=value(agentIndex+1,depth,nextState,evaluate_func,alpha,beta)
                new_value=new_result[0]
                if(new_value>value_):
                    new_action=action
                value_=max(value_,new_value)
                if(value_>beta):
                    return [value_,action]
                alpha=max(alpha,value_)
            list=[value_,new_action]
            return list
        def min_value(agentIndex,depth,gameState,evaluate_func,alpha,beta):
            value_=9999
            legal_action=gameState.getLegalActions(agentIndex)
            #print("the len of legal_action is: ",len(legal_action))
            min_action=legal_action[0]
            for action in legal_action:
                next_state=gameState.generateSuccessor(agentIndex,action)
                if(agentIndex==gameState.getNumAgents()-1):
                    new_result=value(0,depth,next_state,evaluate_func,alpha,beta)
                    new_value=new_result[0]
                    #print("next to run pacman, the new value is: ",new_value)
                    if(new_value<value_):
                        min_actiom=action
                    value_=min(value_,new_value)
                else:
                    new_result=value(agentIndex+1,depth,next_state,evaluate_func,alpha,beta)
                    new_value=new_result[0]
                    #print("next to run ghost, the new value is: ",new_value)
                    if(new_value<value_):
                        min_actiom=action
                    value_=min(value_,new_value)
            #print("now the ghost is: ",agentIndex," the value_ is:",value_)
                if(value_<alpha):
                    return [value_,action]
                beta=min(beta,value_)
            list=[value_,min_action]
            return list

        value_action=value(0,self.depth,gameState,self.evaluationFunction,-999999,999999)
        return value_action[1]

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
        def value(agentIndex,depth,gameState,evaluate_func):
            #print("for now, the depth is: ",depth)
            #print("player: ",agentIndex)
            if(gameState.isWin() or gameState.isLose()):
                list=[evaluate_func(gameState),0]
                return list
            if(depth==0):
                #print("depth==0!")
                list=[evaluate_func(gameState),0]
                return list
            elif(agentIndex==0):
                #print("pacman going")
                return max_value(agentIndex,depth,gameState,evaluate_func)
            elif(agentIndex>0):
                #print("ghost going: ",agentIndex)
                if(agentIndex==gameState.getNumAgents()-1):
                    depth-=1
                return exp_value(agentIndex,depth,gameState,evaluate_func)
        def max_value(agentIndex,depth,gameState,evaluate_func):
            value_=-9999
            legal_action=gameState.getLegalActions(agentIndex)
            new_action=legal_action[0]
            for action in legal_action:
                nextState=gameState.generateSuccessor(0,action)
                new_result=value(agentIndex+1,depth,nextState,evaluate_func)
                new_value=new_result[0]
                if(new_value>value_):
                    new_action=action
                value_=max(value_,new_value)
            list=[value_,new_action]
            return list
        def exp_value(agentIndex,depth,gameState,evaluate_func):
            value_=0
            legal_action=gameState.getLegalActions(agentIndex)
            #print("the len of legal_action is: ",len(legal_action))
            min_action=legal_action[0]
            for action in legal_action:
                next_state=gameState.generateSuccessor(agentIndex,action)
                if(agentIndex==gameState.getNumAgents()-1):
                    new_result=value(0,depth,next_state,evaluate_func)
                    new_value=new_result[0]
                    value_+=new_value*(1/len(legal_action))
                else:
                    new_result=value(agentIndex+1,depth,next_state,evaluate_func)
                    new_value=new_result[0]
                    value_+=new_value*(1/len(legal_action))
            list=[value_,min_action]
            return list

        value_action=value(0,self.depth,gameState,self.evaluationFunction)
        return value_action[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:<calculate the manhattanDistance between pacman and food, pacman and ghost, the closer the food the
    bigger the score, the closer the ghost, the minier the score
    the score of the food is (10-distance)*2, the penalty of the ghost the is (10-distance)*-8>
    """
    "*** YOUR CODE HERE ***"
    num=currentGameState.getNumAgents()-1
    food_num=currentGameState.getNumFood()
    current_food=currentGameState.getFood().asList()
    #print("the height is ",currentGameState.getFood().height)
    ghosts_pos=currentGameState.getGhostPositions()
    capsule_pos=currentGameState.getCapsules()
    food_dis=[]
    ghost_dis=[]
    cal_dis=[]
    all_dot=currentGameState.getFood().height*currentGameState.getFood().width
    dis_sum=0
    pacPos = currentGameState.getPacmanPosition()
    for i in range(0,food_num):
        food_dis.append(util.manhattanDistance(current_food[i],pacPos))
        dis_sum+=util.manhattanDistance(current_food[i],pacPos)
    for i in range(0,len(ghosts_pos)):
        ghost_dis.append(util.manhattanDistance(ghosts_pos[i],pacPos))
    final_score=currentGameState.getScore()
    final_score+=99999
    final_score-=dis_sum

    if(len(food_dis)!=0):
      final_score=final_score-food_num*20-min(food_dis)
    final_score-=len(capsule_pos)*25

    for i in range(0,len(ghost_dis)):
        if(ghost_dis[i]<3):
            return min(ghost_dis)

    return final_score


# Abbreviation
better = betterEvaluationFunction
