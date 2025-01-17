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


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util
import api
from pacman import GameState
from game import AgentState



# Acts as an "Auctioneer"
class MultiGhostAgent( Agent ):
    
    # CONSTANTS
    INTERVAL = 5            # number of steps every ghost agent has to take before an auction is held
    # Shared data between all agents
    bids = {}               # key = indexes, values = [distances, steps, task]
    isAuction = False   
    numAgents = 0           # number of ghost agents present in the game
    winner = 0              # index of winning ghost agent
    # Values unique to each agent
    steps = 0               # number of steps in the game each agent has taken
    pacDist = 0
    currentTask = "PATROL"  # current task of each agent

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
        print("")
        print(self.index, "HOLD START: ", self.bids)
        self.winner = min(MultiGhostAgent.bids, key=MultiGhostAgent.bids.get)
        print("WINNING AGENT: ", self.winner)
        # Reset all tasks
        for items in self.bids.values():
            items[2] = "PATROL"
        # Redistribute tasks to agents
        self.bids[self.winner] = [self.bids[self.winner][0], self.steps, "CHASE"]
        print(self.index, "HOLD FINISH: ", self.bids)
        #return self.bids



class AuctionGhost( MultiGhostAgent ):
    "A ghost that communicates with other ghosts its current state"
    "This can be used as part of the 'bidding' process in the Auction"
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8  ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee
        self.whole = []
        self.walls = []
        self.path = []
        #ghostDict[self.index] = state.getGhostPosition(self.index)
        #print ghostDict
        MultiGhostAgent.numAgents += 1
        MultiGhostAgent.bids[self.index] = [0, 0, "PATROL"] # 1st = bid, 2nd = steps taken, 3rd = current task
        print("Index: ", self.index)
        print("Bids: ", MultiGhostAgent.bids)
        print("Num: ", MultiGhostAgent.numAgents)

    def registerInitialState(self, state):
        
        self.walls = api.walls(state)
        self.whole = self.wholeMap()
        self.path = self.pathMap()

    """
    def chase(self, state):

        num = state.getNumAgents()
        st = state.getGhostState(self.index)
        sta = state.getGhostStates()
        #print st
        #print sta
        #print self.index

        #pacmanPosition = state.getPacmanPosition()

    
    def getAction(self, state):
        num = state.getNumAgents()
        print num


    """

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
        #print ret
        return ret

    
    # Gets a ghost to patrol an area around a capsule
    def patrolNearestCapsule(self, state):
        path = self.capsuleRange(state)
        #print path
        pos = state.getGhostPosition(self.index)
        capDist = {}
        for i in path:
            dist = manhattanDistance(pos, i)
            capDist[i] = dist
        nearestCap = min(capDist)
        #print nearestCap
        visited = []
        unvisited = path[nearestCap]
        #print unvisited
        if pos in unvisited:
            unvisited.remove(pos)
        #print "Unvisited: ", unvisited
      

    # Returns a dictionary of Direction-Probability pairs, highest prob gets chosen as Action to take
    def getDistribution( self, state ):

        # Gets all state information
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        # Gets vectors of ALL legal actions
        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        #print actionVectors
        # Coordinate vectors of ALL legal actions e.g. [(9, 7), (9, 5)]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        #print "new ", newPositions
        pacmanPosition = state.getPacmanPosition()

        # -------- TEST --------
        # Iterate step
        self.steps += 1
        # Measure bid size
        self.pacDist = manhattanDistance(pos, pacmanPosition)
        # Set value of agent index to [bid, step, task]
        tempValue = [self.pacDist, self.steps, self.currentTask]
        MultiGhostAgent.bids[self.index] = tempValue
        #print("Bids: ", MultiGhostAgent.bids)
        # -------- TEST --------

        # Select best actions given the state
        # Calculates Manhattan of ALL legal vectors
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
        #print distancesToPacman

        # TODO: vvvvvvvv REPLACE THIS WHOLE AREA WITH OWN IMPLEMENTATION OF CHASE, PATROL, RUN vvvvvvvv
        # If scared, best choice = vector FURTHEST from pacman
        bestScore = 0
        bestProb = 0
        if isScared:
            self.currentTask = "RUN"
            bestScore = max( distancesToPacman )
            #print "1: ", bestScore
            bestProb = self.prob_scaredFlee
        # If normal, best choice = vector CLOSEST to pacman
        else:
            # Check to see if every agent has step of INTERVAL to carry out Auction 
            # todo: Maybe add here chase() and patrol() methods that return the bestScores
            # If auction -> change current task
            if all(value[1] % MultiGhostAgent.INTERVAL == 0 for value in MultiGhostAgent.bids.values()):
                self.holdAuction(state)
                #print("Auction Finished!", MultiGhostAgent.bids)
                bestScore = MultiGhostAgent.bids[self.index][0]
                bestProb = self.prob_attack
            # Else (no auction) -> keep doing current task
            else:
                # todo: if closer to pacman, CHASE
                
                if MultiGhostAgent.bids.get(self.index)[2] == "CHASE":
                    bestScore = min( distancesToPacman ) 
                    bestProb = self.prob_attack
                # todo: if closer to capsule, PATROL
                else:
                    bestScore = min( distancesToPacman ) 
                    bestProb = self.prob_attack
            
        # TODO: ^^^^^^^^ REPLACE THIS WHOLE AREA WITH OWN IMPLEMENTATION OF CHASE, PATROL, RUN ^^^^^^^^

        #for action, distance in zip(legalActions, distancesToPacman):
            #print action
        #print zip(legalActions, distancesToPacman)

        # Gets "Direction(s)" that matches smallest (or largest if scared) distance
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]
        #print bestActions

        # Construct distribution
        dist = util.Counter()
        # Split probability of all BEST actions (i.e. 1 best = 0.8, 2 best = 0.4 each)
        for a in bestActions: 
            dist[a] = bestProb / len(bestActions)
            #print "1: ", dist[a]
        #print legalActions

        # Add to probability of BEST actions the LEGAL actions, if legal not best then lower probability 
        # (e.g. BEST and LEGAL = 0.8 + 0.1, LEGAL ONLY = 0.1)
        for a in legalActions: 
            dist[a] += ( 1-bestProb ) / len(legalActions)
            #print "2: ", dist[a]
        #print "1: ", dist
        dist.normalize()
        #print "2: ", dist
        #print "\n"
        return dist


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
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
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