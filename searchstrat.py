# Description: This file contains the search algorithms.
import heapq
from collections import deque

# Parent class for search algorithms holding common functions and variables
class Search:
    # Initialize the search algorithm
    def __init__(self, grid):
        self.grid = grid
        self.visited = set()
        self.nodes_explored = 0
        self.visited_order = []
        self.start = self.grid.start
        self.goals = set(self.grid.goals)
        self.directions = [(0, -1), (-1, 0), (0, 1), (1, 0)] # Direction priority: up, left, down, right

    # Check if position is within bounds, unvisited, and not a wall
    def isValidMove(self, x, y):
        
        return (0 <= x < self.grid.cols and 
                0 <= y < self.grid.rows and 
                (x, y) not in self.visited and 
                self.grid.grid[y][x] != '#')

    # Mark the final path on grid
    def markFinalPath(self, path):
        for x, y in path:
            if self.grid.grid[y][x] == 'V':
                self.grid.grid[y][x] = 'P'
            elif (x, y) in self.grid.goals:
                self.grid.grid[y][x] = 'G'

    # Mark visited position on grid
    def markVisited(self, x, y):
        if self.grid.grid[y][x] == '•':
            self.grid.grid[y][x] = 'V'

    # Check if current position is a goal
    def isGoal(self, position):
        return position in self.goals

    # Get valid neighbors of current position
    def getNeighbors(self, x, y, path):
        valid_neighbors = []
        for dx, dy in self.directions:
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            
            if self.isValidMove(next_x, next_y):
                valid_neighbors.append((next_pos, path + [(x, y)]))
        return valid_neighbors

    # Calculate Manhattan distance between current position and goal
    def calculateHeuristic(self, current, goal):
        
        x1, y1 = current
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    # Find minimum Manhattan distance to any goal
    def getMinHeuristic(self, pos):
        return min(self.calculateHeuristic(pos, goal) for goal in self.goals)


# Search algorithms
# Breadth-first search
class BreadthFirstSearch(Search):
    def bfsPath(self):
        # Initialize queue with start position and empty path
        queue = deque([(self.start, [])])
        self.visited.add(self.start)
        self.visited_order.append(self.start)

        while queue:
            # Get next position and path from front of queue
            (x, y), path = queue.popleft()
            self.nodes_explored += 1
            self.markVisited(x, y)

            # Check if current position is a goal
            if self.isGoal((x, y)):
                self.markFinalPath(path + [(x, y)])
                return True, path + [(x, y)]

            # Get valid neighbors and add to queue
            neighbors = self.getNeighbors(x, y, path)
            for next_pos, new_path in neighbors:
                self.visited.add(next_pos)
                self.visited_order.append(next_pos)
                queue.append((next_pos, new_path))

        # No path found
        return False, []


# Depth-first search
class DepthFirstSearch(Search):
    def dfsPath(self):
        # Initialize stack with start position and initial path
        stack = [(self.start, [self.start])]
        self.visited = set()
        self.visited_order = []

        while stack:
            # Get position and path from top of stack
            (x, y), path = stack.pop()
            
            # Process unvisited positions
            if (x, y) not in self.visited:
                self.nodes_explored += 1
                self.markVisited(x, y)
                self.visited.add((x, y))
                self.visited_order.append((x, y))

                # Check if current position is goal
                if self.isGoal((x, y)):
                    self.markFinalPath(path)
                    return True, path

                # Check neighbors in reverse direction order
                for dx, dy in reversed(self.directions):
                    next_x, next_y = x + dx, y + dy
                    next_pos = (next_x, next_y)

                    # Add valid neighbors to stack
                    if (0 <= next_x < self.grid.cols and 
                        0 <= next_y < self.grid.rows and 
                        next_pos not in self.visited and 
                        self.grid.grid[next_y][next_x] != '#'):

                        stack.append((next_pos, path + [next_pos]))

        # No path found
        return False, []


# A* search
class AStarSearch(Search):
    def astarPath(self):
        # Initialize priority queue with start state
        start_h = self.getMinHeuristic(self.start)
        pq = [(start_h, 0, self.start, [])]  # (f_score, nodes_explored, position, path)
        g_scores = {self.start: 0}  # Track cost to reach each node
        
        self.visited.add(self.start)
        self.visited_order.append(self.start)

        while pq:
            # Get node with lowest f_score from priority queue
            f, _, (x, y), path = heapq.heappop(pq)
            current_g = g_scores[(x, y)]  # Current path cost
            
            self.nodes_explored += 1
            self.markVisited(x, y)

            # Check if current node is goal
            if self.isGoal((x, y)):
                self.markFinalPath(path + [(x, y)])
                return True, path + [(x, y)]

            # Check all neighboring positions
            for dx, dy in self.directions:
                next_x, next_y = x + dx, y + dy
                next_pos = (next_x, next_y)
                
                if self.isValidMove(next_x, next_y):
                    new_g = current_g + 1  # Cost to reach neighbor
                    
                    # Update if new path is better
                    if next_pos not in g_scores or new_g < g_scores[next_pos]:
                        g_scores[next_pos] = new_g
                        h = self.getMinHeuristic(next_pos)
                        f = new_g + h  # Calculate f_score
                        
                        self.visited.add(next_pos)
                        self.visited_order.append(next_pos)
                        
                        heapq.heappush(pq, (f, self.nodes_explored, next_pos, path + [(x, y)]))

        # No path found
        return False, []


