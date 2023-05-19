import pygame, os
from settings import *

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\..\\assets")

class GridSystem:
    def __init__(self, rows, cols):
        self.grids = []
        self.img = pygame.image.load(os.path.join(assets_dir, 'pathfinder\\Graphics\\bush.png')).convert_alpha()

        for r in range(rows):
            inner_arr = []
            for c in range(cols):
                inner_arr.append(GridCell(GRID_INIT_X + r*GRID_SIZE,GRID_INIT_Y + c*GRID_SIZE, self.img))
            self.grids.append(inner_arr)    

    def display_grids(self):
        for i in self.grids:
            for j in i:
                j.draw()


class GridCell:
    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.rect = self.surface.get_rect(topleft=(x,y))
        self.display_surface = pygame.display.get_surface()
        
        # Each grid defaults to be a empty cell
        if image:
            self.image = image
        else:
            self.image = None

    def draw(self):
        pygame.draw.rect(self.surface, (0,0,0), (0,0, GRID_SIZE, GRID_SIZE), 1)
        if self.image:
            self.surface.blit(self.image, (0,0))
        self.display_surface.blit(self.surface, (self.x, self.y))

    def update_image(self, image):
        self.image = image

