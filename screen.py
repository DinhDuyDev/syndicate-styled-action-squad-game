import pygame
from pygame.locals import *
class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), FULLSCREEN|HWSURFACE|DOUBLEBUF|RESIZABLE|SCALED, vsync=1)

    def get_dimensions(self):
        return self.screen.get_width(), self.screen.get_height()