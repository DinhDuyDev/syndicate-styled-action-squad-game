import settings
import pygame
import utilityfuncs
class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.count = 0
        self.frames = 3

    def action(self):
        max_hor = settings.hor_cells
        max_ver = settings.ver_cells

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_LEFT]) - (keys[pygame.K_a] or keys[pygame.K_RIGHT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_DOWN])

        if self.count > self.frames:
            self.offset_x = utilityfuncs.clamp(self.offset_x+dx, 0, max_hor-settings.hor_cells/2)
            self.offset_y = utilityfuncs.clamp(self.offset_y+dy, 0, max_ver-settings.ver_cells/2)
            self.count = 0
        self.count += 1

    def set_pos(self, x, y):
        self.offset_x = x
        self.offset_y = y

    def get_pos(self):
        return self.offset_x, self.offset_y

