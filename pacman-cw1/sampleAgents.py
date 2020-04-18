# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
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

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

# GoWestAgent
#
# Always tries to go West. If it cannot, it will choose a random direction
class GoWestAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP

    def getAction(self, state):
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        if Directions.WEST in legal:
            return api.makeMove(Directions.WEST, legal)
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            self.last = pick
            return api.makeMove(pick, legal)

# HungryAgent
#
# Tries to move to the nearest food location
class HungryAgent(Agent):

    # Constructor
    #
    #
    def __init__(self):
        self.last = Directions.STOP

    def getAction(self, state):

        # Get the actions we can try
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        nearest = theFood[0]
        # remove "STOP" action from legal actions
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it
        if self.last in legal:
            return api.makeMove(self.last, legal)
        for i in range(len(theFood)):
            if util.manhattanDistance(pacman, theFood[i]) <= util.manhattanDistance(pacman, nearest):
                nearest = theFood[i]

        # Calculate coords of pacman and food to determine Direction
        xDiff = pacman[0] - nearest[0]
        yDiff = pacman[1] - nearest[1]
        temp = (xDiff, yDiff)
        pick = random.choice(legal)

        # Uses difference in coords to determine Direction to travel
        if abs(temp[0]) > abs(temp[1]):
            if temp[0] < 0 and Directions.EAST in legal:
                print "EAST: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(Directions.EAST, legal)
            elif temp[0] >= 0 and Directions.WEST in legal:
                print "WEST: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(Directions.WEST, legal)
            else:
                print "### RAND: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(pick, legal)
        else:
            if temp[1] < 0 and Directions.NORTH in legal:
                print "NORTH: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(Directions.NORTH, legal)
            elif temp[1] >= 0 and Directions.SOUTH in legal:
                print "SOUTH: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(Directions.SOUTH, legal)
            else:
                print "### RAND: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(pick, legal)         

# SurvivalAgent
#
# Tries to survive as long as possible by avoiding the ghosts
class SurvivalAgent(Agent):

    # Constructor
    #
    #
    def __init__(self):
        self.last = Directions.STOP

    def getAction(self, state):

        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theGhosts = api.ghosts(state)
        nearest = theGhosts[0]
        for i in range(len(theGhosts)):
            if util.manhattanDistance(pacman, theGhosts[i]) <= util.manhattanDistance(pacman, nearest):
                nearest = theGhosts[i]

        # Calculate coords of pacman and ghosts to determine Direction
        xDiff = pacman[0] - nearest[0]
        yDiff = pacman[1] - nearest[1]
        temp = (xDiff, yDiff)

        pick = random.choice(legal)
        
        if util.manhattanDistance(pacman, nearest) < 4:
            # Uses difference in coords to determine Direction to travel
            if abs(temp[0]) > abs(temp[1]):
                if temp[0] < 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                elif temp[0] >= 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if temp[1] < 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                elif temp[1] >= 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    return api.makeMove(pick, legal)
        else:
            return api.makeMove(pick, legal)

