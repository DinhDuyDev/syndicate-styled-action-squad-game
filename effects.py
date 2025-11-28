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
        surf = self.sprite.get_current_image()
        rect = surf.get_rect(center=(x,y))
        dest.blit(surf, rect)
        all_effects.remove(self)

effect_types = MuzzleFlash
all_effects:list[effect_types] = []
