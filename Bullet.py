import math
import settings
import random
import effects

class PlayerBullet:
    all_bullets = []
    def __init__(self, x, y, direction, spawner, damage=10, r=64, deviation=7,lives=1,create_ray=False):
        self.x, self.y = x, y
        self.x_start, self.y_start = x, y
        self.direction = direction
        self.deviation = deviation
        self.spawner = spawner
        self.damage = damage
        self.range = r
        self.lives = lives
        self.hit_targets = []
        self.create_ray = create_ray
        PlayerBullet.all_bullets.append(self)

    def work(self, map_matrix:list[list[int]], enemy_instances:list):
        dev = random.randrange(-self.deviation, self.deviation)
        vec_x = math.cos(math.radians(self.direction+dev))
        vec_y = math.sin(math.radians(self.direction+dev))
        while self.range > 0:
            self.x += vec_x * 4
            self.y -= vec_y * 4
            __x, __y = int(self.x/settings.cell_dimension), int(self.y/settings.cell_dimension)
            if map_matrix[__y][__x] != 0:
                effects.MuzzleFlash(self.x, self.y)
                self.range = -1000 # end the movement
                # Create bullet holes
                obstructed = False
                for hole in effects.BulletHole.all_bullet_holes:
                    if hole.get_hitbox().collidepoint(self.x, self.y):
                        obstructed = True
                if not obstructed:
                    effects.BulletHole(self.x+vec_x*1.5, self.y-vec_y*1.5)

            else:
                for e in enemy_instances:
                    hitbox = e.sprite.get_current_image().get_rect(center=(e.xy()[0], e.xy()[1]))
                    if hitbox.collidepoint(self.x, self.y) and e not in self.hit_targets:
                        self.hit_targets.append(e)
                        effects.MuzzleFlash(self.x, self.y)
                        self.lives -= 1
                        break
                if self.lives <= 0:
                    self.range = -1000
            self.range -= 1
        for hit in self.hit_targets:
            hit.hp -= self.damage

        if self.create_ray:
            effects.Ray(self.x_start, self.y_start, self.x, self.y)
        PlayerBullet.all_bullets.remove(self)