# CornerSeekingAgent
#
# Tries to find the corners of the map
class CornerSeekingAgent(Agent):

    # Constructor
    #
    #
    def __init__(self):
        self.last = Directions.STOP
        self.visited = []

    def getAction(self, state):

        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        theGhosts = api.ghosts(state)
        corners = api.corners(state)
        unvisited = list(set(corners) - set(self.visited))
        print "###############################"
        print pacman
        print corners[0]
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        for i in range(len(corners)):
            elem = corners[i]
            print "ELEM ", i, ": ", elem
            #print abs(pacman[0] - elem[0]) - abs(pacman[1] - elem[1])
            print util.manhattanDistance(pacman, elem)
            # check if pacman is close enough to a corner
            if util.manhattanDistance(pacman, elem) == 2:
                print self.visited
                print unvisited
                if elem not in self.visited:
                    self.visited.append(elem)
                if elem in unvisited:
                    unvisited.remove(elem)
        print "CORNERS: ", len(corners), corners
        print "VISITED: ", len(self.visited), self.visited
        print "UNVISITED: ", len(unvisited), unvisited
        
        nearestCorner = (9999, 9999)
        for i in range(len(unvisited)):
            if util.manhattanDistance(pacman, unvisited[i]) <= util.manhattanDistance(pacman, nearestCorner):
                nearestCorner = unvisited[i]
        tempCorner = (pacman[0] - nearestCorner[0], pacman[1] - nearestCorner[1])

        # If list of food is empty, nearest food is at not in range
        if len(theFood) == 0:
            nearestFood = (9999, 9999)
        else:
            nearestFood = theFood[0]
        # Calculates the Manhattan distances of food and ghosts and assigns nearest
        for i in range(len(theFood)):
            if util.manhattanDistance(pacman, theFood[i]) <= util.manhattanDistance(pacman, nearestFood):
                nearestFood = theFood[i]
        # Calculate coords of pacman and food to determine Direction
        tempFood = (pacman[0] - nearestFood[0], pacman[1] - nearestFood[1])
        
        pick = random.choice(legal)
        #first = unvisited[0]
        #print "CLOSEST: ", first
        #tempCorner = (pacman[0] - first[0], pacman[1], first[1])
        if len(theFood) != 0:
            print "FINDFOOD"
            # FIND FOOD: Uses difference in coords of food to determine Direction to travel
            if abs(tempFood[0]) > abs(tempFood[1]):
                if tempFood[0] < 0 and Directions.EAST in legal:
                    print "EAST: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.EAST, legal)
                elif tempFood[0] >= 0 and Directions.WEST in legal:
                    print "WEST: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.WEST, legal)
                else:
                    print "### RAND: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(pick, legal)
            else:
                if tempFood[1] < 0 and Directions.NORTH in legal:
                    print "NORTH: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.NORTH, legal)
                elif tempFood[1] >= 0 and Directions.SOUTH in legal:
                    print "SOUTH: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    print "### RAND: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(pick, legal)
        else: 
            if abs(tempCorner[0]) > abs(tempCorner[1]):
                if tempCorner[0] < 0 and Directions.EAST in legal:
                    print "    EAST"
                    return api.makeMove(Directions.EAST, legal)
                elif tempCorner[0] >= 0 and Directions.WEST in legal:
                    print "    WEST"
                    return api.makeMove(Directions.WEST, legal)
                else:
                    print "    RAND"
                    return api.makeMove(pick, legal)
            else:
                if tempCorner[1] < 0 and Directions.NORTH in legal:
                    print "    NORTH"
                    return api.makeMove(Directions.NORTH, legal)
                elif tempCorner[1] >= 0 and Directions.SOUTH in legal:
                    print "    SOUTH"
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    print "    RAND"
                    return api.makeMove(pick, legal)
        

        



# BothAgent
#
# Combines both HungryAgent and SurvivalAgent to create a semi-intelligent pacman
class BothAgent(Agent):

    # Constructor
    #
    #
    def __init__(self):
        self.last = Directions.STOP

    def getAction(self, state):

        # Get the actions we can try
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        theGhosts = api.ghosts(state)
        # If list of ghosts is empty, nearest ghost is not in range
        if len(theGhosts) == 0:
            nearestGhost = (9999, 9999)
        else:
            nearestGhost = theGhosts[0]
        # If list of food is empty, nearest food is at not in range
        if len(theFood) == 0:
            nearestFood = (9999, 9999)
        else:
            nearestFood = theFood[0]
        # remove "STOP" action from legal actions
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Calculates the Manhattan distances of food and ghosts and assigns nearest
        for i in range(len(theFood)):
            if util.manhattanDistance(pacman, theFood[i]) <= util.manhattanDistance(pacman, nearestFood):
                nearestFood = theFood[i]
        for i in range(len(theGhosts)):
            if util.manhattanDistance(pacman, theGhosts[i]) <= util.manhattanDistance(pacman, nearestGhost):
                nearestGhost = theGhosts[i]

        # Calculate coords of pacman and food to determine Direction
        tempFood = (pacman[0] - nearestFood[0], pacman[1] - nearestFood[1])
        # Calculate coords of pacman and ghosts to determine Direction
        tempGhost = (pacman[0] - nearestGhost[0], pacman[1] - nearestGhost[1])

        pick = random.choice(legal)
        detectionDist = 5
        
        # If we can repeat the last action, do it
        if self.last in legal:
            return api.makeMove(self.last, legal)
        # DETECT CLOSE GHOSTS
        if util.manhattanDistance(pacman, nearestGhost) < detectionDist:
            print "AVOID"
            # Uses difference in coords to determine Direction to travel
            if abs(tempGhost[0]) > abs(tempGhost[1]):
                if tempGhost[0] < 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                elif tempGhost[0] >= 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if tempGhost[1] < 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                elif tempGhost[1] >= 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    return api.makeMove(pick, legal)
        else:
            print "FINDFOOD"
            # FIND FOOD: Uses difference in coords of food to determine Direction to travel
            if abs(tempFood[0]) > abs(tempFood[1]):
                if tempFood[0] < 0 and Directions.EAST in legal:
                    print "EAST: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.EAST, legal)
                elif tempFood[0] >= 0 and Directions.WEST in legal:
                    print "WEST: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.WEST, legal)
                else:
                    print "### RAND: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(pick, legal)
            else:
                if tempFood[1] < 0 and Directions.NORTH in legal:
                    print "NORTH: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.NORTH, legal)
                elif tempFood[1] >= 0 and Directions.SOUTH in legal:
                    print "SOUTH: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    print "### RAND: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(pick, legal)


