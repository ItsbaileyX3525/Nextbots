from ursina import *
import heapq

app = Ursina()

GRID_SIZE = 10
CELL_SIZE = 2

start_point = (0, 0)
end_point = (9, 9)

obstacles = [(1, 0), (3,0), (5, 0), (5, 1), (7, 0), (9, 0)]

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def get_neighbors(cell):
    x, y = cell
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    neighbors = filter(lambda cell: 0 <= cell[0] < GRID_SIZE and 0 <= cell[1] < GRID_SIZE, neighbors)
    neighbors = filter(lambda cell: cell not in obstacles, neighbors)
    return neighbors

def find_path(start, end):
    heap = [(0, start)]
    visited = set()
    parent = {}

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

    return []

grid = [[Entity(model='cube', scale=CELL_SIZE, position=Vec3(x*CELL_SIZE, y*CELL_SIZE), texture='white_cube') for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]

grid[start_point[0]][start_point[1]].texture = 'brick'
grid[end_point[0]][end_point[1]].texture = 'brick'

for obstacle in obstacles:
    grid[obstacle[0]][obstacle[1]].texture = None
    grid[obstacle[0]][obstacle[1]].color =color.black

path = find_path(start_point, end_point)

for cell in path:
    grid[cell[0]][cell[1]].texture = None
    grid[cell[0]][cell[1]].color = color.green

EditorCamera()
app.run()
