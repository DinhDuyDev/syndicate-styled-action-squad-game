import copy

import pygame
import math
import pathfind
import settings
import utilityfuncs
import Sprites
import random
import Weapons
import Bullet
import effects
import camera

WEAPONS_REF = Weapons.WEAPONS_REF

def gen_all_sprites():
    return {
        "Pistol" : Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0pistol.png",
             "sprites/mob_spr/mobster_torso_45pistol.png",
             "sprites/mob_spr/mobster_torso_90pistol.png",
             "sprites/mob_spr/mobster_torso_135pistol.png",
             "sprites/mob_spr/mobster_torso_180pistol.png",
             "sprites/mob_spr/mobster_torso_225pistol.png",
             "sprites/mob_spr/mobster_torso_270pistol.png",
             "sprites/mob_spr/mobster_torso_315pistol.png")
        ),
        "Shotgun" : Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0shotgun.png",
             "sprites/mob_spr/mobster_torso_45shotgun.png",
             "sprites/mob_spr/mobster_torso_90shotgun.png",
             "sprites/mob_spr/mobster_torso_135shotgun.png",
             "sprites/mob_spr/mobster_torso_180shotgun.png",
             "sprites/mob_spr/mobster_torso_225shotgun.png",
             "sprites/mob_spr/mobster_torso_270shotgun.png",
             "sprites/mob_spr/mobster_torso_315shotgun.png")
        ),
        "Thompson" : Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0thompson.png",
             "sprites/mob_spr/mobster_torso_45thompson.png",
             "sprites/mob_spr/mobster_torso_90thompson.png",
             "sprites/mob_spr/mobster_torso_135thompson.png",
             "sprites/mob_spr/mobster_torso_180thompson.png",
             "sprites/mob_spr/mobster_torso_225thompson.png",
             "sprites/mob_spr/mobster_torso_270thompson.png",
             "sprites/mob_spr/mobster_torso_315thompson.png")
        ),
        "Bar" : Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0bar.png",
             "sprites/mob_spr/mobster_torso_45bar.png",
             "sprites/mob_spr/mobster_torso_90bar.png",
             "sprites/mob_spr/mobster_torso_135bar.png",
             "sprites/mob_spr/mobster_torso_180bar.png",
             "sprites/mob_spr/mobster_torso_225bar.png",
             "sprites/mob_spr/mobster_torso_270bar.png",
             "sprites/mob_spr/mobster_torso_315bar.png")
        )
    }

class SquadMan:
    squad_list:list = []
    @classmethod
    def nums_active(cls):
        nums = 0
        for i in SquadMan.squad_list:
            if i.being_used:
                nums += 1
        return nums

    def __init__(self, loc:tuple[float, float]):
        self.x, self.y = loc
        self.hp = 100
        self.dest_x = self.x
        self.dest_y = self.y

        all_sprs = gen_all_sprites()
        self.pistol_sprite = all_sprs["Pistol"]
        self.shotgun_sprite = all_sprs["Shotgun"]
        self.thompson_sprite = all_sprs["Thompson"]
        self.bar_sprite = all_sprs["Bar"]
        self.leg_sprite = Sprites.Sprite(
            (
                "sprites/mob_spr/mobster_leg_leftup.png",
                "sprites/mob_spr/mobster_leg_rightup.png",
                "sprites/mob_spr/mobster_leg_normal.png"
            )
        )
        self.sprite = self.pistol_sprite
        self.frames = 0
        self.move_path = []
        self.focused = True # so that they look at where they're going
        self.being_used = True

        self.knock_back_strength = 0
        self.knock_back_dir = 0

        self.current_weapon_name = "Shotgun"
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

            # If the squadder is the front man
            if self.cooldown_steps >= 30 * (1/spd_modifier) and SquadMan.squad_list.index(self) == 0:
                effects.SoundSource(self.x, self.y, 10*(5/spd_modifier**2)) # Also used to make noises
                self.cooldown_steps = 0
            else:
                self.cooldown_steps += 1

        # self.hp = 10000
    def render(self, dest:pygame.Surface, x, y):
        # Being used
        dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)))
        dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))
        if self.being_used:
            pygame.draw.rect(dest, (0, 255, 255), (x-1, y-7, 2, 2))
        else:
            pygame.draw.rect(dest, (255, 0, 255), (x-1, y-7, 2, 2))
        pygame.draw.rect(dest, (255, 0, 0), (x - 5, y - 9, 10, 2))
        pygame.draw.rect(dest, (0, 255, 0), (x - 5, y - 9, 10 * self.hp / 100, 2))

    def check_death(self):
        if self.hp < 0:
            SquadMan.squad_list.remove(self)

    def switch_sprites(self):
        if self.current_weapon_name == "Pistol" or self.current_weapon_name == "Revolver":
            self.sprite = self.pistol_sprite
        elif self.current_weapon_name == "Shotgun":
            self.sprite = self.shotgun_sprite
        elif self.current_weapon_name == "Thompson":
            self.sprite = self.thompson_sprite
        elif self.current_weapon_name == "Bar":
            self.sprite = self.bar_sprite

    def firing(self, direction):
        self.switch_sprites()
        self.cooldown += 1
        if pygame.key.get_pressed()[pygame.K_e] or pygame.mouse.get_pressed()[2]:
            if self.cooldown > self.get_weapon().fire_cooldown:
                base_ref = WEAPONS_REF["Pistol"].damage
                total_damage = base_ref
                if self.being_used:
                    md_dir = direction
                    d = md_dir//45
                    vec_x = math.cos(math.radians(d*45)) * 8
                    vec_y = math.sin(math.radians(d*45)) * 8

                    wep = self.get_weapon()
                    for i in range(wep.pellets):
                        _damage = wep.damage
                        total_damage += _damage
                        _inaccuracies = wep.inaccuracy
                        _lives = wep.lives
                        _create_ray = wep.create_ray
                        Bullet.PlayerBullet(self.xy()[0]+vec_x, self.xy()[1]-vec_y, md_dir, self, damage=_damage, deviation=_inaccuracies,lives=_lives,create_ray=_create_ray)

                    effects.SoundSource(self.xy()[0], self.xy()[1], (total_damage / 20) * 30)
                    effects.MuzzleFlash(self.xy()[0]+vec_x, self.xy()[1]-vec_y)
                    self.sprite.set_image_index(d)
                    self.focused = False
                    shake_factor = total_damage / 20
                    camera.Camera.activeCam.screen_shake(shake_factor * 3)

                self.cooldown = 0

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

    map_width = len(m[0])
    map_height = len(m)
    d = 45
    dist_travel = 7

    for sq_m in sq_ls:
        if sq_m.being_used:
            dx, dy = x + math.cos(math.radians(d)) * dist_travel, y - math.sin(math.radians(d)) * dist_travel
            tx = int(dx/settings.cell_dimension)
            ty = int(dy/settings.cell_dimension)
            if 0 <= ty < map_height and 0 <= tx < map_width:
                if m[ty][tx] == 0:
                    sq_m.set_dest(dx, dy, m)
                    sq_m.focused = True
        d += 90


