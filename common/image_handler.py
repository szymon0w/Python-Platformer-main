from os import listdir
from os.path import isfile, join
import pygame
from common import globals

class ImageHandler:
    def __init__(self):
        self.floor = self.load_image(join("assets", "Terrain", "ground.png"))
        self.opponent = self.load_image(join("assets", "MainCharacters", "MaskDude", "jump.png"))
        self.start = self.load_image(join("assets", "MainCharacters", "NinjaFrog", "jump.png"))
        self.fire = self.load_image(join("assets", "Traps", "Fire", "fire.png"))
        self.finish = self.load_image(join("assets", "Items", "Checkpoints", "Checkpoint", "flag.png"))
        self.background = self.load_image(join("assets", "Background", "Bricks.png"))

    def load_image(self, image_path, scale = (globals.GRID_SIZE, globals.GRID_SIZE)):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, scale)
        return image

def load_sprite_sheets(width, height, direction, dir1, dir2, dir3 = ''):
    if dir3:
        path = join("assets", dir1, dir2, dir3)
    else:
        path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]