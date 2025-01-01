# Description: Reads and parses maze configurations from text files.

class FileRead:
    # Read the maze configuration file
    @staticmethod
    def readFile(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]


    # Check if position is within grid bounds
    @staticmethod
    def validatePosition(pos, rows, cols, pos_type):
        x, y = pos
        if not (0 <= x < cols and 0 <= y < rows):
            raise ValueError(f"{pos_type} position {pos} is out of bounds. "f"Grid size is {cols}x{rows}")


    # Check if wall placement is valid
    @staticmethod
    def validateWall(wall_info, rows, cols):
        x, y, width, height = wall_info
        if not (0 <= x < cols and 0 <= y < rows and 
                0 <= x + width - 1 < cols and 
                0 <= y + height - 1 < rows):
            raise ValueError(f"Wall {wall_info} is out of bounds. "f"Grid size is {cols}x{rows}")


    # Parse grid information from configuration lines
    @staticmethod
    def parseGridInfo(lines):
        try:
            # Get grid dimensions
            dimensions = tuple(map(int, lines[0][1:-1].split(',')))
            rows, cols = dimensions
            
            # Get and validate start position
            start = tuple(map(int, lines[1][1:-1].split(',')))
            FileRead.validatePosition(start, rows, cols, "Start")
            
            # Get and validate goal positions
            goals = []
            for goal in lines[2].split('|'):
                goal_pos = tuple(map(int, goal.strip()[1:-1].split(',')))
                FileRead.validatePosition(goal_pos, rows, cols, "Goal")
                goals.append(goal_pos)
            
            # Get and validate wall positions
            walls = []
            for line in lines[3:]:
                wall_info = tuple(map(int, line[1:-1].split(',')))
                FileRead.validateWall(wall_info, rows, cols)
                walls.append(wall_info)
            
            return {
                'dimensions': dimensions,
                'start': start,
                'goals': goals,
                'walls': walls
            }
            
        except IndexError:
            raise ValueError("Incomplete maze configuration file")
        except ValueError as e:
            raise ValueError(f"Invalid maze configuration: {str(e)}")
