import sys
import os
import time
from grid import Grid
from fileRead import FileRead
from testSuiteExtension import TestSuiteExtension
from searchstrat import (
    BreadthFirstSearch,
    DepthFirstSearch,
    AStarSearch,
    GreedyBestFirstSearch,
    BidirectionalSearch,
    BeamSearch
)

# Map of search method strings to their corresponding classes, method names, and full names
SEARCH_METHODS = {
    'bfs': (BreadthFirstSearch, 'bfsPath', 'Breadth First Search'),
    'dfs': (DepthFirstSearch, 'dfsPath', 'Depth First Search'),
    'astar': (AStarSearch, 'astarPath', 'A* Search'),
    'gbfs': (GreedyBestFirstSearch, 'gbfsPath', 'Greedy Best First Search'),
    'bdfs': (BidirectionalSearch, 'bdsPath', 'Bidirectional Search'),
    'bs': (BeamSearch, 'beamPath', 'Beam Search')
}

def convertPathToMoves(path):
    """Convert a path to a list of moves"""
    moves = []
    for i in range(1, len(path)):
        curr_x, curr_y = path[i-1]
        next_x, next_y = path[i]
        
        if next_x > curr_x:
            moves.append('RIGHT')
        elif next_x < curr_x:
            moves.append('LEFT')
        elif next_y > curr_y:
            moves.append('DOWN')
        elif next_y < curr_y:
            moves.append('UP')
    
    return moves

def printMazeOnly(filename):
    """Print only the maze structure from the file"""
    try:
        if not os.path.isfile(filename):
            filename = os.path.join('test_cases', filename)
        lines = FileRead.readFile(filename)
        config = FileRead.parseGridInfo(lines)
        grid = Grid(config['dimensions'], config['start'], config['goals'], config['walls'])
        print(f"\nMaze from {filename}:")
        grid.display()
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file {filename}")
    except Exception as e:
        raise Exception(f"Error parsing file: {str(e)}")

def printDetailedOutput(grid, method, found, path, nodes_explored, visited_order, time_taken_ms):
    """Print detailed output for debugging and verification"""
    print("\n--- To Check ---")
    print(f"\nGrid after {SEARCH_METHODS[method][2]} search:")
    grid.display()
    print(f"\nPath found: {found}")
    if found:
        print(f"Path taken: {path}")
        print(f"Total nodes explored: {nodes_explored}")
        print(f"Time taken: {time_taken_ms:.2f} ms")
        print(f"Visited nodes in order: {visited_order}")
        print("\n--------------------------------")

def runSearch(filename, method, beam_width=2):
    """Run the specified search method on the given maze file"""
    # Validate search method
    if method not in SEARCH_METHODS:
        raise ValueError(
            f"Unknown search method '{method}'\n"
            f"Available methods: {', '.join(SEARCH_METHODS.keys())}"
        )

    # Read and parse the maze file
    try:
        if not os.path.isfile(filename):
            filename = os.path.join('test_cases', filename)
        lines = FileRead.readFile(filename)
        config = FileRead.parseGridInfo(lines)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file {filename}")
    except Exception as e:
        raise Exception(f"Error parsing file: {str(e)}")

    # Create the grid and initialize search
    grid = Grid(config['dimensions'], config['start'], config['goals'], config['walls'])
    search_class, search_method = SEARCH_METHODS[method][:2]
    
    # Initialize search with beam width if it's beam search
    if method == 'bs':
        search = search_class(grid, beam_width=beam_width)
    else:
        search = search_class(grid)
    
    # Start timing using perf_counter for better precision
    start_time = time.perf_counter()
    
    # Run the search
    found, path = getattr(search, search_method)()
    
    # Calculate time taken in milliseconds
    time_taken_ms = (time.perf_counter() - start_time) * 1000

    # Print required assignment format output
    print(f"{filename} {SEARCH_METHODS[method][2]}")
    
    if found:
        goal = path[-1]  # Get the reached goal (last position in path)
        print(f"{goal} {search.nodes_explored}")
        moves = convertPathToMoves(path)
        print(' '.join(moves))
    else:
        print(f"No goal is reachable; {search.nodes_explored}")

    # Print detailed debug output
    printDetailedOutput(
        grid, method, found, path,
        search.nodes_explored, search.visited_order,
        time_taken_ms
    )

def printUsage():
    """Print usage instructions"""
    print("Usage:")
    print("1. Regular mode: python search.py <filename> <method> [beam_width]")
    print("2. Test mode: python search.py --test")
    print("3. Print maze: python search.py --print <filename>")
    print("\nAvailable methods:")
    for short_name, (_, _, full_name) in SEARCH_METHODS.items():
        print(f"  {short_name}: {full_name}")
    print("\nFor Beam Search, beam width is defaulted at 2, but can be changed with the following command:")
    print("Example: python search.py maze.txt bs 3")

def main():
    if len(sys.argv) == 1:
        printUsage()
        sys.exit(1)
    elif len(sys.argv) == 2 and sys.argv[1] == '--test':
        from testSuiteExtension import TestSuiteExtension 
        test_suite = TestSuiteExtension()
        test_suite.runTestSuite()
    elif len(sys.argv) == 3 and sys.argv[1] == '--print':
        try:
            printMazeOnly(sys.argv[2])
        except (FileNotFoundError, Exception) as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    elif len(sys.argv) >= 3:
        filename = sys.argv[1]
        method = sys.argv[2].lower()
        
        # Handle beam width parameter for beam search
        beam_width = 2  # default value
        if method == 'bs' and len(sys.argv) == 4:
            try:
                beam_width = int(sys.argv[3])
                if beam_width < 1:
                    raise ValueError("Beam width must be a positive integer")
            except ValueError as e:
                print(f"Error: {str(e)}")
                sys.exit(1)
        
        try:
            runSearch(filename, method, beam_width)
        except (ValueError, FileNotFoundError, Exception) as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    else:
        printUsage()
        sys.exit(1)

if __name__ == "__main__":
    main()