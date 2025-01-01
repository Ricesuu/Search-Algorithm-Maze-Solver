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

## Screenshots of Application Output
### 1. Program Run Example
<p align="left">
  <img src="https://github.com/user-attachments/assets/51f2382e-75ce-41df-98c6-e636ab99f9cf" alt="Program Run Example" width="500px">
</p>

### 2. Maze Print Example
<p align="left">
  <img src="https://github.com/user-attachments/assets/43c4ba30-eb5c-43e3-9b73-ba8918ca54eb" alt="Maze Print Example" width="500px">
</p>

### 3. Beam Search Output
<p align="left">
  <img src="https://github.com/user-attachments/assets/8464d535-06f4-4759-8944-07ea79dc55c5" alt="Beam Search Output" width="500px">
</p>

### 4. Program Test Example
<p align="left">
  <img src="https://github.com/user-attachments/assets/c60106ef-765c-4050-be53-171a8814fdad" alt="Program Test Example" width="500px">
</p>

## Disclaimer
This project was originally completed as an assignment and has been uploaded to GitHub at a later date due to limited OneDrive storage. As a result, the commit history may not accurately reflect the development process, and there may be only a few commits for the project.
