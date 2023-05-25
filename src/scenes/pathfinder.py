import pygame, os
from base.sprites import Generic, Trees
from base.grid_system import GridSystem
from overlay import Overlay
from settings import *

# Reading Tiled Map Editor's TMX maps
from pytmx.util_pygame import load_pygame

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\..\\assets")

class Pathfinder:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = WorldGroup()
        self.overlay = Overlay()
        self.setup()

    def setup(self):
        # 3D world data
        tmx_data = load_pygame(os.path.join(assets_dir, 'pathfinder\\pathfinder.tmx'))
        self.load_tmx_data(tmx_data)
        self.grid_system = GridSystem(16, 16)
        
        
    def load_tmx_data(self, tmx_data):
        # Converts tmx_data layers to game world
        def import_map_layers(layers, layer_settings, collision=False):
            for layer in layers:
                for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                    Generic((x * PATH_FINDER_TILE_SIZE, y * PATH_FINDER_TILE_SIZE), surf, self.all_sprites, LAYERS[layer_settings])

        # Importing all the map layers
        import_map_layers(['ground'], 'ground')
        import_map_layers(['hills'], 'main') 
        import_map_layers(['forest grass'], 'ground plant')

        # Converts tmx_data objects to game world
        for obj in tmx_data.get_layer_by_name('objects'):
            Trees((obj.x, obj.y), obj.image, self.all_sprites, obj.name)

        init_obj = tmx_data.get_layer_by_name('PathfindingStart')[0]
        self.x = init_obj.x
        self.y = init_obj.y

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.customize_draw(self.x, self.y)
        self.all_sprites.update(dt)   
        self.grid_system.display_grids()
        self.grid_system.check_input()
        self.draw_grid() 
        self.overlay.update()

    # Draw gridlines to user
    def draw_grid(self):
        blockSize = 30
        for x in range(270, 724, blockSize):
            for y in range(30, 510, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.display_surface, (255, 255, 255), rect, 1)

class WorldGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, viewx, viewy):
        self.offset.x = viewx - SCREEN_WIDTH / 2
        self.offset.y = viewy - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            # Using the sorted and lambda function here to determine the order of rendering the objects
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)