import settings
from pathlib import Path
class Level:
    def __init__(self, map_matrix:list[list[int]], spawn_x, spawn_y, miscellaneous="", enemies=""):
        self.map_matrix = map_matrix
        self.spawn_loc:tuple[float, float] = spawn_x, spawn_y
        self.miscellaneous = [objs for objs in miscellaneous.split("//")]
        self.enemies = [objs for objs in enemies.split("//")]

    def get_level_matrix(self):
        return self.map_matrix

    def get_spawn_point(self):
        return self.spawn_loc

    def all_miscellaneous_objects(self):
        return self.miscellaneous

    def set_miscellaneous(self, misc):
        self.miscellaneous = [objs for objs in misc.split("//")]

    def set_enemies(self, ents):
        self.enemies = [objs for objs in ents.split("//")]

    def all_enemies(self):
        return self.enemies

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
    file_path = Path(file_path)
    if file_path.exists():
        with open(file_path, "r") as f:
            geometry = []
            load_data = [l.strip().split(":") for l in f]
            loaded_data_dict = {l[0].strip():l[1].strip() for l in load_data}

            for i in range(settings.ver_cells):
                row_ls = []
                for j in range(settings.hor_cells):
                    row_ls.append(int(loaded_data_dict["MAP_GEOMETRY"][i*settings.hor_cells+j]))
                geometry.append(row_ls)

            # Player location
            location = loaded_data_dict["PLAYER_SPAWN"].split()

            # Miscellaneous Objects
            miscellaneous_objects = loaded_data_dict["MISCELLANEOUS"] if loaded_data_dict["MISCELLANEOUS"] != "" else ""
            enemies = loaded_data_dict["ENEMIES"] if loaded_data_dict["ENEMIES"] != "" else ""

            new_map = Level(
                geometry,
                float(location[0]),
                float(location[1]),
            )
            new_map.set_miscellaneous(miscellaneous_objects)
            new_map.set_enemies(enemies)
            # Entities
            game_map_object.add_level(new_map)


GameMap = Map()
load_level(GameMap, "levels/barricaded_soldiers.dmf")
# load_level(GameMap, "levels/barricaded.dmf")