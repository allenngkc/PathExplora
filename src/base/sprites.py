import pygame
from settings import *
from settings import LAYERS

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class Decorations(Generic):
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups, z)

class Trees(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)
