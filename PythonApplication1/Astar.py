import os
import time
### Parts of this program were inspired by Nicholas Swift,
### https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2


class Node:
    def __init__(self, _position=None, _previous=None):
        #using tuples for positions
        self.position = _position
        self.previous = _previous
        self.c = self.s = self.h = 0
    def __eq__(self, other):
        if (self.position == other.position):
            return True
        else:
            return False



    def calculateCost(self, _end):
        #iterate start distance by 1
        self.s += 1
        #pythagorean theorem to find the distance between current position and end
        self.h = sqrt((_end[0] - self.position[0]) ** 2 + (_end[1] - self.position[1]) **2)
        self.c = self.s + self.h
        return self.c

class Maze:
    def __init__(self, _sizeY, _sizeX, _terrain):
        self.sizeY = _sizeY
        self.sizeX = _sizeX
        self.terrain = _terrain
        self.terrainItr = 0
        self.maze = []
        self.build()
        self.findStartAndEnd()

    def build(self):
        #build maze
        for j in range(self.sizeY):
            temp = []
            for i in range(self.sizeX):
                temp.append(int(self.terrain[self.terrainItr]))
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
    with open("terrain1.txt") as terrain:
        terrain = terrain.read()
    terrain = terrain.split(" ")
    sizeX = terrain[0]
    sizeY = terrain[1]
    del terrain[0:2]
    maze = Maze(sizeY, sizeX, terrain)

    openList = []
    closedList = []
    currentNode = maze.start
    currentIndex = 0
    openList.append(currentNode)
    solutionFlag = False
    while (openList):
        for index, node in enumerate(openList):
            if (node.c < currentNode.c):
                currentNode = node
                currentIndex = index
        #if path done
        if (currentNode == maze.end):
            closedList.append(currentNode)
        else:
            #pop returns the object at the index, append it to the closed list
            closedList.append(openList.pop(currentIndex))
            findAdjacent(currentNode)

def findAdjacent(_node, _maze):
    for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
        #Generate new node
        newNode = Node((currentNode.position[0] + newPos[0], currentNode.position[1] + newPos[1]), currentNode.position)
        #check if not in bounds
        if (not (newNode.position[0] >= 0 and newNode.position[0] < _maze.sizeY and newNode.position[1] >= 0 and newNode.position[1] < _maze.sizeX)):
            continue
        #check if not 1
        if (maze[newNode.position[0]][newNode.position[1]] == 1):
            continue


        







if __name__ == '__main__':
    main()