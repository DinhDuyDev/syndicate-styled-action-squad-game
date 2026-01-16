import random
import pygame
import Sprites
import utilityfuncs
import deletor
import math

class MuzzleFlash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = Sprites.Sprite(
            (
                "FLASH",
                "FLASH"
            )
        )
        all_effects.append(self)
        self.references = []

    def render(self, dest: pygame.Surface, x, y):
        surf = pygame.transform.rotate(self.sprite.get_current_image(), random.randint(0, 360))
        rect = surf.get_rect(center=(x,y))
        dest.blit(surf, rect)
        self.destroy()

    def destroy(self):
        deletor.Deleter.request_delete(self, all_effects)
        for l in self.references:
            deletor.Deleter.request_delete(self, l)

class BulletHole:
    all_bullet_holes:list = []
    def __init__(self, x,y):
        self.x, self.y = x,y
        self.sprite = Sprites.Sprite(
            (
                "HOLE_1",
                "HOLE_2",
                "HOLE_3"
            )
        )
        self.sprite.set_image_index(random.randint(0, self.sprite.get_image_number()-1))
        self.angle = random.randint(0, 360)
        BulletHole.all_bullet_holes.append(self)
        all_effects.append(self)

    def render(self, dest:pygame.Surface, x,y):
        surf = pygame.transform.rotate(self.sprite.get_current_image(), self.angle)
        rect = surf.get_rect(center=(x, y))
        dest.blit(surf, rect)

    def get_hitbox(self):
        rect = pygame.transform.scale_by(self.sprite.get_current_image(), 2).get_rect(center=(self.x,self.y))
        return rect

class BloodSplot:
    all_blood_splots:list = []
    def __init__(self, x,y):
        self.x, self.y = x,y
        self.sprite = Sprites.Sprite(
            (
                "BLOOD_SPLOT1",
                "BLOOD_SPLOT2",
                "BLOOD_SPLOT3"
            )
        )
        self.sprite.set_image_index(random.randint(0, self.sprite.get_image_number()-1))
        self.angle = random.randint(0, 360)
        self.scale = 1 + random.randrange(2, 5) * 0.25
        # all_effects.append(self)
        BloodSplot.all_blood_splots.append(self)

    def render(self, dest:pygame.Surface, x,y):
        surf = pygame.transform.rotate(self.sprite.get_current_image(), self.angle)
        rect = surf.get_rect(center=(x, y))
        dest.blit(surf, rect)

    def get_hitbox(self):
        rect = pygame.transform.scale_by(self.sprite.get_current_image(), 2).get_rect(center=(self.x,self.y))
        return rect

class Ray:
    def __init__(self, x_start, y_start, x_end, y_end, ray_width=2, color=(255,255,255)):
        self.x          = x_start
        self.y          = y_start
        self.x_end      = x_end
        self.y_end      = y_end
        self.color      = color
        self.ray_width  = ray_width
        all_effects.append(self)
        self.references = []
    def render(self, dest:pygame.Surface, x,y):
        dx = self.x_end - self.x
        dy = self.y_end - self.y
        pygame.draw.line(dest, self.color, (x, y), (x+dx, y+dy), width=self.ray_width)
        self.destroy()
    def destroy(self):
        deletor.Deleter.request_delete(self, all_effects)
        for l in self.references:
            deletor.Deleter.request_delete(self, l)

effect_types = MuzzleFlash|Ray|BulletHole|BloodSplot
all_effects:list[effect_types] = []