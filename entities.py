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

GRENADE_DAMAGE = 130
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
            Smoke(self.x, self.y, decrease_multiplier=1)
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

class Rocket:
    def __init__(self, x, y, direction, targets: list, explosion_affects:list, spawner=None, speed=10):#10):
        self.x, self.y = x, y
        self.direction = direction
        self.sprite = Sprites.Sprite(
            ("GRENADE", "GRENADE")
        )
        self.explosion_affects = explosion_affects # NOT A VERY GOOD HACK-AROUND
        self.spawner = spawner
        self.speed = speed
        self.real_speed = 0.5
        self.vec_x = math.cos(math.radians(self.direction))
        self.vec_y = math.sin(math.radians(self.direction))

        self.timer = 5 * 60
        self.references = []
        self.attack_targets:list = targets

        self.cooldown = 0

        self.damage = 120
        self.rocket_scale = 0.1
        all_entities.append(self)

    def action(self):
        self.rocket_scale = min(self.rocket_scale + 0.05, 1)
        self.real_speed = min(self.real_speed + 0.2, self.speed)
        collided = False
        self.timer -= 1
        if self.timer <= 0:
            self.destroy()

        __x = int((self.x+self.vec_x * (self.speed+2))/settings.cell_dimension)
        __y = int((self.y-self.vec_y * (self.speed+2))/settings.cell_dimension)

        __xs = int(self.x/settings.cell_dimension)
        __ys = int(self.y/settings.cell_dimension)

        if MAP_GEOMETRY[__ys][__x] != 0:
            effects.MuzzleFlash(self.x, self.y)
            collided = True
        if MAP_GEOMETRY[__y][__xs] != 0:
            effects.MuzzleFlash(self.x, self.y)
            collided = True

        self.x += self.vec_x * self.real_speed
        self.y -= self.vec_y * self.real_speed

        for target in self.attack_targets:
            if self.get_hitbox().colliderect(target.get_hitbox()):
                target.take_damage(90, self.spawner)
                collided = True
                break
                self.destroy()

        for i in range(3):
            s = Smoke(self.x - self.vec_x * self.speed, self.y + self.vec_y * self.speed
                      , decrease_multiplier=0.96, initial_scale=2)
            s.direction = self.direction + 180 + random.randrange(-10, 10)
            s.speed = random.random() * 3

        if collided:
            self.destroy()

    def get_hitbox(self):
        return pygame.transform.scale_by(self.sprite.get_current_image(), self.rocket_scale).get_rect(center=(self.x, self.y))
    def destroy(self):
        print("Bug")
        Explosion(self.x - self.vec_x * 8, self.y + self.vec_y * 8, GRENADE_DAMAGE, self.explosion_affects)
        for l in self.references:
            deletor.Deleter.request_delete(self, l)
        deletor.Deleter.request_delete(self, all_entities)

    def render(self, dest:pygame.Surface, x, y):
        # spr = self.sprite.get_current_image()
        # spr_rect = spr.get_rect(center=(x,y))
        juan = self.x # Emotional support
        dest_surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        core_rocket = pygame.Surface((24, 24), pygame.SRCALPHA)
        dest_rect = dest_surf.get_rect(center=(x,y))
        core_rect = core_rocket.get_rect(center=(x,y))
        pygame.draw.circle(dest_surf, (255, 255, 255), (32,32), random.random()*31)
        dest_surf.set_alpha(200)
        core_rocket.fill((0,0,0,0))
        pygame.draw.circle(core_rocket, (255, 255, 255), (12,12), random.random()*11)

        dest.blit(core_rocket, core_rect)
        dest.blit(dest_surf, dest_rect)

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

        # Effects
        for i in range(16):
            x_rand = self.x+random.randint(-32, 32)
            y_rand = self.y+random.randint(-32, 32)
            Smoke(x_rand, y_rand)

        # Rays
        for i in range(4):
            d = random.random()*360
            l = random.random()*112 + 48
            vec_x = math.cos(math.radians(d)) * l
            vec_y = math.sin(math.radians(d)) * l
            effects.Ray(self.x, self.y, self.x+vec_x, self.y-vec_y)

        # Smoke rays
        for i in range(7):
            SmokeTrail(self.x, self.y, random.random()*0.2+1, random.random()*360, last_length=2*60)

    def action(self):
        self.destroy()
    def render(self, dest:pygame.Surface, x, y):
        pygame.draw.circle(dest, (255, 255, 255), (x, y), self.radius/2)
    def destroy(self):
        deletor.Deleter.request_delete(self, all_entities)

class DustParticles:
    def __init__(self, x, y, direction=0):
        self.x = x
        self.y = y
        all_entities.append(self)
        self.color = (255, 0, 255)
        self.references = []
        self.cooldown = random.randrange(0, 7)
        self.speed = random.random() * 2
        self.direction = direction#random.random() * 360

    def action(self):
        self.x += math.cos(math.radians(self.direction)) * self.speed
        self.y -= math.sin(math.radians(self.direction)) * self.speed
        if self.cooldown < 0:
            self.destroy()
        else:
            self.cooldown -= 0.5

    def render(self, dest: pygame.Surface, x, y):
        pygame.draw.rect(dest, self.color, (x-1, y-1, 2, 2))

    def destroy(self):
        deletor.Deleter.request_delete(self, all_entities)
        for l in self.references:
            deletor.Deleter.request_delete(self, l)

