import random
import pygame
import Sprites


class MuzzleFlash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = Sprites.Sprite(
            (
                "sprites/muzzle_flash_spr/flash.png",
                "sprites/muzzle_flash_spr/flash.png"
            )
        )
        all_effects.append(self)

    def render(self, dest: pygame.Surface, x, y):
        surf = pygame.transform.rotate(self.sprite.get_current_image(), random.randint(0, 360))
        rect = surf.get_rect(center=(self.x-x,self.y-y))
        dest.blit(surf, rect)
        all_effects.remove(self)

class BulletHole:
    all_bullet_holes:list = []
    def __init__(self, x,y):
        self.x, self.y = x,y
        self.sprite = Sprites.Sprite(
            (
                "sprites/bullet_hole_spr/hole1.png",
                "sprites/bullet_hole_spr/hole1.png",
                "sprites/bullet_hole_spr/hole1.png"
            )
        )
        self.sprite.set_image_index(random.randint(0, self.sprite.get_image_number()-1))
        self.angle = random.randint(0, 360)
        BulletHole.all_bullet_holes.append(self)
        all_effects.append(self)

    def render(self, dest:pygame.Surface, x,y):
        surf = pygame.transform.rotate(self.sprite.get_current_image(), self.angle)
        rect = surf.get_rect(center=(self.x-x, self.y-y))
        dest.blit(surf, rect)

    def get_hitbox(self):
        rect = pygame.transform.scale_by(self.sprite.get_current_image(), 2).get_rect(center=(self.x,self.y))
        return rect

class Ray:
    def __init__(self, x_start, y_start, x_end, y_end, color=(255,255,255)):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end   = x_end
        self.y_end   = y_end
        self.color = color
        all_effects.append(self)
    def render(self, dest:pygame.Surface, x,y):
        pygame.draw.line(dest, self.color, (self.x_start-x, self.y_start-y), (self.x_end-x, self.y_end-y), width=2)
        all_effects.remove(self)

effect_types = MuzzleFlash|Ray|BulletHole
all_effects:list[effect_types] = []
