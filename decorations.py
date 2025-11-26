import Sprites
import pygame

class Crate:
    def __init__(self, loc:tuple[int, int], is_wep_crate=False):
        self.x, self.y = loc
        self.sprite = Sprites.Sprite(
            (
                # Okay
                "sprites/barrel_spr/crate_normal_top.png" if not is_wep_crate else "sprites/barrel_spr/crate_weapons_top.png",
                "sprites/barrel_spr/crate_body.png",

                # Broken
                "sprites/barrel_spr/crate_normal_top_broken.png" if not is_wep_crate else "sprites/barrel_spr/crate_weapons_broken_top.png",
                "sprites/barrel_spr/crate_body_broken.png"
            )
        )
        self.destroyed = False
        self.angle = 0

    def xy(self):
        return self.x, self.y

    def render(self, dest:pygame.Surface, x, y):
        self.angle += 0.5
        top_spr = self.sprite.get_image_at(0) if not self.destroyed else self.sprite.get_image_at(2)
        body_spr = self.sprite.get_image_at(1) if not self.destroyed else self.sprite.get_image_at(3)

        top_spr = pygame.transform.rotate(top_spr, self.angle)
        body_spr = pygame.transform.rotate(body_spr, self.angle)

        # Bottom
        dest.blit(top_spr, top_spr.get_rect(center=(x, y+2.5)))
        # Draw
        for i in range(1, 5):
            dest.blit(body_spr, body_spr.get_rect(center=(x, y+2.5-i)))
        # Top
        dest.blit(top_spr, top_spr.get_rect(center=(x, y-2.5)))