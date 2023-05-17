import pygame

class SceneManager:
    def __init__(self, initial_scene):
        self.scenes = [initial_scene]

    def render(self, dt):
        self.scenes[-1].run(dt)
