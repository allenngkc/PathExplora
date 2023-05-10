import pygame, os, json

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\..\\assets")

class SpriteSheet:
    def __init__(self, object, filename):
        self.filename = filename
        self.object = object
        self.sprite_sheet = pygame.image.load(os.path.join(assets_dir, f"{object}\\{filename}.png")).convert_alpha()

    # Returns the sprite to the screen given current cycle index (x, y, w, h) from parse_sprite()
    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    # Accessing json file to obtain positions of the spritesheet
    def parse_sprite(self, index):
        json_path = os.path.join(assets_dir, f"{self.object}\\{self.filename}.json")

        with open(json_path, "r") as json_file:
            data = json.load(json_file)

        characters_keys = list(data["frames"].keys())
        frame_obj = data["frames"][characters_keys[index]]["frame"]
        return self.get_sprite(frame_obj["x"], frame_obj["y"], frame_obj["w"], frame_obj["h"])


