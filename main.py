# Importing all the library in
import math
import weakref
import psutil
import pygame

import colors
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
import ALL_SPRITES
import SlowMo

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
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 10)
big_font = pygame.font.SysFont("Courier New", 50, bold=True)
ingame_font = pygame.font.SysFont("Arial", 7)

ww, wh = settings.WINDOW_WIDTH/settings.zoom, settings.WINDOW_HEIGHT/settings.zoom

class GameVariables:
    running = True
    debug_mode = False#True
    GAME_FPS = 60

class Performance:
    MAX_FPS = -100000
    MIN_FPS = 999999

class UserInterface:
    ui_offset = 0
    can_show_inventory = False
    loaded_inventory = False
    squad_ui_used = False
    index_selected = 0
    holding_item = False

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
# man2.take_damage(1000)
# man3.take_damage(1000)
# man4.take_damage(1000)

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
    player_enemies.MapData.MAP_GEOMETRY = LoadedScene.loaded_map
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
    offset = 4
    curr_fps = clock.get_fps()
    pygame.draw.rect(draw_dest, (255, 0, 0), (0, 0, 32, 4))
    pygame.draw.rect(draw_dest, (0, 255, 0), (0, 0, 32 * (clock.get_fps() / 60), 4))

    # Max FPS
    if Performance.MIN_FPS < 0.5:
        Performance.MIN_FPS = curr_fps
    if curr_fps > Performance.MAX_FPS:
        Performance.MAX_FPS = curr_fps
    if curr_fps < Performance.MIN_FPS:
        Performance.MIN_FPS = curr_fps

    max_fps = font.render(f"max fps: {str(Performance.MAX_FPS)[:5]}", False, (255, 255, 255))
    cur_fps = font.render(f"cur fps: {str(curr_fps)[:5]}", False, (255, 255, 255))
    min_fps = font.render(f"min fps: {str(Performance.MIN_FPS)[:5]}", False, (255, 255, 255))
    max_rect = max_fps.get_rect(topleft=(0, 8+offset))
    cur_rect = cur_fps.get_rect(topleft=(0, 16+offset))
    min_rect = min_fps.get_rect(topleft=(0, 24+offset))
    draw_dest.blit(max_fps, max_rect)
    draw_dest.blit(cur_fps, cur_rect)
    draw_dest.blit(min_fps, min_rect)

    # MEMORY:
    memory_amount = font.render(f"{str(psutil.Process().memory_info().rss / 1024 ** 2)[:6]}", False, (255, 255, 255))
    memory_rect = memory_amount.get_rect(topleft=(0, offset))
    draw_dest.blit(memory_amount, memory_rect)