# TriAgent
#
# Combines: Ghost avoidance, food finding, corner seeking
class TriAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP
        self.visited = []

    def getAction(self, state):

        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        theGhosts = api.ghosts(state)
        corners = api.corners(state)
        unvisited = list(set(corners) - set(self.visited))

        # Stops pacman from standing still
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If list of ghosts is empty, nearest ghost is not in range
        if len(theGhosts) == 0:
            nearestGhost = (9999, 9999)
        else:
            nearestGhost = theGhosts[0]
        # If list of food is empty, nearest food is at not in range
        if len(theFood) == 0:
            nearestFood = (9999, 9999)
        else:
            nearestFood = theFood[0]
        # Adds corners to be stored persistently
        for i in range(len(corners)):
            elem = corners[i]
            # check if pacman is close enough to a corner
            if util.manhattanDistance(pacman, elem) == 2:
                if elem not in self.visited:
                    self.visited.append(elem)
                if elem in unvisited:
                    unvisited.remove(elem)
        # Calculates the Manhattan distances of ghosts and assigns nearest
        for i in range(len(theGhosts)):
            if util.manhattanDistance(pacman, theGhosts[i]) <= util.manhattanDistance(pacman, nearestGhost):
                nearestGhost = theGhosts[i]
        # Calculates the Manhattan distances of food and assigns nearest
        for i in range(len(theFood)):
            if util.manhattanDistance(pacman, theFood[i]) <= util.manhattanDistance(pacman, nearestFood):
                nearestFood = theFood[i]
        # Calculates the Manhattan distances of corners 
        nearestCorner = (9999, 9999)
        for i in range(len(unvisited)):
            if util.manhattanDistance(pacman, unvisited[i]) <= util.manhattanDistance(pacman, nearestCorner):
                nearestCorner = unvisited[i]

        # Calculate coords of pacman and ghosts to determine Direction
        tempGhost = (pacman[0] - nearestGhost[0], pacman[1] - nearestGhost[1])
        # Calculate coords of pacman and food to determine Direction
        tempFood = (pacman[0] - nearestFood[0], pacman[1] - nearestFood[1])
        # Calculate coords of pacman and corners to determine Direction
        tempCorner = (pacman[0] - nearestCorner[0], pacman[1] - nearestCorner[1])
        # Random direction from legal directions
        pick = random.choice(legal)
        detectionDist = 5
        # DETECT GHOSTS: detects ghosts that are in manhattan range
        if util.manhattanDistance(pacman, nearestGhost) < detectionDist:
            print "AVOID"
            # Uses difference in coords to determine Direction to travel
            if abs(tempGhost[0]) > abs(tempGhost[1]):
                if tempGhost[0] < 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                elif tempGhost[0] >= 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if tempGhost[1] < 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                elif tempGhost[1] >= 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    return api.makeMove(pick, legal)
        # FIND FOOD: Uses difference in coords of food to determine Direction to travel
        elif len(theFood) != 0:
            print "FIND FOOD"
            if abs(tempFood[0]) > abs(tempFood[1]):
                if tempFood[0] < 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                elif tempFood[0] >= 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if tempFood[1] < 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                elif tempFood[1] >= 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    return api.makeMove(pick, legal)
        # FIND CORNER: finds the corners of no food is in range
        else: 
            print "FIND CORNER"
            if abs(tempCorner[0]) > abs(tempCorner[1]):
                if tempCorner[0] < 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                elif tempCorner[0] >= 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if tempCorner[1] < 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                elif tempCorner[1] >= 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    return api.makeMove(pick, legal)

# Finds the nearest entity
def nearFind(pac, theList, nearestEntity):

    ##print "##################"
    ##print "nearFind list: ", theList
    ##print "nearFind entity: ", nearestEntity
    for i in range(len(theList)):
        if util.manhattanDistance(pac, theList[i]) <= util.manhattanDistance(pac, nearestEntity):
            nearestEntity = theList[i]
    return nearestEntity

