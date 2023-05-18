import pygame, sys, os
from scenes.level import Level
from scenes.pathfinder import Pathfinder
from settings import *
from base.scene_manager import SceneManager

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\assets")

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Path Explora")
        self.clock = pygame.time.Clock()
        self.scene_manager = SceneManager(Pathfinder())
        self.display_surface = pygame.display.get_surface()

    def run(self):

        # Implement custom mouse cursor
        pygame.mouse.set_visible(False)
        cursor = pygame.image.load(os.path.join(assets_dir, 'cursor.png'))
        cursor_rect = cursor.get_rect()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            pygame.display.update()
            self.scene_manager.render(dt)
            

            # Handle cursor movements
            cursor_rect.center = pygame.mouse.get_pos()
            self.display_surface.blit(cursor, cursor_rect)
            

if __name__ == '__main__':
    game = Game()
    game.run()