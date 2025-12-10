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

###########################
# Initializing everything #
###########################

pygame.init()
pygame.font.init()

#####################
# UI / Screen setup #
#####################

game_screen = screen.Screen(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
draw_dest = game_screen.screen.copy()
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 10)

#######
# Map #
#######
new_map = False
center_scope = False

#########################################
### ALL THINGS FROM THE LOADED SCENES ###
#########################################
class LoadedScene:
    loaded_map: list[list[int]]|None = None
    current_map = None

    # Game Miscellaneous Objects
    loaded_miscellaneous = None
    all_miscellaneous_objects: list[decorations.all_decoration_types] = []
    all_entities: list[entities.all_entities_types] = [] # Doesn't include the player

    # Draw stack
    draw_stack:list[decorations.all_decoration_types|entities.all_entities_types] = []#entities.SquadMan.squad_list + all_entities + all_miscellaneous_objects

# Very shaky level loading mechanism
def load_level(index: int):
    map.GameMap.set_level(index)
    # Geometry
    LoadedScene.loaded_map = [[0 for x in range(settings.hor_cells)] for y in range(
        settings.ver_cells)] if new_map else map.GameMap.get_map().get_level_matrix()

    # Other Map Data
    curr_map = map.GameMap.get_map()
    LoadedScene.current_map = map.GameMap.get_map()
    LoadedScene.loaded_miscellaneous = curr_map.all_miscellaneous_objects()
    LoadedScene.all_miscellaneous_objects.clear()
    LoadedScene.all_entities.clear()
    loaded_miscellaneous = curr_map.all_miscellaneous_objects()
    loaded_entities = curr_map.all_entities()

    for x in loaded_miscellaneous:
        LoadedScene.all_miscellaneous_objects.append(misc_objs_gen.get_miscellaneous_objects(x))

    for x in loaded_entities:  # This is just the enemies by the
        LoadedScene.all_entities.append(entities_gen.get_entities(x))

# load_level(0)
# load_level(1)

load_level(0)
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
    ####################
    # ORDERING SPRITES #
    ####################
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

        ####################################
        # EVERYTHING INTERACTING WITH GAME #
        ####################################
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

    ###############
    # ALL CAMERAS #
    ###############
    gameCamera.action()

    ##############
    # BACKGROUND #
    ##############
    draw_dest.fill((50, 50, 50))

    #######################
    # RENDERING THE LEVEL #
    #######################
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
    entities.SquadMan.make_footsteps()
    for sq in entities.SquadMan.squad_list:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        # sq_rect = sq.sprite.get_current_image().get_rect(center=(sq.xy()[0] - _x, sq.xy()[1] - _y))
        # pygame.draw.rect(draw_dest, (255, 255, 255), sq_rect)
        # sq.render(draw_dest, sq.xy()[0]-_x, sq.xy()[1]-_y)
        md_dir = utilityfuncs.point_direction(sq.xy()[0]-_x, sq.xy()[1]-_y, mx, my)
        sq.action(LoadedScene.loaded_map)
        sq.firing(md_dir)
        sq.check_death()
        # health_text = font.render(str(sq.hp), False, (255, 0, 0))
        # health_rect = health_text.get_rect(center=(sq.xy()[0]-_x, sq.xy()[1]-6-_y))
        # draw_dest.blit(health_text, health_rect)

    # Entities are enemies and other environmental stuffs
    # So this part is activating for all entities, not just enemies alone
    for ent in LoadedScene.all_entities:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        ent.action(LoadedScene.loaded_map)
        ent.check_death(LoadedScene.all_entities)
        state = font.render(f"{ent.state}", False, (255, 0, 0))
        state_rect = state.get_rect(center=(ent.x-_x, ent.y-_y-16))
        draw_dest.blit(state, state_rect)

    # Bullets
    for bullet in Bullet.PlayerBullet.all_bullets:
        if isinstance(bullet.spawner, entities.SquadMan):
            bullet.work(LoadedScene.loaded_map, entities.EnemyMobster.EnemyList)
        else:
            bullet.work(LoadedScene.loaded_map, entities.SquadMan.squad_list)

    # Effects
    for eff in effects.all_effects:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        eff.render(draw_dest, _x, _y)

    # Sounds
    for snd in effects.SoundSource.all_sounds_sources:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        # For ALL ENEMIES
        for enemy in entities.EnemyMobster.EnemyList:
            enemy.hear_sound(snd)
        pygame.draw.circle(draw_dest, (255, 0, 0), (snd.x-_x, snd.y-_y), radius=snd.radius,width=2)
        snd.destroy()

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
    game_screen.screen.blit(pygame.transform.scale_by(pygame.transform.scale(draw_dest, game_screen.get_dimensions()), settings.zoom), (gameCamera.camera_shake_vector(), gameCamera.camera_shake_vector()))

    pygame.display.flip()
    clock.tick(60)

print(pygame.display.Info())