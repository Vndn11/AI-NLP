import sys
import csv
import time
from queue import PriorityQueue


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




def csv_to_dict(goal_state):

    driving_dist_dict = {}

    with open('driving.csv','r') as drivingcsvfile:
        reader = csv.reader(drivingcsvfile)

        headers = next(reader)[1:]

        for row in reader:
            origin_state = row[0]
            for i, distance in enumerate(row[1:]):
                if float(distance) != -1.0:
                    distance = float(distance)
                    destination_state = headers[i]
                    driving_dist_dict[(origin_state,destination_state)] = distance
    

    straightline_dist_dict = {}

    with open('straightline.csv','r') as straightlinecsvfile:
        reader = csv.reader(straightlinecsvfile)
        headers = next(reader)[1:]
        goal_state_index = headers.index(goal_state)
        for row in reader:
            origin_state = row[0]
            for row in reader:
                node = row[0]
                distance_heuristics = float(row[goal_state_index + 1])
                straightline_dist_dict[node] = distance_heuristics

    return driving_dist_dict, straightline_dist_dict

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.cost < other.cost

class Problem:
    def __init__(self, initial, goal, driving_distances, straight_line_distances):
        self.initial = initial
        self.goal = goal
        self.driving_distances = driving_distances
        self.straight_line_distances = straight_line_distances

    def actions(self, state):
        return [s for s in self.driving_distances if state in s]
    
    def result(self, state, action):
        return action[0] if action[1] == state else action[1]
    
    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, state1, state2):
        return self.driving_distances.get((state1,state2),self.driving_distances.get((state2,state1),float('inf')))

    def heuristic(self, state):
        # return self.straight_line_distances.get(state, float('inf'))
        return self.straight_line_distances[state]



def greedy_best_first_search(problem):
    start_time = time.time()
    expanded_nodes = 0

    initial_node = Node(problem.initial, heuristic=problem.heuristic(problem.initial))
    frontier = PriorityQueue()
    frontier.put((0,initial_node))
    # frontier.put((0, problem.initial))


    best_costs = {}
    explored = set()
    while not frontier.empty():
        _,current_node = frontier.get()
        


        if problem.goal_test(current_node.state):
            end_time = time.time()
            path = reconstruct_path(current_node)
            return path, expanded_nodes,len(path) - 1,end_time - start_time,current_node.cost
        
        explored.add(current_node.state)
        
        expanded_nodes += 1
        
        for action in problem.actions(current_node.state):
            child_state = problem.result(current_node.state, action)
            child_heuristic = problem.heuristic(child_state)
            child_cost = current_node.cost + problem.path_cost(current_node.state, child_state)
            if child_state not in explored or child_heuristic < best_costs.get(child_state, float('inf')):
                
                child_node = Node(child_state, current_node, action, child_cost, child_heuristic)
                best_costs[child_state] = child_heuristic
                frontier.put((child_heuristic,child_node))
    return None

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path


initial_state = input('Enter the Initial State: ').upper()

goal_state = input('Enter the Goal State: ').upper()


# cmdline_arguments = len(sys.argv)

# first_arg = sys.argv[0]
# initial_state = sys.argv[1].upper()
# goal_state = sys.argv[2].upper()

# print('\nScript name:', first_arg)
# print('\nINITIAL STATE:', goal_state)
# print('\nGOAL STATE:', initial_state)

state_flag = check_initial_goal_state(initial_state,goal_state)

if state_flag == 1:

    driving_dist_dict, straightline_dist_dict = csv_to_dict(goal_state)
    problem = Problem(initial_state, goal_state, driving_dist_dict,straightline_dist_dict)
    solution_path_1,expanded_nodes_1,no_of_stops_1,execution_time_1,path_cost_1  = greedy_best_first_search(problem)

    print('\nGreedy Best First Search:')
    print('Initial: ' + initial_state + ' | Goal: ' + goal_state + ' | Path : ' + str(solution_path_1) + '')
    print('Number of nodes Expandes: ' + str(expanded_nodes_1))
    print('Number of stops made: ' + str(no_of_stops_1))
    print('Execution Time: ' + str(execution_time_1))
    print('Path Cost: '+ str(path_cost_1) + ' miles')
    
    print('\nA*:')
    print('Initial: ' + initial_state + ' | Goal: ' + goal_state + ' | Path : [NOT FOUND]')
    print('Path Cost: N/A miles\n')

else:
    print('\nGreedy Best First Search:')
    print('Initial: ' + initial_state + ' | Goal: ' + goal_state + ' | Path : [NOT FOUND]')
    print('Path Cost: N/A miles')
    print('\nA*:')
    print('Initial: ' + initial_state + ' | Goal: ' + goal_state + ' | Path : [NOT FOUND]')
    print('Path Cost: N/A miles\n')