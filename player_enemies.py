import pygame
import math

import ALL_SPRITES
import pathfind
import settings
import utilityfuncs
import Sprites
import random
import Weapons
import Bullet
import effects
import camera
import deletor
import entities

WEAPONS_REF = Weapons.WEAPONS_REF
MAP_GEOMETRY:list[list[int]] = []

# Enemy mobster
enemy_list = []

def gen_all_sprites():
    return {
        "Pistol" : Sprites.Sprite(
            (
                "MOBSTER_TORSO_0PISTOL",
                "MOBSTER_TORSO_45PISTOL",
                "MOBSTER_TORSO_90PISTOL",
                "MOBSTER_TORSO_135PISTOL",
                "MOBSTER_TORSO_180PISTOL",
                "MOBSTER_TORSO_225PISTOL",
                "MOBSTER_TORSO_270PISTOL",
                "MOBSTER_TORSO_315PISTOL",
            )
        ),
        "Shotgun" : Sprites.Sprite(
            (
                "MOBSTER_TORSO_0SHOTGUN",
                "MOBSTER_TORSO_45SHOTGUN",
                "MOBSTER_TORSO_90SHOTGUN",
                "MOBSTER_TORSO_135SHOTGUN",
                "MOBSTER_TORSO_180SHOTGUN",
                "MOBSTER_TORSO_225SHOTGUN",
                "MOBSTER_TORSO_270SHOTGUN",
                "MOBSTER_TORSO_315SHOTGUN",
            )
        ),
        "Thompson" : Sprites.Sprite(
            (
                "MOBSTER_TORSO_0THOMPSON",
                "MOBSTER_TORSO_45THOMPSON",
                "MOBSTER_TORSO_90THOMPSON",
                "MOBSTER_TORSO_135THOMPSON",
                "MOBSTER_TORSO_180THOMPSON",
                "MOBSTER_TORSO_225THOMPSON",
                "MOBSTER_TORSO_270THOMPSON",
                "MOBSTER_TORSO_315THOMPSON",
            )
        ),
        "Bar" : Sprites.Sprite(
            (
                "MOBSTER_TORSO_0BAR",
                "MOBSTER_TORSO_45BAR",
                "MOBSTER_TORSO_90BAR",
                "MOBSTER_TORSO_135BAR",
                "MOBSTER_TORSO_180BAR",
                "MOBSTER_TORSO_225BAR",
                "MOBSTER_TORSO_270BAR",
                "MOBSTER_TORSO_315BAR",
            )
        ),
        "GrenadeLauncher" : Sprites.Sprite(
            (
                "SOLDIER_0_GLAUNCHER",
                "SOLDIER_45_GLAUNCHER",
                "SOLDIER_90_GLAUNCHER",
                "SOLDIER_135_GLAUNCHER",
                "SOLDIER_180_GLAUNCHER",
                "SOLDIER_225_GLAUNCHER",
                "SOLDIER_270_GLAUNCHER",
                "SOLDIER_315_GLAUNCHER",
            )
        ),
        "LEGS" : Sprites.Sprite(
            (
                "SOLDIER_LEGS_LEFT",
                "SOLDIER_LEGS_RIGHT",
                "SOLDIER_LEGS_NORMAL"
            )
        )
    }

def fire_gun(obj, direction):
    obj.cooldown += 1
    if obj.cooldown > obj.get_weapon().fire_cooldown:
        base_ref = WEAPONS_REF[obj.current_weapon_name].damage
        total_damage = base_ref
        md_dir = direction
        d = md_dir // 45
        vec_x = math.cos(math.radians(d * 45)) * 8
        vec_y = math.sin(math.radians(d * 45)) * 8

        wep = obj.get_weapon()

        for i in range(wep.pellets):
            _damage = wep.damage
            total_damage += _damage
            _inaccuracies = wep.inaccuracy
            _lives = wep.lives
            _projectile_type = wep.projectile_type
            _create_ray = wep.create_ray
            if _projectile_type == "GRENADE":
                entities.Grenade(obj.x+vec_x, obj.y - vec_y, md_dir, SquadMan.squad_list + enemy_list)
            else:
                Bullet.PlayerBullet(obj.xy()[0] + vec_x, obj.xy()[1] - vec_y, md_dir, obj, damage=_damage,
                                    deviation=_inaccuracies, lives=_lives, create_ray=_create_ray)
                effects.MuzzleFlash(obj.xy()[0] + vec_x, obj.xy()[1] - vec_y)

        entities.SoundSource(obj.xy()[0], obj.xy()[1], (total_damage / 20) * 30)
        obj.sprite.set_image_index(d)
        shake_factor = total_damage / 20
        camera.Camera.activeCam.screen_shake(shake_factor * 3)
        obj.knockback((total_damage / 50) ** 0.8 + random.randint(1, 2), direction + 180)
        obj.cooldown = 0

