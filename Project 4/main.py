#Jared Staman
'''This project creates a eecs.utk search engine. There are two modes: Command line and Interactive.
In each mode, you can train the webcrawler and send queries to it to get back documents/links that
correspond to that specific query'''

from engine import *
import sys
def main():
    
    #Argument requirements
    #usage: python main.py -root https://eecs.utk.edu -mode C -query graduate

    #check if arguments has root,mode
    root_check = 0
    mode_check = 0
    verbose_check = 1
    query_check = 1
    query = 0
    verbose = 0
    for i, j in enumerate(sys.argv):
        if(j == '-root'):
            root_check = 1
            #check if argument after -root is valid
            if(i + 1 < len(sys.argv)):
                #must start with http (or https)
                if(sys.argv[i+1].startswith("http") == False):
                    print("ERROR: Invalid arguments provided")
                    sys.exit()
                #set root
                root = sys.argv[i+1]
            else:
                print("ERROR: Missing required arguments")
                sys.exit()

        if(j == '-mode'):
            mode_check = 1
            if(i+1 < len(sys.argv)):
                if(sys.argv[i+1] != 'C' and sys.argv[i+1] != 'I'):
                    print("ERROR: Invalid arguments provided")
                    sys.exit()
                #set mode
                mode = sys.argv[i+1]

                #-query is required for C
                if(sys.argv[i+1] == 'C'):
                    query_check = 0
                    for l, k in enumerate(sys.argv):
                        if(k == '-query'):
                            query_check = 1
                            if(l + 1 >= len(sys.argv)):
                                print("ERROR: Missing query argument")
                                sys.exit()
                            else:
                                query = sys.argv[l+1]
                        #-verbose is optional for C
                        if(k == '-verbose'):
                            if(l + 1 >= len(sys.argv)):
                                pass
                            else:
                                verbose = sys.argv[l+1]

                #-verbose is required for I
                if(sys.argv[i+1] == 'I'):
                    verbose_check = 0
                    for l, k in enumerate(sys.argv):
                        #should not use -query in I
                        if(k == '-query'):
                            print("ERROR: Interactive mode does not use query argument")
                            sys.exit()
                        if(k == '-verbose'):
                            verbose_check = 1
                            if(l + 1 >= len(sys.argv)):
                                print("ERROR: Missing verbose argument")
                                sys.exit()
                            else:
                                verbose = sys.argv[l+1]
            else:
                print("ERROR: Missing required arguments")
                sys.exit()

    #check if all arguments are there
    if(root_check == 0 or mode_check == 0):
        print("ERROR: Missing required arguments")
        sys.exit()
    if(query_check == 0):
        print("ERROR: Missing query argument")
        sys.exit()
    if(verbose_check == 0):
        print("ERROR: Missing verbose argument")
        sys.exit()
    
    if(verbose != 'T'):
        verbose = 'F'
    
    engine = SearchEngine(mode, root, 1, verbose, query)
    engine.start()

if __name__ == "__main__":
    main()