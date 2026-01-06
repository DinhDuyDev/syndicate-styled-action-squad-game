import tiles
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

def pathfind(x, y, x1, y1, mat):
    if mat[y1][x1] not in tiles.TRAVERSABLE_TILES:
        return []
    grid = Grid(matrix=mat)
    # Start and end node
    start = grid.node(x, y)
    end   = grid.node(x1, y1)

    # A-Star pathfinder
    finder = AStarFinder(diagonal_movement = DiagonalMovement.always)

    # Use the pathfinder to find the path
    path, repeats = finder.find_path(start,end,grid)

    res = []
    for grid in path:
        res.append((grid.x, grid.y))
    return res