class Smoke:
    def __init__(self, x, y, decrease_multiplier=0.97, initial_scale=1):
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
        self.scale = initial_scale
        self.decrease_multiplier = decrease_multiplier
        self.vec_x = math.cos(math.radians(self.direction)) * self.speed
        self.vec_y = math.sin(math.radians(self.direction)) * self.speed
        self.started = True
        all_entities.append(self)

    def action(self):
        if self.started:
            self.vec_x = math.cos(math.radians(self.direction)) * self.speed
            self.vec_y = math.sin(math.radians(self.direction)) * self.speed
            self.started = False

        front_x = self.x + self.vec_x * 2
        front_y = self.y - self.vec_y * 2

        if MAP_GEOMETRY[int(front_y / settings.cell_dimension)][int(self.x / settings.cell_dimension)] != 0:
            self.vec_y = 0
        else:
            self.x += self.vec_x
        if MAP_GEOMETRY[int(self.y / settings.cell_dimension)][int(front_x / settings.cell_dimension)] != 0:
            self.vec_x = 0
        else:
            self.y -= self.vec_y

        self.sprite.run_sprite()
        if self.sprite.get_image_index() >= self.sprite.get_image_number()-1:
            self.destroy()
        self.rotation += 1
        self.scale *= self.decrease_multiplier

    def render(self, dest:pygame.Surface, x,y):
        spr = pygame.transform.scale_by(pygame.transform.rotate(self.sprite.get_current_image(), self.rotation), self.scale)
        spr_rect = spr.get_rect(center=(x, y))
        dest.blit(spr, spr_rect)

    def destroy(self):
        for l in self.references:
            deletor.Deleter.request_delete(self, l)
        deletor.Deleter.request_delete(self, all_entities)

class SmokeTrail:
    def __init__(self, x:float, y:float, speed:float, direction:float, create_cooldown:int=1, last_length:int=60, gravity:bool=False):
        self.x, self.y = x, y
        self.direction = direction
        self.speed = speed
        self.vec_x = math.cos(math.radians(direction)) * speed
        self.vec_y = math.sin(math.radians(direction)) * speed
        self.create_cooldown = create_cooldown
        self.cooldown = 0
        self.last_length = last_length
        self.references = []

        # Gravity effects
        self.gravity = gravity
        self.grav_speed = -random.random() * 5
        self.grav_accel = 0.2
        self.grav_limit = 4

        all_entities.append(self)


    def action(self):
        front_x = self.x + self.vec_x * 2
        front_y = self.y - self.vec_y * 2 + self.grav_speed
        self.x += self.vec_x
        self.y -= self.vec_y

        if MAP_GEOMETRY[int(front_y / settings.cell_dimension)][int(self.x / settings.cell_dimension)] != 0:
            self.vec_y = 0
            if self.grav_speed > 0:
                self.grav_speed = 0
            else:
                self.grav_speed = -self.grav_speed
        else:
            self.x += self.vec_x
        if MAP_GEOMETRY[int(self.y / settings.cell_dimension)][int(front_x / settings.cell_dimension)] != 0:
            self.vec_x = 0
        else:
            self.y -= self.vec_y

        # Gravity
        if self.gravity:
            self.y += self.grav_speed
            self.grav_speed = min(self.grav_speed + self.grav_accel, self.grav_limit)

        # Dying
        self.last_length -= 1
        if self.last_length <= 0:
            self.destroy()

        # Create smoke
        self.cooldown += 1
        if self.cooldown > self.create_cooldown:
            s = Smoke(self.x, self.y)
            s.direction = self.direction + random.randrange(-20, 20)
            s.speed = random.random() * 2
            self.cooldown = 0

    def render(self, dest:pygame.Surface, x, y):
        pass

    def destroy(self):
        for l in self.references:
            deletor.Deleter.request_delete(self, l)
        deletor.Deleter.request_delete(self, all_entities)

class SoundSource:
    all_sounds_sources:list = []
    def __init__(self, x, y, radius, sound_tag="GUNSHOT"):
        self.x = x
        self.y = y
        self.radius = radius
        self.num_alert = 3
        self.references = []
        self.sound_tag = sound_tag
        SoundSource.all_sounds_sources.append(self)
    def destroy(self):
        deletor.Deleter.request_delete(self, SoundSource.all_sounds_sources)
        for l in self.references:
            deletor.Deleter.request_delete(self, l)

all_entities_type = Grenade|Explosion|Smoke|SmokeTrail|DustParticles|Rocket
all_entities:list[all_entities_type] = []

enemyGroup = pygame.sprite.Group()
class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
