import settings
from pathlib import Path
class Level:
    def __init__(self, map_matrix:list[list[int]], spawn_x, spawn_y, miscellaneous="", entities=""):
        self.map_matrix = map_matrix
        self.spawn_loc:tuple[float, float] = spawn_x, spawn_y
        self.miscellaneous = [objs for objs in miscellaneous.split("//")]
        self.entities = [objs for objs in entities.split("//")]

    def get_level_matrix(self):
        return self.map_matrix

    def get_spawn_point(self):
        return self.spawn_loc

    def all_miscellaneous_objects(self):
        return self.miscellaneous

    def set_miscellaneous(self, misc):
        self.miscellaneous = [objs for objs in misc.split("//")]

    def set_entities(self, ents):
        self.entities = [objs for objs in ents.split("//")]

    def all_entities(self):
        return self.entities

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
            load_data = [l.strip() for l in f]
            for i in range(settings.ver_cells):
                row_ls = []
                for j in range(settings.hor_cells):
                    row_ls.append(int(load_data[0][i*settings.hor_cells+j]))
                geometry.append(row_ls)

            # Player location
            location = load_data[1].split()

            # Miscellaneous Objects
            miscellaneous_objects = load_data[2] if len(load_data) >= 3 else ""
            entities = load_data[3] if len(load_data) >= 4 else ""
            new_map = Level(
                geometry,
                float(location[0]),
                float(location[1]),
                miscellaneous=miscellaneous_objects,
                entities=entities
            )
            # Entities
            game_map_object.add_level(new_map)


GameMap = Map()
load_level(GameMap, "levels/prison.dmf")
# load_level(GameMap, "levels/4room.dmf")
# load_level(GameMap, "levels/only_crates.dmf")