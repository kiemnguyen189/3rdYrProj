# ghostAgents.py
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
#
# Auction Method Extentions written by Kiem Mark Duc Nguyen 
# Finished 20th April 2020
# The Auction Method Extention allows the ghost agents in this package to emulate 
# market-based coodrination techniques. Each agent submits a "bid" to the auctioneer,
# implemented as a parent class to the AuctionGhost agents that holds the central
# "bids" variable, implemented as a dictionary containing agent indexes and bid
# values. Bid sizes are measured according to each agent's Manhattan distances to
# Pacman, where the closest ghost agent to pacman has the highest bid.


from game import Agent
from game import AgentState
from game import Actions
from game import Directions
from pacman import GameState
import util
from util import manhattanDistance
import api
import random
import csv


# Acts as an "Auctioneer"
class MultiGhostAgent( Agent ):

    # Read test variables from csv file 'AuctionVars.csv'
    with open('AuctionVars.csv') as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=',')
        for row in csv_reader:
            # Variables to change between tests
            INTERVAL = row[0]       # number of steps every ghost agent has to take before an auction is held
            PATROL_MODE = row[1]    # can be: ["FOOD", "CAP"]
            PRINTS = row[2]         # boolean to control printing of detailed auction

    # Shared data between all agents
    bids = {}               # key = indexes, values = [distances, steps, task]
    numAgents = 0           # number of ghost agents present in the game
    winner = 0              # index of winning ghost agent
    # Values unique to each agent
    steps = 0               # number of steps in the game each agent has taken
    pacDist = 0             # Distance between a ghost and pacman

    def __init__( self, index ):
        self.index = index 

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()


    # Holds an auction
    # Returns the 'bids' class variable as a dictionary containing agent indexes and values
    def holdAuction(self, state):

        MultiGhostAgent.winner = min(MultiGhostAgent.bids, key=MultiGhostAgent.bids.get)
        # Reset all tasks
        for items in self.bids.values():
            items[2] = "PATROL"
        # Redistribute tasks to agents
        self.bids[MultiGhostAgent.winner] = [self.bids[MultiGhostAgent.winner][0], self.steps, "CHASE"]

        if MultiGhostAgent.PRINTS == "TRUE":
            print ""
            print "Auction number:", self.steps / int(MultiGhostAgent.INTERVAL)
            for key, value in MultiGhostAgent.bids.items():
                print " - Ghost index:", key, ", Bid:", value[0], ", Current Task:", value[2]
            print "Winner = Ghost index", MultiGhostAgent.winner

