# Importing all the library in
import pygame

import decorations
import map
import player
import screen
import settings
import player as p
import tiles
import utilityfuncs
import camera
import misc_objs_gen
pygame.init()
pygame.font.init()

# UI / Screen setup
game_screen = screen.Screen(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
draw_dest = game_screen.screen.copy()
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 10)

# Map
new_map = False
center_scope = True
class LoadedScene:
    loaded_map:list[list[int]] = [[0 for x in range(settings.hor_cells)] for y in range(settings.ver_cells)] if new_map else map.GameMap.get_map().get_level_matrix()
    current_map = map.GameMap.get_map()
    # Game Miscellaneous Objects
    loaded_miscellaneous = current_map.all_miscellaneous_objects()
    all_miscellaneous_objects: list[decorations.all_decoration_types] = []
    for x in loaded_miscellaneous:
        all_miscellaneous_objects.append(misc_objs_gen.get_miscellaneous_objects(x))

spawn_xy = LoadedScene.current_map.get_spawn_point()

man1 = p.SquadMan(spawn_xy)
man2 = p.SquadMan(spawn_xy)
man3 = p.SquadMan(spawn_xy)
man4 = p.SquadMan(spawn_xy)

# Camera
gameCamera = camera.Camera()
gameCamera.offset_x = int((spawn_xy[0]-settings.WINDOW_WIDTH/(2*settings.zoom))/settings.cell_dimension)
gameCamera.offset_y = int((spawn_xy[1]-settings.WINDOW_HEIGHT/(2*settings.zoom))/settings.cell_dimension)

# Game Tiles
LEVEL_TILES = tiles.get_tiles()

while running:
    c_x, c_y = gameCamera.get_pos()
    c_x = int(c_x)
    c_y = int(c_y)
    mx, my = utilityfuncs.mouse_xy_transformation(draw_dest, game_screen.screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                _x = c_x * settings.cell_dimension
                _y = c_y * settings.cell_dimension
                if LoadedScene.loaded_map[int(my/settings.cell_dimension)+c_y][int(mx/settings.cell_dimension)+c_x] == 0:
                    p.move_squad(mx+_x, my+_y, LoadedScene.loaded_map)

    # Camera
    gameCamera.action()

    draw_dest.fill((25, 25, 25))

    # Grid drawing
    for y in range(settings.ver_cells):
        for x in range(settings.hor_cells):
            # pygame.draw.line(draw_dest, (75, 75, 75),
            #                  (x*settings.cell_dimension, y*settings.cell_dimension),
            #                  (x*settings.cell_dimension+settings.cell_dimension, y*settings.cell_dimension))
            # pygame.draw.line(draw_dest, (75, 75, 75),
            #                  (x * settings.cell_dimension, y * settings.cell_dimension),
            #                  (x * settings.cell_dimension, y * settings.cell_dimension + settings.cell_dimension))
            if LoadedScene.loaded_map[y][x] != 0 and LoadedScene.loaded_map[y][x] != 3:
                _x = x*settings.cell_dimension - c_x * settings.cell_dimension
                _y = y*settings.cell_dimension - c_y * settings.cell_dimension
                # pygame.draw.rect(draw_dest, (75, 75, 75), (_x, _y
                #                                            , settings.cell_dimension, settings.cell_dimension))
                tile_spr = LEVEL_TILES[LoadedScene.loaded_map[y][x]]
                tile_rect = tile_spr.get_rect(topleft=(_x, _y))
                draw_dest.blit(tile_spr, tile_rect)

    # Miscellaneous Objects
    for msc_objs in LoadedScene.all_miscellaneous_objects:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        msc_objs.render(draw_dest, msc_objs.xy()[0]-_x, msc_objs.xy()[1]-_y)

    # Squad
    for sq in player.SquadMan.squad_list:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        sq.render(draw_dest, sq.xy()[0]-_x, sq.xy()[1]-_y)
        sq.action(LoadedScene.loaded_map)

    # Center
    if center_scope:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        w = 32
        pygame.draw.line(draw_dest, (255, 0, 0), (settings.WINDOW_WIDTH-w-_x-1, settings.WINDOW_HEIGHT-_y-1),
                         (settings.WINDOW_WIDTH+w-_x-1, settings.WINDOW_HEIGHT-_y-1), 2)
        pygame.draw.line(draw_dest, (255, 0, 0), (settings.WINDOW_WIDTH-_x-1, settings.WINDOW_HEIGHT-w-_y-1),
                     (settings.WINDOW_WIDTH-_x-1, settings.WINDOW_HEIGHT+w-_y-1), 2)

    # Performance
    if pygame.key.get_pressed()[pygame.K_TAB]:
        pygame.draw.rect(draw_dest, (255, 0, 0), (0, 0, 32, 4))
        pygame.draw.rect(draw_dest, (0, 255, 0), (0, 0, 32 * (clock.get_fps()/60), 4))

    # Resizing Screem
    game_screen.screen.blit(pygame.transform.scale_by(pygame.transform.scale(draw_dest, game_screen.get_dimensions()), settings.zoom), (0, 0))

    pygame.display.flip()
    clock.tick(60)

map.print_map(LoadedScene.loaded_map)
print(pygame.display.Info())