import pygame
import settings
import screen
import camera
import utilityfuncs
import math
from pathlib import Path

pygame.init()
pygame.font.init()

# Screen setup
game_screen = screen.Screen(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
draw_dest = game_screen.screen.copy()
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 10)

# Level Setup
LEVEL_WIDTH = settings.hor_cells
LEVEL_HEIGHT = settings.ver_cells
c_dimensions = settings.cell_dimension
command = ""
using_commands = False

level = []
def setup_level(lv, width, height):
    for i in range(height):
        row = []
        for j in range(width):
            row.append(0)
        lv.append(row)
setup_level(level, LEVEL_WIDTH, LEVEL_HEIGHT)

# Sprites
LEVEL_TILES = {
    0 : pygame.image.load("sprites/level_tiles/empty.png").convert_alpha(),
    1 : pygame.image.load("sprites/level_tiles/normal_brick.png").convert_alpha(),
    2 : pygame.image.load("sprites/level_tiles/dirty_brick.png").convert_alpha(),
    3 : pygame.image.load("sprites/level_tiles/NO_ACCESS.png").convert_alpha()
}
current_sprite = 1

# Tools
TOOLS = {
    "Pencil" : pygame.image.load("sprites/Level Editor/pencil.png").convert_alpha(),
    "Bucket": pygame.image.load("sprites/Level Editor/bucket.png").convert_alpha(),
    "Player_Spawn": pygame.image.load("sprites/Level Editor/player_spawn.png").convert_alpha(),
}
tool_mode = "Pencil"

# Camera
CameraView = camera.Camera()
CameraView.frames = 3

# Entities
class Entities:
    player_spawn_point = (0, 0)

# Files
def renew_level():
    setup_level(level, LEVEL_WIDTH, LEVEL_HEIGHT)

def save_level(lv:list[list[int]], pth):
    if ".dmf" in pth:
        with open(pth, 'w') as f:
            write_data = []
            for row in lv:
                r = ""
                for cell in row:
                    r += str(cell)
                r += "\n"
                write_data.append(r)
            write_data.append("P_SPAWN\n")
            write_data.append(f"{Entities.player_spawn_point[0]} {Entities.player_spawn_point[1]}")
            f.writelines(write_data)

def load_level(pth):
    setup_level(level, LEVEL_WIDTH, LEVEL_HEIGHT)
    lvl_pth = Path(pth)
    if lvl_pth.exists():
        with open(pth, 'r') as f:
            row_index = 0
            level_data = [l.strip() for l in f]
            for row in range(LEVEL_HEIGHT):
                cell_index = 0
                l = level_data[row]
                for cell in l:
                    level[row_index][cell_index] = int(cell)
                    cell_index += 1
                row_index += 1

# Running
while running:
    # Mouse and Camera coordinates
    c_x, c_y = CameraView.get_pos()
    c_x = int(c_x)
    c_y = int(c_y)
    mx, my = utilityfuncs.mouse_xy_transformation(draw_dest, game_screen.screen)

    for event in pygame.event.get():
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
                                save_level(level, n[0])
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
            if level[i][j] != 0:
                # pygame.draw.rect(draw_dest, (75, 75, 75), (j * c_dimensions-_x, i * c_dimensions-_y, c_dimensions, c_dimensions))
                curr_tile = LEVEL_TILES[level[i][j]]
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
                    pygame.draw.rect(draw_dest, (255, 0, 255), img_rect, width=1)
                else:
                    pygame.draw.rect(draw_dest, (255, 0, 255), img_rect)
            draw_dest.blit(image, img_rect)
        SW = settings.WINDOW_WIDTH

        for index, tile in LEVEL_TILES.items():
            tx, ty = SW - 16, (index + 1) * 16
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
        if tool_mode == "Pencil":
            if pygame.mouse.get_pressed()[0]:
                level[_y][_x] = current_sprite
            elif pygame.mouse.get_pressed()[2]:
                level[_y][_x] = 0
        elif tool_mode == "Bucket":
            if pygame.mouse.get_pressed()[0]:
                utilityfuncs.flood_fill(_x, _y, level, current_sprite, level[_y][_x])
        elif tool_mode == "Player_Spawn": # setting the player's spawn:
            if pygame.mouse.get_pressed()[0]:
                d = 0
                can_place = True
                for i in range(36):
                    __x, __y = (int((mx + math.cos(math.radians(d))*10 + c_x * c_dimensions)/c_dimensions),
                                int((my - math.cos(math.radians(d))*10 + c_y * c_dimensions)/c_dimensions))
                    if level[__y][__x] != 0:
                        can_place = False

                    __x, __y = (int((mx + math.cos(math.radians(d)) * 5 + c_x * c_dimensions) / c_dimensions),
                                int((my - math.cos(math.radians(d)) * 5 + c_y * c_dimensions) / c_dimensions))
                    if level[__y][__x] != 0:
                        can_place = False

                    d += 10
                if can_place:
                    Entities.player_spawn_point = (mx + c_x * c_dimensions, my + c_y * c_dimensions)

    if Entities.player_spawn_point != (None, None):
        sp = Entities.player_spawn_point
        pygame.draw.circle(draw_dest, (255, 165, 0), (sp[0]-c_x*c_dimensions, sp[1]-c_y*c_dimensions), 2)
        pygame.draw.circle(draw_dest, (255, 0, 0), (sp[0]-c_x*c_dimensions, sp[1]-c_y*c_dimensions), 10, width=1)

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


# Tried out some Git