import pygame
import ALL_SPRITES
class Sprite:
    def __init__(self, images_links:list|tuple):
        self.image_links = images_links
        self.images:list[pygame.Surface] = []
        self.image_index = 0
        self.image_speed = 0
        for link in images_links:
            self.images.append(ALL_SPRITES.ASP[link])

    def get_current_image(self):
        return self.images[int(self.image_index)]

    def run_sprite(self):
        self.image_index += self.image_speed
        if self.image_index >= len(self.images):
            self.image_index = 0

    def set_image_speed(self, s:float):
        self.image_speed = s

    def set_image_index(self, i:int):
        self.image_index = int(i)

    def get_image_at(self, i:int):
        return self.images[i]

    def get_image_number(self):
        return len(self.images)

    def __copy__(self):
        return Sprite(self.image_links)


