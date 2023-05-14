import pygame
from settings import *
from base.spritesheet import SpriteSheet

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Decorations(Generic):
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups, z)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class Trees(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)
        # self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9) 

class Mailbox(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.frame_index = 0    
        self.init_anim()
        
    def update(self, dt):
        self.animate(dt)

    # Initialize the metadata we need to animate the object
    def init_anim(self):
        self.sprite_sheet = SpriteSheet('mailbox', 'unopen-mail')

        self.animations = []
        for index in range(0, 5):
            self.animations.append(self.sprite_sheet.parse_sprite(index))

    # Animate the mailbox
    def animate(self, dt):
        self.frame_index += 1.5 * dt
        if self.frame_index >= len(self.animations):
            self.frame_index = 0

        self.image = self.animations[int(self.frame_index)]


