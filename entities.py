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
        self.state = "MOVEMENT"

        self.pistol_sprite = Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0pistol.png",
             "sprites/mob_spr/mobster_torso_45pistol.png",
             "sprites/mob_spr/mobster_torso_90pistol.png",
             "sprites/mob_spr/mobster_torso_135pistol.png",
             "sprites/mob_spr/mobster_torso_180pistol.png",
             "sprites/mob_spr/mobster_torso_225pistol.png",
             "sprites/mob_spr/mobster_torso_270pistol.png",
             "sprites/mob_spr/mobster_torso_315pistol.png")
        )
        self.shotgun_sprite = Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0shotgun.png",
             "sprites/mob_spr/mobster_torso_45shotgun.png",
             "sprites/mob_spr/mobster_torso_90shotgun.png",
             "sprites/mob_spr/mobster_torso_135shotgun.png",
             "sprites/mob_spr/mobster_torso_180shotgun.png",
             "sprites/mob_spr/mobster_torso_225shotgun.png",
             "sprites/mob_spr/mobster_torso_270shotgun.png",
             "sprites/mob_spr/mobster_torso_315shotgun.png")
        )
        self.thompson_sprite = Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0thompson.png",
             "sprites/mob_spr/mobster_torso_45thompson.png",
             "sprites/mob_spr/mobster_torso_90thompson.png",
             "sprites/mob_spr/mobster_torso_135thompson.png",
             "sprites/mob_spr/mobster_torso_180thompson.png",
             "sprites/mob_spr/mobster_torso_225thompson.png",
             "sprites/mob_spr/mobster_torso_270thompson.png",
             "sprites/mob_spr/mobster_torso_315thompson.png")
        )
        self.bar_sprite = Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0bar.png",
             "sprites/mob_spr/mobster_torso_45bar.png",
             "sprites/mob_spr/mobster_torso_90bar.png",
             "sprites/mob_spr/mobster_torso_135bar.png",
             "sprites/mob_spr/mobster_torso_180bar.png",
             "sprites/mob_spr/mobster_torso_225bar.png",
             "sprites/mob_spr/mobster_torso_270bar.png",
             "sprites/mob_spr/mobster_torso_315bar.png")
        )
        self.leg_sprite = Sprites.Sprite(
            (
                "sprites/mob_spr/mobster_leg_leftup.png",
                "sprites/mob_spr/mobster_leg_rightup.png",
                "sprites/mob_spr/mobster_leg_normal.png"
            )
        )
        self.sprite = self.pistol_sprite
        self.move_dir = 0
        self.frames = 0
        self.move_path = []
        self.focused = True # so that they look at where they're going
        self.being_used = True

        self.current_weapon_name = "Colt 1911"
        self.current_weapon = WEAPONS_REF[self.current_weapon_name]

        self.cooldown = 0
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
            if utilityfuncs.point_distance(self.dest_x, self.dest_y, self.x, self.y) > 5:
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
                    self.sprite.set_image_index(dir_//45)
                self.move_dir = dir_
                self.x += math.cos(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * spd_modifier
                self.y -= math.sin(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * spd_modifier
            else:
                m[self.move_path[0][1]][self.move_path[0][0]] = 0
                self.move_path.pop(0)

            self.leg_sprite.run_sprite()
            self.leg_sprite.set_image_speed(4/30)
            if self.leg_sprite.image_index > 2:
                self.leg_sprite.image_index = 0


    def render(self, dest:pygame.Surface, x, y):
        # Being used
        dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)))
        dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))
        if self.being_used:
            pygame.draw.rect(dest, (0, 255, 255), (x-1, y-7, 2, 2))
        else:
            pygame.draw.rect(dest, (255, 0, 255), (x-1, y-7, 2, 2))

    # def check_death(self):
        # if self.hp < 0:

    def firing(self, direction, c:camera.Camera):
        self.cooldown += 1
        if pygame.key.get_pressed()[pygame.K_e]:
            if self.cooldown > self.get_weapon().fire_cooldown:
                total_damage = 20
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

                    effects.MuzzleFlash(self.xy()[0]+vec_x, self.xy()[1]-vec_y)
                    self.sprite.set_image_index(d)
                    self.focused = False
                    shake_factor = total_damage / 20
                    c.screen_shake(shake_factor * 3)

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
        self.pistol_sprite = Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0pistol.png",
             "sprites/mob_spr/mobster_torso_45pistol.png",
             "sprites/mob_spr/mobster_torso_90pistol.png",
             "sprites/mob_spr/mobster_torso_135pistol.png",
             "sprites/mob_spr/mobster_torso_180pistol.png",
             "sprites/mob_spr/mobster_torso_225pistol.png",
             "sprites/mob_spr/mobster_torso_270pistol.png",
             "sprites/mob_spr/mobster_torso_315pistol.png")
        )
        self.shotgun_sprite = Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0shotgun.png",
             "sprites/mob_spr/mobster_torso_45shotgun.png",
             "sprites/mob_spr/mobster_torso_90shotgun.png",
             "sprites/mob_spr/mobster_torso_135shotgun.png",
             "sprites/mob_spr/mobster_torso_180shotgun.png",
             "sprites/mob_spr/mobster_torso_225shotgun.png",
             "sprites/mob_spr/mobster_torso_270shotgun.png",
             "sprites/mob_spr/mobster_torso_315shotgun.png")
        )
        self.thompson_sprite = Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0thompson.png",
             "sprites/mob_spr/mobster_torso_45thompson.png",
             "sprites/mob_spr/mobster_torso_90thompson.png",
             "sprites/mob_spr/mobster_torso_135thompson.png",
             "sprites/mob_spr/mobster_torso_180thompson.png",
             "sprites/mob_spr/mobster_torso_225thompson.png",
             "sprites/mob_spr/mobster_torso_270thompson.png",
             "sprites/mob_spr/mobster_torso_315thompson.png")
        )
        self.bar_sprite = Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0bar.png",
             "sprites/mob_spr/mobster_torso_45bar.png",
             "sprites/mob_spr/mobster_torso_90bar.png",
             "sprites/mob_spr/mobster_torso_135bar.png",
             "sprites/mob_spr/mobster_torso_180bar.png",
             "sprites/mob_spr/mobster_torso_225bar.png",
             "sprites/mob_spr/mobster_torso_270bar.png",
             "sprites/mob_spr/mobster_torso_315bar.png")
        )
        self.leg_sprite = Sprites.Sprite(
            (
                "sprites/mob_spr/mobster_leg_leftup.png",
                "sprites/mob_spr/mobster_leg_rightup.png",
                "sprites/mob_spr/mobster_leg_normal.png"
            )
        )
        self.sprite = self.thompson_sprite

        self.leg_sprite = Sprites.Sprite(
            (
                "sprites/mob_spr/mobster_leg_leftup.png",
                "sprites/mob_spr/mobster_leg_rightup.png",
                "sprites/mob_spr/mobster_leg_normal.png"
            )
        )
        self.weapon_type = weapon_type
        self.move_dir = 0
        self.frames = 0
        self.move_path = []
        self.focused = True
        self.faction_color = (255, 0, 0)
        self.weapon_type = weapon_type
        self.exclude = exclude
        self.repr_name = ""
        EnemyMobster.EnemyList.append(self)

    def set_dest(self, x, y, m):
        self.move_path.clear()
        self.dest_x, self.dest_y = x, y
        def conv(val):
            return int(val/settings.cell_dimension)
        self.move_path = pathfind.pathfind(conv(self.x), conv(self.y), conv(self.dest_x), conv(self.dest_y), m)

    def xy(self):
        return self.x, self.y

    def action(self, m:list[list[int]]):
        if len(self.move_path) == 0:
            if utilityfuncs.point_distance(self.dest_x, self.dest_y, self.x, self.y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, self.dest_x, self.dest_y)
                self.x += math.cos(math.radians(dir_)) * 0.5
                self.y -= math.sin(math.radians(dir_)) * 0.5
            else:
                self.dest_x, self.dest_y = self.x, self.y
                self.leg_sprite.set_image_index(2)
                self.leg_sprite.set_image_speed(0)
                dest_x = random.randint(64, settings.hor_cells * settings.cell_dimension-64)
                dest_y = random.randint(64, settings.ver_cells * settings.cell_dimension-64)
                while m[dest_y // settings.cell_dimension][dest_x // settings.cell_dimension] != 0:
                    dest_x = random.randint(64, settings.hor_cells * settings.cell_dimension-64)
                    dest_y = random.randint(64, settings.ver_cells * settings.cell_dimension-64)
                self.set_dest(dest_x, dest_y, m)

        else:
            x, y = (self.move_path[0][0] * settings.cell_dimension + settings.cell_dimension/2
                        , self.move_path[0][1] * settings.cell_dimension + settings.cell_dimension/2 - 2.5)

            if utilityfuncs.point_distance(self.x, self.y, x, y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, x, y)
                if self.focused:
                    self.sprite.set_image_index(dir_//45)
                self.move_dir = dir_
                self.x += math.cos(math.radians(dir_)) * 0.5
                self.y -= math.sin(math.radians(dir_)) * 0.5
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

    def render(self, dest:pygame.Surface, x, y):
        dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)), None)
        dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))
        pygame.draw.rect(dest, (255, 0, 0), (x-5, y-9, 10, 2))
        pygame.draw.rect(dest, (0, 255, 0), (x-5, y-9, 10*self.hp/100, 2))

    def check_death(self, ref:list):
        if self.hp <= 0:
            ref.remove(self)
            EnemyMobster.EnemyList.remove(self)

    def __copy__(self):
        return EnemyMobster((self.x, self.y), exclude=self.exclude, weapon_type=self.weapon_type)

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

all_entities_types = EnemyMobster|SquadMan