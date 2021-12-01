#Interface

class Interface:

    #constructor
    def __init__(self, mode, engine, query = ''):
        self.mode = mode
        self.engine = engine
        self.query = query

    def listen(self):
        
        #Command line mode
        # send the query to the parental SearchEngine component’s “handle_query” function and print the results to the terminal.
        if(self.mode == 'C' and self.query != ''):
            self.engine.query = self.query
            self.engine.handle_query()

        #Interactive mode
        if(self.mode == 'I'):
            print("------------------------------")
            print("|      UTK EECS SEARCH       |")
            print("------------------------------")
            inp = ''

            #stdin
            while(inp != ":exit"):
                inp = input("\n> ")
                self.query = inp
                self.handle_input()
                
    #facilitate the routing of queries to functions in the search engine
    def handle_input(self):

        if(self.query == ":delete"):
            self.engine.delete()
        elif(self.query == ":train"):
            self.engine.train()
        else:
            self.engine.query = self.query
            self.engine.handle_query()