def switch_sprite(obj):
    if obj.current_weapon_name == "Pistol" or obj.current_weapon_name == "Revolver":
        obj.sprite = obj.pistol_sprite
    elif obj.current_weapon_name == "Shotgun":
        obj.sprite = obj.shotgun_sprite
    elif obj.current_weapon_name == "Thompson":
        obj.sprite = obj.thompson_sprite
    elif obj.current_weapon_name == "Bar":
        obj.sprite = obj.bar_sprite
    elif obj.current_weapon_name == "GrenadeLauncher":
        obj.sprite = obj.grenade_sprite

class SquadMan:
    MAX_SQUAD = 4
    squad_list:list = []
    squad_footstep_counter = 0
    @classmethod
    def nums_active(cls):
        nums = 0
        for i in SquadMan.squad_list:
            if i.being_used:
                nums += 1
        return nums
    @classmethod
    def make_footsteps(cls):
        spd_modifier = (2-SquadMan.nums_active()/4) * 1.25
        if SquadMan.squad_footstep_counter >= 30 * (1/spd_modifier):
            for e in SquadMan.squad_list:
                if e.being_used and len(e.move_path) != 0:
                    entities.SoundSource(e.x, e.y, 10 * (6 / spd_modifier ** 2)) # Making footstep noises
                    break
            SquadMan.squad_footstep_counter = 0
        else:
            SquadMan.squad_footstep_counter += 1

    def __init__(self, loc:tuple[float, float]):
        self.x, self.y = loc
        self.max_hp = 100
        self.hp = self.max_hp
        self.dest_x = self.x
        self.dest_y = self.y

        all_sprs = gen_all_sprites()

        self.references = []

        self.pistol_sprite = all_sprs["Pistol"]
        self.shotgun_sprite = all_sprs["Shotgun"]
        self.thompson_sprite = all_sprs["Thompson"]
        self.bar_sprite = all_sprs["Bar"]
        self.grenade_sprite = all_sprs["GrenadeLauncher"]

        self.leg_normal_sprite = all_sprs["LEGS"]

        self.leg_crouch_sprite = Sprites.Sprite(
            (
                "MOBSTER_LEG_CROUCHING_LEFT",
                "MOBSTER_LEG_CROUCHING_RIGHT",
                "MOBSTER_LEG_CROUCHING_RIGHT"
            )
        )
        self.leg_sprite = self.leg_normal_sprite

        self.crouching = False # Crouching enemy
        self.sprite = self.pistol_sprite
        self.frames = 0
        self.move_path = []
        self.focused = True # so that they look at where they're going
        self.being_used = True

        self.knock_back_strength = 0
        self.knock_back_dir = 0

        self.current_weapon_name = "Thompson"#random.choice(["Shotgun", "Revolver", "Pistol", "Thompson", "Bar", "GrenadeLauncher"])
        self.current_weapon = WEAPONS_REF[self.current_weapon_name]

        self.cooldown = 0
        self.cooldown_steps = 0

        SquadMan.squad_list.append(self)

    def set_dest(self, x, y, m):
        self.move_path.clear()
        self.dest_x, self.dest_y = x, y
        def conv(val):
            return int(val/settings.cell_dimension)
        self.move_path = pathfind.pathfind(conv(self.x), conv(self.y), conv(self.dest_x), conv(self.dest_y), m)

    def xy(self):
        return self.x, self.y

    def action(self, m:list[list[int]]):
        # self.hp = 115
        if self.knock_back_strength >= 0.001:
            self.knock_back_strength *= 0.9
            self.leg_sprite.set_image_speed(4/30)
        else:
            self.knock_back_strength = 0
        spd_modifier = (2-SquadMan.nums_active()/4) * 1.25

        if len(self.move_path) == 0:
            if utilityfuncs.point_distance(self.dest_x, self.dest_y, self.x, self.y) > 2:
                dir_ = utilityfuncs.point_direction(self.x, self.y, self.dest_x, self.dest_y)
                self.x += math.cos(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * spd_modifier
                self.y -= math.sin(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * spd_modifier
            else:
                self.dest_x, self.dest_y = self.x, self.y
                self.leg_sprite.set_image_index(2)
                self.leg_sprite.set_image_speed(0)
        else:
            x, y = (self.move_path[0][0] * settings.cell_dimension + settings.cell_dimension/2
                        , self.move_path[0][1] * settings.cell_dimension + settings.cell_dimension/2 - 2.5)

            if utilityfuncs.point_distance(self.x, self.y, x, y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, x, y)
                if self.focused:
                    self.sprite.set_image_index(int(dir_/45))
                self.x += math.cos(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * spd_modifier
                self.y -= math.sin(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * spd_modifier
            else:
                m[self.move_path[0][1]][self.move_path[0][0]] = 0
                self.move_path.pop(0)

            self.leg_sprite.run_sprite()
            self.leg_sprite.set_image_speed(4/30)
            if self.leg_sprite.image_index > 2:
                self.leg_sprite.image_index = 0

        # self.hp = 10000
    def render(self, dest:pygame.Surface, x, y):
        # Being used
        vec_x = math.cos(math.radians(self.knock_back_dir)) * self.knock_back_strength
        vec_y = math.sin(math.radians(self.knock_back_dir)) * self.knock_back_strength
        x += vec_x
        y -= vec_y

        self.switch_sprites()
        dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)))
        dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))
        # if self.being_used:
        #     pygame.draw.rect(dest, (0, 255, 255), (x-1, y-7, 2, 2))
        # else:
        #     pygame.draw.rect(dest, (255, 0, 255), (x-1, y-7, 2, 2))

        # Health
        pygame.draw.rect(dest, (255, 0, 0), (x - 5, y - 9, 10, 2))
        pygame.draw.rect(dest, (0, 255, 0), (x - 5, y - 9, 10 * self.hp / self.max_hp, 2))

        pygame.draw.rect(dest, (0, 0, 0), (x - 10, y-3, 2, 13))
        r = self.cooldown / self.get_weapon().fire_cooldown
        pygame.draw.rect(dest, (255, 255, 255), (x - 10, y+10 - 13 * r, 2, 13 * r))

    def take_damage(self, amount, source=None):
        self.hp -= amount

    def check_death(self):
        if self.hp < 0:
            self.destroy()

    def destroy(self):
        deletor.Deleter.request_delete(self, SquadMan.squad_list)
        for l in self.references:
            deletor.Deleter.request_delete(self, l)

    def switch_sprites(self):
        switch_sprite(self)

    def firing(self, direction):
        if self.being_used:
            if pygame.key.get_pressed()[pygame.K_e] or pygame.mouse.get_pressed()[2]:
                fire_gun(self, direction)

    def knockback(self, strength, knock_dir):
        self.knock_back_dir = knock_dir
        self.knock_back_strength = strength

    def get_weapon(self):
        return self.current_weapon

    def get_weapon_name(self):
        return self.current_weapon_name

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

