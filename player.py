import copy

import pygame
import math
import pathfind
import settings
import utilityfuncs
import Sprites


class SquadMan:
    squad_list:list = []
    def __init__(self, loc:tuple[float, float]):
        self.x, self.y = loc
        self.hp = 100
        self.sprite = pygame.Surface((5, 5))
        self.sprite.fill((255, 255, 255))
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
        self.frames = 0
        self.move_path = []
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
                self.x += math.cos(math.radians(dir_))
                self.y -= math.sin(math.radians(dir_))

            if utilityfuncs.point_distance(self.x, self.y, self.dest_x, self.dest_y) < 1:
                self.x, self.y = self.dest_x, self.dest_y
                self.leg_sprite.set_image_index(2)
                self.leg_sprite.set_image_speed(0)

        else:
            x, y = (self.move_path[0][0] * settings.cell_dimension + settings.cell_dimension/2
                        , self.move_path[0][1] * settings.cell_dimension + settings.cell_dimension/2 - 2.5)

            if utilityfuncs.point_distance(self.x, self.y, x, y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, x, y)
                self.sprite.set_image_index(dir_//45)
                self.x += math.cos(math.radians(dir_))
                self.y -= math.sin(math.radians(dir_))
            else:
                m[self.move_path[0][1]][self.move_path[0][0]] = 0
                self.move_path.pop(0)

            self.leg_sprite.run_sprite()
            self.leg_sprite.set_image_speed(10/30)
            if self.leg_sprite.image_index > 2:
                self.leg_sprite.image_index = 0


    def render(self, dest:pygame.Surface, x, y):
        dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)))
        dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))

def move_squad(x, y, m):
    sq_ls = SquadMan.squad_list

    map_width = len(m[0])
    map_height = len(m)
    d = 45
    dist_travel = 7

    for sq_m in sq_ls:
        dx, dy = x + math.cos(math.radians(d)) * dist_travel, y - math.sin(math.radians(d)) * dist_travel
        tx = int(dx/settings.cell_dimension)
        ty = int(dy/settings.cell_dimension)
        if 0 <= ty < map_height and 0 <= tx < map_width:
            if m[ty][tx] == 0:
                sq_m.set_dest(dx, dy, m)
        d += 90