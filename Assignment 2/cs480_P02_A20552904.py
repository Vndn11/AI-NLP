import sys 
import csv
import time
import pandas as pd

################################################################################################################################################################################################
## BRUTE-FORCE ALGORITHM
################################################################################################################################################################################################


def check_board_validity(sudoku):
    for i in range(9):
        if not verify_uniqueness(sudoku[i]):
            return False

        column = [sudoku[row][i] for row in range(9)]
        if not verify_uniqueness(column):
            return False
        
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            subgrid = [sudoku[row][col] for row in range(start_row, start_row + 3)
                                        for col in range(start_col, start_col + 3)]
            if not verify_uniqueness(subgrid):
                return False

    return True

def verify_uniqueness(elements):
    non_zeros = [elem for elem in elements if elem != 0]
    return len(non_zeros) == len(set(non_zeros))

def solve_sudoku_brute_force(sudoku, counter=0):
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:  
                for num in domain_values[(row, col)]:  
                    sudoku[row][col] = num
                    counter += 1  
                    solution_found, attempts, sudoku = solve_sudoku_brute_force(sudoku, counter)
                    if solution_found:
                        return True, attempts, sudoku
                    sudoku[row][col] = 0  
                return False, counter, sudoku  

    
    if check_board_validity(sudoku):
        return True, counter, sudoku
    else:
        return False, counter, sudoku

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

    for x in range(9):
        if int(grid[row][x]) == num:
            return False

    for x in range(9):
        if int(grid[x][col]) == num:
            return False

    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if int(grid[i + start_row][j + start_col]) == num:
                return False
    return True

def solve_sudoku_with_BackTrack(grid, node_count=0):
    unassigned_pos = find_unassigned_location(grid)
    if not unassigned_pos:
        return True, node_count,grid  
    row, col = unassigned_pos

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            next_node_count = node_count + 1  
            success, node_count,_  = solve_sudoku_with_BackTrack(grid, next_node_count)
            if success:
                return True, node_count,grid  

            grid[row][col] = 0  
    return False, node_count,grid  

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
    
    for i in range(9):
        if (row, i) in assignment and assignment[(row, i)] == value or \
           (i, col) in assignment and assignment[(i, col)] == value:
            return False
    
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


def backtrack(assignment, domains,counter=0):
    if len(assignment) == 81:
        return assignment,counter

    var = select_unassigned_variable(assignment, domains)
    if not var:
        return None ,counter 

    for value in domains[var]:
        if is_consistent(value, var, assignment):
            assignment[var] = value
            domains_copy = domains.copy()
            counter+=1
            success, updates = forward_check(value, var, domains)
            if success:
                result,counter = backtrack(assignment, domains,counter)
                if result:
                    return assignment,counter
            del assignment[var]
            domains = domains_copy
            for k, v in updates.items():
                domains[k] = v
    return None ,counter 

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

    def display_and_save_sudoku(sudoku):
        pd.DataFrame(sudoku).to_csv("solution.csv", index=False, header=False)
        for row in sudoku:
            formatted_row = " ".join(str(cell) for cell in row)
            print(formatted_row)

    new_sudoku = [[0 for _ in range(9)] for _ in range(9)]
    sudoku_grid = load_sudoku_from_file(filename)
    domain_values = find_domain(sudoku_grid) 
    T1=time.time()
    
    if mode == "1":
        solution_found, node_val ,sol_sudoku = solve_sudoku_brute_force(new_sudoku, 0)
        T2=time.time()
        if solution_found:
            print("Vaishya Vandan A20552904 solution:")
            print("Input file:", filename)
            print("Algorithm: Brute Force Method")
            print("Input Puzzle: ")
            display_and_save_sudoku(sudoku_grid)
            print("Number of search tree nodes generated: ",node_val)
            print("Search time: ",T2-T1,"seconds")
            print("Solved Puzzle: ")
            display_and_save_sudoku(sol_sudoku)
        else:
            print("No solution exists (Brute Force Method).")


    elif mode == "2":
        solution_found,node_val, sol_sudoku = solve_sudoku_with_BackTrack(new_sudoku)
        T2=time.time()
        if solution_found:
            print("Vaishya Vandan A20552904 solution:")
            print("Input file:", filename)
            print("Algorithm: CSP WITH BACKTRACK SEARCH")
            print("Input Puzzle: ")
            display_and_save_sudoku(sudoku_grid)
            print("Number of search tree nodes generated: ",node_val)
            print("Search time: ",T2-T1,"seconds")
            print("Solved Puzzle: ")
            display_and_save_sudoku(sol_sudoku)
        else:
            print("No solution exists (CSP WITH BACKTRACK SEARCH).")

    elif mode == "3":
        assignment = {}
        domains = initialize_domains(sudoku_grid)
        solution,node_val = backtrack(assignment, domains)
        T2=time.time()
        if solution:
            print("Vaishya Vandan A20552904 solution:")
            print("Input file:", filename)
            print("Algorithm: CSP WITH FORWARD CHECKING AND MRV HEUSRISTICS")
            print("Input Puzzle: ")
            display_and_save_sudoku(sudoku_grid)
            print("Number of search tree nodes generated: ",node_val)
            print("Search time: ",T2-T1,"seconds")
            print("Solved Puzzle: ")
            solved_grid = [[0 for _ in range(9)] for _ in range(9)]
            for (r, c), val in solution.items():
                solved_grid[r][c] = val
            for row in solved_grid:
                print(' '.join(map(str, row)))
        else:
            print("No solution found. CSP WITH FORWARD CHECKING AND MRV HEUSRISTICS")

    elif mode == "4":
        print("Test") 
        if validate_sudoku_solution(sudoku_grid):
            print("This is a valid, solved, Sudoku puzzle.")
        else:
            print("ERROR: This is NOT a solved Sudoku puzzle.")

    else:
        print("Invalid mode. Please choose one of: 1. Brute Force Search 2. Backtracking Search 3. Forward Checking Search 4. Validate Sudoku")
        sys.exit(1)
