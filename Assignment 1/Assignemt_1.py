import pandas as pd
import numpy as np
import sys
import time
from queue import PriorityQueue

driving_data=pd.read_csv("driving.csv")
straightline_data=pd.read_csv("straightline.csv")

# print(driving_data.head())
# print(straightline_data.head())

def get_input():
    if "".join(sys.argv[1:]).islower():
        print("Enter the arguments in UPPERCASE!!")
        sys.exit(-1)
    if len(sys.argv[1:]) <2:
        print("ERROR: Not enough input arguments")
        sys.exit(-1)
    if len(sys.argv[1:]) >2:
        print("ERROR: too many input arguments")
        sys.exit(-1)
    
    argv1=sys.argv[1]
    argv2=sys.argv[2]
    
    if argv1 not in driving_data.columns[1:]:
        print(argv1," is not part of given state")
        sys.exit(-1)
    if argv2 not in driving_data.columns[1:]:
        print(argv2," is not part of given state")
        sys.exit(-1)
    return argv1,argv2

def get_neighbors(state, driving_df):
    neighbors = []
    for col in driving_df.columns[1:]:  # Skip the 'STATE' column
        distance = driving_df.loc[driving_df['STATE'] == state, col].values[0]
        if distance > 0:  # A positive distance indicates a neighbor
            neighbors.append((col, distance))
    return neighbors

# Helper function to get the straight line distance from the straightline DataFrame
def get_straight_line_distance(state, goal_state, straightline_df):
    return straightline_df.loc[straightline_df['STATE'] == state, goal_state].values[0]


def Gready_BFS(g_state,i_state,driving_df, straightline_df):
    explored = set() 
    frontier = PriorityQueue()  
    #adding the initial state into frontier
    frontier.put((0, i_state, [i_state]))  # (heuristic, state, path)
    
    cost_so_far = {i_state: 0}

    while not frontier.empty():
        heuristic, current_state, path = frontier.get()
        explored.add(current_state)


        if current_state == g_state:
            return path, cost_so_far[current_state],explored

        # Expand the frontier
        for neighbor, step_cost in get_neighbors(current_state, driving_df):
            if neighbor not in explored:
                # Calculate the new cost
                new_cost = cost_so_far[current_state] + step_cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    new_path = path + [neighbor]
                    neighbor_heuristic = get_straight_line_distance(neighbor, g_state, straightline_df)
                    frontier.put((neighbor_heuristic, neighbor, new_path))

    # If the goal state was never reached
    return None, None,None
    
def A_Star_Search(g_state,i_state,driving_df, straightline_df):
    explored = set()  # Set to keep track of explored states
    frontier = PriorityQueue()  # Priority queue for the frontier with priority as straight line distance
    frontier.put((0, i_state, [i_state]))  # (heuristic, state, path)
    
    cost_so_far = {i_state: 0}

    while not frontier.empty():
        heuristic, current_state, path = frontier.get()
        explored.add(current_state)

        if current_state == g_state:
            return path, cost_so_far[current_state],explored
        
        for neighbor, step_cost in get_neighbors(current_state, driving_df):
            if neighbor not in explored:
                new_cost = cost_so_far[current_state] + step_cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    new_path = path + [neighbor]
                    priority_heuristic = new_cost + get_straight_line_distance(neighbor, goal_state, straightline_df)
                    frontier.put((priority_heuristic, neighbor, new_path))

    return None, None,None


# goal_state,initial_state=get_input()
initial_state = input('Enter Initial State: ')
goal_state = input('Enter Goal State: ')


start_time=time.time()
path, path_cost,explored=Gready_BFS(goal_state,initial_state,driving_data,straightline_data)
end_time=time.time()
path=None
if not path and not path_cost and not explored:
    print("Solution: NO SOLUTION FOUND")
    print("Number of stops on a path: 0")
    print("Execution time:",str(end_time-start_time)," seconds")
    print("Complete path cost: 0")
else:
    print("Chougule Aniket A20552758 Solution:")
    print("Intital State:'"+str(initial_state)+"'")
    print("Goal State:'"+str(goal_state)+"'")
    print("Greedy Best First Search:")
    print("Solution: ",path)
    print("Number of expanded nodes :",len(explored))
    print("Number of stops on a path:",len(path))
    print("Execution time:",str(end_time-start_time)," Second")
    print("Complete path cost:",path_cost," Miles")


start_time=time.time()
path, path_cost,explored=A_Star_Search(goal_state,initial_state,driving_data,straightline_data)
end_time=time.time()

print("\nA * Search:")
print("Solution: ",path)
print("Number of expanded nodes :",len(explored))
print("Number of stops on a path:",len(path))
print("Execution time:",str(end_time-start_time)," Second")
print("Complete path cost:",path_cost," Miles")