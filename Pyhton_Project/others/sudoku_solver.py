 
def sudoku_grid():
  sudoku_grid_line_one =  []
  sudoku_grid_line_two =  []
  sudoku_grid_line_three =  []
  sudoku_grid_line_four =  []
  sudoku_grid_line_five =  []
  sudoku_grid_line_six =  []
  sudoku_grid_line_seven =  []
  sudoku_grid_line_eight =  []
  sudoku_grid_line_nine =  []
  print("Welcome to the Sudoku Solver Program!")
  print("Enter the Sudoku grid row by row. Use '0' for empty cells.")
  for line_num in range(1, 10):
    print(f"Enter the {line_num} line of the sudoku grid (9 numbers separated by spaces):")
    line = input().split()
    if len(line) != 9:
      print("Invalid input. Please enter exactly 9 numbers separated by spaces.")
      return sudoku_grid() 
    try:
      line = [int(num) for num in line]
    except ValueError:
      print("Invalid input. Please enter numbers only.")
      return sudoku_grid()
    if line_num == 1:
      sudoku_grid_line_one = line
    elif line_num == 2:
      sudoku_grid_line_two = line
    elif line_num == 3:
      sudoku_grid_line_three = line
    elif line_num == 4:
      sudoku_grid_line_four = line
    elif line_num == 5:
      sudoku_grid_line_five = line
    elif line_num == 6:
      sudoku_grid_line_six = line
    elif line_num == 7:
      sudoku_grid_line_seven = line
    elif line_num == 8:
      sudoku_grid_line_eight = line
    elif line_num == 9:
      sudoku_grid_line_nine = line
  all_lines = sudoku_grid_line_one + sudoku_grid_line_two + sudoku_grid_line_three + sudoku_grid_line_four + sudoku_grid_line_five + sudoku_grid_line_six + sudoku_grid_line_seven + sudoku_grid_line_eight + sudoku_grid_line_nine
  all_cells = sudoku_grid_line_one, sudoku_grid_line_two, sudoku_grid_line_three, sudoku_grid_line_four, sudoku_grid_line_five, sudoku_grid_line_six, sudoku_grid_line_seven, sudoku_grid_line_eight, sudoku_grid_line_nine
  if len(all_lines) != 81:
    return sudoku_grid()
  def print_sudoku_grid(grid):
    print("\n" + "="*25)
    for i in range(9):
      formatted_line = ""
      for j in range(9):
        if j % 3 == 0 and j > 0:
          formatted_line += "| "
        formatted_line += str(grid[i][j]) + " "
      print("| " + formatted_line + "|")
      if (i + 1) % 3 == 0 and i < 8:
        print("|" + "-"*7 + "+" + "-"*7 + "+" + "-"*7 + "|")
    print("="*25)

  grid = [sudoku_grid_line_one, sudoku_grid_line_two, sudoku_grid_line_three, sudoku_grid_line_four, sudoku_grid_line_five, sudoku_grid_line_six, sudoku_grid_line_seven, sudoku_grid_line_eight, sudoku_grid_line_nine]
  print_sudoku_grid(grid)
  return all_cells

def sudokusolver(all_cells):
  def find_empty_location(arr, l):
    for row in range(9):
      for col in range(9): 
        if(arr[row][col]== 0):
          l[0]= row
          l[1]= col
          return True
    return False
  
  def used_in_row(arr, row, num):
    for i in range(9):
      if(arr[row][i] == num):
        return True
    return False
  
  def used_in_col(arr, col, num):
      for i in range(9):
        if(arr[i][col] == num):
          return True
      return False
  
  def used_in_box(arr, row, col, num):
      for i in range(3):
        for j in range(3):
          if(arr[i + row][j + col] == num):
            return True
      return False
  
  def check_location_is_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3, col - col % 3, num)
  
  def solve_sudoku(arr):
    l = [0, 0]
    if not find_empty_location(arr, l):
      return True
    row = l[0]
    col = l[1]
    for num in range(1, 10):
      if check_location_is_safe(arr, row, col, num):
        arr[row][col] = num
        if solve_sudoku(arr):
          return True
        arr[row][col] = 0
    return False
  grid = [list(row) for row in all_cells]
  
  if solve_sudoku(grid):
    print("\nSolved Sudoku:")
    print("="*25)
    for i in range(9):
      formatted_line = ""
      for j in range(9):
        if j % 3 == 0 and j > 0:
          formatted_line += "| "
        formatted_line += str(grid[i][j]) + " "
      print("| " + formatted_line + "|")
      if (i + 1) % 3 == 0 and i < 8:
        print("|" + "-"*7 + "+" + "-"*7 + "+" + "-"*7 + "|")
    print("="*25)
  else:
    print("No solution exists for this Sudoku puzzle.")

all_cells = sudoku_grid()
approved = input("Is this the sudoku grid you want to solve? (Yes/No) :")
while approved.lower() != "yes":
  print("Please re-enter the sudoku grid.")
  all_cells = sudoku_grid()
  approved = input("Is this the sudoku grid you want to solve? (Yes/No) :")
sudokusolver(all_cells)
print("Thank you for using the Sudoku Solver Program!")