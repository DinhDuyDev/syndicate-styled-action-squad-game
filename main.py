# Importing all the library in
import math
import pygame
import decorations
import entities_gen
import map
import entities
import screen
import settings
import entities as p
import tiles
import utilityfuncs
import camera
import misc_objs_gen
import Bullet
import effects

# Commit Message

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
center_scope = False
class LoadedScene:
    loaded_map: list[list[int]] = [[0 for x in range(settings.hor_cells)] for y in range(
        settings.ver_cells)] if new_map else map.GameMap.get_map().get_level_matrix()
    current_map = map.GameMap.get_map()
    # Game Miscellaneous Objects
    loaded_miscellaneous = current_map.all_miscellaneous_objects()
    all_miscellaneous_objects: list[decorations.all_decoration_types] = []
    all_entities: list[entities.all_entities_types] = []
    loaded_entities = current_map.all_entities()
    for x in loaded_miscellaneous:
        all_miscellaneous_objects.append(misc_objs_gen.get_miscellaneous_objects(x))

    for x in loaded_entities:
        all_entities.append(entities_gen.get_entities(x))

    draw_stack:list[decorations.all_decoration_types|entities.all_entities_types] = entities.SquadMan.squad_list + all_entities + all_miscellaneous_objects


print(LoadedScene.all_entities)
spawn_xy = LoadedScene.current_map.get_spawn_point()

man1 = p.SquadMan(spawn_xy)
man2 = p.SquadMan(spawn_xy)
man3 = p.SquadMan(spawn_xy)
man4 = p.SquadMan(spawn_xy)

entities.move_squad(spawn_xy[0], spawn_xy[1], LoadedScene.loaded_map)

# Camera
gameCamera = camera.Camera()
gameCamera.offset_x = int((spawn_xy[0]-settings.WINDOW_WIDTH/(2*settings.zoom))/settings.cell_dimension)
gameCamera.offset_y = int((spawn_xy[1]-settings.WINDOW_HEIGHT/(2*settings.zoom))/settings.cell_dimension)

# Game Tiles
LEVEL_TILES = tiles.get_tiles()

# Mouse Clicking
class user_mouse:
    mouse_pressed = False
while running:
    LoadedScene.draw_stack.clear()
    LoadedScene.draw_stack = entities.SquadMan.squad_list + LoadedScene.all_entities + LoadedScene.all_miscellaneous_objects
    LoadedScene.draw_stack.sort()
    c_x, c_y = gameCamera.get_pos()
    c_x = int(c_x)
    c_y = int(c_y)
    mx, my = utilityfuncs.mouse_xy_transformation(draw_dest, game_screen.screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            for sq in entities.SquadMan.squad_list:
                if sq.being_used:
                    md_dir = utilityfuncs.point_direction(sq.xy()[0], sq.xy()[1], mx+c_x*settings.cell_dimension, my+c_y*settings.cell_dimension)
                    d = md_dir//45
                    vec_x = math.cos(math.radians(d*45)) * 8
                    vec_y = math.sin(math.radians(d*45)) * 8
                    Bullet.Bullet(sq.xy()[0]+vec_x, sq.xy()[1]-vec_y, md_dir, sq)
                    effects.MuzzleFlash(sq.xy()[0]+vec_x, sq.xy()[1]-vec_y)
                    sq.sprite.set_image_index(d)
                    sq.focused = False

        # Interacting with game
        if pygame.MOUSEBUTTONDOWN:
            if not pygame.mouse.get_pressed()[0]:
                user_mouse.mouse_pressed = False

            if pygame.mouse.get_pressed()[0] and not user_mouse.mouse_pressed:
                clicking_on_player = False
                _x = c_x * settings.cell_dimension
                _y = c_y * settings.cell_dimension
                # Interacting with the player squad
                for sq in entities.SquadMan.squad_list:
                    sq_rect = pygame.Rect(sq.x-2-_x, sq.y-9-_y, 4, 4)#sq.sprite.get_current_image().get_rect(center=(sq.xy()[0] - _x, sq.xy()[1] - _y))
                    if sq_rect.collidepoint(mx, my):
                        print("God given")
                        clicking_on_player = True
                        sq.being_used = not sq.being_used

                user_mouse.mouse_pressed = True
                if not clicking_on_player:
                    if LoadedScene.loaded_map[int(my/settings.cell_dimension)+c_y][int(mx/settings.cell_dimension)+c_x] == 0:
                        p.move_squad(mx+_x, my+_y, LoadedScene.loaded_map)

    # Camera
    gameCamera.action()

    draw_dest.fill((50, 50, 50))

    # Rendering the level
    for y in range(c_y, c_y + settings.ver_cells//2//settings.zoom):#settings.ver_cells):
        for x in range(c_x, c_x + settings.hor_cells//2//settings.zoom):#settings.hor_cells):
            if LoadedScene.loaded_map[y][x] != 0 and LoadedScene.loaded_map[y][x] != 3:
                _x = x*settings.cell_dimension - c_x * settings.cell_dimension
                _y = y*settings.cell_dimension - c_y * settings.cell_dimension

                shadow_surf = pygame.Surface((settings.cell_dimension, settings.cell_dimension))
                shadow_surf.fill((0, 0, 0))
                shadow_surf.set_alpha(127)
                shadow_rect = shadow_surf.get_rect(topleft=(_x+settings.cell_dimension/4, _y+settings.cell_dimension/4))

                tile_spr = LEVEL_TILES[LoadedScene.loaded_map[y][x]]
                tile_rect = tile_spr.get_rect(topleft=(_x, _y))
                draw_dest.blit(shadow_surf, shadow_rect)
                draw_dest.blit(tile_spr, tile_rect)

    for scene_points in LoadedScene.draw_stack:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        scene_points.render(draw_dest, scene_points.xy()[0]-_x, scene_points.xy()[1]-_y)

    # # Miscellaneous Objects
    # for msc_objs in LoadedScene.all_miscellaneous_objects:
    #     _x = c_x * settings.cell_dimension
    #     _y = c_y * settings.cell_dimension
    #     msc_objs.render(draw_dest, msc_objs.xy()[0]-_x, msc_objs.xy()[1]-_y)
    #
    # Squad
    for sq in entities.SquadMan.squad_list:
        # _x = c_x * settings.cell_dimension
        # _y = c_y * settings.cell_dimension
        # sq_rect = sq.sprite.get_current_image().get_rect(center=(sq.xy()[0] - _x, sq.xy()[1] - _y))
        # pygame.draw.rect(draw_dest, (255, 255, 255), sq_rect)
        # sq.render(draw_dest, sq.xy()[0]-_x, sq.xy()[1]-_y)
        sq.action(LoadedScene.loaded_map)
    #
    # Enemy
    for ent in LoadedScene.all_entities:
        # _x = c_x * settings.cell_dimension
        # _y = c_y * settings.cell_dimension
        # ent.render(draw_dest, ent.xy()[0]-_x, ent.xy()[1]-_y)
        ent.action(LoadedScene.loaded_map)

    # Bullets
    for bullet in Bullet.Bullet.all_bullets:
        bullet.work(LoadedScene.loaded_map)

    # Effects
    for eff in effects.all_effects:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        eff.render(draw_dest, eff.x-_x, eff.y-_y)

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

print(pygame.display.Info())