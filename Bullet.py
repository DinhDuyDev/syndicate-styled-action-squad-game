import math
import settings
import random
import effects

class Bullet:
    all_bullets = []
    def __init__(self, x, y, direction, spawner, damage=10, r=64, deviation=7):
        self.x, self.y = x, y
        self.x_start, self.y_start = x, y
        self.direction = direction
        self.deviation = deviation
        self.spawner = spawner
        self.damage = damage
        self.range = r
        Bullet.all_bullets.append(self)

    def work(self, map_matrix:list[list[int]]):
        dev = random.randrange(-self.deviation, self.deviation)
        vec_x = math.cos(math.radians(self.direction+dev))
        vec_y = math.sin(math.radians(self.direction+dev))
        while self.range > 0:
            self.x += vec_x * 4
            self.y -= vec_y * 4
            __x, __y = int(self.x/settings.cell_dimension), int(self.y/settings.cell_dimension)
            if map_matrix[__y][__x] != 0:
                effects.MuzzleFlash(self.x, self.y)
                break
            self.range -= 1

        # Ray(self.x_start, self.y_start, self.x, self.y)
        Bullet.all_bullets.remove(self)


class Ray:
    all_rays = []
    def __init__(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end   = x_end
        self.y_end   = y_end
        Ray.all_rays.append(self)
        print(Ray.all_rays)
    def render(self, draw_dest):
        Ray.all_rays.remove(self)