# AuctionGhost inherits MultiGhostAgent functionality of holding auctions and relevent variables
class AuctionGhost( MultiGhostAgent ):
    "A ghost that communicates with other ghosts its current state"
    "This can be used as part of the 'bidding' process in the Auction"
    def __init__( self, index, prob_attack=0.99, prob_scaredFlee=0.99  ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee
        self.whole = []
        self.walls = []
        self.path = []

        MultiGhostAgent.numAgents += 1
        MultiGhostAgent.bids[self.index] = [0, 0, "PATROL"] # 1st = bid, 2nd = steps taken, 3rd = current task

    def registerInitialState(self, state):
        
        self.walls = api.walls(state)
        self.whole = self.wholeMap()
        self.path = self.pathMap()

    # Creates a list of coords of the whole map
    def wholeMap(self):
        ret = []
        for i in range(self.walls[-1][0] + 1):
            for j in range(self.walls[-1][1] + 1):
                ret.append((i, j))
        return ret

    # Creates a list of coords that can be moved in (i.e. non walls)
    def pathMap(self):
        ret = []
        for i in range(self.walls[-1][0] + 1):
            for j in range(self.walls[-1][1] + 1):
                if (i, j) not in self.walls:
                    ret.append((i, j))
        return ret

    # Creates a dictionary of capsule positions (key) and coords around a capsule that a ghost will patrol (value)
    def capsuleRange(self, state):
        ret = {}
        capsulePos = state.getCapsules()
        radius = 4
        #print capsulePos
        for cap in capsulePos:
            capPath = []
            for i in range(cap[0]-radius, cap[0]+radius+1):
                for j in range(cap[1]-radius, cap[1]+radius+1):
                    if (i, j) in self.path:
                        capPath.append((i, j))
            ret[cap] = capPath
        #return ret

    # Returns a coordinate of the nearest capsule to the ghost
    def getNearestCap(self, state, pos):
        capsulePos = state.getCapsules()
        if len(capsulePos) != 0:
            currentMin = util.manhattanDistance(pos, capsulePos[0])
            for cap in capsulePos:
                if util.manhattanDistance(pos, cap) <= currentMin:
                    currentMin = cap
        else:
            currentMin = pos
        return currentMin

    # Returns a list of all current food on the map
    def getAllFood(self, state):
        foodList = []
        foodGrid = state.getFood()
        width = foodGrid.width
        height = foodGrid.height
        for i in range(width):
            for j in range(height):
                if foodGrid[i][j] == True:
                    foodList.append((i, j))
        return foodList

    # Returns the position of the nearest food pill
    def getNearestFood(self, state, pos):
        food = self.getAllFood(state)
        if len(food) != 0: 
            minimum = food[0]
            for i in food:
                if util.manhattanDistance(pos, i) < util.manhattanDistance(pos, minimum):
                    minimum = i
        else: 
            minimum = pos
        return minimum


    # Returns a dictionary of Direction-Probability pairs, highest prob gets chosen as Action to take
    def getDistribution( self, state ):

        # Gets all state information
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        food = api.food(state)
        isScared = ghostState.scaredTimer > 0
        self.steps += 1

        speed = 1
        if isScared: speed = 0.5

        # Gets vectors of ALL legal actions e.g. [(1, 0), (0, -1)]
        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        # Coordinate vectors of ALL legal actions e.g. [(9, 7), (9, 5)]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]

        # Retrieve Task mode defined in AuctionVars.csv and gets positions of points of interest
        pacmanPos = state.getPacmanPosition()
        capsulePos = self.getNearestCap(state, pos)
        pillPos = self.getNearestFood(state, pos)
        if MultiGhostAgent.PATROL_MODE == "FOOD": 
            patrolPos = pillPos
        elif MultiGhostAgent.PATROL_MODE == "CAP": 
            patrolPos = capsulePos

        # Measure distance between ghost and Pacman
        self.pacDist = manhattanDistance(pos, pacmanPos)
        # Set value of agent index to [bid, step, task]
        MultiGhostAgent.bids[self.index] = [self.pacDist, self.steps, MultiGhostAgent.bids[self.index][2]]

        # Select best actions given the state
        # Calculates Manhattan of ALL legal vectors
        distancesToPacman = [manhattanDistance( pos, pacmanPos ) for pos in newPositions]
        # Different modes of ghost patrolling
        distancesToPatrol = [manhattanDistance( pos, patrolPos ) for pos in newPositions]

        # If scared, best choice = vector FURTHEST from pacman
        if isScared:
            self.currentTask = "RUN"
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        # If normal, best choice = vector CLOSEST to pacman
        else:
            # Check to see if every agent has step of INTERVAL to carry out Auction 
            # If auction -> change current task
            if all(value[1] % int(MultiGhostAgent.INTERVAL) == 0 for value in MultiGhostAgent.bids.values()):
                self.holdAuction(state)
                bestScore = MultiGhostAgent.bids[self.index][0]
                bestProb = self.prob_attack
            # Else (no auction) -> do current task
            else:
                if MultiGhostAgent.bids.get(self.index)[2] == "CHASE":
                    bestScore = min( distancesToPacman ) 
                    bestProb = self.prob_attack
                else:
                    bestScore = min( distancesToPatrol ) 
                    bestProb = self.prob_attack

        # Gets "Direction(s)" that matches smallest (or largest if scared) distance
        if MultiGhostAgent.bids.get(self.index)[2] == "CHASE": bestDistances = distancesToPacman
        else: bestDistances = distancesToPatrol
        bestActions = [action for action, distance in zip( legalActions, bestDistances ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        # Split probability of all BEST actions (i.e. 1 best = 0.8, 2 best = 0.4 each)
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        # Add to probability of BEST actions the LEGAL actions, if legal not best then lower probability 
        # (e.g. BEST and LEGAL = 0.8 + 0.1, LEGAL ONLY = 0.1)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist

# -------------------------------------------------------------------------------------------------------------------------------------------------------
# OLD CODE
# -------------------------------------------------------------------------------------------------------------------------------------------------------

class GhostAgent( Agent ):

    def __init__( self, index ):
        self.index = index            

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()


class RandomGhost( GhostAgent ):
    "A ghost that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist


class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPos = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance( pos, pacmanPos ) for pos in newPositions]
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist