# Description: Creates a grid with the specified dimensions, start position, goals, and walls.

class Grid:
    # Initialize the grid
    def __init__(self, dimensions, start, goals, walls):
        self.rows, self.cols = dimensions
        self.start = start
        self.goals = goals
        self.walls = walls
        self.grid = self.createGrid()

    # Check if position is within grid bounds
    def isValidPosition(self, x, y):
        return 0 <= y < self.rows and 0 <= x < self.cols

    # Create the grid
    def createGrid(self):
        # Initialize empty grid
        grid = [['•' for _ in range(self.cols)] for _ in range(self.rows)]

        # Place walls
        for wx, wy, w, h in self.walls:
            for i in range(h):
                for j in range(w):
                    if self.isValidPosition(wx + j, wy + i):
                        grid[wy + i][wx + j] = '#'

        # Place start position
        sx, sy = self.start
        if self.isValidPosition(sx, sy):
            grid[sy][sx] = 'S'

        # Place goals
        for gx, gy in self.goals:
            if self.isValidPosition(gx, gy):
                grid[gy][gx] = 'G'
        
        return grid

    # Display the grid
    def display(self):
        for row in self.grid:
            print(' '.join(row))