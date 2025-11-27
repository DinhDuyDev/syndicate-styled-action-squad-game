import Sprites
import pygame
import random

# Decorations ADT:
# x, y: (loc)
# repr_name: for file editor
# sprite: Sprite Object
# xy(): tuple of x and y
# render(dest, x, y): draws on the specified surface
# __copy__(): to copy itself
# __repr__(): Code representation
# All significant attributes necessary for object initialization must be available on the constructor
class Crate:
    def __init__(self, loc:tuple[int, int], is_wep_crate=False, destroyed=False):
        self.x, self.y = loc
        self.is_wep_crate = is_wep_crate

        self.sprite = Sprites.Sprite(
            (
                # Okay
                ("sprites/barrel_spr/crate_normal_top.png" if not destroyed else "sprites/barrel_spr/crate_normal_top_broken.png")
                if not is_wep_crate else
                ("sprites/barrel_spr/crate_weapons_top.png" if not destroyed else "sprites/barrel_spr/crate_weapons_broken_top.png"),
                "sprites/barrel_spr/crate_body.png" if not destroyed else "sprites/barrel_spr/crate_body_broken.png"
            )
        )
        self.repr_name = ""
        self.destroyed = destroyed
        self.angle = random.randint(0, 360)

    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc

    def xy(self):
        return self.x, self.y

    def render(self, dest:pygame.Surface, x, y):
        # self.angle += 0.5
        top_spr = self.sprite.get_image_at(0) #if not self.destroyed else self.sprite.get_image_at(2)
        body_spr = self.sprite.get_image_at(1) #if not self.destroyed else self.sprite.get_image_at(3)

        top_spr = pygame.transform.rotate(top_spr, self.angle)
        body_spr = pygame.transform.rotate(body_spr, self.angle)

        # Bottom
        dest.blit(top_spr, top_spr.get_rect(center=(x, y+2.5)))
        # Draw
        for i in range(1, 5):
            dest.blit(body_spr, body_spr.get_rect(center=(x, y+2.5-i)))
        # Top
        dest.blit(top_spr, top_spr.get_rect(center=(x, y-2.5)))

    def __copy__(self):
        return Crate((0, 0), is_wep_crate=self.is_wep_crate, destroyed=self.destroyed)

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

# All the types of decoration (just to make sure when I code the completion doesn't freak out)
all_decoration_types = Crate