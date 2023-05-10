import pygame, os
from base.sprites import Generic
from player import Player

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\assets")

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.setup()

    def setup(self):
        Generic(pos=(0,0),
                surf=pygame.image.load(os.path.join(assets_dir, 'world/ground.png')).convert_alpha(),
                groups=self.all_sprites)
        self.player = Player((512, 384), self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.customize_draw()
        self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def customize_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)