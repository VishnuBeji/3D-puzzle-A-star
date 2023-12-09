import numpy as np
import heapq

#Calculate manhattan distance by adding absolute value of difference in i, j and k
def manhat_distance(cur_state, goal_state):
    manhat_dist = 0
    size = len(cur_state)
    for i in range(size):
        for j in range(size):
            for k in range(size):
                i2, j2, k2 = np.argwhere(cur_state == goal_state[i, j, k])[0]
                if(goal_state[i, j, k]!=0):
                    manhat_dist += abs(i-i2)+abs(j-j2)+abs(k-k2)
    return manhat_dist

#Computes what the next state will be based on current state and what action is performed 
def compute_next_state(cur_state, action):
    size = len(cur_state)
    i, j, k = np.argwhere(cur_state == 0)[0]
    i2, j2, k2 = i, j, k
    if(action == 'N'):
        j2 = j-1
    if(action == 'S'):
        j2 = j+1
    if(action == 'W'):
        k2 = k-1
    if(action == 'E'):
        k2 = k+1        
    if(action == 'U'):
        i2 = i-1
    if(action == 'D'):
        i2 = i+1  

    #Handling edge cases with if condition to avoid invalid actions
    if(i2<size and i2>=0 and j2<size and j2>=0 and k2<size and k2>=0):
        #We create a copy to avoid overwriting, as list would be passed by reference
        next_state = np.copy(cur_state)    
        # Swap the values
        next_state[i, j, k], next_state[i2, j2, k2] = next_state[i2, j2, k2], next_state[i, j, k]
        return next_state
    else:
        return None

#This generator will generate a monotonically increasing counter everytime it gets called. 
#It is called everytime we generate a new node.
#This will be the second value in priority queues' sorting key, to pick the older element first, 
#once multiple states have same priority(f-value) and thereby break the tie. 
def monotonically_increasing_generator():
    current_value = 0
    while True:
        current_value += 1
        yield current_value

#This is the function that searches for goal state using A* algorithm with the heuristic
#f(node) = manhattan_distance(node,goal) + distance(start,node)
def solve(start_state, goal_state, actions):
    frontier = [] 
    visited = [tuple(start_state.ravel())]
    mono_gen = monotonically_increasing_generator()
    
    start_dist = manhat_distance(start_state, goal_state)
    
    start_node = (start_dist, next(mono_gen), start_state, 0, [], [start_dist])
    heapq.heappush(frontier, start_node)
    #boolean variable to check if we have reached a goal state
    found = False
    while(frontier):
        #We use this heapq to maintain out priority queue. Node contains details about the state,
        #the actions taken to reach till there, the value of f (distance)
        cur_node = heapq.heappop(frontier)
        
        cur_state,  cur_depth, cur_actionpath, cur_dist_list = cur_node[2:6]

        #If we reach a goal we return the node and the number of nodes generated and halt the iteration
        if np.array_equal(cur_state, goal_state):
            found = True
            #Here next(mono_gen)-1 will give the output as the total number of nodes generated
            return cur_node, next(mono_gen)-1 

        #Here we generate child nodes for every node expanded
        for action in actions:
            #First compute the set of next states based on actions
            next_state = compute_next_state(cur_state, action)

            #Check if the action would have led to a valid state
            if next_state is not None:
                #We flatten the 3D arr and convert to tuple as np array cannot be used for direct comparison
                next_state_tuple = tuple(next_state.ravel())
                #We check if the state has been reached previously and avoid if yes, as it is graph search
                if next_state_tuple not in visited:
                    visited.append(next_state_tuple)
                    depth = cur_depth + 1 
                    
                    #Calculating f(node) = manhattan_distance(node,goal) + distance(start,node)
                    dist = manhat_distance(next_state, goal_state) + depth  
                    dist_list = cur_dist_list[:]
                    dist_list.append(dist)

                    #Compute action path by taking parent's actionpath and appending the current action
                    actionpath = cur_actionpath[:]
                    actionpath.append(action)

                    #Node is generated with its distance(priority key), counter, state, depth, actionpath
                    #and distance list
                    #We use monotonic generator to handle cases with same priority, priority will be 
                    #given to older entries in the priority queue. We prioritise by distance.
                    next_node = (dist, next(mono_gen), next_state, depth, actionpath, dist_list)
                    
                    #Push the child into the priority queue with given information
                    heapq.heappush(frontier, next_node)

    if(found == False):
        print("No solution exists")
        return 