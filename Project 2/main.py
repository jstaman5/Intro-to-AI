#Jared Staman
import sys
import pprint

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
    
def dfs_recursive(grid, node, goal, visited):
    global DFS_TRAVERSALS
    DFS_TRAVERSALS += 1
    curr = node
    print(curr.tuple)
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
    if(isValid(grid, curr_row+1, curr_col, visited)):
        new = (curr_row+1, curr_col)
        new_node = Node(curr, new, curr.depth + 1)
        visited.append(new_node.tuple)
        dfs_recursive(grid, new_node, goal, visited)

    #right
    if(isValid(grid, curr_row, curr_col+1, visited)):
        new = (curr_row, curr_col+1)
        new_node = Node(curr, new, curr.depth + 1)
        visited.append(new_node.tuple)
        dfs_recursive(grid, new_node, goal, visited)

    #up
    if(isValid(grid, curr_row-1, curr_col, visited)):
        new = (curr_row-1, curr_col)
        new_node = Node(curr, new, curr.depth + 1)
        visited.append(new_node.tuple)
        dfs_recursive(grid, new_node, goal, visited)

    #left
    if(isValid(grid, curr_row, curr_col-1, visited)):
        new = (curr_row, curr_col-1)
        new_node = Node(curr, new, curr.depth + 1)
        visited.append(new_node.tuple)
        dfs_recursive(grid, new_node, goal, visited)


class Node:
    def __init__(self, prev, tuple, depth=0):
        self.prev = prev
        self.row = tuple[0]
        self.col = tuple[1]
        self.tuple = tuple
        self.depth = depth

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

        visited = []

        start_node = Node(None, start, 1)
        visited.append(start)
        dfs_recursive(self.grid, start_node, goal, visited)
        global DFS_PATH
        global DFS_TRAVERSALS
        print(f"Path: {DFS_PATH}")
        print(f"Traversals: {DFS_TRAVERSALS}")
        return

    def a_star_search(self, start, goal):
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
    PathPlanner(grid).depth_first_search(start, goal)

    return


if __name__ == "__main__":
    main()