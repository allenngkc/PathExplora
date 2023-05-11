import pygame
from settings import *
from base.spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pygame.Surface((96,96))
        self.rect = self.image.get_rect(center = pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 275

        self.display_surface = pygame.display.get_surface()
        
        # Rendering dimension
        self.z = LAYERS['main']
        
        # Player Status
        self.status = 'down'
        self.idle = True
        self.frame_index = 0

        self.init_anim()
        self.image = self.animations['down'][0]
        


    # Initialize the animations from spritesheets
    def init_anim(self):
        self.sprites = [SpriteSheet("player", "player-up"), SpriteSheet("player", "player-down"),
                        SpriteSheet("player", "player-left"), SpriteSheet("player", "player-right")]
        self.animations = {'up': [], 'down': [], 'left': [], 'right': []}

        direction_keys = list(self.animations.keys())

        cur_dir = 0 # Looping cur_dir to indicate which direction of sprites apply to animation

        for sprite in self.sprites:
            for i in range(0, 4):
                # Appending sprite to self.animations by calling parse_sprite() in from spitesheet.py
                self.animations[direction_keys[cur_dir]].append(sprite.parse_sprite(i))

            cur_dir += 1

    # Animate the character
    def animate(self, dt):
        # If user is not moving, then don't animate the player
        if self.idle: return

        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    # Handling user input and defining self.status for character animation
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
            self.idle = False
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
            self.idle = False
        else:
            self.direction.y = 0
            self.idle = True
        
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
            self.idle = False
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
            self.idle = False
        else:
            self.direction.x = 0

    def move(self, dt):
        # Normalize the value of self.direction to prevent exceeding the desired speed
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Handling the x position
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Handling the y position
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)