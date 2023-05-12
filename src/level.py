import pygame, os
from base.sprites import Generic, Decorations, Trees
from player import Player
from settings import *

# Reading Tiled Map Editor's TMX maps
from pytmx.util_pygame import load_pygame

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\assets")

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.setup()

    def setup(self):
        # 3D world data
        tmx_data = load_pygame(os.path.join(assets_dir, 'world\\data\\map.tmx'))

        self.load_tmx_data(tmx_data)

        Generic(pos=(0,0),
                surf=pygame.image.load(os.path.join(assets_dir, 'world/ground.png')).convert_alpha(),
                groups=self.all_sprites,
                z=LAYERS['ground'])
        
    def load_tmx_data(self, tmx_data):

        # Converts tmx_data layers to game world
        def import_map_layers(layers, layer_settings, collision=False):
            for layer in layers:
                for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                    if not collision:
                        Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS[layer_settings])
                    else:
                        Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS[layer_settings])

        # Importing all the map layers
        import_map_layers(['HouseFloor', 'HouseFurnitureBottom'], 'house bottom')
        import_map_layers(['HouseWalls', 'HouseFurnitureTop'], 'house top')
        import_map_layers(['Fence'], 'main', True) 
        import_map_layers(['Hills'], 'main')
        import_map_layers(['Forest Grass', 'Outside Decoration'], 'ground plant')
        import_map_layers(['Ground'], 'ground')
        import_map_layers(['Water'], 'water')

        # Transparent collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), [self.all_sprites, self.collision_sprites])

        # Converts tmx_data objects to game world
        for obj in tmx_data.get_layer_by_name('Decoration'):
            Decorations((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites], LAYERS['main'])
        for obj in tmx_data.get_layer_by_name('Trees'):
            Trees((obj.x, obj.y), obj.image, self.all_sprites, obj.name)
        for obj in tmx_data.get_layer_by_name('Objects'):
            Trees((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites], obj.name)
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.customize_draw(self.player)
        self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        sprites_obj = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': []}

        # Saving all sprites to sprites_obj and sort to display them in order
        # for sprite in self.sprites():
        #     sprites_obj[str(sprite.z)].append(sprite)
            
        # for layer in sprites_obj:
        #     for sprite in sprites_obj[layer]:
        #         offset_rect = sprite.rect.copy()
        #         offset_rect.center -= self.offset
        #         self.display_surface.blit(sprite.image, offset_rect)

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)