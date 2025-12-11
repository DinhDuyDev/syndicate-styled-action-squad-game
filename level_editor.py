import pygame
import settings
import screen
import camera
import utilityfuncs
import math
from pathlib import Path
import tiles
import decorations
import copy
import misc_objs_gen
import entities_gen

pygame.init()
pygame.font.init()

# Screen setup
game_screen = screen.Screen(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
draw_dest = game_screen.screen.copy()
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 10)
settings.zoom = 1

# Level Setup
LEVEL_WIDTH = settings.hor_cells
LEVEL_HEIGHT = settings.ver_cells
c_dimensions = settings.cell_dimension
command = "levels/barricaded.dmf=load"
using_commands = False

class Level:
    level = []

def setup_level(lv, width, height):
    lv.clear()
    for i in range(height):
        row = []
        for j in range(width):
            row.append(0)
        lv.append(row)
setup_level(Level.level, LEVEL_WIDTH, LEVEL_HEIGHT)

def draw_level(lv):
    for i in range(len(lv)):
        for j in range(len(lv[0])):
            print(lv[i][j], end="")
        print()
# Sprites
LEVEL_TILES = tiles.get_tiles()

current_sprite = 1

# Tools
TOOLS = {
    "Pencil" : pygame.image.load("sprites/Level Editor/pencil.png").convert_alpha(),
    "Bucket": pygame.image.load("sprites/Level Editor/bucket.png").convert_alpha(),
    "Player_Spawn": pygame.image.load("sprites/Level Editor/player_spawn.png").convert_alpha(),
    "Misc": pygame.image.load("sprites/Level Editor/miscellaneous.png").convert_alpha(),
    "Enemy_Place": pygame.image.load("sprites/Level Editor/enemy_tool.png").convert_alpha(),
}
tool_mode = "Pencil"

# Miscellaneous Objects (AKA decorators) and Entities Generator
MISC_OBJECTS = misc_objs_gen.misc_objects_generator()
ENTITY_OBJECTS = entities_gen.entities_generator()
print(ENTITY_OBJECTS)
selected_object = "NormalCrate"
selected_entity = "EnemyMobsterPistol"
mouse_held_down = False
misc_objs:list[decorations.all_decoration_types] = []
ent_list:list[decorations.all_decoration_types] = []

scroll_y = 0

# Camera
CameraView = camera.Camera()

# Entities
class Entities:
    player_spawn_point = (0, 0)

# Files
def renew_level():
    setup_level(Level.level, LEVEL_WIDTH, LEVEL_HEIGHT)

def save_level(lv:list[list[int]], pth):
    if ".dmf" in pth:
        with open(pth, 'w') as f:
            f.write("") # Delete everything inside the files
            write_data = []
            level_data = ""
            for row in lv:
                for cell in row:
                    level_data += str(cell)
            level_data += "\n"
            write_data.append(f"MAP_GEOMETRY : {level_data}")
            write_data.append(f"PLAYER_SPAWN : {Entities.player_spawn_point[0]} {Entities.player_spawn_point[1]}\n")

            # Miscellaneous
            save_objs = ""
            for i in range(len(misc_objs)):
                obj = misc_objs[i]
                if i < len(misc_objs)-1:
                    save_objs += repr(obj) + "//"
                else:
                    save_objs += repr(obj)
            write_data.append(f"MISCELLANEOUS : {save_objs}\n")

            # Entities
            save_objs = ""
            for i in range(len(ent_list)):
                obj = ent_list[i]
                if i < len(ent_list) - 1:
                    save_objs += repr(obj) + "//"
                else:
                    save_objs += repr(obj)
            write_data.append(f"ENTITIES : {save_objs}")
            f.writelines(write_data)

