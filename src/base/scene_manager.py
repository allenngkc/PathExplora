import pygame

class SceneManager:
    def __init__(self):
        self.cur_scene = None

    def render(self, dt):
        self.cur_scene.run(dt)

    def update_scene(self, scene):
        self.cur_scene = scene