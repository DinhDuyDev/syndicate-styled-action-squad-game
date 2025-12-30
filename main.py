# Importing all the library in
import weakref
import psutil
import pygame
import decorations
import map
import player_enemies
import screen
import settings
import player_enemies as p
import tiles
import utilityfuncs
import camera
import Bullet
import effects
import deletor
import entities

###########################
# Initializing everything #
###########################

pygame.init()
pygame.font.init()

for fnt in pygame.font.get_fonts():
    print(fnt)

#####################
# UI / Screen setup #
#####################

game_screen = screen.Screen(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
draw_dest = game_screen.screen.copy()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 10)
big_font = pygame.font.SysFont("Courier New", 50)
ingame_font = pygame.font.SysFont("Arial", 7)

class GameVariables:
    running = True
    debug_mode = False
    GAME_FPS = 60

class Performance:
    MAX_FPS = -100000
    MIN_FPS = 999999

class UserInterface:
    ui_offset = 0
    squad_ui_used = False
##########
# Player #
##########
man1 = p.SquadMan((-1000, -1000))
man2 = p.SquadMan((-1000, -1000))
man3 = p.SquadMan((-1000, -1000))
man4 = p.SquadMan((-1000, -1000))

##########
# Camera #
##########
gameCamera = camera.Camera()

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

    # Draw stack
    draw_stack:list[decorations.all_decoration_types | player_enemies.all_enemies_type | player_enemies.SquadMan] = []#entities.SquadMan.squad_list + all_entities + all_miscellaneous_objects

# Very shaky level loading mechanism
def load_level(index: int):
    map.GameMap.set_level(index)
    # Geometry
    LoadedScene.loaded_map = [[0 for x in range(settings.hor_cells)] for y in range(
        settings.ver_cells)] if new_map else map.GameMap.get_map().get_level_matrix()

    # COMPOSITION
    player_enemies.MAP_GEOMETRY = LoadedScene.loaded_map
    entities.MAP_GEOMETRY = LoadedScene.loaded_map

    # Loading current map data, like misc (decorations) objects
    curr_map = map.GameMap.get_map()
    LoadedScene.current_map = map.GameMap.get_map()
    LoadedScene.loaded_miscellaneous = curr_map.all_miscellaneous_objects()
    LoadedScene.all_miscellaneous_objects.clear()
    player_enemies.enemy_list.clear()

    # Player
    spawn_xy = LoadedScene.current_map.get_spawn_point()
    for sq in player_enemies.SquadMan.squad_list:
        sq.x, sq.y = spawn_xy[0], spawn_xy[1]
    player_enemies.move_squad(spawn_xy[0], spawn_xy[1], LoadedScene.loaded_map)

    # Camera
    spawn_xy = map.GameMap.get_map().get_spawn_point()
    gameCamera.offset_x = int((spawn_xy[0] - settings.WINDOW_WIDTH / (2 * settings.zoom)) / settings.cell_dimension)
    gameCamera.offset_y = int((spawn_xy[1] - settings.WINDOW_HEIGHT / (2 * settings.zoom)) / settings.cell_dimension)

    # LoadedScene.all_enemies.clear()
    loaded_miscellaneous = curr_map.all_miscellaneous_objects()
    loaded_enemies = curr_map.all_enemies()

    # Loading Miscellaneous Objects
    for x in loaded_miscellaneous:
        if x != "":
            LoadedScene.all_miscellaneous_objects.append(decorations.get_miscellaneous_objects(x))

    # Loading Miscellaneous Objects
    for x in loaded_enemies:  # Loaded
        if x != "":
            player_enemies.get_enemies(x)
        # e.references.append(LoadedScene.all_enemies)
        # LoadedScene.all_enemies.append(e)


load_level(0)

# Memory
process = psutil.Process()

all_enemy_refs = [
    weakref.ref(e) for e in player_enemies.enemy_list
]

# Game Tiles
LEVEL_TILES = tiles.get_tiles()

# Mouse Clicking
class user_input:
    mouse_pressed = False
    key_pressed = False

