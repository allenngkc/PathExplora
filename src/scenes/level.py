import pygame, os
from base.sprites import Generic, Decorations, Trees, Mailbox, MailboxTrigger, Base
from player import Player
from overlay import Overlay
from settings import *
from scenes.pathfinder import Pathfinder

# Reading Tiled Map Editor's TMX maps
from pytmx.util_pygame import load_pygame

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\..\\assets")

class Level:
    def __init__(self, scene_manager):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.scene_manager = scene_manager
        self.setup()
        
    def setup(self):
        # 3D world data
        tmx_data = load_pygame(os.path.join(assets_dir, 'world\\data\\map.tmx'))

        # Handling mailbox overlay when user collides with the mailbox, initializes the objects and groups needed
        button_obj = tmx_data.get_layer_by_name('MailboxButton')[0]
        buttonFont = pygame.font.Font(os.path.join(assets_dir, 'world\\m6x11.ttf'), 16)
        self.ui_sprites = MailboxGroup(button_obj.x, button_obj.y, button_obj.image, self.all_sprites)

        self.load_tmx_data(tmx_data)
        
        
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
        import_map_layers(['Ground'], 'ground')
        import_map_layers(['HouseFloor', 'HouseFurnitureBottom'], 'house bottom')
        import_map_layers(['HouseWalls', 'HouseFurnitureTop'], 'main')
        import_map_layers(['Fence'], 'main') 
        import_map_layers(['Hills'], 'main')
        import_map_layers(['Forest Grass', 'Outside Decoration'], 'ground plant')
        import_map_layers(['Ground'], 'ground')
        import_map_layers(['Water'], 'water')

        # Transparent collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

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



        # Spawning mailbox object and starting the animation
        for obj in tmx_data.get_layer_by_name('Mailbox'):
            Mailbox((obj.x, obj.y), obj.image, self.all_sprites)

        # Mailbox Trigger as a collision check object placed within the mailbox position
        for x, y, surf in tmx_data.get_layer_by_name('MailboxTrigger').tiles():
            MailboxTrigger((x * TILE_SIZE, y * TILE_SIZE), 
                           pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA), self.ui_sprites, self.player)

            
    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.customize_draw(self.player)
        self.all_sprites.update(dt)

        self.ui_sprites.customize_draw(self.player)
        self.ui_sprites.update(dt)

        # TEMP FOR TRANSITIONING SCENE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.scene_manager.update_scene(Pathfinder())

        # self.overlay.display()


""" 
CameraGroup class exists to check for player movement to match with objects rendering
By constantly being called on update functions, through customize_draw(), when evaulating
player's movement and computing the offsets xy positions. This class is able to render
objects mostly from tmx_data to the game world. 
"""
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player):
        # Computing the offsets
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            # Using the sorted and lambda function here to determine the order of rendering the objects
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

"""
Mailbox Group specially exists to check for collison between Player and MailboxTrigger,
If collided, customize_draw() will blit self.button_overlay, oppositely, not blitting if
Not colliding, one potential problem for this class would be the class arguments, as
It might not be a good practice ask for specfic arguments from a class. But in this case
This class has only one usage.
"""
class MailboxGroup(CameraGroup):
    def __init__(self, bx, by, bimage, camera_group_ref):
        super().__init__()
        self.bx = bx
        self.by = by
        self.image = bimage
        self.clicked = False
        
        # Getting the current camera group reference to display images
        self.camera_group_ref = camera_group_ref

        self.button_overlay = Base((bx, by), bimage)

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # Abundancy code here, don't really need to iterate all the layers and sprites, but it works
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    if not player.hitbox.colliderect(sprite.hitbox) or self.clicked:
                        continue

                    # Player is colliding with object
                    offset_rect = self.button_overlay.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(self.button_overlay.image, offset_rect)
                    self.show_dialogue()

    def show_dialogue(self):
        # If key is pressed, then show dialogue to user
        dialogue_surf = pygame.image.load(os.path.join(assets_dir, 'ui\\dialog.png')).convert_alpha()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.clicked = True
            Generic((self.bx-30, self.by-80), dialogue_surf, self.camera_group_ref, LAYERS['ui'])