def squad_information_ui():
    # On top of the screen
    middle_screen = ww/2
    # pygame.draw.line(draw_dest, (255, 255, 255), (middle_screen, 0), (middle_screen, wh))

    # Names
    squad_names = ["Markus", "Hans", "Tish", "Madsen"]
    mx, my = utilityfuncs.mouse_xy_transformation(draw_dest, game_screen.screen)
    squad_ls = player_enemies.SquadMan.squad_list
    for index in range(len(squad_ls)):
        ui_x, ui_y = middle_screen - 68 * (1 - index + 0.5), 8
        squad_member_sprite = squad_ls[index].get_sprite()
        mask_outline = pygame.mask.from_surface(squad_member_sprite)
        mask_surf = mask_outline.to_surface()
        mask_surf.set_colorkey((0,0,0))
        outline_color  = (255, 0, 0)
        if squad_ls[index].being_used:
            outline_color = (0, 255, 0)
        if squad_ls[index].is_dead:
            outline_color = (175, 175, 175)

        # Character and health and names
        name_render = ingame_font.render(squad_names[index], False, outline_color)
        name_rect = name_render.get_rect(midleft=(ui_x+12, ui_y-3))
        draw_dest.blit(name_render, name_rect)

        px_arr = pygame.PixelArray(mask_surf)
        px_arr.replace((255,255,255), outline_color)
        px_arr.close()
        pos = [
            (0, -1),
            (-1, 0), (1, 0),
            (0, 1),
        ]
        for offset in pos:
            draw_dest.blit(mask_surf, mask_surf.get_rect(center=(ui_x-offset[0], ui_y-offset[1])))

        # draw_dest.blit(outline_sprite, outline_sprite.get_rect(center=(64,64)))
        draw_dest.blit(squad_member_sprite, squad_member_sprite.get_rect(center=(ui_x, ui_y)))

        # Statistics (cooldown)
        pygame.draw.rect(draw_dest, (0, 0, 0), (ui_x+12-1, ui_y+3-1, 18, 4), width=2)
        pygame.draw.rect(draw_dest, (10, 10, 10), (ui_x+12, ui_y+3, 16, 2))
        pygame.draw.rect(draw_dest, (255, 255, 255), (ui_x+12, ui_y+3, 16 * squad_ls[index].cooldown_ratio(), 2))

        # Statistics (ammo)
        pygame.draw.rect(draw_dest, (0, 0, 0), (ui_x+12-1, ui_y+8-1, 18, 4), width=2)
        pygame.draw.rect(draw_dest, (10, 10, 10), (ui_x+12, ui_y+8, 16, 2))
        pygame.draw.rect(draw_dest, (55, 63, 12), (ui_x+12, ui_y+8, 16 * squad_ls[index].ammo_ratio(), 2))

        # Statistics (health)
        pygame.draw.rect(draw_dest, (0, 0, 0), (ui_x - 10, ui_y-4, 4, 14), width=2)
        pygame.draw.rect(draw_dest, (0, 255, 0), (ui_x - 9, ui_y-3, 2, 12))
        pygame.draw.rect(draw_dest, (255, 0, 0), (ui_x - 9, ui_y-3, 2, 12 * abs((1-squad_ls[index].health_ratio()))))

    # # Inventory
    if UserInterface.loaded_inventory:
        UserInterface.ui_offset = pygame.math.lerp(UserInterface.ui_offset, 0, 0.2)
    else:
        UserInterface.ui_offset = pygame.math.lerp(UserInterface.ui_offset, wh+16, 0.2)

    if UserInterface.ui_offset > wh:
        UserInterface.can_show_inventory = True

    if UserInterface.ui_offset <= wh:
        ofs = UserInterface.ui_offset
        pygame.draw.rect(draw_dest, (25, 25, 25), (0, ofs, ww, wh))

        # UI Inventory
        if UserInterface.can_show_inventory:
            for item in player_enemies.SquadMan.inventory:
                if item.weapon_name != "None":
                    item.render(draw_dest, item.x, item.y + ofs)
                else:
                    pygame.draw.rect(draw_dest, (0, 0, 0), (0, ofs, 16, 16))

    # Drawing number
    if UserInterface.loaded_inventory:
        # soldier index selected
        selected_index = ingame_font.render(str(UserInterface.index_selected + 1), False, (0, 255, 0))
        selected_index_rect = selected_index.get_rect(bottomleft=(mx, my))
        draw_dest.blit(selected_index, selected_index_rect)


# # =====================================================================
def game():
    while GameVariables.running:
        # for event in pygame.event.get(): # need this to work
        #     if event.type == pygame.QUIT:
        #         GameVariables.running = False

        ###########
        # EXITING #
        ###########
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            GameVariables.running = False

        ##############
        # BACKGROUND #
        ##############
        draw_dest.fill((50, 50, 50))

        # Title Screen
        # Menu Selection Screen
        # Option Screen
        # Audio Selections Screen
        # Level
        in_level()

        # Performance
        if GameVariables.debug_mode:
            debug_information()
        else:
            # 640x360 screen
            # 1/4 of the screen
            squad_information_ui()

        # Anything requesting to be deleted will be deleted here
        deletor.Deleter.delete_all_requests()

        # Resizing Screen
        game_screen.screen.blit(pygame.transform.scale_by(pygame.transform.scale(draw_dest, game_screen.get_dimensions()), settings.zoom), (gameCamera.camera_shake_vector(), gameCamera.camera_shake_vector()))
        pygame.display.flip()
        clock.tick(GameVariables.GAME_FPS)

