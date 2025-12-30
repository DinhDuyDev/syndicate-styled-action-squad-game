import math
import deletor
import settings
import random
import effects
import utilityfuncs
import entities

class PlayerBullet:
    all_bullets = []
    def __init__(self, x, y, direction, spawner, damage=10, r=64, deviation=7,lives=1,create_ray=False):
        self.x, self.y = x, y
        self.x_start, self.y_start = x, y
        self.direction = direction
        self.deviation = deviation
        self.spawner = spawner
        self.damage = damage
        self._range = r
        self.lives = lives
        self.hit_targets = []
        self.create_ray = create_ray

        v = entities.Smoke(self.x, self.y)
        v.direction = self.direction + random.randrange(-17, 17)
        v.speed = random.randrange(1, 5) * 0.1
        PlayerBullet.all_bullets.append(self)

    def work(self, map_matrix:list[list[int]], enemy_instances:list):
        dev = random.randrange(-self.deviation, self.deviation)
        vec_x = math.cos(math.radians(self.direction+dev))
        vec_y = math.sin(math.radians(self.direction+dev))
        while self._range > 0:
            self.x += vec_x * 4
            self.y -= vec_y * 4
            __x, __y = int(self.x/settings.cell_dimension), int(self.y/settings.cell_dimension)
            __fx, __fy = int((self.x+vec_x*4)/settings.cell_dimension), int((self.y-vec_y*4)/settings.cell_dimension)
            hit_wall = map_matrix[__fy][__x] != 0 or map_matrix[__y][__fx] != 0
            rebound_direction = 0
            if map_matrix[__fy][__x] != 0: # x-plane:
                rebound_direction = utilityfuncs.point_direction(0, 0, 0, -vec_y)
            elif map_matrix[__y][__fx] != 0: # y-plane:
                rebound_direction = utilityfuncs.point_direction(0, 0, vec_x, 0)

            if hit_wall:
                effects.MuzzleFlash(self.x, self.y)
                self._range = -1000 # end the movement
                v = entities.Smoke(self.x, self.y)
                v.direction = rebound_direction
                v.speed = -random.random() * 0.4
                for i in range(4):
                    entities.DustParticles(self.x, self.y, direction=rebound_direction+180 + random.randrange(-17, 17))

            else:
                for e in enemy_instances:
                    hitbox = e.sprite.get_current_image().get_rect(center=(e.xy()[0], e.xy()[1]))
                    if hitbox.collidepoint(self.x, self.y) and e not in self.hit_targets:
                        self.hit_targets.append(e)
                        effects.MuzzleFlash(self.x, self.y)
                        self.lives -= 1
                        __d = utilityfuncs.point_direction(self.x, self.y, e.x, e.y)
                        break
                if self.lives <= 0:
                    self._range = -1000
            self._range -= 1
        for hit in self.hit_targets:
            hit.take_damage(self.damage, self.spawner)

        if self.create_ray:
            effects.Ray(self.x_start, self.y_start, self.x, self.y)
        deletor.Deleter.request_delete(self, PlayerBullet.all_bullets)