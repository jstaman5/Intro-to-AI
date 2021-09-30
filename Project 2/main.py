#Jared Staman
#CS 423 Project 2: Path Planning
#This code takes in a grid, start coord, goal coord, and a search algorithm (BFS, DFS, A*).
#It then prints the shortest path using the specified algorithm along with how many traversals it went through

import sys
import pprint
from math import sqrt

#global variables used in dfs to keep track of shortest path and traversals
SHORTEST_PATH = 100000
DFS_TRAVERSALS = 0
DFS_PATH = []

def isValid(grid, row, col, visited):
    '''
    This function is used in BFS. It checks whether the given coordinate is in the grid.
    It also checks to make sure the value at the coordinate is a '0' not a '1'
    Finally, it checks to make sure we have not already visited this coordinate
    '''
    if(row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])):
        if(grid[row][col] == '0'):
            for coord in visited:
                if(row == coord[0] and col == coord[1]):
                    return False
            return True
    
    return False

def dfsValid(grid, row, col):
    '''
    This function is used in DFS and A*.
    It checks whether the given coordinate is in the grid.
    Also, it checks to make sure the value at the coordiante is a '0' and not a '1'
    '''
    if(row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])):
        if(grid[row][col] == '0'):
            return True
    return False

def dfsVisited(node, tuple):
    '''
    This function is used in DFS.
    It checks whether this path has already checked a given coordinate. If it has, then we shouldn't go there again.
    '''
    while(node.prev):
        if(tuple == node.tuple):
            return False
        node = node.prev
    return True
    
def dfs_recursive(grid, node, goal):
    '''
    This function is the recursive part for our DFS algorithm.
    First it checks whether we are at the goal.
    Then it branches into its children, checking if they are valid coordinates.
    If they are then, then we go there and call the recursive function
    '''
    global DFS_TRAVERSALS
    DFS_TRAVERSALS += 1
    curr = node
    global SHORTEST_PATH
    if(curr.tuple == goal):
        if(curr.depth < SHORTEST_PATH):
            SHORTEST_PATH = curr.depth
            global DFS_PATH
            DFS_PATH = []
            while(curr):
                DFS_PATH.insert(0,curr.tuple)
                curr = curr.prev
            return
    '''
    This following commented out code, if uncommented out, will significantly lower the amount of traversals.
    This is because the code cuts of paths that already have a longer length than a previously found shortest path.
    '''
    #if(curr.depth >= SHORTEST_PATH-1):
        #return    

    curr_row = node.row
    curr_col = node.col
    #bottom
    if(dfsValid(grid, curr_row+1, curr_col) and dfsVisited(curr, (curr_row+1, curr_col))):
        new = (curr_row+1, curr_col)
        new_node = Node(curr, new, curr.depth + 1)
        dfs_recursive(grid, new_node, goal)

    #right
    if(dfsValid(grid, curr_row, curr_col+1) and dfsVisited(curr, (curr_row, curr_col+1))):
        new = (curr_row, curr_col+1)
        new_node = Node(curr, new, curr.depth + 1)
        dfs_recursive(grid, new_node, goal)

    #up
    if(dfsValid(grid, curr_row-1, curr_col) and dfsVisited(curr, (curr_row-1, curr_col))):
        new = (curr_row-1, curr_col)
        new_node = Node(curr, new, curr.depth + 1)
        dfs_recursive(grid, new_node, goal)

    #left
    if(dfsValid(grid, curr_row, curr_col-1) and dfsVisited(curr, (curr_row, curr_col-1))):
        new = (curr_row, curr_col-1)
        new_node = Node(curr, new, curr.depth + 1)
        dfs_recursive(grid, new_node, goal)

def calcH(tuple, goal):
    '''
    This is a helper function that calculates the H value used in A*
    '''
    H = (((tuple[0]-goal[0])**2) + ((tuple[1]-goal[1])**2))
    return H

class Node:

    #Constructor for our Node.
    def __init__(self, prev, tuple, depth=0, g = 0, h = 0, f = 0):
        self.prev = prev
        self.row = tuple[0]
        self.col = tuple[1]
        self.tuple = tuple
        self.depth = depth
        self.g = g
        self.h = h
        self.f = f


