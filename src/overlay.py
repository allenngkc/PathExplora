import pygame, os
from settings import *

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\assets")

class Overlay:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.tiles = ['grass', 'wall2']

        self.selection_ui = pygame.image.load(os.path.join(assets_dir, 'ui\\selection.png')).convert_alpha()

    # Check for user input for block selection
    def block_cursor_trigger(self):
        pass
        
    def display(self):
        self.display_surface.blit(self.selection_ui, (-50,350))
        # Draw block trigger
        # for block in self.blocks:
        #      block.draw()

    def update(self):
         self.display()
         self.block_cursor_trigger()

"""
This class represents the blocks that are avaiable for the user to place, right now
The visualizer only has two blocks (Walls, Blank). This class exists to assist the
Implementation of Overlay, by using constants to locate the ui elements. Future
Blocks could be added (Features such as weighted path finding etc.) Which might
require a rewrite of this class/system if needed to made scalable. 
"""
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surface = pygame.Surface((48, 48), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(x,y))

        self.display_surface = pygame.display.get_surface()

    def draw(self):
        self.display_surface.blit(self.surface, (self.x, self.y))

                    