import pygame, os
from settings import *

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\assets")

class Overlay:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        