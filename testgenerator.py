import random
import os
from collections import deque
from grid import Grid
from fileRead import FileRead

class TestGenerator:
    def __init__(self):
        self.test_cases_dir = 'test_cases'
        if not os.path.exists(self.test_cases_dir):
            os.makedirs(self.test_cases_dir)

    def createTestFile(self, filename, content):
        # Create a test file with given content
        filepath = os.path.join(self.test_cases_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def generateRandomMaze(self, rows, cols, difficulty='medium'):
        # Generate a random maze with guaranteed path using recursive backtracking
        max_attempts = 10
        for attempt in range(max_attempts):
            # Initialize grid with all walls
            grid = [[1 for _ in range(cols)] for _ in range(rows)]
            
            # Set start position
            start = (0, 0)
            grid[0][0] = 0

            # Generate the main maze structure
            self._generateMazePaths(grid, 0, 0)
            
            # Find a valid distant goal and verify path exists
            min_distance = self._getMinRequiredDistance(rows, cols, difficulty)
            goal = self._findValidDistantGoal(grid, start, min_distance)
            
            if not goal:
                continue  # Try again if no valid goal found

            # Add random walls based on difficulty while maintaining path
            if difficulty == 'medium':
                self._addRandomWalls(grid, start, goal, density=0.15)
            elif difficulty == 'hard':
                self._addRandomWalls(grid, start, goal, density=0.25)
            elif difficulty == 'extreme':
                self._addRandomWalls(grid, start, goal, density=0.35)
                # For extreme difficulty, might block the path
                if random.random() < 0.3:  # 30% chance to make it potentially unsolvable
                    self._addRandomWalls(grid, start, goal, density=0.2, maintain_path=False)

            # Verify path exists (except for extreme difficulty)
            if difficulty != 'extreme' and not self._pathExists(grid, start, goal):
                continue

            # Convert grid to wall format
            walls = self._convertToWalls(grid)
            return start, goal, walls

        # If all attempts fail, create a simple maze with guaranteed path
        return self._createSimpleMaze(rows, cols, difficulty)

    def _getMinRequiredDistance(self, rows, cols, difficulty):
        # Calculate minimum required distance based on maze size and difficulty
        base_distance = (rows + cols) // 4  # Base minimum distance
        
        if difficulty == 'medium':
            return base_distance
        elif difficulty == 'hard':
            return base_distance * 1.5
        else:  # extreme
            return base_distance * 2

    def _generateMazePaths(self, grid, x, y):
        # Generate maze paths using recursive backtracking
        rows, cols = len(grid), len(grid[0])
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < cols and 0 <= new_y < rows and 
                grid[new_y][new_x] == 1):
                
                # Clear path cells
                grid[new_y][new_x] = 0
                grid[y + dy//2][x + dx//2] = 0
                
                self._generateMazePaths(grid, new_x, new_y)

    def _findValidDistantGoal(self, grid, start, min_distance):
        # Find a valid goal point that's sufficiently far from start
        rows, cols = len(grid), len(grid[0])
        distances = {}
        queue = deque([(start, 0)])
        distances[start] = 0
        valid_goals = []

        while queue:
            pos, dist = queue.popleft()
            x, y = pos

            # If point is far enough, consider it as potential goal
            if dist >= min_distance:
                valid_goals.append((pos, dist))

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                new_pos = (new_x, new_y)
                
                if (0 <= new_x < cols and 0 <= new_y < rows and 
                    grid[new_y][new_x] == 0 and 
                    new_pos not in distances):
                    
                    distances[new_pos] = dist + 1
                    queue.append((new_pos, dist + 1))

        # Sort valid goals by distance and prefer corners/edges
        if valid_goals:
            valid_goals.sort(key=lambda x: (
                -x[1],  # Prefer more distant points
                -(x[0][0] == 0 or x[0][0] == cols-1),  # Prefer edges
                -(x[0][1] == 0 or x[0][1] == rows-1)   # Prefer edges
            ))
            return valid_goals[0][0]
        return None

    def _addRandomWalls(self, grid, start, goal, density, maintain_path=True):
        # Add random walls while optionally maintaining path
        rows, cols = len(grid), len(grid[0])
        num_walls = int(rows * cols * density)
        added_walls = 0
        max_attempts = num_walls * 3

        for _ in range(max_attempts):
            if added_walls >= num_walls:
                break

            x = random.randint(1, cols-2)
            y = random.randint(1, rows-2)
            
            # Don't block start or goal
            if (x, y) in [start, goal]:
                continue

            # Save current state
            original_value = grid[y][x]
            if grid[y][x] == 0:
                grid[y][x] = 1
                
                # If we need to maintain path and it's broken, revert
                if maintain_path and not self._pathExists(grid, start, goal):
                    grid[y][x] = original_value
                else:
                    added_walls += 1

    def _pathExists(self, grid, start, goal):
        # Check if a path exists between start and goal
        rows, cols = len(grid), len(grid[0])
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                return True

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                new_pos = (new_x, new_y)
                
                if (0 <= new_x < cols and 0 <= new_y < rows and 
                    grid[new_y][new_x] == 0 and 
                    new_pos not in visited):
                    visited.add(new_pos)
                    queue.append(new_pos)

        return False

    def _createSimpleMaze(self, rows, cols, difficulty):
        # Create a simple maze with guaranteed path as fallback
        grid = [[0 for _ in range(cols)] for _ in range(rows)]
        start = (0, 0)
        goal = (cols-1, rows-1)

        # Add some random walls while ensuring path exists
        if difficulty == 'medium':
            wall_density = 0.1
        elif difficulty == 'hard':
            wall_density = 0.2
        else:  # extreme
            wall_density = 0.3

        self._addRandomWalls(grid, start, goal, wall_density, maintain_path=True)
        walls = self._convertToWalls(grid)
        return start, goal, walls

    def _convertToWalls(self, grid):
        # Convert grid representation to wall list representation
        rows, cols = len(grid), len(grid[0])
        walls = []
        visited = set()

        for y in range(rows):
            for x in range(cols):
                if grid[y][x] == 1 and (x, y) not in visited:
                    # Find connected wall region
                    width = 1
                    height = 1
                    
                    # Extend width
                    while (x + width < cols and 
                            grid[y][x + width] == 1 and 
                            all(grid[y + h][x + width] == 1 
                                for h in range(height))):
                        width += 1
                    
                    # Extend height
                    while (y + height < rows and 
                            all(grid[y + height][x + w] == 1 
                                for w in range(width))):
                        height += 1

                    # Mark all cells in this wall as visited
                    for h in range(height):
                        for w in range(width):
                            visited.add((x + w, y + h))

                    walls.append([x, y, width, height])

        return walls

    def generateHardcodedTests(self):
        # Generate the original 5 hardcoded test cases
        test_files = {
            'test1.txt': "[5,5]\n[0,0]\n[4,4]\n",  # Simple straight line
            'test2.txt': "[8,8]\n[0,0]\n[5,7]|[7,2]\n[1,1,2,2]\n[5,1,2,2]\n[1,5,2,2]",  # Multiple goals
            'test3.txt': "[4,4]\n[0,0]\n[3,3]\n[1,1,3,2]\n[0,3,4,1]",  # No solution
            'test4.txt': "[7,7]\n[0,0]\n[6,6]\n[2,0,1,5]\n[4,2,1,5]",  # Narrow passage
            'test5.txt': "[10,10]\n[0,0]\n[9,9]\n[2,2,2,2]\n[6,2,2,2]\n[2,6,2,2]\n[6,6,2,2]\n[4,4,2,2]\n[0,4,1,2]\n[9,4,1,2]"  # Complex maze
        }

        for name, content in test_files.items():
            self.createTestFile(name, content)

    def generateAllTests(self):
        # Generate all test cases
        # Generate tests 1-5 (hardcoded)
        self.generateHardcodedTests()

        # Generate tests 6-12 (medium and hard random mazes)
        random_configs = [
            ('test6.txt', 15, 15, 'medium'),
            ('test7.txt', 15, 15, 'medium'),
            ('test8.txt', 20, 20, 'medium'),
            ('test9.txt', 20, 20, 'hard'),
            ('test10.txt', 25, 25, 'hard'),
            ('test11.txt', 25, 25, 'hard'),
            ('test12.txt', 30, 30, 'hard')
        ]

        for filename, rows, cols, difficulty in random_configs:
            start, goal, walls = self.generateRandomMaze(rows, cols, difficulty)
            content = (f"[{rows},{cols}]\n"
                        f"[{start[0]},{start[1]}]\n"
                        f"[{goal[0]},{goal[1]}]\n" + 
                        '\n'.join(f"[{w[0]},{w[1]},{w[2]},{w[3]}]" for w in walls))
            self.createTestFile(filename, content)

        # Generate tests 13-14 (extreme difficulty)
        extreme_configs = [
            ('test13.txt', 35, 35, 'extreme'),
            ('test14.txt', 50, 50, 'extreme')
        ]

        for filename, rows, cols, difficulty in extreme_configs:
            start, goal, walls = self.generateRandomMaze(rows, cols, difficulty)
            content = (f"[{rows},{cols}]\n"
                        f"[{start[0]},{start[1]}]\n"
                        f"[{goal[0]},{goal[1]}]\n" + 
                        '\n'.join(f"[{w[0]},{w[1]},{w[2]},{w[3]}]" for w in walls))
            self.createTestFile(filename, content)

    def runTestSuite(self):
        # Generate and run all test cases
        print("Generating test cases...")
        self.generateAllTests()
        
        print("\nTest cases generated successfully in the 'test_cases' directory.")
        print("\nTest suite summary:")
        print("1. Hardcoded Tests (Tests 1-5):")
        print("   - Test 1: Simple path test")
        print("   - Test 2: Multiple goals test")
        print("   - Test 3: No solution test")
        print("   - Test 4: Narrow passage test")
        print("   - Test 5: Complex maze test")
        print("\n2. Random Tests (Tests 6-12):")
        print("   - Tests 6-8: Medium difficulty (15x15, 20x20)")
        print("   - Tests 9-12: Hard difficulty (20x20, 25x25, 30x30)")
        print("\n3. Extreme Tests (Tests 13-14):")
        print("   - Test 13: 35x35 extreme maze (might be solvable)")
        print("   - Test 14: 40x40 extreme maze (might be unsolvable)")