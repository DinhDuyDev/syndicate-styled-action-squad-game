import Sprites
import pygame
import deletor
import math
import settings
import utilityfuncs
import camera
import random
import effects
import ALL_SPRITES

## ENTITIES ADT:
# - action()
# - render()
# ENTITIES ARE THINGS THAT ACT AS A STIMULUS TO THE ENVIRONMENT AROUND THEM.
# SOUND SOURCES ARE, FOR SOME REASON, NOT CONSIDERED ENTITIES?

GRENADE_DAMAGE = 200
MAP_GEOMETRY:list[list[int]]|None = None
class Grenade:
    def __init__(self, x, y, direction, targets:list, speed=5):
        self.x, self.y = x, y
        self.direction = direction
        self.sprite = Sprites.Sprite(
            ("GRENADE", "GRENADE")
        )
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.randint(6, 20)

        self.speed = speed
        self.vec_x = math.cos(math.radians(self.direction))
        self.vec_y = math.sin(math.radians(self.direction))

        self.timer = 2 * 60
        self.references = []
        self.attack_targets:list = targets

        self.cooldown = 0

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
            self.speed -= 0.5
            effects.MuzzleFlash(self.x, self.y)
        if MAP_GEOMETRY[__y][__xs] != 0:
            self.vec_y = -self.vec_y
            self.speed -= 0.5
            effects.MuzzleFlash(self.x, self.y)

        self.speed = max(self.speed - 0.05, 0)
        self.x += self.vec_x * self.speed
        self.y -= self.vec_y * self.speed
        self.rotation += self.rotation_speed
        self.rotation_speed *= 0.9

        if self.cooldown > 1:
            Smoke(self.x, self.y)
            self.cooldown = 0
        else:
            self.cooldown += 1

    def destroy(self):
        Explosion(self.x, self.y, GRENADE_DAMAGE, self.attack_targets)
        for l in self.references:
            deletor.Deleter.request_delete(self, l)
        deletor.Deleter.request_delete(self, all_entities)

    def render(self, dest:pygame.Surface, x, y):
        spr = pygame.transform.rotate(self.sprite.get_current_image(), self.rotation)
        spr_rect = spr.get_rect(center=(x,y))
        dest.blit(spr, spr_rect)

    def xy(self):
        return self.x, self.y

class Explosion:
    def __init__(self, x, y, radius, targets):
        self.x = x
        self.y = y
        self.radius = radius
        self.attack_targets:list = []
        for l in targets:
            self.attack_targets.append(l)
        # Damage
        for t in self.attack_targets:
            d = utilityfuncs.point_distance(self.x, self.y, t.xy()[0], t.xy()[1])
            if d <= radius:
                if utilityfuncs.line_of_sight(self.x, self.y, t.xy()[0], t.xy()[1], MAP_GEOMETRY):
                    t.take_damage(self.radius - d, self)
        all_entities.append(self)
        camera.Camera.activeCam.screen_shake(3)

    def action(self):
        self.destroy()
    def render(self, dest:pygame.Surface, x, y):
        pygame.draw.circle(dest, (255, 255, 255), (x, y), self.radius/2)
    def destroy(self):
        deletor.Deleter.request_delete(self, all_entities)

class Smoke:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = Sprites.Sprite(
            (
                "SMOKE1",
                "SMOKE2",
                "SMOKE3"
             )
        )
        self.rotation = random.randint(0, 360)
        self.references = []
        self.direction = random.randint(0, 360)
        self.speed = random.randint(3, 5) * 0.01
        self.sprite.set_image_speed(1/30)
        all_entities.append(self)

    def action(self):
        self.x += math.cos(math.radians(self.direction)) * self.speed
        self.y -= math.sin(math.radians(self.direction)) * self.speed
        self.sprite.run_sprite()
        if self.sprite.get_image_index() >= self.sprite.get_image_number()-1:
            self.destroy()
        self.rotation += 1

    def render(self, dest:pygame.Surface, x,y):
        spr = pygame.transform.rotate(self.sprite.get_current_image(), self.rotation)
        spr_rect = spr.get_rect(center=(x, y))
        dest.blit(spr, spr_rect)

    def destroy(self):
        deletor.Deleter.request_delete(self, all_entities)

class SoundSource:
    all_sounds_sources:list = []
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.num_alert = 3
        self.references = []
        SoundSource.all_sounds_sources.append(self)
    def destroy(self):
        deletor.Deleter.request_delete(self, SoundSource.all_sounds_sources)
        for l in self.references:
            deletor.Deleter.request_delete(self, l)

all_entities_type = Grenade|Explosion|Smoke
all_entities:list[all_entities_type] = []