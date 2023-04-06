from ursina import *
import heapq

app = Ursina()

# Define the size of the grid and the size of each cell
GRID_SIZE = 10
CELL_SIZE = 2

# Define the start and end points for the entity
start_point = (0, 0)
end_point = (9, 9)

# Define the obstacles in the environment
obstacles = [(1, 0), (3,0), (5, 0), (5, 1), (7, 0), (9, 0)]

# Define a function to calculate the distance between two points
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

# Define a function to get the neighbors of a cell
def get_neighbors(cell):
    x, y = cell
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    neighbors = filter(lambda cell: 0 <= cell[0] < GRID_SIZE and 0 <= cell[1] < GRID_SIZE, neighbors)
    neighbors = filter(lambda cell: cell not in obstacles, neighbors)
    return neighbors

# Define the pathfinding function using A* algorithm
def find_path(start, end):
    # Initialize the data structures
    heap = [(0, start)]
    visited = set()
    parent = {}

    # Loop until we find the end point or exhaust all options
    while heap:
        _, cell = heapq.heappop(heap)
        if cell == end:
            path = [cell]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.reverse()
            return path
        if cell in visited:
            continue
        visited.add(cell)
        for neighbor in get_neighbors(cell):
            g_score = distance(start, cell) + distance(cell, neighbor)
            if neighbor in visited:
                continue
            parent[neighbor] = cell
            heapq.heappush(heap, (g_score, neighbor))

    # Return an empty path if no path is found
    return []

# Create a grid of cells
grid = [[Entity(model='cube', scale=CELL_SIZE, position=Vec3(x*CELL_SIZE, y*CELL_SIZE), texture='white_cube') for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]

# Mark the start and end points
grid[start_point[0]][start_point[1]].texture = 'brick'
grid[end_point[0]][end_point[1]].texture = 'brick'

# Mark the obstacles
for obstacle in obstacles:
    grid[obstacle[0]][obstacle[1]].texture = None
    grid[obstacle[0]][obstacle[1]].color =color.black

# Find the path from the start to the end point
path = find_path(start_point, end_point)

# Mark the path in green
for cell in path:
    grid[cell[0]][cell[1]].texture = None
    grid[cell[0]][cell[1]].color = color.green
EditorCamera()
# Run the Ursina application
app.run()