def load_level(pth):
    lvl_pth = Path(pth)
    if lvl_pth.exists():
        setup_level(Level.level, LEVEL_WIDTH, LEVEL_HEIGHT)
        with open(pth, 'r') as f:
            # Clear all previous data
            misc_objs.clear()
            ent_list.clear()
            load_data = [l.strip().split(":") for l in f]
            loaded_data_dict = {l[0].strip():l[1].strip() for l in load_data}
            print(loaded_data_dict)

            for row in range(LEVEL_HEIGHT):
                for cell in range(LEVEL_WIDTH):
                    Level.level[row][cell] = int(loaded_data_dict["MAP_GEOMETRY"][row*LEVEL_WIDTH+cell])

            player_loc = loaded_data_dict["PLAYER_SPAWN"].split()
            Entities.player_spawn_point = (float(player_loc[0]), float(player_loc[1]))

            all_miscellaneous = loaded_data_dict["MISCELLANEOUS"].split("//") if loaded_data_dict["MISCELLANEOUS"] != "" else ""
            for misc_o in all_miscellaneous:
                misc_objs.append(misc_objs_gen.get_miscellaneous_objects(misc_o))

            all_entities = loaded_data_dict["ENTITIES"].split("//") if loaded_data_dict["ENTITIES"] != "" else ""
            for ent_o in all_entities:
                ent_list.append(entities_gen.get_entities(ent_o))
