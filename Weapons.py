import random

import ALL_SPRITES
import pygame
import settings

ww, wh = settings.WINDOW_WIDTH/settings.zoom, settings.WINDOW_HEIGHT/settings.zoom
padding = ww/4

class Weapons:
    def __init__(self, name, fire_cooldown, damage, pellets, inaccuracy, ammo, lives=1, create_ray=False,sound_radius=15,speed_modifier:float=1, projectile_type="BULLET"):
        self.name = name
        self.fire_cooldown = fire_cooldown
        self.damage = damage
        self.pellets = pellets
        self.inaccuracy = inaccuracy
        self.ammo = ammo
        self.lives = lives # determines piercing of number of people
        self.create_ray = create_ray
        self.sound_radius = sound_radius
        self.speed_modifier = speed_modifier
        self.projectile_type = projectile_type

    def __copy__(self):
        return Weapons(self.name, self.fire_cooldown, self.damage, self.pellets, self.inaccuracy, self.ammo, lives=self.lives, create_ray=self.create_ray)

class InventoryWeapon:
    def __init__(self, weapon_name, ammo, x, y):
        self.weapon_name = weapon_name
        self.max_ammo = WEAPONS_REF[self.weapon_name].ammo
        self.ammo = min(max(0, ammo), self.max_ammo)
        if (x, y) == (-1, -1):
            sprite_width = ALL_SPRITES.ASP[weapon_name].get_rect().width
            sprite_height = ALL_SPRITES.ASP[weapon_name].get_rect().height
            self.x = random.randrange(int(sprite_width/2)+2, int(ww-padding-sprite_width/2)-2)
            self.y = random.randrange(int(sprite_height/2)+2, int(wh)-2)
        else:
            self.x = x
            self.y = y
        self.outlined = True
        self.being_used = False
        self.used_by_obj = None

    def hitbox(self):
        spr = ALL_SPRITES.ASP[self.weapon_name]
        return spr.get_rect(center=(self.x, self.y))

    def render(self, dest:pygame.Surface, x, y):
        spr = ALL_SPRITES.ASP[self.weapon_name]
        color = (255, 0, 0)
        if self.being_used:
            color = (0, 255, 0)
        outlined_spr = spr.copy()
        outlined_fill = pygame.PixelArray(outlined_spr)
        outlined_fill.replace((255, 255, 255), color)
        outlined_fill.close()
        # Outline
        if self.outlined:
            pos = [
                (-1, -1), (0, -1), (1, -1),
                (-1, 0), (1, 0),
                (-1, 1), (0, 1), (1, 1),
            ]
            for offsets in pos:
                outline_rect = outlined_spr.get_rect(center=(x-offsets[0], y-offsets[1]))
                dest.blit(outlined_spr, outline_rect)
        # Draw actual sprite
        spr_rect = spr.get_rect(center=(x,y))
        dest.blit(spr, spr_rect)


WEAPONS_REF = {
    "None" : Weapons("None", 1, 0, 0, 4, 0, speed_modifier=1.5),
    "Pistol": Weapons("Colt 1911", 15, 15, 1, 4, 30, speed_modifier=1.5),
    "Revolver": Weapons("Magnum", 60, 100, 1, 1, 6,lives=2, create_ray=True, speed_modifier=1.5),
    "Shotgun": Weapons("RMT 970",  60, 11, 15, 8, 8, speed_modifier=1),
    "Thompson": Weapons("Thompson",  4, 10, 1, 6, 100, speed_modifier=0.8), # damage 8, cooldown 4, pellets 1
    "Bar": Weapons("Bar", 12, 30, 1, 1, 10, lives=2, create_ray=True, speed_modifier=0.6),
    "GrenadeLauncher": Weapons("Grenade Launcher", 70, 0, 5, 4, 7, speed_modifier=0.6, projectile_type="GRENADE"),
    "RocketLauncher" : Weapons("Rocket Launcher", 60, 35, 3, 4, 1, projectile_type="ROCKET", speed_modifier=0.5),
    # "GasLauncher"
}