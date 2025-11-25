import settings
class Level:
    def __init__(self, map_matrix:list[list[int]], spawn_x, spawn_y):
        self.map_matrix = map_matrix
        self.spawn_loc:tuple[float, float] = spawn_x, spawn_y

    def get_level_matrix(self):
        return self.map_matrix

    def get_spawn_point(self):
        return self.spawn_loc

class Map:
    def __init__(self):
        self.map_geometry:list[Level] = []
        self.level = -1

    def add_level(self, lv:Level):
        self.map_geometry.append(lv)
        self.level += 1

    def get_map(self):
        return self.map_geometry[self.level]

    def set_level(self, l:int):
        self.level = l

def print_map(ls:list[list[int]]):
    print("m=[")
    for i in  ls:
        print(str(i), end=",\n")
    print("]")

def load_level(game_map_object:Map, file_path):
    with open(file_path, "r") as f:
        geometry = []
        map_list = [l.strip() for l in f]
        # print(map_list)
        # print(len(map_list))
        row_index = 0
        for i in range(settings.ver_cells):
            row_data = map_list[i]
            row_ls = []
            for j in range(settings.hor_cells):
                row_ls.append(int(row_data[j]))
            geometry.append(row_ls)
            row_index += 1

        # print(row_index)
        row_index += 1
        while map_list[row_index] == "SPLIT\n":
            row_index += 1
        # Player location
        location = map_list[row_index].split()
        new_map = Level(geometry, float(location[0]), float(location[1]))
        game_map_object.add_level(new_map)

GameMap = Map()
load_level(GameMap, "levels/prison.dmf")