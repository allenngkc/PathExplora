import pygame
from base.spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pygame.Surface((16,48))
        # self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.display_surface = pygame.display.get_surface()

        # Initialize character animations sprites
        self.sprite_up = SpriteSheet("player", "player-up")
        self.sprite_down = SpriteSheet("player", "player-down")
        self.sprite_left = SpriteSheet("player", "player-left")
        self.sprite_right = SpriteSheet("player", "player-right")

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_p]:
            print("Key P Pressed")
            self.display_surface.blit(self.sprite_up.parse_sprite(1), (100, 50))

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)