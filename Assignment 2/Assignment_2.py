import sys 
import csv
import os 
import copy
import time
import numpy as np
import pandas as pd

################################################################################################################################################################################################
## BRUTE-FORCE ALGORITHM
################################################################################################################################################################################################

def is_board_valid(board):
    for row in range(9):
        if not is_unique(board[row]):
            return False
    for col in range(9):
        if not is_unique([board[row][col] for row in range(9)]):
            return False
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            block = [board[i][j] for i in range(row, row + 3) for j in range(col, col + 3)]
            if not is_unique(block):
                return False
    return True

def is_unique(items):
    items = [item for item in items if item != 0]
    return len(items) == len(set(items))

def solve_sudoku(board, counter=0):
    local_counter = counter 
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:  
                for num in domain_values[i,j]:  
                    board[i][j] = num  
                    local_counter += 1
                    success, new_counter,board = solve_sudoku(board, local_counter)  
                    if success:  
                        return True, new_counter,board
                    board[i][j] = 0  
                return False, local_counter ,board
    if is_board_valid(board):  
        return True, local_counter,board
    return False, local_counter,board

# def create_domain_arrays(board):
#     sudoku_arrays = []

#     for row in board:
#         row_arrays = []
#         for cell in row:
#             if cell != 0:
#                 row_arrays.append([cell])
#             else:
#                 row_arrays.append(list(range(1, 10)))
#         sudoku_arrays.append(row_arrays)

#     return sudoku_arrays

# def solve_sudoku(board, sudoku_initial, counter=0):
#     local_counter = counter

#     for i in range(9):
#         for j in range(9):
#             if board[i][j] == 0:
#                 for num in sudoku_initial[i][j]:
#                     board[i][j] = num
#                     local_counter += 1
#                     success, new_counter = solve_sudoku(board, sudoku_initial, local_counter)
#                     if success:
#                         return True, new_counter
#                     board[i][j] = 0
#                 return False, local_counter

#     if validate_sudoku_solution(board):
#         return True, local_counter
#     return False, local_counter

# def brute_force_search(sudoku):
#     print("Algorithm: Brute Force Search")
#     times = []
#     total_nodes_generated = 0

#     for _ in range(10):  # Run the search 10 times
#         sudoku_initial = create_domain_arrays(sudoku)
#         t1 = time.time()
#         _, nodes_generated = solve_sudoku(copy.deepcopy(sudoku), sudoku_initial)
#         t2 = time.time()

#         total_nodes_generated += nodes_generated
#         times.append(t2 - t1)

#     average_time = np.average(times)
#     average_nodes = total_nodes_generated / 10

#     print(f"Average Time: {average_time} seconds")
#     print(f"Average Nodes: {average_nodes}")



# def create_domain_arrays(board):
#     sudoku_arrays = []

#     for row in board:
#         row_arrays = []
#         for cell in row:
#             if cell != 0:
#                 # For non-zero cells, create an array with just that value
#                 row_arrays.append([cell])
#             else:
#                 # For zero cells, create an array with values 1 to 9
#                 row_arrays.append([i for i in range(1, 10)])
#         sudoku_arrays.append(row_arrays)

#     return sudoku_arrays


# def solve_sudoku(board,sudoku_initial, counter=0):
    
#     local_counter = counter 
#     # print("board\n",board) 
#     for i in range(9):
#         for j in range(9):  
#             if sudoku_grid[i][j] == 0:
#                 for num in sudoku_initial[i][j]:  
#                     board[i][j] = num 
#                     local_counter += 1
#                     success, new_counter = solve_sudoku(board, sudoku_initial,local_counter)  
#                     if success:  
#                         return True, new_counter  
#                     board[i][j] = 0  
#                 return False, local_counter 
#     if validate_sudoku_solution(board):  
#         return True, local_counter
#     return False, local_counter

# def brute_force_search(sudoku):
#     print("Algorithm : brute force search")
#     sudoku_initial=create_domain_arrays(sudoku)

#     for i in range(10):
        
#         times=[]
#         t1=0
#         t1=time.time()
#         success,counter=solve_sudoku(sudoku,sudoku_initial)
#         print(success, counter)
#         # print(sudoku)
#         t2=time.time()
#         print("time required:",t2-t1)
#         times.append(t2-t1)
#     print(times)
#     print("average time:",np.average(times))

