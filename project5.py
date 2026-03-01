import random
from collections import deque
from colorama import Fore, Style, init

# initialize colorama
init(autoreset=True)


class Maze:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = [['#' for _ in range(cols)] for _ in range(rows)]


    # Generate random maze using DFS
    def generate(self):

        def dfs(r, c):

            directions = [(0,1), (1,0), (0,-1), (-1,0)]
            random.shuffle(directions)

            for dr, dc in directions:

                nr, nc = r + dr*2, c + dc*2

                if (0 <= nr < self.rows and
                    0 <= nc < self.cols and
                    self.maze[nr][nc] == '#'):

                    self.maze[r+dr][c+dc] = ' '
                    self.maze[nr][nc] = ' '

                    dfs(nr, nc)

        # start position
        self.maze[1][1] = ' '
        dfs(1, 1)

        # mark start and end
        self.maze[1][1] = 'S'
        self.maze[self.rows-2][self.cols-2] = 'E'


    # Solve maze using BFS (shortest path)
    def solve(self):

        start = (1, 1)
        end = (self.rows-2, self.cols-2)

        queue = deque([start])
        visited = set([start])
        parent = {}

        while queue:

            r, c = queue.popleft()

            if (r, c) == end:
                break

            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:

                nr, nc = r + dr, c + dc

                if (0 <= nr < self.rows and
                    0 <= nc < self.cols and
                    self.maze[nr][nc] != '#' and
                    (nr, nc) not in visited):

                    queue.append((nr, nc))
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)

        # reconstruct shortest path
        curr = end

        while curr != start:

            r, c = curr

            if self.maze[r][c] not in ('S', 'E'):
                self.maze[r][c] = '.'

            curr = parent[curr]


    # Display maze with colors
    def display(self):

        for row in self.maze:

            for cell in row:

                if cell == '#':
                    print(Fore.WHITE + "█", end=" ")

                elif cell == 'S':
                    print(Fore.GREEN + "S", end=" ")

                elif cell == 'E':
                    print(Fore.RED + "E", end=" ")

                elif cell == '.':
                    print(Fore.YELLOW + "●", end=" ")

                else:
                    print(" ", end=" ")

            print()


# Main program
print("\n=== Maze Generator & Shortest Path Solver ===\n")

# user input
rows = int(input("Enter number of rows (>=5): "))
cols = int(input("Enter number of cols (>=5): "))

# ensure minimum size
if rows < 5:
    rows = 5

if cols < 5:
    cols = 5

# ensure odd numbers
if rows % 2 == 0:
    rows += 1

if cols % 2 == 0:
    cols += 1

# create maze
maze = Maze(rows, cols)

print("\nGenerating Maze...\n")
maze.generate()

print("Maze:\n")
maze.display()

print("\nSolving Maze (Shortest Path)...\n")
maze.solve()

print("Solved Maze:\n")
maze.display()