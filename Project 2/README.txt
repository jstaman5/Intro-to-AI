Jared Staman

This project reads in a grid, start coordinate, goal coordinate, 
and a search algorithm (BFS, DFS, A*, or all of them). It then uses the specified algorithm
to find and print the shortest path. It also prints how many traversals the algorithm went through.

How to use:
python main.py --input FILENAME --start START_NODE --goal GOAL_NODE --search SEARCH_TYPE

FILENAME = grid that is made of 0's and 1's separated by commas. 0's are considered
valid spaces to move to and 1's are considered obstacles that cannot be moved to.
Only up, down, right, left movements are allowed, no diagonals.
Here is an example grid input

0,1,0,0
0,1,0,0
0,0,0,0
0,1,0,0

START_NODE and GOAL_NODE must be a number followed by a comma followed by a number
such as 0,0 and 3,3

SEARCH_TYPE can either be BFS, DFS, A*, or ALL