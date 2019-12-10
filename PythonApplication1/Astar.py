import os
import random
import string
import time
import math
import sys

### Parts of the code for the A* algorithm were inspired by Nicholas Swift,
### https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

#Astar vs GA comparison program
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
        for j in range(self.sizeY):
            temp = []
            for i in range(self.sizeX):
                temp.append(int(self.terrain[terrainItr]))
                terrainItr+=1
            self.maze.append(temp)

    def findStartAndEnd(self):
        for j in range(self.sizeY):
            for i in range(self.sizeX):
                if (self.maze[j][i] == 2):
                    self.start = Node((j, i), None)
                if (self.maze[j][i] == 3):
                    self.end = Node((j, i), None)

def SelectRandomChromosome(_fitnessArray):
    """
    Selects and returns a random chromosome from a fitness array
    Using roulette wheel method
    roulette = % of the chromosome to be chosen
    fitnessArray = array of fitness values of chromosomes(in %)
    """

    #add up all fitness values(should originally = 100)
    _fitnessArray_sum = sum(_fitnessArray)
    rouletteRoll = random.random() * 100
    for i in range(len(_fitnessArray)):
        #use proportion of total
        if (rouletteRoll >= (100 - _fitnessArray_sum) and rouletteRoll < (100 - _fitnessArray_sum + _fitnessArray[i])):
            return i
        #subtract current fitness from the sum to offset the proportion calculation
        _fitnessArray_sum -= _fitnessArray[i]
    return print("Failed to select a chromosome, function SelectRandomChromosome")

def AstarSearch(maze, _print):
    """
    Implements A* Path-finding algorithm in Chebyshev space.
    Goes through a 2D binary grid terrain map and finds the optimal path
    maze = maze Object
    print = bool for printing progress(for time benchmarks)
    """


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
    for newPos in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]: # Adjacent positions
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
    """
    Optimizes path in the search area, whenever solution is reached
    currentNode = node which reached the end of the maze
    displayMaze = maze Object which is used for printing
    print = bool for printing progress
    """
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
    if(_print):
        os.system('cls')
        print('\n'.join(map(str, _displayMaze.maze)))
        print("\nSolved!")
    #we optimize from the end to the start
    #so need to return reversed path
    return solutionPath[::-1]

def GeneticAlgorithmSearch(maze, _print):
    """
    Implements Genetic Algorithm in Manhattan space
    An individual is a 16bit string of 0 and 1
    Moves are represented binary  as:
    # 00 - up
    # 11 - down
    # 01 - right
    # 10 - left
    maze = maze Object
    print = bool for printing progress(for time benchmarks)


    """
    chromosomeLength = int(input("Enter number of moves:")) * 2
    chromosomeCount = int(input("Enter number of individuals in the genetic pool:"))
    #generate chromosomes
    chromosome = [[round(random.random()) for i in range(chromosomeLength)] for j in range(chromosomeCount)]
    
    if(_print):
        os.system('cls')
        print('\n'.join(map(str, maze.maze)))
    print("Working...")
    generation = 0
    solutionFlag = False
    finishFlag = False
    #variable for resetting population if fitness stays same
    fitnessCheck = 0
    while(not finishFlag):
        fitness = []
        for i in range(chromosomeCount):
            #set initial position of chromosome            
            Ycurrent = maze.start.position[0]
            Xcurrent = maze.start.position[1]
            chromosomeItr = 0   #iterator for traversing the chromosome string
            #execute path of chromosome
            for chromosomeItr in range(0, len(chromosome[i]), 2):
                #case for moving up first
                if (chromosome[i][chromosomeItr] == 0 and chromosome[i][chromosomeItr+1] == 0):
                    Ycurrent -= 1
                    #check if its inbounds
                    if (Ycurrent < 0 or Xcurrent < 0 or Ycurrent >= maze.sizeY or Xcurrent >= maze.sizeX):
                        Ycurrent += 1
                    else:
                        #check if it hit a wall
                        if (maze.maze[Ycurrent][Xcurrent] == 1):
                            Ycurrent += 1
                        else:
                            #check if it reached the finish
                            if(maze.maze[Ycurrent][Xcurrent] == 3 and not solutionFlag):
                                solution = chromosome[i][:chromosomeItr+2]
                                solutionFlag= True

                #case for moving down
                if (chromosome[i][chromosomeItr] == 1 and chromosome[i][chromosomeItr+1] == 1):
                    Ycurrent += 1
                    #check if its inbounds
                    if (Ycurrent < 0 or Xcurrent < 0 or Ycurrent >= maze.sizeY or Xcurrent >= maze.sizeX):
                        Ycurrent -= 1
                    else:
                        #check if it hit a wall
                        if (maze.maze[Ycurrent][Xcurrent] == 1):
                            Ycurrent -= 1
                        else:
                            #check if it reached the finish
                            if(maze.maze[Ycurrent][Xcurrent] == 3 and not solutionFlag):
                                solution = chromosome[i][:chromosomeItr+2]
                                solutionFlag = True


                #case for moving right
                if (chromosome[i][chromosomeItr] == 0 and chromosome[i][chromosomeItr+1] == 1):
                    Xcurrent += 1
                    #check if its inbounds
                    if (Ycurrent < 0 or Xcurrent < 0 or Ycurrent >= maze.sizeY or Xcurrent >= maze.sizeX):
                        Xcurrent -= 1
                    else:
                        #check if it hit a wall
                        if (maze.maze[Ycurrent][Xcurrent] == 1):
                            Xcurrent -= 1
                        else:
                            #check if it reached the finish
                            if(maze.maze[Ycurrent][Xcurrent] == 3 and not solutionFlag):
                                solution = chromosome[i][:chromosomeItr+2]
                                solutionFlag = True


                #case for moving left
                if (chromosome[i][chromosomeItr] == 1 and chromosome[i][chromosomeItr+1] == 0):
                    Xcurrent -= 1
                    #check if its inbounds
                    if (Ycurrent < 0 or Xcurrent < 0 or Ycurrent >= maze.sizeY or Xcurrent >= maze.sizeX):
                        Xcurrent += 1
                    else:
                        #check if it hit a wall
                        if (maze.maze[Ycurrent][Xcurrent] == 1):
                            Xcurrent += 1
                        else:
                            #check if it reached the finish
                            if(maze.maze[Ycurrent][Xcurrent] == 3 and not solutionFlag):
                                solution = chromosome[i][:chromosomeItr+2]
                                solutionFlag = True
    
                
            #calculate fitness of current chromosome and append it to fitness list
            #use pythagorean formula for distance calculation
            #fitness = 1/ (sqrt(dY^2 + dX^2) + 1)
            fitness.append(1 / (math.sqrt((maze.end.position[0]-Ycurrent)**2 + (maze.end.position[1]-Xcurrent)**2) + 1))


        fitnessTotal = sum(fitness)
        #create relative fitness(%-based) array
        rel_fitness = [(fitness[i] / fitnessTotal*100) for i in range(0, chromosomeCount)]
        #create parent chromosome list by using the Roulette Wheel Method
        parentChromosome = [(chromosome[SelectRandomChromosome(rel_fitness)]) for _ in range(len(chromosome))]
        #initialize offspringChromosome list
        offspringChromosome = []


        #set crossover Rate
        crossoverRate = 0.7
        #crossover parentChrommies
        i = 0
        while(i < len(parentChromosome)):
            #if chromosomes are an uneven count, e.g. 15, 1 chromosome is left without a pair, so check
            #if index is at least 1 position before the last element
            if (i < len(parentChromosome)-1):
                #generate crossover rate
                crossover = random.random()
                if(crossover <= crossoverRate):
                    #take first half of first parent and second half of second parent
                    firstChild = parentChromosome[i][:int(chromosomeLength/2)] + parentChromosome[i+1][int(chromosomeLength/2):]
                    #vice versa
                    secondChild = parentChromosome[i+1][:int(chromosomeLength/2)] + parentChromosome[i][int(chromosomeLength/2):]
                    #add both to offspring list
                    offspringChromosome.append(firstChild)
                    offspringChromosome.append(secondChild)
                else:
                    offspringChromosome.append(parentChromosome[i])
                    offspringChromosome.append(parentChromosome[i+1])
                i+=2
            else:
                offspringChromosome.append(parentChromosome[i])
                i+=1

        for i in range(len(offspringChromosome)):
            for j in range(len(offspringChromosome[i])):
                mutation = random.random()
                if (mutation <= 0.001):
                    if (offspringChromosome[i][j] == 0):
                        offspringChromosome[i][j] = 1
                    else:
                        offspringChromosome[i][j] = 0

        #fill chromosome list with the offspring chromosomes
        chromosome = offspringChromosome
        generation += 1

        #if the fitness doesn't change in a decent amount of generations,
        #the chromosome pool is likely to be filled with parents optimized to a local optimum instead of the global maximum, 
        #so we reset the chromosome pool


        #reset threshold is half the total amount of bi-crossover possibilities in the current set,
        #using the combination formula: nCr = n! / (r! * (n-r)!)
        resetThreshold = math.factorial(chromosomeCount) / (math.factorial(2) * math.factorial(chromosomeCount-2))
        resetThreshold /= 2
        if (generation%resetThreshold == 0):
            #save the total fitness
            fitnessCheck = fitnessTotal
        #if the total fitness hasn't changed in that many generations-1
        if (generation%(resetThreshold-1) == 0 and fitnessCheck == fitnessTotal):
            #generate brand new chromosome pool
            chromosome = [[round(random.random()) for i in range(chromosomeLength)] for j in range(chromosomeCount)]
            fitnessCheck = 0




        #in that case, restart the program hoping for better non-deterministic results.
        #uncomment this line to see the real-time progress of the program
        if (solutionFlag):
            finishFlag = True
    if (_print):
        Ycurrent = maze.start.position[0]
        Xcurrent = maze.start.position[1]
        #draw path of algorithm according to solution
        for b in range(0, len(solution), 2):
            #case for moving up first
            if (solution[b] == 0 and solution[b+1] == 0):
                Ycurrent -= 1
                #check if its inbounds
                if (Ycurrent < 0 or Xcurrent < 0 or Ycurrent >= maze.sizeY or Xcurrent >= maze.sizeX):
                    Ycurrent += 1
                elif (maze.maze[Ycurrent][Xcurrent] == 1):
                    Ycurrent += 1
                else:
                    maze.maze[Ycurrent][Xcurrent] = 4

            #case for moving down
            if (solution[b] == 1 and solution[b+1] == 1):
                Ycurrent += 1
                #check if its inbounds
                #check if its inbounds
                if (Ycurrent < 0 or Xcurrent < 0 or Ycurrent >= maze.sizeY or Xcurrent >= maze.sizeX):
                    Ycurrent -= 1
                elif (maze.maze[Ycurrent][Xcurrent] == 1):
                    Ycurrent -= 1
                else:
                    maze.maze[Ycurrent][Xcurrent] = 4


            #case for moving right
            if (solution[b] == 0 and solution[b+1] == 1):
                Xcurrent += 1
                #check if its inbounds
                if (Ycurrent < 0 or Xcurrent < 0 or Ycurrent >= maze.sizeY or Xcurrent >= maze.sizeX):
                    Xcurrent -= 1
                elif (maze.maze[Ycurrent][Xcurrent] == 1):
                    Xcurrent -= 1
                else:
                    maze.maze[Ycurrent][Xcurrent] = 4


            #case for moving left
            if (solution[b] == 1 and solution[b+1] == 0):
                Xcurrent -= 1
                #check if its inbounds
                if (Ycurrent < 0 or Xcurrent < 0 or Ycurrent >= maze.sizeY or Xcurrent >= maze.sizeX):
                    Xcurrent += 1
                elif (maze.maze[Ycurrent][Xcurrent] == 1):
                    Xcurrent += 1
                else:
                    maze.maze[Ycurrent][Xcurrent] = 4
        print("Solved!\n" +'\n'.join(map(str, maze.maze)), "\nSolution chromosome:", solution, "\nGeneration count:", generation)




def main():
    print("Maze legend:\n 0 - Open space\n 1 - Wall\n 2 - Start\n 3 - End\n 4 - Search area\n 9 - Optimized path\n")
    mapTerrain = input("Enter maze file(in UTF8 txt format) to be used:\n>> ")
    algorithm = int(input("Select algorithm:\n1. A* search\n2. Genetic algorithm search\n>> "))
    printString = input("Print progress?(y/n):\n>> ")
    if (printString == "y"):
        printProgress = True
    else:
        printProgress = False
    with open(mapTerrain) as terrain:
        terrain = terrain.read()
    terrain = terrain.split(" ")
    sizeX = terrain[0]
    sizeY = terrain[1]
    del terrain[0:2]
    maze = Maze(sizeY, sizeX, terrain)
    startTime = time.time()
    if (algorithm == 1):
        AstarSearch(maze, printProgress)
    elif (algorithm == 2):
        GeneticAlgorithmSearch(maze, printProgress)
    else:
        print("invalid selection of algorithm, please type in '1' or '2' ")
    print("Elapsed time:", time.time() - startTime, "\n")
    print("See you next time.")
    endinput = input("")

if __name__ == '__main__':
    main()