def move_squad(x, y, m):
    sq_ls = SquadMan.squad_list
    num_active = SquadMan.nums_active() if SquadMan.nums_active() > 0 else 1
    map_width = len(m[0])
    map_height = len(m)
    d = 45
    dist_travel = 7 * (num_active / SquadMan.MAX_SQUAD)

    for sq_m in sq_ls:
        if sq_m.being_used:
            dx, dy = x + math.cos(math.radians(d)) * dist_travel, y - math.sin(math.radians(d)) * dist_travel
            tx = int(dx/settings.cell_dimension)
            ty = int(dy/settings.cell_dimension)
            if 0 <= ty < map_height and 0 <= tx < map_width:
                if m[ty][tx] == 0:
                    sq_m.set_dest(dx, dy, m)
                    sq_m.focused = True
        d +=  360 / num_active


class Enemy:
    def __init__(self, loc:tuple[float, float], exclude=False, weapon_type="Pistol"):
        self.x, self.y = loc
        self.hp = 100
        self.dest_x = self.x
        self.dest_y = self.y
        self.state = "IDLE"

        self.variable_space:list = [0] * 15 # 15 slots for different variables

        self.state_collection = {
            "IDLE",
            "HASTE_AMBUSH",
            "WAIT_AMBUSH",
            "SEARCH",
        }

        self.references = []

        self.inaccuracy_multiplier = 1
        self.surprise_factor = 90

        all_sprs = gen_all_sprites()

        self.pistol_sprite = all_sprs["Pistol"]
        self.shotgun_sprite = all_sprs["Shotgun"]
        self.thompson_sprite = all_sprs["Thompson"]
        self.bar_sprite = all_sprs["Bar"]
        self.grenade_sprite = all_sprs["GrenadeLauncher"]
        self.sprite = self.thompson_sprite

        self.leg_sprite = Sprites.Sprite(
            (
                "MOBSTER_LEG_LEFTUP",
                "MOBSTER_LEG_RIGHTUP",
                "MOBSTER_LEG_NORMAL"
            )
        )

        self.alerted_saw_player = 0

        self.current_weapon_name = weapon_type
        self.current_weapon = WEAPONS_REF[self.current_weapon_name]
        self.frames = 0
        self.move_path = []
        self.faction_color = (255, 0, 0)
        self.exclude = exclude
        self.repr_name = ""

        self.target_x = 0
        self.target_y = 0

        self.front_direction = 0
        self.speed_factor = 1

        self.cooldown = 0
        self.is_firing = False

        self.knock_back_dir = 0
        self.knock_back_strength = 0

        # The sound heard by the enemy
        self.sound_heard:entities.SoundSource|None = None
        if not exclude:
            enemy_list.append(self)

    def set_dest(self, x, y, m):
        self.move_path.clear()
        self.dest_x, self.dest_y = x, y
        def conv(val):
            return int(val/settings.cell_dimension)
        self.move_path = pathfind.pathfind(conv(self.x), conv(self.y), conv(self.dest_x), conv(self.dest_y), m)

    def xy(self):
        return self.x, self.y

    def switch_state(self):
        self.variable_space.clear()

    def seeing_enemy(self, enemies:list, m:list[list[int]]):
        fov = 120
        for e in enemies:
            if utilityfuncs.line_of_sight(self.x, self.y, e.xy()[0], e.xy()[1], m):
                self.target_x = e.xy()[0]
                self.target_y = e.xy()[1]
                direction_to_enemy = utilityfuncs.point_direction(self.x, self.y, e.x, e.y)
                if abs(direction_to_enemy - self.front_direction) < fov/2:
                    return True
        return False

    def enemy_seen(self, enemies:list, m:list[list[int]]):
        for e in enemies:
            if utilityfuncs.line_of_sight(self.x, self.y, e.xy()[0], e.xy()[1], m):
                return e
        return None

    def clear_variable_space(self):
        for i in range(len(self.variable_space)):
            self.variable_space[i] = 0

    def stop_moving(self):
        self.dest_x, self.dest_y = self.x, self.y
        self.move_path.clear()

    def alert_others(self):
        alert_num = 2
        for e in enemy_list:
            if utilityfuncs.point_distance(self.x, self.y, e.x, e.y) < 60 and alert_num > 0:
                if type(self) is type(e):
                    e.target_x = self.target_x
                    e.target_y = self.target_y
                    e.front_direction = utilityfuncs.point_direction(e.x, e.y, e.target_x, e.target_y)
                    e.set_dest(self.target_x, self.target_y, MAP_GEOMETRY) # This works
                    print("Alerted others")
                    alert_num -= 1

    def action(self):
        self.switch_sprites()
        if self.state == "IDLE":
            if self.sound_heard is not None:
                self.state = "DECISION"
                self.clear_variable_space()

            if self.seeing_enemy(SquadMan.squad_list, MAP_GEOMETRY):
                self.state = "ATTACK"
                self.move_path.clear()
                self.cooldown = 0
                self.inaccuracy_multiplier = self.surprise_factor
                self.clear_variable_space()
                self.alerted_saw_player = 5
                self.alert_others()

            self.variable_space[0] += 1
            if self.variable_space[0] >= 1 * 60:
                self.look_around(45)
                self.variable_space[0] = 0
                self.sprite.set_image_index(int(self.front_direction//45))

        elif self.state == "DECISION":
            # If heard a sound, decide what happens next
            if self.sound_heard is not None:
                # if utilityfuncs.point_distance(self.x, self.y, self.sound_heard.x, self.sound_heard) > 90:
                __x = int(self.sound_heard.x/settings.cell_dimension)
                __y = int(self.sound_heard.y/settings.cell_dimension)
                if MAP_GEOMETRY[__y][__x] == 0:
                    self.set_dest(self.sound_heard.x, self.sound_heard.y, MAP_GEOMETRY)
                    self.clear_variable_space()
                    self.sound_heard = None
                    self.state = "MOVE_TO_WHERE_LAST_SEEN_ENEMY"
                    self.set_speed_factor(3)

        elif self.state == "MOVE_TO_WHERE_LAST_SEEN_ENEMY":
            # Using space 1 of variable space to hold cooldown
            # If the enemy cannot legitimately find player anymore, they move around in search of them
            if len(self.move_path) == 0:
                # Temporary Fix
                self.variable_space[14] = True # If didn't see the player anymore
                if self.sound_heard is not None:
                    self.state = "DECISION"
                    self.clear_variable_space()

                self.variable_space[0] += 1
                if self.variable_space[0] >= 12 * 60:
                    self.state = "IDLE"
                    self.clear_variable_space()
                else:
                    self.variable_space[1] += 1
                    if self.variable_space[1] >= 0.5 * 30 + self.variable_space[2]:
                        # Freakout cooldown
                        self.variable_space[2] += 20
                        __search_range = 20
                        self.look_around(45)
                        self.move_forward_a_little(MAP_GEOMETRY, __search_range)
                        self.variable_space[1] = 0

            # Seeing player then destroy them
            if self.seeing_enemy(SquadMan.squad_list, MAP_GEOMETRY):
                self.state = "ATTACK"
                self.alerted_saw_player = 5
                self.inaccuracy_multiplier = self.surprise_factor
                self.move_path.clear()
                self.cooldown = 0 # Already expected the enemy
                self.clear_variable_space()
                self.alert_others()

        elif self.state == "ATTACK":
            # Move around a little
            self.inaccuracy_multiplier = max(self.inaccuracy_multiplier * 0.9, 1)
            __d = utilityfuncs.point_direction(self.x, self.y, self.target_x, self.target_y)
            if self.seeing_enemy(SquadMan.squad_list, MAP_GEOMETRY):
                self.sprite.set_image_index(int(__d / 45))
                self.firing(__d + random.randrange(-1, 1) * self.inaccuracy_multiplier)
                self.stop_moving()
            else:
                self.is_firing = False
                self.state = "MOVE_TO_WHERE_LAST_SEEN_ENEMY" # when going to where enemy is last seen, do not have an empty move path
                self.clear_variable_space()
                self.set_dest(self.target_x, self.target_y, MAP_GEOMETRY)
                self.set_speed_factor(1)
                self.sound_heard = None

        # elif self.state == "WAIT_AMBUSH":
        self.movement(MAP_GEOMETRY)
        if self.alerted_saw_player > 0:
            self.alerted_saw_player = max(self.alerted_saw_player - 0.1, 0)

    def look_around(self, _range):
        self.front_direction += random.choice([-_range, _range])
        self.front_direction = max(min(self.front_direction, 360), 0)
        if self.front_direction >= 360:
            self.front_direction = 0

    def move_forward_a_little(self, m:list[list[int]], search_range=16):
        __x = self.x + math.cos(math.radians(self.front_direction)) * search_range
        __y = self.y - math.sin(math.radians(self.front_direction)) * search_range
        self.set_speed_factor(1)
        if m[int(__y / settings.cell_dimension)][int(__x / settings.cell_dimension)] != 0:
            return False
        else:
            self.set_dest(__x, __y, m)
            return True

    def set_speed_factor(self, spd:float):
        self.speed_factor = spd

    def firing(self, direction):
        fire_gun(self, direction)

    def hear_sound(self, snd:entities.SoundSource):
        # chance = random.randint(0, 100)
        # if chance < 33:
        dist = utilityfuncs.point_distance(self.x, self.y, snd.x, snd.y)
        if dist < snd.radius:
            if snd.sound_tag == "GUNSHOT":
                self.sound_heard = snd
            elif snd.sound_tag == "ENEMY_DEATH":
                self.sound_heard  = snd

    def get_weapon(self):
        return self.current_weapon

    def get_weapon_name(self):
        return self.current_weapon_name

    ## Pathfinding wing
    def movement(self, m:list[list[int]]):
        if len(self.move_path) == 0:
            if utilityfuncs.point_distance(self.dest_x, self.dest_y, self.x, self.y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, self.dest_x, self.dest_y)
                self.front_direction = dir_
                self.x += math.cos(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * 0.8
                self.y -= math.sin(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * 0.8
            else:
                self.dest_x, self.dest_y = self.x, self.y
                self.leg_sprite.set_image_index(2)
                self.leg_sprite.set_image_speed(0)
        else:
            x, y = (self.move_path[0][0] * settings.cell_dimension + settings.cell_dimension/2
                        , self.move_path[0][1] * settings.cell_dimension + settings.cell_dimension/2 - 2.5)

            if utilityfuncs.point_distance(self.x, self.y, x, y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, x, y)
                self.front_direction = dir_
                if not self.is_firing:
                    self.sprite.set_image_index(dir_//45)
                self.x += math.cos(math.radians(dir_)) * 0.5 * self.speed_factor
                self.y -= math.sin(math.radians(dir_)) * 0.5 * self.speed_factor
            else:
                m[self.move_path[0][1]][self.move_path[0][0]] = 0
                self.move_path.pop(0)

            self.leg_sprite.run_sprite()
            self.leg_sprite.set_image_speed(4/30)
            if self.leg_sprite.image_index > 2:
                self.leg_sprite.image_index = 0


    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc
        self.dest_x, self.dest_y = loc

    def switch_sprites(self):
        switch_sprite(self)

    def render(self, dest:pygame.Surface, x, y):
        vec_x = math.cos(math.radians(self.knock_back_dir)) * self.knock_back_strength
        vec_y = math.sin(math.radians(self.knock_back_dir)) * self.knock_back_strength
        x += vec_x
        y -= vec_y
        self.switch_sprites()
        dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)), None)
        dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))
        pygame.draw.rect(dest, (255, 0, 0), (x-5, y-9, 10, 2))
        pygame.draw.rect(dest, (0, 255, 0), (x-5, y-9, 10*self.hp/100, 2))

        # Alerted
        if self.alerted_saw_player > 0:
            alr_spr = ALL_SPRITES.ASP["ALERTED0"]
            fluctuate = random.randint(0, 100)
            if fluctuate <= 50:
                alr_spr = ALL_SPRITES.ASP["ALERTED1"]
            alr_rect = alr_spr.get_rect(center=(x, y-8))
            dest.blit(pygame.transform.scale_by(alr_spr, 0.5), alr_rect)

        # Target line
        dx, dy = self.target_x - self.x, self.target_y - self.y
        # pygame.draw.line(dest, (255, 255, 0), (x, y), (x+dx, y+dy))

    def take_damage(self, amount, source):
        source_dir = utilityfuncs.point_direction(self.x, self.y, source.x, source.y)
        damage_multiplier = (abs(self.front_direction - source_dir) / 180) * 1.25 + 1
        print(f"{amount} : {amount * damage_multiplier}")
        self.hp -= amount * damage_multiplier
        self.front_direction = source_dir

    def knockback(self, strength, knock_dir):
        self.knock_back_dir = knock_dir
        self.knock_back_strength = strength

    def check_death(self):
        if self.hp <= 0:
            self.destroy()

    def destroy(self):
        entities.SoundSource(self.x, self.y,  150, sound_tag="ENEMY_DEATH")
        for l in self.references:
            deletor.Deleter.request_delete(self, l)
        deletor.Deleter.request_delete(self, enemy_list)

    def __copy__(self):
        return Enemy((self.x, self.y), exclude=False, weapon_type=self.current_weapon_name)

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

all_enemies_type = Enemy