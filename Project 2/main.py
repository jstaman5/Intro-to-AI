#Jared Staman
import sys
import pprint

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

    return


if __name__ == "__main__":
    main()