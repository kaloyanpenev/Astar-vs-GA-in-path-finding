import os
import time
import math

### Parts of this program were inspired by Nicholas Swift,
### https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

#Astar algorithm implementation.
#Maze legend
#0 - open path
#1 - obstacle
#2 - start
#3 - end
#4 - searched by Astar
#9 - optimized path


class Node:
    def __init__(self, _position=None, _previous=None):
        #using tuples for positions
        self.position = _position
        #pointer to previous node
        self.previous = _previous

        #S - Distance from Start
        if (not _previous):
            self.s = 0
        else:
            self.s = _previous.s
        #H - Heuristic - Euclidean distance to finish
        self.h = 0
        #C - Cost - Total heuristic 
        self.c = 0
    #operator overload of ==, for readability when comparing nodes
    def __eq__(self, other):
        if (self.position == other.position):
            return True
        else:
            return False

    def calculateCost(self, _end):
        #always iterate start distance by 1(on top of already added previous distance in constructor)
        self.s += 1
        #pythagorean theorem to find euclidean distance between current position and end
        self.h = math.sqrt(math.pow((_end.position[0] - self.position[0]),2) + math.pow((_end.position[1] - self.position[1]),2))
        #calculate total heuristic cost
        self.c = self.s + self.h

class Maze:
    def __init__(self, _sizeY, _sizeX, _terrain):
        self.sizeY = int(_sizeY)
        self.sizeX = int(_sizeX)
        self.terrain = _terrain
        self.maze = []
        self.buildMaze()
        self.findStartAndEnd()

    def buildMaze(self):
        terrainItr = 0
        #build maze
        for j in range(self.sizeY):
            temp = []
            for i in range(self.sizeX):
                temp.append(int(self.terrain[terrainItr]))
                terrainItr+=1
            self.maze.append(temp)

    def findStartAndEnd(self):
        #find start and end
        for j in range(self.sizeY):
            for i in range(self.sizeX):
                if (self.maze[j][i] == 2):
                    self.start = Node((j, i), None)
                if (self.maze[j][i] == 3):
                    self.end = Node((j, i), None)



def main():
    with open("terrain3.txt") as terrain:
        terrain = terrain.read()
    terrain = terrain.split(" ")
    sizeX = terrain[0]
    sizeY = terrain[1]
    del terrain[0:2]
    maze = Maze(sizeY, sizeX, terrain)
    printProgress = True
    startTime = time.time()
    AstarSearch(maze, printProgress)
    print("Elapsed time:", time.time() - startTime, "\n")


def AstarSearch(maze, _print):

    openList = []
    closedList = []

    currentNode = maze.start
    currentIndex = 0

    openList.append(currentNode)
    #calculate cost for the current node
    currentNode.calculateCost(maze.end)
    #maze we will use for displaying the solution
    displayMaze = Maze(maze.sizeY, maze.sizeX, maze.terrain)
    while (len(openList) > 0):
        #array for storing the costs of the nodes in the queue
        costArray = [node.c for node in openList]
        #find node with lowest cost and make it current
        for index, node in enumerate(openList):
            if (node.c == min(costArray)):
                currentNode = node
                currentIndex = index

        #display a 4 for current position
        if(_print):
            displayMaze.maze[currentNode.position[0]][currentNode.position[1]] = 4
            os.system('cls')
            print('\n'.join(map(str, displayMaze.maze)), "\nSearching...")
        #if path is done
        if (currentNode == maze.end):
            closedList.append(currentNode)
            #create array to display search area
            searchArea = [node.position for node in closedList]
            solution = optimizePath(currentNode, displayMaze, _print)
            print("\nstart:", maze.start.position, "\nend:", maze.end.position, "\nTotal Search area:", ' '.join(map(str, searchArea)), "\n")
            print("path optimized:", ' '.join(map(str, solution)), "\n")
            return
        else:
            #pop returns the object at the index, append it to the closed list
            closedList.append(openList.pop(currentIndex))
            openList.extend(findAdjacent(currentNode, maze, closedList, openList))

def findAdjacent(_currentNode, _maze, _closedList, _openList):
    #temporary list for adding new nodes
    temp = []
    for newPos in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]: # Adjacent squares
        #Generate new node
        newNode = Node((_currentNode.position[0] + newPos[0], _currentNode.position[1] + newPos[1]), _currentNode)
        #check if not in bounds
        if (not (newNode.position[0] >= 0 and newNode.position[0] < _maze.sizeY and newNode.position[1] >= 0 and newNode.position[1] < _maze.sizeX)):
            continue
        #check if not 1
        if (_maze.maze[newNode.position[0]][newNode.position[1]] == 1):
            continue

        #check if its on the closed list and continue to next if it is
        onClosedList = False
        for nodeOnClosed in _closedList:
            if (newNode.position == nodeOnClosed.position):
                onClosedList = True
        if (onClosedList):
            continue

        #check if its on the open list and continue to next if it is
        onOpenList = False
        for nodeOnOpen in _openList:
            if (newNode.position == nodeOnOpen.position):
                onOpenList = True
        if (onOpenList):
            continue

        newNode.calculateCost(_maze.end)
        temp.append(newNode)
    return temp

def optimizePath(_currentNode, _displayMaze, _print):
    solutionPath = []
    currentNode = _currentNode
    while (currentNode):
        #handle display
        if (_print):
            _displayMaze.maze[currentNode.position[0]][currentNode.position[1]] = 9
            os.system('cls')
            print('\n'.join(map(str, _displayMaze.maze)))
            print("\nOptimizing...")
        #add current position to solutionPath
        solutionPath.append(currentNode.position)
        #current
        currentNode = currentNode.previous
    #we optimize from the end to the start
    #so need to return reversed path
    return solutionPath[::-1]

if __name__ == '__main__':
    main()