# Greedy best-first search
class GreedyBestFirstSearch(Search):
    def gbfsPath(self):
        # Initialize priority queue with start state using heuristic
        pq = [(self.getMinHeuristic(self.start), 0, self.start, [])]  # (heuristic, nodes_explored, position, path)
        
        self.visited.add(self.start)
        self.visited_order.append(self.start)

        while pq:
            # Get node with lowest heuristic value from queue
            h, _, (x, y), path = heapq.heappop(pq)
            
            self.nodes_explored += 1
            self.markVisited(x, y)

            # Check if current node is goal
            if self.isGoal((x, y)):
                self.markFinalPath(path + [(x, y)])
                return True, path + [(x, y)]

            # Check all neighboring positions
            for dx, dy in self.directions:
                next_x, next_y = x + dx, y + dy
                next_pos = (next_x, next_y)
                
                if self.isValidMove(next_x, next_y):
                    # Calculate heuristic for neighbor
                    h = self.getMinHeuristic(next_pos)
                    
                    self.visited.add(next_pos)
                    self.visited_order.append(next_pos)
                    
                    heapq.heappush(pq, (h, self.nodes_explored, next_pos, path + [(x, y)]))

        # No path found
        return False, []


#Custom Searches
# Bidirectional BFS search 
class BidirectionalSearch(BreadthFirstSearch):
    def __init__(self, grid):
        # Initialize using parent BFS class constructor
        super().__init__(grid)
        
    def bdsPath(self):
        # Initialize queues and visited dictionaries for both directions
        forward_queue = deque([(self.start, [])])  # Starts from beginning
        backward_queue = deque([(next(iter(self.goals)), [])])  # Starts from goal
        forward_visited = {self.start: [self.start]}  # Track forward paths
        backward_visited = {next(iter(self.goals)): [next(iter(self.goals))]}  # Track backward paths
        
        self.visited_order = [self.start]
        
        while forward_queue and backward_queue:
            # Forward search from start
            current_f, path_f = forward_queue.popleft()
            self.nodes_explored += 1
            self.markVisited(*current_f)
            
            # Process neighbors in forward direction
            for next_pos, new_path in self.getNeighbors(*current_f, path_f):
                if next_pos not in forward_visited:
                    # Update path and visited info
                    current_path = path_f + [current_f]
                    forward_visited[next_pos] = current_path + [next_pos]
                    forward_queue.append((next_pos, current_path))
                    self.visited_order.append(next_pos)
                    
                # Check if paths meet
                if next_pos in backward_visited:
                    intersection = next_pos
                    # Mark intersection point with X
                    self.grid.grid[intersection[1]][intersection[0]] = 'X'
                    # Get forward path to intersection
                    forward_path = forward_visited[next_pos]
                    # Get backward path from intersection to goal and reverse it
                    backward_path = backward_visited[next_pos][::-1]
                    # Combine paths: forward_path + backward_path[1:] to avoid duplicate intersection
                    complete_path = forward_path + backward_path[1:]
                    self.markFinalPath(complete_path)
                    return True, complete_path
            
            # Backward search from goal
            current_b, path_b = backward_queue.popleft()
            self.nodes_explored += 1
            self.markVisited(*current_b)
            
            # Process neighbors in backward direction
            for next_pos, new_path in self.getNeighbors(*current_b, path_b):
                if next_pos not in backward_visited:
                    # Update path and visited info
                    current_path = path_b + [current_b]
                    backward_visited[next_pos] = current_path + [next_pos]
                    backward_queue.append((next_pos, current_path))
                    self.visited_order.append(next_pos)
                    
                # Check if paths meet
                if next_pos in forward_visited:
                    intersection = next_pos
                    # Mark intersection point with X
                    self.grid.grid[intersection[1]][intersection[0]] = 'X'
                    # Get forward path to intersection
                    forward_path = forward_visited[next_pos]
                    # Get backward path from intersection to goal and reverse it
                    backward_path = backward_visited[next_pos][::-1]
                    # Combine paths: forward_path + backward_path[1:] to avoid duplicate intersection
                    complete_path = forward_path + backward_path[1:]
                    self.markFinalPath(complete_path)
                    return True, complete_path
        
        # No path found
        return False, []


# Beam search
class BeamSearch(Search):
    def __init__(self, grid, beam_width=2):
        super().__init__(grid)
        self.beam_width = beam_width

    def beamPath(self):
        # Initialize beam with start node
        start_h = self.getMinHeuristic(self.start)
        current_beam = [(start_h, 0, self.start, [])]  # (f_value, g_value, position, path)
        self.visited.add(self.start)
        self.visited_order.append(self.start)

        while current_beam:
            next_candidates = []
            
            # Process current beam
            for f_val, g_val, (x, y), path in current_beam:
                self.nodes_explored += 1
                self.markVisited(x, y)
                
                # Check if current position is goal
                if self.isGoal((x, y)):
                    self.markFinalPath(path + [(x, y)])
                    return True, path + [(x, y)]

                for next_pos, new_path in self.getNeighbors(x, y, path):
                    # Calculate new costs
                    new_g = g_val + 1
                    h_value = self.getMinHeuristic(next_pos)
                    f_value = new_g + h_value * 1.1  # Slight weight on heuristic
                    
                    next_candidates.append((f_value, new_g, next_pos, new_path))

            if not next_candidates:
                break

            # Remove duplicates and select top k candidates
            unique_candidates = []
            seen_positions = set()
            for candidate in next_candidates:
                pos = candidate[2]
                if pos not in seen_positions:
                    seen_positions.add(pos)
                    unique_candidates.append(candidate)

            # Sort by f_value, then g_value and select beam_width best candidates
            unique_candidates.sort(key=lambda x: (x[0], x[1]))
            current_beam = unique_candidates[:self.beam_width]
            
            # Mark selected candidates as visited
            for _, _, pos, _ in current_beam:
                self.visited.add(pos)
                self.visited_order.append(pos)

        return False, []