def debug_information():
    if pygame.key.get_pressed()[pygame.K_TAB]:
        curr_fps = clock.get_fps()
        pygame.draw.rect(draw_dest, (255, 0, 0), (0, 0, 32, 4))
        pygame.draw.rect(draw_dest, (0, 255, 0), (0, 0, 32 * (clock.get_fps() / 60), 4))

        # Max FPS
        if curr_fps > Performance.MAX_FPS:
            Performance.MAX_FPS = curr_fps
        if curr_fps < Performance.MIN_FPS:
            Performance.MIN_FPS = curr_fps

        max_fps = font.render(f"max fps: {Performance.MAX_FPS}", False, (255, 255, 255))
        min_fps = font.render(f"min fps: {Performance.MIN_FPS}", False, (255, 255, 255))
        max_rect = max_fps.get_rect(topleft=(0, 8))
        min_rect = min_fps.get_rect(topleft=(0, 16))
        draw_dest.blit(max_fps, max_rect)
        draw_dest.blit(min_fps, min_rect)
        # load_level(not map.GameMap.level)
    else:
        # MEMORY:
        memory_amount = font.render(f"{psutil.Process().memory_info().rss / 1024 ** 2}", False, (255, 255, 255))
        memory_rect = memory_amount.get_rect(topleft=(0, 0))
        draw_dest.blit(memory_amount, memory_rect)

def squad_information_ui():
    ww, wh = settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT
    pygame.draw.rect(draw_dest, (128, 128, 128), (0, 0, ww/8, wh/2))
    ind = 0
    for i in range(2):
        for j in range(2):
            ind += 1
            pygame.draw.rect(draw_dest, (50, 50, 50), (j * ww/16, i * wh/4, ww/16, wh/4), width=2)
            pygame.draw.rect(draw_dest, (0, 0, 0), (j * ww / 16-2, i * wh / 4-2, ww / 16, wh / 4), width=1)
            center = (j * ww/16+ww/32, i * wh/4+wh/8)
            number = big_font.render(str(ind), False, (170, 170, 170))
            number_rect = number.get_rect(center=center)
            draw_dest.blit(number, number_rect)
            if ind-1 < len(player_enemies.SquadMan.squad_list):
                sq_member = player_enemies.SquadMan.squad_list[ind-1]
                sq_member.render(draw_dest, center[0], center[1], show_stats=True)
# All Screens:
# - Title Screen
# - Menu / Selection Screen
# - Options Screen
# - Audio / Selections Screen
# - Level
def game():
    while GameVariables.running:
        # Title Screen
        # Menu / Selection Screen
        # Option Screen
        # Audio / Selections Screen
        # Level
        in_level()

        # Performance
        if GameVariables.debug_mode:
            debug_information()
        else:
            # 640x360 screen
            # 1/4 of the screen
            # if pygame.key.get_pressed()[pygame.K_TAB]:
            #     UserInterface.squad_ui_used = True
            # else:
            #     UserInterface.squad_ui_used = False
            UserInterface.squad_ui_used = True
            if UserInterface.squad_ui_used:
                squad_information_ui()

        # Resizing Screen
        game_screen.screen.blit(pygame.transform.scale_by(pygame.transform.scale(draw_dest, game_screen.get_dimensions()), settings.zoom), (gameCamera.camera_shake_vector(), gameCamera.camera_shake_vector()))
        pygame.display.flip()
        clock.tick(GameVariables.GAME_FPS)