class PathPlanner:
    #Constructor for our pathplanner (sets grid)
    def __init__(self, grid):
        self.grid = grid
    

    def breadth_first_search(self, start, goal):
        '''
        This is the breadth first search function. It loops through a queue, first checking if the coordinate
        we are at is the goal coordinate. If it isn't then we check our current node's neighbors to see if we can go there.
        We then add valid neighbors to our queue and also to our visited list to keep track of where we have been.
        '''
        queue = []
        visited = []

        count = 0
        start_node = Node(None, start)
        queue.append(start_node)
        visited.append(start)

        while(queue):
            curr = queue.pop(0)
            count += 1
            
            #check if we are at goal
            if(curr.tuple == goal):
                path = []
                while(curr):
                    path.insert(0,curr.tuple)
                    curr = curr.prev
                print(f"Path: {path}")
                print(f"Traversed: {count}")
                return

            curr_row = curr.row
            curr_col = curr.col

            #add to queue
            #down
            if(isValid(self.grid, curr_row+1, curr_col, visited)):
                new = (curr_row+1, curr_col)
                new_node = Node(curr, new)
                queue.append(new_node)
                visited.append(new_node.tuple)

            #right
            if(isValid(self.grid, curr_row, curr_col+1, visited)):
                new = (curr_row, curr_col+1)
                new_node = Node(curr, new)
                queue.append(new_node)
                visited.append(new_node.tuple)

            #up
            if(isValid(self.grid, curr_row-1, curr_col, visited)):
                new = (curr_row-1, curr_col)
                new_node = Node(curr, new)
                queue.append(new_node)
                visited.append(new_node.tuple)

            #left
            if(isValid(self.grid, curr_row, curr_col-1, visited)):
                new = (curr_row, curr_col-1)
                new_node = Node(curr, new)
                queue.append(new_node)
                visited.append(new_node.tuple)
            
        return -1

    def depth_first_search(self, start, goal):
        '''
        This function performs our depth first search. It mainly just calls the recursive function and then prints the results.
        '''
        start_node = Node(None, start, 1)
        dfs_recursive(self.grid, start_node, goal)
        global DFS_PATH
        global DFS_TRAVERSALS
        if (DFS_PATH == []):
            print("Could not find a path")
        else:
            print(f"Path: {DFS_PATH}")
            print(f"Traversed: {DFS_TRAVERSALS}")
        
        return

    def a_star_search(self, start, goal):
        
        '''
        Similar to BFS in which we loop through a queue, except we treat this one more as a priority queue.
        The priority is based off of the f value, which is g + h. g is the spots away from the start. h is the 
        euclidean distance from the goal. Loop through the queue, checking if we are at the goal and adding neighbors to the queue.
        '''
        start_node = Node(None, start)
        open_list = []
        closed_list = []
        traversals = 0

        open_list.append(start_node)

        while(open_list):
            #check to make sure there is a path
            if (traversals > 10000):
                break
            #get the current node with the lowest f value
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            traversals += 1

            #check if we are at the goal
            if(current_node.tuple == goal):
                path = []
                current = current_node
                while(current):
                    path.insert(0,current.tuple)
                    current = current.prev
                print(f"Path: {path}")
                print(f"Traversed: {traversals}")
                return
            
            #generate children
            curr_row = current_node.row
            curr_col = current_node.col
        
            #down
            if(dfsValid(self.grid, curr_row+1, curr_col)):
                new = (curr_row+1, curr_col)
                new_node = Node(current_node, new)

                #skip if child is in closed_list (seen it already)
                for node in closed_list:
                    if new_node == node:
                        continue
                
                #creating the f, g, h values for the node
                new_node.g = current_node.g + 1
                new_node.h = calcH(new_node.tuple, goal)
                new_node.f = new_node.g + new_node.h

                #skip if child is already in open list
                for node in open_list:
                    if new_node == node and new_node.g > node.g:
                        continue
                
                open_list.append(new_node)
             

            #right
            if(dfsValid(self.grid, curr_row, curr_col+1)):
                new = (curr_row, curr_col+1)
                new_node = Node(current_node, new)
                for node in closed_list:
                    if new_node == node:
                        continue
                
                new_node.g = current_node.g + 1
                new_node.h = calcH(new_node.tuple, goal)
                new_node.f = new_node.g + new_node.h

                for node in open_list:
                    if new_node == node and new_node.g > node.g:
                        continue
                
                open_list.append(new_node)
              

            #up
            if(dfsValid(self.grid, curr_row-1, curr_col)):
                new = (curr_row-1, curr_col)
                new_node = Node(current_node, new)
                for node in closed_list:
                    if new_node == node:
                        continue
                
                new_node.g = current_node.g + 1
                new_node.h = calcH(new_node.tuple, goal)
                new_node.f = new_node.g + new_node.h

                for node in open_list:
                    if new_node == node and new_node.g > node.g:
                        continue
                
                open_list.append(new_node)
               

            #left
            if(dfsValid(self.grid, curr_row, curr_col-1)):
                new = (curr_row, curr_col-1)
                new_node = Node(current_node, new)
                for node in closed_list:
                    if new_node == node:
                        continue
                
                new_node.g = current_node.g + 1
                new_node.h = calcH(new_node.tuple, goal)
                new_node.f = new_node.g + new_node.h

                for node in open_list:
                    if new_node == node and new_node.g > node.g:
                        continue
                
                open_list.append(new_node)
               
            
        return -1


