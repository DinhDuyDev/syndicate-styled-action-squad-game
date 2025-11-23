import math
import pygame
import map
import settings

def mouse_xy_transformation(screen_interact:pygame.Surface, screen_base:pygame.Surface):
    x, y = pygame.mouse.get_pos()[0] * (screen_interact.get_width() / screen_base.get_width()), pygame.mouse.get_pos()[1] * (screen_interact.get_height() / screen_base.get_height())
    return x, y

def point_distance(x, y, a, b):
    sdx = (a - x)**2
    sdy = (b - y)**2
    dist = math.sqrt(sdx + sdy)
    return dist

def point_direction(x, y, a, b):
    dx = a - x
    dy = b - y
    deg = math.atan2(-dy, dx)
    return math.degrees(deg)

def point_distance_perpendicular(x, y, x_s, y_s, x_e, y_e):
    numerator = abs((x_e - x_s) * (y_s - y) - (x_s - x) * (y_e - y_s))
    denominator = math.sqrt((x_e - x_s)**2 + (y_e - y_s) ** 2)

    return numerator / denominator

def sign(a):
    if a == 0:
        return 0
    return abs(a) / a

# Flood fill at a certain index
def flood_fill(x, y, arr, num, touched_element):
    # Implement BFS
    queue = [(x, y)]
    visited = set()

    if num == touched_element:
        return

    while queue:
        cx, cy = queue.pop(0)
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        if 0 <= cx < len(arr[0]) and 0 <= cy < len(arr) and arr[cy][cx] == touched_element:
            arr[cy][cx] = num

            queue.append((cx + 1, cy))
            queue.append((cx - 1, cy))
            queue.append((cx, cy + 1))
            queue.append((cx, cy - 1))

def clamp(val, minimum, maximum):
    return max(minimum, min(val, maximum))


# Defunct
# def pathfind(x, y, dest_x, dest_y, m, nav_matrix):
#     x, y = int(x/settings.cell_dimension), int(y/settings.cell_dimension)
#     dest_x, dest_y = int(dest_x/settings.cell_dimension), int(dest_y/settings.cell_dimension)
#     if m[y][x] != 0:
#         return []
#
#     beginning = map.NavBlock(x, y)
#     visited:list[map.NavBlock] = list()
#     queue:list[map.NavBlock] = list()
#     mapped_dir:dict[tuple[int, int],tuple[int, int]] = dict()
#
#     visited.append(map.NavBlock(x, y))
#     queue.append(map.NavBlock(x, y))
#
#     # BFS section
#
#     while len(queue) != 0:
#         neighbors = [
#             (-1, -1), (0, -1), (1, -1),
#             (-1, 0), (1, 0),
#             (-1, 1), (0, 1), (1, 1),
#         ]
#         previous = queue.pop(0)
#         # print("Scanning Map")
#         for (x, y) in neighbors:
#             if map.NavBlock(previous.x+x, previous.y+y) not in visited and map.NavBlock(previous.x+x, previous.y+y) in nav_matrix and m[previous.y+y][previous.x+x] == 0:
#                 visited.append(map.NavBlock(previous.x+x, previous.y+y))
#                 queue.append(map.NavBlock(previous.x+x, previous.y+y))
#                 mapped_dir[(previous.x+x, previous.y+y)] = previous.x, previous.y
#
#                 if (previous.x+x, previous.y+y) == (dest_x, dest_y):
#                     break
#
#     # print("Map scanned")
#
#     move_path = []
#     curr = (dest_x, dest_y)
#     if curr not in mapped_dir:
#         return move_path
#     else:
#         while curr != (beginning.x, beginning.y):
#             print(curr)
#             move_path.insert(0, curr)
#             curr = mapped_dir[curr]
#             m[curr[1]][curr[0]] = 2
#     return move_path
