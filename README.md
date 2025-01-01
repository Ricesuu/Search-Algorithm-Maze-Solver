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
  <img src="https://github.com/user-attachments/assets/437d60bc-2587-4182-adf1-727cb12fbb90" alt="Program Run Example" width="500px">
</p>

### 2. Maze Print Example
<p align="left">
  <img src="https://github.com/user-attachments/assets/42528f71-ff8d-47fc-9c0c-6e12d1a86642" alt="Maze Print Example" width="500px">
</p>

### 3. Beam Search Output
<p align="left">
  <img src="https://github.com/user-attachments/assets/3f873560-3244-40b4-bd31-a1d97471b886" alt="Beam Search Output" width="500px">
</p>

### 4. Program Test Example
<p align="left">
  <img src="https://github.com/user-attachments/assets/c61f43cc-ba8f-4642-b172-026ccf78d5a3" alt="Program Test Example" width="500px">
</p>

## Disclaimer
This project was originally completed as an assignment and has been uploaded to GitHub at a later date due to limited OneDrive storage. As a result, the commit history may not accurately reflect the development process, and there may be only a few commits for the project.
