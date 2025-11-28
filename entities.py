import copy

import pygame
import math
import pathfind
import settings
import utilityfuncs
import Sprites
import random


class SquadMan:
    squad_list:list = []
    def __init__(self, loc:tuple[float, float]):
        self.x, self.y = loc
        self.hp = 100
        self.dest_x = self.x
        self.dest_y = self.y
        self.state = "MOVEMENT"
        self.sprite = Sprites.Sprite(
            ("sprites/mob_spr/mobster_torso_0pistol.png",
            "sprites/mob_spr/mobster_torso_45pistol.png",
            "sprites/mob_spr/mobster_torso_90pistol.png",
            "sprites/mob_spr/mobster_torso_135pistol.png",
            "sprites/mob_spr/mobster_torso_180pistol.png",
            "sprites/mob_spr/mobster_torso_225pistol.png",
            "sprites/mob_spr/mobster_torso_270pistol.png",
            "sprites/mob_spr/mobster_torso_315pistol.png")
        )
        self.leg_sprite = Sprites.Sprite(
            (
                "sprites/mob_spr/mobster_leg_leftup.png",
                "sprites/mob_spr/mobster_leg_rightup.png",
                "sprites/mob_spr/mobster_leg_normal.png"
            )
        )
        self.move_dir = 0
        self.frames = 0
        self.move_path = []
        self.focused = True # so that they look at where they're going
        self.being_used = True
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
        if len(self.move_path) == 0:
            if utilityfuncs.point_distance(self.dest_x, self.dest_y, self.x, self.y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, self.dest_x, self.dest_y)
                self.x += math.cos(math.radians(dir_)) * 0.5
                self.y -= math.sin(math.radians(dir_)) * 0.5
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
                self.x += math.cos(math.radians(dir_)) * 0.5
                self.y -= math.sin(math.radians(dir_)) * 0.5
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
        self.sprite = Sprites.Sprite(
            (
                "sprites/mob_spr/mobster_torso_0pistol.png",
                "sprites/mob_spr/mobster_torso_45pistol.png",
                "sprites/mob_spr/mobster_torso_90pistol.png",
                "sprites/mob_spr/mobster_torso_135pistol.png",
                "sprites/mob_spr/mobster_torso_180pistol.png",
                "sprites/mob_spr/mobster_torso_225pistol.png",
                "sprites/mob_spr/mobster_torso_270pistol.png",
                "sprites/mob_spr/mobster_torso_315pistol.png"
            )
        )
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
                dest_x = random.randint(0, settings.hor_cells * settings.cell_dimension)
                dest_y = random.randint(0, settings.ver_cells * settings.cell_dimension)
                while m[dest_y // settings.cell_dimension][dest_x // settings.cell_dimension] != 0:
                    dest_x = random.randrange(0, settings.hor_cells * settings.cell_dimension)
                    dest_y = random.randrange(0, settings.ver_cells * settings.cell_dimension)
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