# Returns a direction of an entity relative to pacman
def pairBearing(pac, entity):

    direc = Directions.STOP
    x = pac[0] - entity[0]
    y = pac[1] - entity[1]
    if abs(x) > abs(y):
        if x < 0: direc = Directions.EAST
        else: direc = Directions.WEST
    else:
        if y < 0: direc = Directions.NORTH
        else: direc = Directions.SOUTH
    return direc

# Makes pacman run away from the nearest ghost
def runAway(pac, ghost, legality, l1):

    direc = Directions.STOP
    ghostDirec = pairBearing(pac, ghost)
    #print "GHOST: ", ghostDirec
    #print "LEGAL: ", legality
    if len(legality) != 0:
        if ghostDirec in legality:
            #print "removed: ", ghostDirec
            legality.remove(ghostDirec)
    else:
        legality[0] = Directions.STOP

    return (legality[0], legality)

#TODO: Create a waypoint system / A star
# Returns a direction based on the nearest entity (food / capsule)
def findDirection(tempEntity, legality, l1):
    
    #print "###########################################"
    #print "findDirection entity: ", tempEntity
    #print "findDirection reverse: ", reverse
    #print "findDirection legality: ", legality
    direc = Directions.STOP

    if abs(tempEntity[0]) > abs(tempEntity[1]): # HORIZONTAL
        ##print "IF"
        if tempEntity[0] < 0 and Directions.EAST in legality:
            direc = Directions.EAST
        elif tempEntity[0] >= 0 and Directions.WEST in legality:
            direc = Directions.WEST
        else:
            #print "RANDOM"
            direc = random.choice(legality)
    else:   # VERTICAL
        ##print "ELSE"
        if tempEntity[1] < 0 and Directions.NORTH in legality:
            direc = Directions.NORTH
        elif tempEntity[1] >= 0 and Directions.SOUTH in legality:
            direc = Directions.SOUTH
        else:
            #print "RANDOM"
            direc = random.choice(legality)
    #print "RETURN: ", direc, ", ", legality
    if len(l1) == 1:
        l1.pop(0)
    if len(l1) < 1:
        l1.append(direc)
    return (direc, legality) 

#def waypoints():
    

# TestAgent
#
# A cleaner version of TriAgent
class TestAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP
        self.last3 = [Directions.STOP]
        self.visited = []

    def getAction(self, state):

        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        theGhosts = api.ghosts(state)
        corners = api.corners(state)
        unvisited = list(set(corners) - set(self.visited))

        # Stops pacman from standing still
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If list of ghosts is empty, nearest ghost is not in range
        if len(theGhosts) == 0: nearestGhost = (9999, 9999)
        else: nearestGhost = theGhosts[0]
        # If list of food is empty, nearest food is at not in range
        if len(theFood) == 0: nearestFood = (9999, 9999)
        else: nearestFood = theFood[0]
        # If list of unvisited corners is empty
        if len(unvisited) == 0: nearestCorner = (9999, 9999)
        else: nearestCorner = unvisited[0]
        # Adds corners to be stored persistently
        for i in range(len(corners)):
            elem = corners[i]
            # check if pacman is close enough to a corner
            if util.manhattanDistance(pacman, elem) == 2:
                if elem not in self.visited:
                    self.visited.append(elem)
                if elem in unvisited:
                    unvisited.remove(elem)
        ##print "nG"
        nG = nearFind(pacman, theGhosts, nearestGhost)
        ##print "nF"
        nF = nearFind(pacman, theFood, nearestFood)
        ##print "nC"
        nC = nearFind(pacman, unvisited, nearestCorner)
        
        # TODO: Change to use pairBearing method
        # Calculate coords of pacman and ghosts to determine Direction
        tempGhost = (pacman[0] - nG[0], pacman[1] - nG[1])
        # Calculate coords of pacman and food to determine Direction
        tempFood = (pacman[0] - nF[0], pacman[1] - nF[1])
        # Calculate coords of pacman and corners to determine Direction
        tempCorner = (pacman[0] - nC[0], pacman[1] - nC[1])
        # Random direction from legal directions
        pick = random.choice(legal)
        detectionDist = 3
        l1 = self.last3
        #test

        # TODO: Change to relative positioning of ghosts to pac instead of absolute coords
        if util.manhattanDistance(pacman, nearestGhost) <= detectionDist:
            (d, l) = runAway(pacman, nG, legal, l1)
            #print "LAST 3: ", self.last3
            return api.makeMove(d, l)
        elif len(theFood) != 0:
            (d, l) = findDirection(tempFood, legal, l1)
            #print "LAST 3: ", self.last3
            return api.makeMove(d, l)
        elif len(theFood) == 0:
            (d, l) = findDirection(tempCorner, legal, l1)
            #print "LAST 3: ", self.last3
            return api.makeMove(d, l)
        