def in_level():
    ####################
    # ORDERING SPRITES #
    ####################
    LoadedScene.draw_stack.clear()
    LoadedScene.draw_stack = player_enemies.SquadMan.squad_list + player_enemies.enemy_list + LoadedScene.all_miscellaneous_objects
    LoadedScene.draw_stack.sort()

    c_x, c_y = gameCamera.get_pos()
    c_x = int(c_x)
    c_y = int(c_y)
    mx, my = utilityfuncs.mouse_xy_transformation(draw_dest, game_screen.screen)

    # UI Interaction
    can_click = True
    if UserInterface.squad_ui_used:
        if mx < settings.WINDOW_WIDTH/8:
            can_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            GameVariables.running = False
        elif event.type == pygame.KEYDOWN and can_click:
            if event.key == pygame.K_SPACE:
                squad_man = player_enemies.SquadMan.squad_list
                if player_enemies.SquadMan.nums_active() != 4:
                    for sq in squad_man:
                        sq.being_used = True
                else:
                    for sq in squad_man:
                        sq.being_used = False

    ####################################
    # EVERYTHING INTERACTING WITH GAME #
    ####################################
    if can_click:
        if not pygame.mouse.get_pressed()[0]:
            user_input.mouse_pressed = False

        if pygame.mouse.get_pressed()[0] and not user_input.mouse_pressed:
            clicking_on_player = False
            _x = c_x * settings.cell_dimension
            _y = c_y * settings.cell_dimension
            # Interacting with the player squad
            for sq in player_enemies.SquadMan.squad_list:
                sq_rect = pygame.Rect(sq.x-4-_x, sq.y-9-_y, 8, 16)#sq.sprite.get_current_image().get_rect(center=(sq.xy()[0] - _x, sq.xy()[1] - _y))
                if sq_rect.collidepoint(mx, my):
                    clicking_on_player = True
                    sq.being_used = not sq.being_used

            user_input.mouse_pressed = True
            if not clicking_on_player:
                if LoadedScene.loaded_map[int(my/settings.cell_dimension)+c_y][int(mx/settings.cell_dimension)+c_x] == 0:
                    p.move_squad(mx+_x, my+_y, LoadedScene.loaded_map)

        # Selecting soldiers individually
        all_soldiers_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
        squad_list = player_enemies.SquadMan.squad_list
        any_keys_being_pressed = False
        for i in range(len(all_soldiers_keys)):
            if pygame.key.get_pressed()[i]:
                any_keys_being_pressed = True

        if not any_keys_being_pressed:
            user_input.key_pressed = False
        for i in range(len(squad_list)):
            squad_man = player_enemies.SquadMan.squad_list
            if not user_input.key_pressed:
                if pygame.key.get_pressed()[all_soldiers_keys[i]]:
                    user_input.key_pressed = True
                    squad_man[i].being_used = True
                    for j in range(len(squad_list)):
                        if j != i:
                            squad_man[j].being_used = False

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

    # Drawing blood splatters
    for blood_splots in effects.BloodSplot.all_blood_splots:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        blood_splots.render(draw_dest, blood_splots.x-_x, blood_splots.y-_y)

    # Drawing everything else
    for scene_points in LoadedScene.draw_stack:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        scene_points.render(draw_dest, scene_points.x-_x, scene_points.y-_y)


    # Squad
    player_enemies.SquadMan.make_footsteps()
    for sq in player_enemies.SquadMan.squad_list:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        col = (255, 0, 0)
        if sq.being_used:
            col = (58, 255, 0)
        num = ingame_font.render(str(player_enemies.SquadMan.squad_list.index(sq)+1), False, col)
        num_rect = num.get_rect(center=(sq.x-_x, sq.y-_y-16))
        draw_dest.blit(num, num_rect)
        md_dir = utilityfuncs.point_direction(sq.x-_x, sq.y-_y, mx, my)
        sq.action(LoadedScene.loaded_map)
        sq.firing(md_dir)
        sq.check_death()

    # All enemies
    for e in player_enemies.enemy_list:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        # enemy_state = font.render(str(e.state), False, (255, 0, 0))
        # rect = enemy_state.get_rect(center=(e.x-_x, e.y-_y-16))
        # draw_dest.blit(enemy_state, rect)
        e.action()
        e.check_death()

    # All entities
    for ent in entities.all_entities:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        ent.action()
        ent.render(draw_dest, ent.x-_x, ent.y-_y)

    # Bullets
    for bullet in Bullet.PlayerBullet.all_bullets:
        if isinstance(bullet.spawner, player_enemies.SquadMan):
            bullet.work(LoadedScene.loaded_map, player_enemies.enemy_list)
        else:
            bullet.work(LoadedScene.loaded_map, player_enemies.SquadMan.squad_list)

    # Effects
    for eff in effects.all_effects:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        eff.render(draw_dest, eff.x-_x, eff.y-_y)

    # Sounds
    for snd in entities.SoundSource.all_sounds_sources:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        # For ALL ENEMIES
        for enemy in player_enemies.enemy_list:
            enemy.hear_sound(snd)
        pygame.draw.circle(draw_dest, (255, 0, 0), (snd.x-_x, snd.y-_y), radius=snd.radius,width=2)
        snd.destroy()

    # Anything requesting to be deleted will be deleted here
    deletor.Deleter.delete_all_requests()

    # Center
    if center_scope:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        w = 32
        pygame.draw.line(draw_dest, (255, 0, 0), (settings.WINDOW_WIDTH-w-_x-1, settings.WINDOW_HEIGHT-_y-1),
                         (settings.WINDOW_WIDTH+w-_x-1, settings.WINDOW_HEIGHT-_y-1), 2)
        pygame.draw.line(draw_dest, (255, 0, 0), (settings.WINDOW_WIDTH-_x-1, settings.WINDOW_HEIGHT-w-_y-1),
                     (settings.WINDOW_WIDTH-_x-1, settings.WINDOW_HEIGHT+w-_y-1), 2)

    #

if __name__ == "__main__":
    game()

LoadedScene.draw_stack.clear()
print(pygame.display.Info())
for i in all_enemy_refs:
    print(i)
print(player_enemies.enemy_list)

print("--------------------------------")
print("performance report")
print("CPU usage (%):", psutil.cpu_percent(interval=1))

ram = psutil.virtual_memory()
print("RAM usage (%):", ram.percent)
print("RAM used (GB):", round(ram.used / 1e9, 2))
pygame.quit()
