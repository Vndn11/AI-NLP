import csv

initial_state = 'MA'
goal_state = 'MD'



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


heuristics = input('Enter the state for heuristics: ')
Driving_dist_start = input('Enter the state for starting driving distance: ')
Driving_dist_end = input('Enter the state for ending driving distance: ')


print('heuristics: ' , straightline_dist_dict[heuristics])

print('Driving Distances: ',driving_dist_dict[(Driving_dist_start,Driving_dist_end)])