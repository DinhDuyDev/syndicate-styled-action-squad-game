import Sprites
import pygame
import deletor
import math
import settings
## ENTITIES ADT:
# - action()
# - render()
MAP_GEOMETRY:list[list[int]]|None = None
class Grenade:
    def __init__(self, x, y, direction,speed=5):
        self.x, self.y = x, y
        self.direction = direction
        self.sprite = Sprites.Sprite(
            ("GRENADE", "GRENADE")
        )
        self.rotation = 0
        self.speed = speed
        self.vec_x = math.cos(math.radians(self.direction))
        self.vec_y = math.sin(math.radians(self.direction))

        self.timer = 5 * 60
        self.references = []
        all_entities.append(self)

    def action(self):
        self.timer -= 1
        if self.timer <= 0:
            self.destroy()

        __x = int((self.x+self.vec_x * (self.speed*1.5+2))/settings.cell_dimension)
        __y = int((self.y-self.vec_y * (self.speed*1.5+2))/settings.cell_dimension)

        __xs = int(self.x/settings.cell_dimension)
        __ys = int(self.y/settings.cell_dimension)

        if MAP_GEOMETRY[__ys][__x] != 0:
            self.vec_x = -self.vec_x
        if MAP_GEOMETRY[__y][__xs] != 0:
            self.vec_y = -self.vec_y

        self.speed = max(self.speed - 0.05, 0)
        self.x += self.vec_x * self.speed
        self.y -= self.vec_y * self.speed
    def destroy(self):
        for l in self.references:
            deletor.Deleter.request_delete(self, l)
        deletor.Deleter.request_delete(self, all_entities)

    def render(self, dest:pygame.Surface, x, y):
        spr = self.sprite.get_current_image()
        spr_rect = spr.get_rect(center=(x,y))
        dest.blit(spr, spr_rect)
        print("drawing grenade")

    def xy(self):
        return self.x, self.y

all_entities_type = Grenade
all_entities:list[all_entities_type] = []