# search.py
# ---------
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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    fringe.push((problem.getStartState(), []))
    explored = set()

    while not fringe.isEmpty():
        # state is location, while actions is path
        state, actions = fringe.pop()
        explored.add(state) #_

        if problem.isGoalState(state):
            return actions

        for next in problem.getSuccessors(state):
            next_state = next[0]
            next_direction = next[1]
            if next_state not in explored:
                fringe.push((next_state, actions + [next_direction]))

    return None

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    fringe.push((problem.getStartState(), []))
    explored = set()
    explored.add(problem.getStartState())

    while not fringe.isEmpty():
        # state is location, while actions is path
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            return actions

        for next in problem.getSuccessors(state):
            next_state = next[0]
            next_direction = next[1]
            if next_state not in explored:
                explored.add(next_state)
                fringe.push((next_state, actions + [next_direction]))

    return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    
    # the fringe apart from the state , action, cost also has priority 0 here
    # which is same as the cost as we want the least total cost first
    fringe.push((problem.getStartState(), [], 0), 0)
    explored = set()

    while not fringe.isEmpty():
        # state is location, while actions is path
        state, actions, cost = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in explored:   #_
            explored.add(state)     #_
            for next in problem.getSuccessors(state):
                next_state = next[0]
                next_direction = next[1]
                next_cost = next[2]
                if next_state not in explored:
                    new_cost = cost + next_cost
                    fringe.push((next_state, actions + [next_direction], new_cost), new_cost)

    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()

    # the fringe apart from the state , action, cost also has priority 0 here
    # which is same as the cost as we want the least total cost first
    fringe.push((problem.getStartState(), [], 0), 0)
    explored = set()

    while not fringe.isEmpty():
        # state is location, while actions is path
        state, actions, cost = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in explored:
            explored.add(state)
            for next in problem.getSuccessors(state):
                next_state = next[0]
                next_direction = next[1]
                next_cost = next[2]
                if next_state not in explored:
                    new_cost = cost + next_cost
                    total_cost = new_cost + heuristic(next_state, problem)
                    fringe.push((next_state, actions + [next_direction], new_cost), total_cost)

    return None

def iterativeDeepeningSearch(problem):
    """This function is for the first of the grad students questions"""
    "*** MY CODE HERE ***"
    from game import Directions

    #initialization
    fringe = util.Stack()
    limit = 1

    while limit <= 100: # repeat search with the depth increases until we find the goal
        explored = []

        #### DFS ####
        # push the starting point into stack
        fringe.push((problem.getStartState(),[],0))
        (state, actions, cost) = fringe.pop()
        explored.append(state)

        while not problem.isGoalState(state): # while we do not find the goal point
            successors = problem.getSuccessors(state) # get the point's succesors
            for next in successors:
                next_state = next[0]
                next_direction = next[1]
                next_cost = next[2]
                new_cost = cost + next_cost
                # add the points when it meets 1. not been visited 2. within the depth 
                if (not next_state in explored) and (new_cost <= limit): 
                    fringe.push((next_state, actions + [next_direction], new_cost)) 
                    explored.append(next_state) # add this point to visited list

            if fringe.isEmpty(): # if the no goal is found within the current depth, jump out and increase the depth
                break

            (state,actions,cost) = fringe.pop()
        #############
        
        if problem.isGoalState(state):
            return actions

        limit += 1 # increase the depth

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch