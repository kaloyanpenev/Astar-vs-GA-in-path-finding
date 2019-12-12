# A* path-finding vs Genetic Algorithm search

This program implements A* and Genetic Algorithm to traverse and solve a maze that is represented as a 2d binary grid terrain map.
It takes in .txt files that are **STRICTLY** in **UTF-8** format in the following sequence:
<COLUMNS> <ROWS> <GRID> <GRID> <GRID> etc.
Available files:
1. terrain1.txt - easy difficulty
2. terrain2.txt - medium difficulty
3. terrain3.txt - hard difficulty
4. terrain4.txt - hard difficulty

Maze legend:
1. 0 - Open space
2. 1 - Wall
3. 2 - Start
4. 3 - End
When running:
1. 4 - Search area
2. 9 - Optimized path(A* only)

#To run
If you have python installed:
1. Open Anaconda prompt
2. Go to the folder which contains AstarVsGA.py
3. Type in "py AstarVsGA.py"

If you DON'T have python installed:
1. Go into the "dist" folder
2. Run AstarVsGA.exe

#NOTE
When you are inputting the file name, please enter the .txt extension too.
As in "terrain1.txt",
not "terrain1".