# Running
while running:
    # Mouse and Camera coordinates
    c_x, c_y = CameraView.get_pos()
    c_x = int(c_x)
    c_y = int(c_y)
    mx, my = utilityfuncs.mouse_xy_transformation(draw_dest, game_screen.screen)

    for event in pygame.event.get():
        # Scrolling
        if event.type == pygame.MOUSEWHEEL:
            scroll_y -= event.y
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                using_commands = not using_commands
            if using_commands:
                if event.key == pygame.K_RETURN:
                    if len(command) != 0: # Save or load functionality
                        n = command.split("=")
                        if len(n) == 1:
                            if n[0] in "new":
                                renew_level()
                        elif len(n) == 2:
                            if n[1].lower() in "save":
                                save_level(Level.level, n[0])
                            elif n[1].lower() in "load":
                                load_level(n[0])
                elif event.key == pygame.K_BACKSPACE:
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        name = ""
                    if len(command) != 0:
                        command = command[:len(command)-1]
                else:
                    if event.key != pygame.K_TAB:
                        command += event.unicode
    # Camera action
    if not using_commands:
        CameraView.action()

    # Clearing the screen
    draw_dest.fill((0, 0, 0))

    _x = c_x * settings.cell_dimension
    _y = c_y * settings.cell_dimension
    w = 32

    # Drawing level grid
    for i in range(c_y, c_y+LEVEL_HEIGHT//2):
        for j in range(c_x, c_x+LEVEL_WIDTH//2):
            pygame.draw.line(draw_dest, (75, 75, 75), ((j-c_x) * c_dimensions, (i-c_y) * c_dimensions)
                             , ((j-c_x) * c_dimensions + c_dimensions, (i-c_y) * c_dimensions))
            pygame.draw.line(draw_dest, (75, 75, 75), ((j-c_x) * c_dimensions, (i-c_y) * c_dimensions)
                             , ((j-c_x) * c_dimensions, (i-c_y) * c_dimensions + c_dimensions))
            if Level.level[i][j] != 0:
                # pygame.draw.rect(draw_dest, (75, 75, 75), (j * c_dimensions-_x, i * c_dimensions-_y, c_dimensions, c_dimensions))
                curr_tile = LEVEL_TILES[Level.level[i][j]]
                draw_dest.blit(curr_tile, curr_tile.get_rect(topleft=(j*c_dimensions - _x, i*c_dimensions - _y)))

    # Drawing the center
    pygame.draw.line(draw_dest, (255, 0, 0), (settings.WINDOW_WIDTH - w - _x - 1, settings.WINDOW_HEIGHT - _y - 1),
                     (settings.WINDOW_WIDTH + w - _x - 1, settings.WINDOW_HEIGHT - _y - 1), 2)
    pygame.draw.line(draw_dest, (255, 0, 0), (settings.WINDOW_WIDTH - _x - 1, settings.WINDOW_HEIGHT - w - _y - 1),
                     (settings.WINDOW_WIDTH - _x - 1, settings.WINDOW_HEIGHT + w - _y - 1), 2)

    # Level Drawing
    _x, _y = int(mx / settings.cell_dimension) + c_x, int(my / settings.cell_dimension) + c_y

    # Performance and Tools
    if pygame.key.get_pressed()[pygame.K_TAB]:
        pygame.draw.rect(draw_dest, (255, 0, 0), (0, 0, 32, 4))
        pygame.draw.rect(draw_dest, (0, 255, 0), (0, 0, 32 * (clock.get_fps() / 60), 4))
        x = 0
        for tool_name, image in TOOLS.items():
            img_rect = image.get_rect(topleft=(x * 16, 0))
            x += 1
            if tool_mode == tool_name:
                pygame.draw.rect(draw_dest, (0, 255, 0), img_rect)
            if img_rect.collidepoint(mx, my):
                if pygame.mouse.get_pressed()[0]:
                    tool_mode = tool_name
                    print(tool_mode)
                    scroll_y = 0
                    pygame.draw.rect(draw_dest, (255, 0, 255), img_rect, width=1)
                else:
                    pygame.draw.rect(draw_dest, (255, 0, 255), img_rect)
            draw_dest.blit(image, img_rect)
        SW = settings.WINDOW_WIDTH

        if tool_mode == "Misc":
            index = 0
            for key, obj in MISC_OBJECTS.items():
                tx, ty = SW - 32, (index + 1) * 16 - scroll_y
                obj_spr = obj.sprite.get_current_image()
                obj_rect = obj_spr.get_rect(center=(tx, ty))
                item_name = font.render(key, False, (255, 0, 0))
                item_name_rect = item_name.get_rect(topleft=(tx-64, ty))
                if key == selected_object:
                    pygame.draw.rect(draw_dest, (0, 255, 0), (tx - 8, ty - 8, 16, 16))

                if obj_rect.collidepoint(mx, my):
                    if pygame.mouse.get_pressed()[0]:
                        selected_object = key
                        pygame.draw.rect(draw_dest, (255, 0, 255), (tx - 8, ty - 8, 16, 16), width=1)
                    else:
                        pygame.draw.rect(draw_dest, (255, 0, 255), (tx - 8, ty - 8, 16, 16))

                draw_dest.blit(obj_spr, obj_rect)
                draw_dest.blit(item_name, item_name_rect)
                index += 1

        elif tool_mode == "Enemy_Place":
            index = 0
            for key, obj in ENTITY_OBJECTS.items():
                tx, ty = SW - 32, (index + 1) * 16 - scroll_y
                obj_spr = obj.sprite.get_current_image()
                obj_rect = obj_spr.get_rect(center=(tx, ty))
                obj.switch_sprites()

                if key == selected_entity:
                    pygame.draw.rect(draw_dest, (0, 255, 0), (tx - 3, ty - 3, 16, 16))

                if obj_rect.collidepoint(mx, my):
                    if pygame.mouse.get_pressed()[0]:
                        selected_entity = key
                        pygame.draw.rect(draw_dest, (255, 0, 255), (tx - 3, ty - 3, 16, 16), width=1)
                    else:
                        pygame.draw.rect(draw_dest, (255, 0, 255), (tx - 3, ty - 3, 16, 16))

                draw_dest.blit(obj_spr, obj_rect)
                index += 1
        else:
            for index, tile in LEVEL_TILES.items():
                tx, ty = SW - 24, (index + 1) * 16 - scroll_y
                index_text = font.render(f"{index}", False, (255,255,255))
                index_rect = index_text.get_rect(topleft=(tx-8, ty))
                tile_rect = tile.get_rect(topleft=(tx, ty))

                if index == current_sprite:
                    pygame.draw.rect(draw_dest, (0, 255, 0), (tx - 3, ty - 3, 16, 16))

                if tile_rect.collidepoint(mx, my):
                    if pygame.mouse.get_pressed()[0]:
                        current_sprite = index
                        pygame.draw.rect(draw_dest, (255, 0, 255), (tx-3, ty-3, 16,16), width=1)
                    else:
                        pygame.draw.rect(draw_dest, (255, 0, 255), (tx-3, ty-3, 16,16))

                draw_dest.blit(tile, tile_rect)
                draw_dest.blit(index_text, index_rect)
    else:
        scroll_y = 0
        if tool_mode == "Pencil":
            if pygame.mouse.get_pressed()[0]:
                Level.level[_y][_x] = current_sprite
            elif pygame.mouse.get_pressed()[2]:
                Level.level[_y][_x] = 0
        elif tool_mode == "Bucket":
            if pygame.mouse.get_pressed()[0]:
                utilityfuncs.flood_fill(_x, _y, Level.level, current_sprite, Level.level[_y][_x])
        elif tool_mode == "Player_Spawn": # setting the player's spawn:
            if pygame.mouse.get_pressed()[0]:
                d = 0
                can_place = True
                for i in range(36):
                    __x, __y = (int((mx + math.cos(math.radians(d))*10 + c_x * c_dimensions)/c_dimensions),
                                int((my - math.cos(math.radians(d))*10 + c_y * c_dimensions)/c_dimensions))
                    if Level.level[__y][__x] != 0:
                        can_place = False

                    __x, __y = (int((mx + math.cos(math.radians(d)) * 5 + c_x * c_dimensions) / c_dimensions),
                                int((my - math.cos(math.radians(d)) * 5 + c_y * c_dimensions) / c_dimensions))
                    if Level.level[__y][__x] != 0:
                        can_place = False
                    d += 10
                if can_place:
                    Entities.player_spawn_point = (mx + c_x * c_dimensions, my + c_y * c_dimensions)
        elif tool_mode == "Misc":
            _x = c_x * c_dimensions
            _y = c_y * c_dimensions
            if not pygame.mouse.get_pressed()[0]:
                mouse_held_down =  False

            # I don't have a trackpad right now so I'm just going to put this here first
            if pygame.mouse.get_pressed()[2]:
                for o in misc_objs:
                    o_rect = o.sprite.get_current_image().get_rect(center=(o.xy()[0], o.xy()[1]))
                    spawn_x, spawn_y = mx + _x, my + _y
                    if o_rect.collidepoint(spawn_x, spawn_y):
                        misc_objs.remove(o)

            if pygame.mouse.get_pressed()[0] and not mouse_held_down:
                spawn_x, spawn_y = mx + _x, my + _y
                new_object = copy.copy(MISC_OBJECTS[selected_object])
                new_object.repr_name = selected_object
                new_object.set_xy((spawn_x, spawn_y))
                misc_objs.append(new_object)
                mouse_held_down = True

        elif tool_mode == "Enemy_Place":
            _x = c_x * c_dimensions
            _y = c_y * c_dimensions
            if not pygame.mouse.get_pressed()[0]:
                mouse_held_down = False

            # I don't have a trackpad right now so I'm just going to put this here first
            if pygame.mouse.get_pressed()[2]:
                for o in ent_list:
                    o_rect = o.sprite.get_current_image().get_rect(center=(o.xy()[0], o.xy()[1]))
                    spawn_x, spawn_y = mx + _x, my + _y
                    if o_rect.collidepoint(spawn_x, spawn_y):
                        ent_list.remove(o)
            if pygame.mouse.get_pressed()[0] and not mouse_held_down:
                spawn_x, spawn_y = mx + _x, my + _y
                new_object = copy.copy(ENTITY_OBJECTS[selected_entity])
                new_object.repr_name = selected_entity
                new_object.set_xy((spawn_x, spawn_y))
                ent_list.append(new_object)
                mouse_held_down = True

    # Spawn Point
    if Entities.player_spawn_point != (None, None):
        sp = Entities.player_spawn_point
        pygame.draw.circle(draw_dest, (255, 165, 0), (sp[0]-c_x*c_dimensions, sp[1]-c_y*c_dimensions), 2)
        pygame.draw.circle(draw_dest, (255, 0, 0), (sp[0]-c_x*c_dimensions, sp[1]-c_y*c_dimensions), 10, width=1)

    # For decorative objects
    _x = c_x * c_dimensions
    _y = c_y * c_dimensions
    for o in misc_objs:
        o.render(draw_dest, o.xy()[0]-_x, o.xy()[1]-_y)

    # For entities
    _x = c_x * c_dimensions
    _y = c_y * c_dimensions
    for o in ent_list:
        o.render(draw_dest, o.xy()[0]-_x, o.xy()[1]-_y)

    # Commands
    y_name = 330
    text_col = (255, 255, 255)
    if not using_commands:
        text_col = (255, 0, 0)

    name_surf = font.render(f"> {command}<", False, text_col)
    name_rect = name_surf.get_rect(topleft=(80, y_name))
    draw_dest.blit(name_surf, name_rect)

    # Rendering on game
    game_screen.screen.blit(pygame.transform.scale(draw_dest, (game_screen.get_dimensions())), (0, 0))
    pygame.display.flip()
    clock.tick(60)

print(misc_objs)