# Enemy mobster
class EnemyMobster:
    EnemyList:list = []
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

        all_sprs = gen_all_sprites()

        self.pistol_sprite = all_sprs["Pistol"]
        self.shotgun_sprite = all_sprs["Shotgun"]
        self.thompson_sprite = all_sprs["Thompson"]
        self.bar_sprite = all_sprs["Bar"]
        self.sprite = self.thompson_sprite

        self.leg_sprite = Sprites.Sprite(
            (
                "sprites/mob_spr/mobster_leg_leftup.png",
                "sprites/mob_spr/mobster_leg_rightup.png",
                "sprites/mob_spr/mobster_leg_normal.png"
            )
        )

        self.current_weapon_name = random.choice(["Pistol", "Shotgun", "Thompson", "Bar"])
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

        # The sound heard by the enemy
        self.sound_heard:effects.SoundSource|None = None
        EnemyMobster.EnemyList.append(self)

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
        for e in enemies:
            if utilityfuncs.line_of_sight(self.x, self.y, e.xy()[0], e.xy()[1], m):
                self.target_x = e.xy()[0]
                self.target_y = e.xy()[1]
                return True
        return False

    def clear_variable_space(self):
        for i in range(len(self.variable_space)):
            self.variable_space[i] = 0

    def stop_moving(self):
        self.dest_x, self.dest_y = self.x, self.y
        self.move_path.clear()

    def action(self, m:list[list[int]]):
        self.switch_sprites()
        if self.state == "IDLE":
            if self.sound_heard is not None:
                self.state = "DECISION"
                self.clear_variable_space()

            if self.seeing_enemy(SquadMan.squad_list, m):
                self.state = "ATTACK"
                self.move_path.clear()
                self.cooldown = -20
                self.clear_variable_space()

        elif self.state == "DECISION":
            # If heard a sound, decide what happens next
            if self.sound_heard is not None:
                # if utilityfuncs.point_distance(self.x, self.y, self.sound_heard.x, self.sound_heard) > 90:
                __x = int(self.sound_heard.x/settings.cell_dimension)
                __y = int(self.sound_heard.y/settings.cell_dimension)
                if m[__y][__x] == 0:
                    print("Can move to player")
                    self.set_dest(self.sound_heard.x, self.sound_heard.y, m)
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
                    if self.variable_space[1] >= 1 * 30 + self.variable_space[2]:
                        # Freakout cooldown
                        self.variable_space[2] += 20
                        __search_range = 20
                        __x = self.x+random.randrange(-__search_range, __search_range)
                        __y = self.y+random.randrange(-__search_range, __search_range)
                        while m[int(__y/settings.cell_dimension)][int(__x/settings.cell_dimension)] != 0:
                            __x = self.x + random.randrange(-__search_range, __search_range)
                            __y = self.y + random.randrange(-__search_range, __search_range)
                        self.set_dest(__x, __y, m)
                        self.variable_space[1] = 0

            # Seeing player then destroy them
            if self.seeing_enemy(SquadMan.squad_list, m):
                self.state = "ATTACK"
                self.move_path.clear()
                self.cooldown = -10 # Bit of a delay
                self.clear_variable_space()

        elif self.state == "ATTACK":
            # Move around a little
            __search_range = 15
            if len(self.move_path) == 0:
                __x = self.x + random.randrange(-__search_range, __search_range)
                __y = self.y + random.randrange(-__search_range, __search_range)
                while m[int(__y / settings.cell_dimension)][int(__x / settings.cell_dimension)] != 0 and utilityfuncs.line_of_sight(self.x, self.y, __x, __y, m, settings.cell_dimension/1.5):
                    __x = self.x + random.randrange(-__search_range, __search_range)
                    __y = self.y + random.randrange(-__search_range, __search_range)
                self.set_speed_factor(1)
                self.set_dest(__x, __y, m)
                self.is_firing = True

            __d = utilityfuncs.point_direction(self.x, self.y, self.target_x, self.target_y)
            if self.seeing_enemy(SquadMan.squad_list, m):
                self.sprite.set_image_index(int(__d / 45))
                self.firing(__d)
                # self.stop_moving()
            else:
                self.is_firing = False
                self.state = "MOVE_TO_WHERE_LAST_SEEN_ENEMY" # when going to where enemy is last seen, do not have an empty move path
                self.clear_variable_space()
                self.set_dest(self.target_x, self.target_y, m)
                self.set_speed_factor(1)
                self.sound_heard = None

        # elif self.state == "WAIT_AMBUSH":


        self.movement(m)

    def set_speed_factor(self, spd:float):
        self.speed_factor = spd

    def firing(self, direction):
        self.cooldown += 1
        if self.cooldown > self.get_weapon().fire_cooldown:
            base_ref = WEAPONS_REF["Pistol"].damage
            total_damage = base_ref
            md_dir = direction
            d = md_dir // 45
            vec_x = math.cos(math.radians(d * 45)) * 8
            vec_y = math.sin(math.radians(d * 45)) * 8

            wep = self.get_weapon()
            for i in range(wep.pellets):
                _damage = wep.damage
                total_damage += _damage
                _inaccuracies = wep.inaccuracy
                _lives = wep.lives
                _create_ray = wep.create_ray
                Bullet.PlayerBullet(self.xy()[0] + vec_x, self.xy()[1] - vec_y, md_dir, self, damage=_damage,
                                    deviation=_inaccuracies, lives=_lives, create_ray=_create_ray)

            effects.SoundSource(self.xy()[0], self.xy()[1], (total_damage / 20) * 30)
            effects.MuzzleFlash(self.xy()[0] + vec_x, self.xy()[1] - vec_y)
            self.sprite.set_image_index(d)
            shake_factor = total_damage / 20
            camera.Camera.activeCam.screen_shake(shake_factor * 3)
            self.cooldown = 0

    def hear_sound(self, snd:effects.SoundSource):
        chance = random.randint(0, 100)
        if chance < 33:
            if utilityfuncs.point_distance(self.x, self.y, snd.x, snd.y) < snd.radius:
                self.sound_heard = snd

    def get_weapon(self):
        return self.current_weapon

    def get_weapon_name(self):
        return self.current_weapon_name


    ## Pathfinding wing
    def movement(self, m:list[list[int]]):
        if len(self.move_path) == 0:
            if utilityfuncs.point_distance(self.dest_x, self.dest_y, self.x, self.y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, self.dest_x, self.dest_y)
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
        if self.current_weapon_name == "Pistol" or self.current_weapon_name == "Revolver":
            self.sprite = self.pistol_sprite
        elif self.current_weapon_name == "Shotgun":
            self.sprite = self.shotgun_sprite
        elif self.current_weapon_name == "Thompson":
            self.sprite = self.thompson_sprite
        elif self.current_weapon_name == "Bar":
            self.sprite = self.bar_sprite

    def render(self, dest:pygame.Surface, x, y):
        dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)), None)
        dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))
        pygame.draw.rect(dest, (255, 0, 0), (x-5, y-9, 10, 2))
        pygame.draw.rect(dest, (0, 255, 0), (x-5, y-9, 10*self.hp/100, 2))

    def check_death(self, ref:list):
        if self.hp <= 0:
            EnemyMobster.EnemyList.remove(self)
            ref.remove(self)
    #
    def __copy__(self):
        return EnemyMobster((self.x, self.y), exclude=self.exclude, weapon_type=self.current_weapon_name)

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

all_entities_types = EnemyMobster|SquadMan