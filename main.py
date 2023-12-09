from puzzleOperations import solve
from puzzle import Puzzle

size = 3
input = 'input1.txt'
output = 'output1.txt'
#Initialise puzzle object with contents from the input file
puzzle = Puzzle(input, size)

#solve function takes the start state, goal state and actions to search and return goal node 
#containing all the meta info about the search and number of nodes generated
goal_node, num_gen_nodes = solve(puzzle.startgrid, puzzle.goalgrid, puzzle.actions)

#Retrieving depth, action path and list of distances from goal node
depth_goal_node = goal_node[3]
actionpath_goal_node = ' '.join(goal_node[4])
distlist_goal_node = ' '.join(map(str, goal_node[5])) 

#Outputs
puzzle.print_start_and_goal_grid()
print("", depth_goal_node, num_gen_nodes, actionpath_goal_node, distlist_goal_node, sep='\n')

#Write the ouputs to a file
with open(output, 'w') as f:
    # Redirect the last two print statements to the file
    puzzle.print_to_file(f)
    print("", depth_goal_node, num_gen_nodes, actionpath_goal_node, distlist_goal_node, sep='\n', file=f)