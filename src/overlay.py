import pygame, os
from settings import *

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\assets")

class Overlay:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        self.ui_dialog = pygame.image.load(os.path.join(assets_dir, 'ui\\dialog.png')).convert_alpha()
        
    def display(self):
        self.display_surface.blit(self.ui_dialog,(0,0))

        