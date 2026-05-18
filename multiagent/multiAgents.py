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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """

        # 1. Hàm Điều phối (Dispatcher)
        def value(state, depth, agentIndex):
            # Điều kiện dừng: đạt độ sâu tối đa hoặc game kết thúc
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            # Lượt của Pacman (agent 0) -> Tìm Max
            if agentIndex == 0:
                return maxValue(state, depth, agentIndex)
            # Lượt của Ma (agent > 0) -> Tìm Min
            else:
                return minValue(state, depth, agentIndex)

        # 2. Hàm cho Pacman (MAX)
        def maxValue(state, depth, agentIndex):
            v = float("-inf")
            legalActions = state.getLegalActions(agentIndex)
            
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                # Lượt tiếp theo luôn là con ma đầu tiên (agent 1) ở CÙNG độ sâu
                v = max(v, value(successor, depth, agentIndex + 1))
            return v

        # 3. Hàm cho các Ghost (MIN)
        def minValue(state, depth, agentIndex):
            v = float("inf")
            legalActions = state.getLegalActions(agentIndex)
            
            # Tính toán ai đi tiếp theo
            nextAgent = agentIndex + 1
            nextDepth = depth
            
            # Nếu đã duyệt xong con ma cuối cùng, quay vòng lại cho Pacman
            # VÀ tăng độ sâu (depth) lên 1
            if nextAgent == state.getNumAgents():
                nextAgent = 0
                nextDepth += 1

            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                v = min(v, value(successor, nextDepth, nextAgent))
            return v

        # 4. Tìm kiếm hành động tốt nhất ở Node gốc (Root)
        bestAction = None
        maxScore = float("-inf")
        
        # Pacman thử từng hành động hợp lệ ở trạng thái hiện tại
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            # Gọi đệ quy bắt đầu từ con ma đầu tiên (agent 1) tại độ sâu 0
            score = value(successor, 0, 1) 
            
            # Cập nhật hành động tốt nhất
            if score > maxScore:
                maxScore = score
                bestAction = action

        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            numAgents = state.getNumAgents()
            # PACMAN (MAX)
            if agentIndex == 0:
                value = float('-inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = max(value, alphabeta(successor, depth, 1, alpha, beta))

                    if value > beta:
                        return value
                    alpha = max(alpha, value)
                return value
            # GHOST (MIN)
            else:
                value = float('inf')
                nextAgent = agentIndex + 1
                nextDepth = depth
                if nextAgent == numAgents:
                    nextAgent = 0
                    nextDepth += 1
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = min(value, alphabeta(successor, nextDepth, nextAgent, alpha, beta))
                    if value < alpha:
                        return value
                    beta = min(beta, value)
                return value
        # ROOT (Pacman)
        bestAction = None
        bestValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = alphabeta(successor, 0, 1, alpha, beta)
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, bestValue)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        legalActions = gameState.getLegalActions(0)

        # Tinh expectimax value cho tung nuoc di cua Pacman
        # Bat dau tu agent 1 (ghost dau tien), depth = 0
        scores = [self.expectimax(gameState.generateSuccessor(0, action), 1, 0)
                        for action in legalActions]

        # Chon action co score cao nhat
        bestScore = max(scores)
        bestAction = legalActions[scores.index(bestScore)]
        return bestAction

    def expectimax(self, gameState: GameState, agentIndex: int, depth: int):
        numAgents = gameState.getNumAgents()

        # Dung khi thang hoac thua
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Dung khi Pacman da di du so luot (depth)
        if agentIndex == 0 and depth == self.depth:
            return self.evaluationFunction(gameState)

        # Tinh agent va depth tiep theo
        nextAgent = (agentIndex + 1) % numAgents
        nextDepth = depth + 1 if nextAgent == 0 else depth

        # Lay tat ca nuoc di hop le cua agent hien tai
        legalActions = gameState.getLegalActions(agentIndex)

        # Tinh value cua tung successor
        successorValues = [
            self.expectimax(gameState.generateSuccessor(agentIndex, action),
                            nextAgent, nextDepth)
            for action in legalActions
        ]

        # Pacman -> MAX node: chon gia tri lon nhat
        if agentIndex == 0:
            return max(successorValues)

        # Ghost -> CHANCE node: tinh trung binh cac gia tri
        else:
            return sum(successorValues) / len(successorValues)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
