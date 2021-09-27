#Jared Staman
import sys
import pprint
from math import sqrt

SHORTEST_PATH = 100000
DFS_TRAVERSALS = 0
DFS_PATH = []

def isValid(grid, row, col, visited):
    if(row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])):
        if(grid[row][col] == '0'):
            for coord in visited:
                if(row == coord[0] and col == coord[1]):
                    return False
            return True
    
    return False

def dfsValid(grid, row, col):
    if(row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])):
        if(grid[row][col] == '0'):
            return True
    return False

def dfsVisited(node, tuple):
    while(node.prev):
        if(tuple == node.tuple):
            return False
        node = node.prev
    return True
    
def dfs_recursive(grid, node, goal):
    global DFS_TRAVERSALS
    DFS_TRAVERSALS += 1
    curr = node
    global SHORTEST_PATH
    if(curr.tuple == goal):
        if(curr.depth < SHORTEST_PATH):
            SHORTEST_PATH = curr.depth
            global DFS_PATH
            DFS_PATH = []
            while(curr.prev):
                DFS_PATH.insert(0,curr.tuple)
                curr = curr.prev
            return
    #if(curr.depth >= SHORTEST_PATH-1):
        #return    

    curr_row = node.row
    curr_col = node.col
    #bottom
    if(dfsValid(grid, curr_row+1, curr_col) and dfsVisited(curr, (curr_row+1, curr_col))):
        new = (curr_row+1, curr_col)
        new_node = Node(curr, new, curr.depth + 1)
        #visited.append(new_node.tuple)
        dfs_recursive(grid, new_node, goal)

    #right
    if(dfsValid(grid, curr_row, curr_col+1) and dfsVisited(curr, (curr_row, curr_col+1))):
        new = (curr_row, curr_col+1)
        new_node = Node(curr, new, curr.depth + 1)
        #visited.append(new_node.tuple)
        dfs_recursive(grid, new_node, goal)

    #up
    if(dfsValid(grid, curr_row-1, curr_col) and dfsVisited(curr, (curr_row-1, curr_col))):
        new = (curr_row-1, curr_col)
        new_node = Node(curr, new, curr.depth + 1)
        #visited.append(new_node.tuple)
        dfs_recursive(grid, new_node, goal)

    #left
    if(dfsValid(grid, curr_row, curr_col-1) and dfsVisited(curr, (curr_row, curr_col-1))):
        new = (curr_row, curr_col-1)
        new_node = Node(curr, new, curr.depth + 1)
        #visited.append(new_node.tuple)
        dfs_recursive(grid, new_node, goal)

def calcH(tuple, goal):
    H = sqrt((tuple[0]-goal[0])**2 + (tuple[1]-goal[1])**2)
    return H

class Node:
    def __init__(self, prev, tuple, depth=0, g=0, h=0, f=0):
        self.prev = prev
        self.row = tuple[0]
        self.col = tuple[1]
        self.tuple = tuple
        self.depth = depth
        self.g = g
        self.h = h
        self.f = f

class PathPlanner:

    def __init__(self, grid):
        self.grid = grid
    
    def breadth_first_search(self, start, goal):
        queue = []
        visited = []

        count = 0
        start_node = Node(None, start)
        queue.append(start_node)
        visited.append(start)

        while(queue):
            curr = queue.pop(0)
            count += 1
            #visited.append(curr.tuple)

            if(curr.tuple == goal):
                path = []
                while(curr.prev != None):
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


        start_node = Node(None, start, 1)
        dfs_recursive(self.grid, start_node, goal)
        global DFS_PATH
        global DFS_TRAVERSALS
        DFS_PATH.insert(0, start)
        print(f"Path: {DFS_PATH}")
        print(f"Traversals: {DFS_TRAVERSALS}")
        return

    def a_star_search(self, start, goal):

        traversals = 0       
        open_list = []
        closed_list = []

        start_node = Node(None,start)
        goal_node = Node(None, goal)

        open_list.append(start_node)

        while(open_list):
            #Priority Queue, find node in open list with smallest f value
            curr = open_list[0]
            index = 0
            for i, node in enumerate(open_list):
                if(node.f < curr.f):
                    curr = node
                    index = i
            
            open_list.pop(index)
            closed_list.append(curr)
            traversals += 1
            if curr.tuple == goal:
                path = []
                while(curr):
                    path.insert(0,curr.tuple)
                    curr = curr.prev
                print(f"Path: {path}")
                print(f"Traversals: {traversals}")
                return
            
            curr_row = curr.row 
            curr_col = curr.col

            #bottom
            if(dfsValid(self.grid, curr_row+1, curr_col)):
                new = (curr_row+1, curr_col)
                new_node = Node(curr, new)
                for closed_child in closed_list:
                    if new_node == closed_child:
                        continue
                new_node.g = curr.g + 1
                new_node.h = calcH(new_node.tuple,goal)
                new_node.f = new_node.g + new_node.h

                for open_node in open_list:
                    if(new_node == open_node and new_node.g > open_node.g):
                        continue
                open_list.append(new_node)

            #right
            if(dfsValid(self.grid, curr_row, curr_col+1)):
                new = (curr_row, curr_col+1)
                new_node = Node(curr, new)
                for closed_child in closed_list:
                    if new_node == closed_child:
                        continue
                new_node.g = curr.g + 1
                new_node.h = calcH(new_node.tuple,goal)
                new_node.f = new_node.g + new_node.h

                for open_node in open_list:
                    if(new_node == open_node and new_node.g > open_node.g):
                        continue
                open_list.append(new_node)

            #up
            if(dfsValid(self.grid, curr_row-1, curr_col)):
                new = (curr_row-1, curr_col)
                new_node = Node(curr, new)
                for closed_child in closed_list:
                    if new_node == closed_child:
                        continue
                new_node.g = curr.g + 1
                new_node.h = calcH(new_node.tuple,goal)
                new_node.f = new_node.g + new_node.h

                for open_node in open_list:
                    if(new_node == open_node and new_node.g > open_node.g):
                        continue
                open_list.append(new_node)

            #left
            if(dfsValid(self.grid, curr_row, curr_col-1)):
                new = (curr_row, curr_col-1)
                new_node = Node(curr, new)
                for closed_child in closed_list:
                    if new_node == closed_child:
                        continue
                new_node.g = curr.g + 1
                new_node.h = calcH(new_node.tuple,goal)
                new_node.f = new_node.g + new_node.h

                for open_node in open_list:
                    if(new_node == open_node and new_node.g > open_node.g):
                        continue
                open_list.append(new_node)
        return

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
    PathPlanner(grid).a_star_search(start, goal)

    return


if __name__ == "__main__":
    main()