def main():

    usage = "python main.py --input FILENAME --start START_NODE --goal GOAL_NODE --search SEARCH_TYPE"
    #error check how many arguments
    if(len(sys.argv) < 9):
        print(f"Too few arguments: {usage}")
        sys.exit()
    
    if(len(sys.argv) > 9):
        print("Too many arguments: {usage}")
        sys.exit()

    if(sys.argv[1] != "--input"):
        print(f"USAGE: {usage}")
        sys.exit()
    
    #error check FILENAME
    try:
        f = open(sys.argv[2], "r")
    except OSError:
        print("Invalid filename")
        sys.exit()
    
    #read in grid
    grid = []
    for line in f:
        row = []
        for char in line:
            if(char.isspace()):
                continue
            # valid characters are only '0', '1', ','
            elif(char != '0' and char != '1' and char != ','):
                print(f"Invalid grid: cannot have {char}")
                sys.exit()
            if(char == '0' or char == '1'):
                row.append(char)
        grid.append(row)

    #pprint.pprint(grid)

    if(sys.argv[3] != "--start"):
        print(f"USAGE: {usage}")
        sys.exit()

    #error check start node in coordinate form
    s = sys.argv[4]
    comma_check = 0
    num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    str1 = ""
    str2 = ""
    for i in s:
        if(i != ','):
            if(comma_check == 0):
                if i in num_list:
                    str1 += i
                else:
                    print("Invalid start coordinate format")
                    sys.exit()
            if(comma_check == 1):
                if i in num_list:
                    str2 += i
                else:
                    print("Invalid start coordinate format")
                    sys.exit()
        else:
            comma_check = 1

    if(comma_check == 0):
        print(f"Invalid start coordinate: no comma")
        sys.exit()

    if(str1.isdigit()):
        start_row = int(str1)
    else:
        print("Invalid start coordinate")
        sys.exit()
    if(str2.isdigit()):
        start_col = int(str2)
    else:
        print("Invalid start coordinate")
        sys.exit()
    
    #must be within the grid
    if(start_row >= len(grid)):
        print("Invalid start coordinate: outside grid")
        sys.exit()
    if(start_col >= len(grid[0])):
        print("Invalid start coordiante: outside grid")
        sys.exit()

    if(sys.argv[5] != "--goal"):
        print(f"USAGE: {usage}")
        sys.exit()

    #error check goal state
    s = sys.argv[6]
    comma_check = 0
    str3 = ""
    str4 = ""
    for i in s:
        if(i != ','):
            if(comma_check == 0):
                if i in num_list:
                    str3 += i
                else:
                    print("Invalid goal coordinate format")
                    sys.exit()
            if(comma_check == 1):
                if i in num_list:
                    str4 += i
                else:
                    print("Invalid goal coordinate format")
                    sys.exit()
        else:
            comma_check = 1

    if(comma_check == 0):
        print(f"Invalid goal coordinate: no comma")
        sys.exit()

    if(str3.isdigit()):
        goal_row = int(str3)
    else:
        print("Invalid goal coordinate")
        sys.exit()
    if(str4.isdigit()):
        goal_col = int(str4)
    else:
        print("Invalid goal coordinate")
        sys.exit()
    
    #must be within the grid
    if(goal_row >= len(grid)):
        print("Invalid goal coordinate: outside grid")
        sys.exit()
    if(goal_col >= len(grid[0])):
        print("Invalid goal coordiante: outside grid")
        sys.exit()

    if(sys.argv[7] != "--search"):
        print(f"USAGE: {usage}")
        sys.exit()
    
    #search type can be BFS, DFS, A* or ALL
    search_list = ["BFS", "DFS", "A*", "ALL"]
    search = sys.argv[8]
    if search not in search_list:
        print("Invalid search type")
        sys.exit()

    start = (start_row, start_col)
    goal =(goal_row, goal_col)

    #calling functions depending on search type
    if(search == "BFS"):
        if (PathPlanner(grid).breadth_first_search(start, goal) == -1):
            print("Could not find a path")
    elif (search == "DFS"):
        PathPlanner(grid).depth_first_search(start, goal)
    elif (search == "A*"):
        if (PathPlanner(grid).a_star_search(start, goal) == -1):
            print("Could not find a path")
    elif (search == "ALL"):
        print("Algorithm: BFS")
        if (PathPlanner(grid).breadth_first_search(start,goal) == -1):
            print("Could not find a path")
        print('\n' + "Algorithm: DFS")
        PathPlanner(grid).depth_first_search(start, goal)
        print('\n' + "Algorithm: A*")
        if (PathPlanner(grid).a_star_search(start, goal) == -1):
            print("Could not find a path")
    
    return


if __name__ == "__main__":
    main()