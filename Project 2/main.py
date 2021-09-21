#Jared Staman
import sys

def main():

    usage = "python main.py --input FILENAME --start START_NODE --goal GOAL_NODE --search SEARCH_TYPE"
    #error check how many arguments
    if(len(sys.argv) < 9):
        print(f"Too few arguments: {usage}")
        return
    
    if(len(sys.argv) > 9):
        print("Too many arguments: {usage}")
        return

    if(sys.argv[1] != "--input"):
        print(f"USAGE: {usage}")
        return
    
    #error check FILENAME
    #read in grid
    f = open(sys.argv[2], "r")
    print(f.read())
    #check if invalid char (anything not '0' ',' or '1')

    

    #for i, arg in enumerate(sys.argv):
        
    
    return


if __name__ == "__main__":
    main()