################################################################################################################################################################################################
## CSP WITH BACKTRACKING SEARCH
################################################################################################################################################################################################

def find_unassigned_location(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None

def is_safe(grid, row, col, num):
    # Check row
    for x in range(9):
        if int(grid[row][x]) == num:
            return False

    # Check column
    for x in range(9):
        if int(grid[x][col]) == num:
            return False

    # Check 3x3 sub-grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if int(grid[i + start_row][j + start_col]) == num:
                return False
    return True

# def solve_sudoku_with_BackTrack(grid, node_count=0):
#     unassigned_pos = find_unassigned_location(grid)
#     if not unassigned_pos:
#         return True, node_count  # Puzzle solved, return node count
#     row, col = unassigned_pos

#     for num in range(1, 10):
#         if is_safe(grid, row, col, num):
#             grid[row][col] = num
#             next_node_count = node_count + 1  # Increment node count
#             success, total_nodes = solve_sudoku_with_BackTrack(grid, next_node_count)
#             if success:
#                 return True, total_nodes  # Return accumulated node count

#             grid[row][col] = 0  # Undo & try again
#     return False, node_count  # No solution, return current node count


def solve_sudoku_with_BackTrack(grid):
    unassigned_pos = find_unassigned_location(grid)
    if not unassigned_pos:
        return True, grid  # Puzzle solved
    row, col = unassigned_pos

    for num in domain_values[row,col]:
        if is_safe(grid, row, col, num):
            grid[row][col] = num

            if solve_sudoku_with_BackTrack(grid):
                return True, grid

            grid[row][col] = 0  # Undo & try again

    return False, grid

################################################################################################################################################################################################
## CSP WITH FORWARD CHECKING AND MRV HEURISTICS
################################################################################################################################################################################################

def initialize_domains(grid):
    domains = {(r, c): set(range(1, 10)) if grid[r][c] == 0 else {grid[r][c]} for r in range(9) for c in range(9)}
    return domains

def select_unassigned_variable(assignment, domains):
    return min((v for v in domains if v not in assignment), key=lambda var: len(domains[var]), default=None)

def is_consistent(value, var, assignment):
    row, col = var
    # Check row and column
    for i in range(9):
        if (row, i) in assignment and assignment[(row, i)] == value or \
           (i, col) in assignment and assignment[(i, col)] == value:
            return False
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if (start_row + i, start_col + j) in assignment and assignment[(start_row + i, start_col + j)] == value:
                return False
    return True

def forward_check(value, var, domains):
    row, col = var
    updates = {}
    for i in range(9):
        if (row, i) != var and value in domains[(row, i)]:
            if len(domains[(row, i)]) == 1:
                return False, updates
            updates[(row, i)] = domains[(row, i)].copy()
            domains[(row, i)].remove(value)
        if (i, col) != var and value in domains[(i, col)]:
            if len(domains[(i, col)]) == 1:
                return False, updates
            updates[(i, col)] = domains[(i, col)].copy()
            domains[(i, col)].remove(value)
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            cell = (start_row + i, start_col + j)
            if cell != var and value in domains[cell]:
                if len(domains[cell]) == 1:
                    return False, updates
                updates[cell] = domains[cell].copy()
                domains[cell].remove(value)
    return True, updates

# def backtrack(assignment, domains, node_count=0):
#     if len(assignment) == 81:
#         return assignment, node_count  # Solution found, return it along with node count

#     var = select_unassigned_variable(assignment, domains)
#     if not var:
#         return None, node_count  # No solution, return None and the current node count

#     for value in domains[var]:
#         # Each iteration here is considered generating a new node
#         node_count += 1  
#         if is_consistent(value, var, assignment):
#             assignment[var] = value
#             success, updates = forward_check(value, var, domains)
#             if success:
#                 # Recursively call with updated node count
#                 result, result_node_count = backtrack(assignment, domains, node_count)
#                 if result:
#                     return result, result_node_count  # Solution found, return it and the final node count
#             # Undo the assignment and updates if not successful
#             del assignment[var]
#             domains = {k: (updates[k] if k in updates else v) for k, v in domains.items()}

#     return None, node_count


def backtrack(assignment, domains):
    if len(assignment) == 81:
        return assignment

    var = select_unassigned_variable(assignment, domains)
    if not var:
        return None  # Failure

    for value in domains[var]:
        if is_consistent(value, var, assignment):
            assignment[var] = value
            domains_copy = domains.copy()
            success, updates = forward_check(value, var, domains)
            if success:
                result = backtrack(assignment, domains)
                if result:
                    return result
            del assignment[var]
            domains = domains_copy
            for k, v in updates.items():
                domains[k] = v
    return None  # Trigger backtracking

################################################################################################################################################################################################
## VALIDITY CHECK
################################################################################################################################################################################################

def validate_sudoku_solution(board):
    def is_valid_unit(unit):
        non_empty_cells = []
        for cell in unit:
            if cell != '0':
                non_empty_cells.append(cell)
        if len(non_empty_cells) != len(set(non_empty_cells)):
            return False
        return True
    
    for i in range(9):
        if not is_valid_unit(board[i]):
            return False
        
        column_elements = []
        for j in range(9):
            column_elements.append(board[j][i])
        if not is_valid_unit(column_elements):
            return False
        
        row_start, col_start = 3 * (i // 3), 3 * (i % 3)
        subgrid = []
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                subgrid.append(board[r][c])
        if not is_valid_unit(subgrid):
            return False

    return True

################################################################################################################################################################################################
## MAIN FUNCTION
################################################################################################################################################################################################

if __name__ == "__main__":
    # Check for correct command line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <mode> <filename>")
        sys.exit(1)

    mode = sys.argv[1]
    filename = sys.argv[2]

    def find_domain(sudoku):
        domain = {(i, j): [sudoku[i][j]] if sudoku[i][j] != 0 else list(range(1, 10)) 
            for i in range(9) for j in range(9)}
        return domain

    def load_sudoku_from_file(filename):
        grid = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                grid.append([int(cell) if cell != 'X' else 0 for cell in row])
        return grid

    def print_board(board):
        pd.DataFrame(board).to_csv("solution.csv",index=None,header=None)
        for row in board:
            solution=" ".join(str(num) for num in row)

    new_sudoku = [[0 for _ in range(9)] for _ in range(9)]
    sudoku_grid = load_sudoku_from_file(filename)
    domain_values = find_domain(sudoku_grid) 

    

    # Execute based on the provided mode
    if mode == "1":
        solution_found, _ ,sol_sudoku = solve_sudoku(new_sudoku, 0)
        
        if solution_found:
            print("Vaishya Vandan A20552904 solution:")
            print("Input file:", filename)
            print("Algorithm: Brute Force Method")
            print("Input Puzzle: ")
            print(sudoku_grid)
            print("Number of search tree nodes generated: ")
            print("Search time: ")
            print("Solved Puzzle: ")
            print_board(sol_sudoku)
        else:
            print("No solution exists (Brute Force Method).")


    elif mode == "2":
        solution_found, sol_sudoku = solve_sudoku_with_BackTrack(new_sudoku)
        
        if solution_found:
            print("Vaishya Vandan A20552904 solution:")
            print("Input file:", filename)
            print("Algorithm: CSP WITH BACKTRACK SEARCH")
            print("Input Puzzle: ")
            print(sudoku_grid)
            print("Number of search tree nodes generated: ")
            print("Search time: ")
            print("Solved Puzzle: ")
            print_board(sol_sudoku)
        else:
            print("No solution exists (CSP WITH BACKTRACK SEARCH).")

    elif mode == "3":
        assignment = {}
        domains = initialize_domains(sudoku_grid)
        solution = backtrack(assignment, domains)

        if solution:
            print("Vaishya Vandan A20552904 solution:")
            print("Input file:", filename)
            print("Algorithm: CSP WITH FORWARD CHECKING AND MRV HEUSRISTICS")
            print("Input Puzzle: ")
            print(sudoku_grid)
            print("Number of search tree nodes generated: ")
            print("Search time: ")
            print("Solved Puzzle: ")
            solved_grid = [[0 for _ in range(9)] for _ in range(9)]
            for (r, c), val in solution.items():
                solved_grid[r][c] = val
            for row in solved_grid:
                print(' '.join(map(str, row)))
        else:
            print("No solution found. CSP WITH FORWARD CHECKING AND MRV HEUSRISTICS ")

    elif mode == "4":
        print("Test") 
        if validate_sudoku_solution(sudoku_grid):
            print("This is a valid, solved, Sudoku puzzle.")
        else:
            print("ERROR: This is NOT a solved Sudoku puzzle.")

    else:
        print("Invalid mode. Please choose one of: 1. Brute Force Search 2. Backtracking Search 3. Forward Checking Search 4. Validate Sudoku")
        sys.exit(1)



# def benchmark_algorithm(algorithm, original_grid, iterations=10):
#     total_time = 0
#     total_nodes = 0
#     for _ in range(iterations):
#         grid = copy.deepcopy(original_grid)
#         start_time = time.perf_counter()
#         _, node_count = algorithm(grid)  # Capture node count
#         total_time += time.perf_counter() - start_time
#         total_nodes += node_count

#     average_time = total_time / iterations
#     average_nodes = total_nodes / iterations
#     return average_time, average_nodes


# def benchmark_algorithm(algorithm, grid, iterations=10):
#     total_time = 0
#     total_nodes = 0
#     for _ in range(iterations):
#         start_time = time.perf_counter()
#         grid_copy = copy.deepcopy(grid)  # Ensure a fresh grid for each iteration
#         assignment = {k: v.pop() for k, v in initialize_domains(grid_copy).items() if len(v) == 1}
#         domains = initialize_domains(grid_copy)
#         _, node_count = algorithm(assignment, domains, 0)
#         total_time += time.perf_counter() - start_time
#         total_nodes += node_count

#     average_time = total_time / iterations
#     average_nodes = total_nodes / iterations
#     return average_time, average_nodes


# def load_sudoku_from_file(filename):
#     grid = []
#     with open(filename, 'r') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             grid.append([int(cell) if cell != 'X' else 0 for cell in row])
#     return grid


# filename = input('Enter File Name: ')
# new_sudoku = [[0 for _ in range(9)] for _ in range(9)]
# sudoku_grid = load_sudoku_from_file(filename)
# domain_values=find_domain(sudoku_grid) 
# solution_found, final_counter,sol_sudoku = solve_sudoku(new_sudoku, 0)
# T1 = time.time()

# if solution_found:
#         T2 = time.time()
#         print("Time:", T2 - T1,"seconds")
#         print("Number of nodes generated:", final_counter)
#         print("Solved puzzle:")
#         print_board(sol_sudoku)
# else:
#     T2 = time.time()
#     print("Time:", T2 - T1,"seconds")
#     print("Number of nodes generated:", final_counter)
#     print("No solution exists (Brute Force Method).")
# brute_force_search(sudoku_grid)

# sudoku_grid = []
# with open(filename, 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         sudoku_grid.append([int(cell.replace('X', '0')) for cell in row])


# assignment = {}
# domains = initialize_domains(sudoku_grid)
# solution = backtrack(assignment, domains)


# average_time, average_nodes = benchmark_algorithm(backtrack, sudoku_grid)
# print(f"Average Time: {average_time} seconds, Average Nodes: {average_nodes}")

# average_time_backtrack = benchmark_algorithm(solve_sudoku_with_BackTrack, sudoku_grid)
# print(f"CSP Backtracking Average Time: {average_time_backtrack} seconds")

# def find_domain(sudoku):
#     domain = {(i, j): [sudoku[i][j]] if sudoku[i][j] != 0 else list(range(1, 10)) 
#         for i in range(9) for j in range(9)}
#     return domain

# domain_values = find_domain(sudoku_grid)
# def print_board(board):
#     pd.DataFrame(board).to_csv("solution.csv",index=None,header=None)
#     for row in board:
#         solution = " ".join(str(num) for num in row)     

# solution_found, sol_sudoku = solve_sudoku_with_BackTrack(new_sudoku)
# if solution_found:
#     print(sol_sudoku)
# else:
#     print("No solution exists (CSP WITH BACKTRACK SEARCH).")