class MDPAgent(Agent):
    
    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        # params
        self.direcProb = 1        # Direction probability (80%)
        self.emptyReward = -0.04    # The 'reward' for moving pacman
        self.discountFactor = 0.5   # Discount factor
        self.avoidRadius = 0        # Radius around a ghost that pacman should avoid
        # Rewards
        self.foodReward = 1         # Reward for food
        self.capsuleReward = 1      # Reward for capsule
        self.ghostReward = -4       # Reward for ghost
        # Init lists
        # FIXED
        self.whole = []             # List of coordinates of the whole map
        self.walls = []             # List of coordinates of walls
        # UPDATED
        self.food = []              # List of food pills
        self.capsules = []          # List of capsules
        self.ghosts = []            # List of ghosts
        self.radiusList = []        # List of coordinates within the avoidance radius

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        # Lists that stay constant throughout program initialized once
        self.walls = api.walls(state)
        self.whole = self.wholeMap()
        # Avoidance radius of ghosts depends on size of map. Smaller map = smaller radius
        self.avoidRadius = 1#int((min(self.walls[-1]) - 2) / 4)

    # Gets pacman to make a move
    # First, Updates values of states at every call (food, capsules, ghosts etc.)
    # Then calls value iteration after mapping initial values
    # Returns: A direction to move in (with 80% success) 
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # Updates new list of entities with new game state
        self.food = api.food(state)         
        self.capsules = api.capsules(state)
        self.ghosts = api.ghosts(state)
        self.stateTimes = api.ghostStatesWithTimes(state)
        self.ghostRadius()
        pac = api.whereAmI(state)

        # Updates map with new info e.g. eaten food / capsules / ghosts
        dictMap = self.mapValues(state, self.whole)
        # Converges the mapped values from mapValues using Bellman update
        self.valueIteration(dictMap)

        # ---- PRINTS FOR DEBUG ----
        #self.gridPrint(state, dictMap)      # Print grid in terminal
        #print sorted(dictMap.iteritems())  # Print dictionary of full util values

        # Makes a move by calling findMax function that returns the best direction to move
        return api.makeMove(self.findMax(pac, dictMap)[0], legal)

    # Returns a list of tuples representing coordinates of the whole map 
    # Called once at initialization
    def wholeMap(self):
        ret = []
        for i in range(self.walls[-1][0] + 1):
            for j in range(self.walls[-1][1] + 1):
                ret.append((i, j))
        return ret

    # Creates a list of all new locations within the avoidRadius of all ghosts
    # i.e. a square ring area with side lengths avoidRadius + 1 not including ghost coords
    def ghostRadius(self):
        self.radiusList = []        # reset list of new radius
        for ghost in self.ghosts:
            for i in range(int(ghost[0]-self.avoidRadius), int(ghost[0]+self.avoidRadius+1)):
                for j in range(int(ghost[1]-self.avoidRadius), int(ghost[1]+self.avoidRadius+1)):
                    # If rounded radius coord around ghost (because scared ghosts move in half steps)
                    # is not diagonal to ghosts and is not a wall or the ghost itself, add to radiusList
                    if (int(i), int(j)) not in self.walls or not ghost: self.radiusList.append((int(i), int(j)))

    # Updates the utility values of all the ghosts depending on their states
    # Returns: utility value of a specified ghost at a coordinate
    def ghostValue(self, coord):
        for pair in self.stateTimes:
            if pair[1] == 0: util = self.ghostReward    # i.e. not scared = default value
            else: util = (pair[1] - 20) / 2.5           # function mapping scared time left to ranges 8 to -8
        return util

    # Creates a dictionary of coordinate - utility value pairs
    # Returns: A dictionary mapping coordinate values to utility values
    def mapValues(self, state, map1):
        dictMap = {}
        for i in map1:
            if i in self.ghosts: dictMap[i] = self.ghostValue(i)            # Util of ghost calculated using ghostValue
            elif i in self.radiusList: dictMap[i] = self.ghostValue(i) / 2  # Util of cells near ghosts = half of ghostValue
            elif i in self.food: dictMap[i] = self.foodReward               # Util of food = foodReward
            elif i in self.capsules: dictMap[i] = self.capsuleReward        # Util of capsules = capsuleReward
            elif i in self.walls: dictMap[i] = 0                            # Util of walls = 0
            else: dictMap[i] = self.emptyReward                             # Util of empty space = default reward
        return dictMap
    
    # Find adjacent coords of current
    # Returns: Max util of states using the Bellman equation
    def findMax(self, coord, dictMap):
        # Dictionary of utilities in each direction
        self.utilityDict = {Directions.NORTH: 0.0, Directions.SOUTH: 0.0, Directions.EAST: 0.0, Directions.WEST: 0.0}
        # adjacent coords in all 4 directions in dictionary
        for i in self.utilityDict:
            self.utilityDict[i] = self.setUtil(i, coord, dictMap)

        return max(self.utilityDict.iteritems(), key = lambda x: x[1])
    
    # Called 4 times in findMax, 1 for each direction
    # Sums up the utility of each of the 4 directions by calculating
    # front, left and right probabilities
    def setUtil(self, direc, coord, dictMap):
        # Dictionary mapping direction parameter to actual coordinate locations around it
        dirDict = {
            Directions.NORTH: (coord[0], coord[1] + 1), 
            Directions.SOUTH: (coord[0], coord[1] - 1), 
            Directions.EAST: (coord[0] + 1, coord[1]), 
            Directions.WEST: (coord[0] - 1, coord[1]), 
        }

        # If direction (direc) not a wall,
        # multiply direction probability with utility
        # otherwise stay in place (coord)
        if dirDict[direc] not in self.walls:
            util = (self.direcProb * dictMap[dirDict[direc]])
        else:
            util = (self.direcProb * dictMap[coord])
        # LEFT perpendicular
        if dirDict[Directions.LEFT[direc]] not in self.walls:
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[Directions.LEFT[direc]]])
        else: # stay in place
            util += (((1 - self.direcProb)/2) * dictMap[coord])
        # RIGHT perpendicular
        if dirDict[Directions.RIGHT[direc]] not in self.walls:
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[Directions.RIGHT[direc]]])
        else: # stay in place
            util += (((1 - self.direcProb)/2) * dictMap[coord])

        return util

    # Converges util values performing Bellman update
    # Returns: new dictionary mapping with converged values from Bellman update
    def valueIteration(self, dictMap):
        oldMap = None
        while dictMap != oldMap:
            oldMap = dictMap.copy()
            for i in self.whole:    # Iterate through created map
                if i not in self.walls + self.food + self.ghosts + self.radiusList + self.capsules:
                    # Bellman update
                    dictMap[i] = self.emptyReward + (self.discountFactor * self.findMax(i, oldMap)[1])
        return dictMap

    # Prints the map in the terminal with utility values in empty spaces
    def gridPrint(self, state, map):
        out = ""
        for row in reversed(range(self.walls[-1][1]+1)):
            for col in range(self.walls[-1][0]+1):
                if (row == 0 and col == 0): out += "[001]"              # Bottom Left corner
                elif (row == 0 and col == 19): out += "[002]"           # Bottom Right corner
                elif (row == 10 and col == 0): out += "[003]"           # Top Left corner
                elif (row == 10 and col == 19): out += "[004]"          # Top right corner
                elif (col, row) in self.walls: out += "[###]"           # Wall
                elif (col, row) in self.ghosts: out += "  X  "          # Ghost
                elif (col, row) in self.food: out += "  .  "            # Food
                elif (col, row) in self.capsules: out += "  o  "        # Capsule
                elif (col, row) == api.whereAmI(state): out += "  @  "  # Pacman
                else: out += "{: 5.2f}".format(map[(col, row)])         # Empty space with util value
            out += "\n"     # Next row
        print out

class MapBuildingAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP


    def getAction(self, state):
        legal = api.legalActions(state)
        walls = api.walls(state)
        finalCell = walls[len(walls) - 1]
        ##print "FINAL: ", finalCell
        whole = []
        for i in range(finalCell[0]+1):
            for j in range(finalCell[1]+1):
                whole.append((i, j))
                ##print i, j
        ##print whole
        diff = [x for x in whole if x not in set(walls)]
        ##diff = list(set(whole) - set(walls))
        print diff
        return api.makeMove(Directions.STOP, legal)