# =====================================================================

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
    can_click = True and (not UserInterface.loaded_inventory)
    if UserInterface.squad_ui_used:
        if mx < settings.WINDOW_WIDTH/8:
            can_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            GameVariables.running = False
        elif event.type == pygame.KEYDOWN and can_click:
            if event.key == pygame.K_SPACE:
                squad_man = player_enemies.SquadMan.squad_list
                if player_enemies.SquadMan.nums_active() != player_enemies.SquadMan.nums_alive():
                    for sq in squad_man:
                        sq.being_used = True
                else:
                    for sq in squad_man:
                        sq.being_used = False
            else:
                if not UserInterface.loaded_inventory:
                    # Selecting soldiers individually
                    all_soldiers_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
                    squad_list = player_enemies.SquadMan.squad_list
                    # If UI is opened
                    for i in range(len(squad_list)):
                        squad_man = player_enemies.SquadMan.squad_list
                        if pygame.key.get_pressed()[all_soldiers_keys[i]]:
                            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                                squad_man[i].being_used = not squad_man[i].being_used
                            else:
                                squad_man[i].being_used = True
                                for j in range(len(squad_man)):
                                    if j != i:
                                        squad_man[j].being_used = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            middle_x = ww/2
            sq_ls = player_enemies.SquadMan.squad_list
            width = 24
            for index in range(4):
                ui_x, ui_y = middle_x - 68 * (1 - index + 0.5), 8
                hitbox = pygame.Rect(ui_x-width/2, ui_y-width/2, width, width)
                if hitbox.collidepoint(mx, my):
                    if not sq_ls[index].is_dead:
                        sq_ls[index].being_used = not sq_ls[index].being_used
                        pygame.draw.rect(draw_dest, (255, 0, 0), hitbox)


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
                print(f"Picked point: {LoadedScene.loaded_map[int(my/settings.cell_dimension)+c_y][int(mx/settings.cell_dimension)+c_x]}", end=" -> ")
                if LoadedScene.loaded_map[int(my/settings.cell_dimension)+c_y][int(mx/settings.cell_dimension)+c_x] in tiles.TRAVERSABLE_TILES:
                    print("Traversable")
                    p.move_squad(mx+_x, my+_y, LoadedScene.loaded_map)

    if UserInterface.loaded_inventory:
        # Clicking on the weapons
        all_soldiers_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
        for key_index in range(len(all_soldiers_keys)):
            if pygame.key.get_pressed()[all_soldiers_keys[key_index]]:
                if not player_enemies.SquadMan.squad_list[key_index].is_dead:
                    UserInterface.index_selected = key_index

        for item in player_enemies.SquadMan.inventory:
            item_rect = item.hitbox()
            touching_hitbox = item_rect.collidepoint(mx, my)
            item_is_not_used = not item.being_used
            pressing_mouse = pygame.mouse.get_pressed()[0]
            selectee_is_alive = not player_enemies.SquadMan.squad_list[UserInterface.index_selected].is_dead
            if selectee_is_alive and pressing_mouse and touching_hitbox and item_is_not_used:
                player_enemies.SquadMan.squad_list[UserInterface.index_selected].select_item(item)
                UserInterface.holding_item = True
                deletor.Deleter.request_delete(item, player_enemies.SquadMan.inventory)

    if not pygame.key.get_pressed()[pygame.K_TAB]:
        user_input.key_pressed = False

    if pygame.key.get_pressed()[pygame.K_TAB] and not user_input.key_pressed and UserInterface.can_show_inventory:
        UserInterface.loaded_inventory = not UserInterface.loaded_inventory
        user_input.key_pressed = True


    ###############
    # ALL CAMERAS #
    ###############
    gameCamera.action()

    #######################
    # RENDERING THE LEVEL #
    #######################
    for y in range(c_y, c_y + settings.ver_cells//2//settings.zoom):#settings.ver_cells):
        for x in range(c_x, c_x + settings.hor_cells//2//settings.zoom):#settings.hor_cells):
            if LoadedScene.loaded_map[y][x] not in tiles.INVISIBLE_TILES:
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

    #########
    # Logic #
    #########

    # Slow Motion
    SlowMo.SlowMo.slow_motion()

    # Squad
    player_enemies.SquadMan.make_footsteps()
    for sq in player_enemies.SquadMan.squad_list:
        if not sq.is_dead:
            _x = c_x * settings.cell_dimension
            _y = c_y * settings.cell_dimension
            col = (255, 0, 0)
            if sq.being_used:
                col = (58, 255, 0)
            num = ingame_font.render(str(player_enemies.SquadMan.squad_list.index(sq)+1), False, col)
            num_rect = num.get_rect(center=(sq.x-_x, sq.y-_y-16))
            draw_dest.blit(num, num_rect)
            md_dir = utilityfuncs.point_direction(sq.x-_x, sq.y-_y, mx, my)
            sq.action()
            sq.firing(md_dir)
            sq.check_death()

    # All enemies
    for e in player_enemies.enemy_list:
        _x = c_x * settings.cell_dimension
        _y = c_y * settings.cell_dimension
        # enemy_state = ingame_font.render(str(e.state), False, (255, 0, 0))
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
    if GameVariables.debug_mode:
        debug_information()
    else:
        # 640x360 screen
        # 1/4 of the screen
        squad_information_ui()

if __name__ == "__main__":
    game()

print("======== Video Information ========\n", pygame.display.Info())

print("======== Enemy Information ========")
for i in all_enemy_refs:
    print(i)

print("--------------------------------")
print("performance report")
print("CPU usage (%):", psutil.cpu_percent(interval=1))

ram = psutil.virtual_memory()
print("RAM usage (%):", ram.percent)
print("RAM used (GB):", round(ram.used / 1e9, 2))
pygame.quit()
