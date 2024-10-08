import pandas as pd
from queue import PriorityQueue
import sys
import time
import csv

def check_initial_goal_state(initial_state,goal_state):
    with open('driving.csv','r') as drivingcsvfile:
        reader = csv.reader(drivingcsvfile)

        headers = next(reader)[1:]
        try:
            A = headers.index(initial_state)
            B = headers.index(goal_state)
        except:
            return -1
        else:            
            return 1

class ExplorationNode:
    def __init__(self, location, ancestor=None, path_cost=0, estimate=0):
        self.location = location
        self.ancestor = ancestor
        self.path_cost = path_cost  
        self.estimate = estimate  
        self.total_cost = path_cost + estimate  

    def __lt__(self, comp):
        return self.total_cost < comp.total_cost

def Astar(start_point, end_point, heuristics, roads):
    return search_strategy(start_point, end_point, heuristics, roads, method='astar')

def Greedy_Search(start_point, end_point, heuristics, roads):
    return search_strategy(start_point, end_point, heuristics, roads, method='heuristic')

def search_strategy(start_point, end_point, heuristics, roads, method):
    start_time = time.time()
    expanded_nodes = 0


    locations = heuristics['STATE'].tolist()
    heuristic_map = {row['STATE']: row.drop('STATE').to_dict() for _, row in heuristics.iterrows()}
    road_map = {row['STATE']: row.drop('STATE').to_dict() for _, row in roads.iterrows()}

    boundary = PriorityQueue()
    initial_node = ExplorationNode(start_point, path_cost=0, estimate=heuristic_map[start_point][end_point])
    boundary.put(initial_node)

    visited = set()

    while not boundary.empty():
        node = boundary.get()

        if node.location == end_point:
            end_time = time.time()
            return True, trace_path(node), node.path_cost, end_time - start_time, expanded_nodes

        visited.add(node.location)
        expanded_nodes += 1

        for next_loc in locations:
            travel_cost = road_map[node.location][next_loc]
            if travel_cost == -1 or next_loc in visited:
                continue

            new_path_cost = node.path_cost + travel_cost
            new_estimate = heuristic_map[next_loc][end_point]
            successor_node = ExplorationNode(next_loc, ancestor=node, path_cost=new_path_cost, estimate=new_estimate)

            if method == 'astar':
                if all(not (existing_node.location == next_loc and existing_node.total_cost <= successor_node.total_cost) for existing_node in boundary.queue):
                    boundary.put(successor_node)
            else:  
                successor_node.total_cost = successor_node.estimate  
                if all(not (existing_node.location == next_loc and existing_node.estimate <= successor_node.estimate) for existing_node in boundary.queue):
                    boundary.put(successor_node)

    return False, [], 0

def trace_path(terminal_node):
    route = []
    while terminal_node:
        route.append(terminal_node.location)
        terminal_node = terminal_node.ancestor
    route.reverse()
    return route

roads_df = pd.read_csv('driving.csv')
heuristics_df = pd.read_csv('straightline.csv')

cmdline_arguments = len(sys.argv)

if "".join(sys.argv[1:]).islower():
    print("Enter the arguments in UPPERCASE!!")
    sys.exit(-1)
if len(sys.argv[1:]) <2:
    print("ERROR: Not enough input arguments")
    sys.exit(-1)
if len(sys.argv[1:]) >2:
    print("ERROR: too many input arguments")
    sys.exit(-1)

first_arg = sys.argv[0]
initial_state = sys.argv[1].upper()
goal_state = sys.argv[2].upper()

print('\nScript name:', first_arg)
print('\nINITIAL STATE:', goal_state)
print('\nGOAL STATE:', initial_state)
    

state_flag = check_initial_goal_state(initial_state,goal_state)

if state_flag == 1:
    A,solution_path_1,path_cost_1, execution_time_1,expanded_nodes_1 = Greedy_Search(initial_state, goal_state, heuristics_df, roads_df)
    no_of_stops_1 = len(solution_path_1)

    B,solution_path_2,path_cost_2, execution_time_2,expanded_nodes_2 = Astar(initial_state, goal_state, heuristics_df, roads_df)
    no_of_stops_2 = len(solution_path_2)

    print('\nGreedy Best First Search:')
    print('Initial: ' + initial_state + ' | Goal: ' + goal_state + ' | Path : ' + str(solution_path_1) + '')
    print('Number of nodes Expandes: ' + str(expanded_nodes_1))
    print('Number of stops made: ' + str(no_of_stops_1))
    print('Execution Time: ' + str(execution_time_1))
    print('Path Cost: '+ str(path_cost_1) + ' miles')
    
    print('\nA*:')
    print('Initial: ' + initial_state + ' | Goal: ' + goal_state + ' | Path : ' + str(solution_path_2) + '')
    print('Number of nodes Expandes: ' + str(expanded_nodes_2))
    print('Number of stops made: ' + str(no_of_stops_2))
    print('Execution Time: ' + str(execution_time_2))
    print('Path Cost: '+ str(path_cost_2) + ' miles')

    
else:
    print('\nGreedy Best First Search:')
    print('Initial: ' + initial_state + ' | Goal: ' + goal_state + ' | Path : [NOT FOUND]')
    print('Path Cost: N/A miles')
    print('\nA*:')
    print('Initial: ' + initial_state + ' | Goal: ' + goal_state + ' | Path : [NOT FOUND]')
    print('Path Cost: N/A miles\n')