import numpy as np

#Class puzzle will contain the functions required to initialise our puzzle grid, goal grid and actions. 
#We are currently treating the size to be variable and it will work for a larger puzzle as well, the value \
#of 3 is given in main
class Puzzle:
    def __init__(self, input_file, size):
        self.size = size
        self.startgrid = np.zeros((self.size, self.size, self.size), dtype=int)
        self.goalgrid = np.zeros((self.size, self.size, self.size), dtype=int)
        self.actions = ['N','E','W','S','U','D']
        self.load_puzzle(input_file)
        
    #Loads the startgrid and goalgrid arrays by reading the input file
    def load_puzzle(self, input_file):
        with open(input_file, 'r') as file:
            # Read the entire file content into a string
            self.file_content = file.read().strip()

        #We split by double EOL to get each 3x3 layer of the puzzle
        layers = self.file_content.split('\n\n')

        #We get line by line and thereafter space separated numbers to fill into the arrays
        for i in range(self.size):
            lines = layers[:self.size][i].split('\n')
            for j in range(self.size):
                nums = lines[j].split(' ') 
                for k in range(self.size):
                    self.startgrid[i][j][k] = nums[k]

        for i in range(self.size):
            lines = layers[self.size:][i].split('\n')
            for j in range(self.size):
                nums = lines[j].split(' ') 
                for k in range(self.size):
                    self.goalgrid[i][j][k] = nums[k]

    #Prints the input file as such, as defined in the output format
    def print_start_and_goal_grid(self):
        print(self.file_content)

    #Prints the input file as such, to a defined output file f
    def print_to_file(self, f):
        print(self.file_content, file=f)