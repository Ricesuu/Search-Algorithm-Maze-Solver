# Search Algorithm Maze Solver
A program that uses different search algorithms to solve a CLI maze. The tool is flexible and supports testing and visualisation of the maze.

## Usage

Run the script using the following command structure:

### Regular Mode
```bash
python search.py <filename> <method> [beam_width]
```
- `<filename>`: Path to the maze file.
- `<method>`: The search method to use (see "Available Methods" below).
- `[beam_width]` (optional): Specifies the beam width for Beam Search (default is 2).

### Test Mode
Run the tool in test mode to verify functionality:
```bash
python search.py --test
```

### Print Maze
Print the maze from a specified file:
```bash
python search.py --print <filename>
```
- `<filename>`: Path to the maze file to be printed.

## Available Methods
The following search algorithms are supported:

- **bfs**: Breadth First Search
- **dfs**: Depth First Search
- **astar**: A* Search
- **gbfs**: Greedy Best First Search
- **bdfs**: Bidirectional Search
- **bs**: Beam Search

## Example Usage

1. Perform A* Search on a maze:
   ```bash
   python search.py maze.txt astar
   ```

2. Perform Beam Search with a custom beam width:
   ```bash
   python search.py maze.txt bs 3
   ```

3. Print the maze layout:
   ```bash
   python search.py --print maze.txt
   ```

4. Run test cases:
   ```bash
   python search.py --test
   ```


## Disclaimer
This project was originally completed as an assignment and has been uploaded to GitHub at a later date due to limited OneDrive storage. As a result, the commit history may not accurately reflect the development process, and there may be only a few commits for the project.
