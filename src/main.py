import pygame, sys
from scenes.level import Level
from scenes.pathfinder import Pathfinder
from settings import *
from base.scene_manager import SceneManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Path Explora")
        self.clock = pygame.time.Clock()
        self.scene_manager = SceneManager(Pathfinder())

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.scene_manager.render(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()