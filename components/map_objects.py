import pygame
from os.path import join
import common.image_handler as image_handler



def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, window):
        super().__init__(x, y, width, height, "fire")
        self.fire = image_handler.load_sprite_sheets( width, height, False, window, "Traps", "Fire")
        self.image = self.fire["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "on"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = int((self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites))
        self.image = sprites[sprite_index]
        self.animation_count += 0.5
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Finish(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, window):
        super().__init__(x, y, width, height, "finish")
        self.finish = image_handler.load_sprite_sheets(width, height, False, window, "Items", "Checkpoints", "Checkpoint")
        self.animation_name = "unfold_flag"
        self.image = self.finish[self.animation_name][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        print(self.finish[self.animation_name])

    def on(self):
        self.animation_name = "unfold_flag"

    def off(self):
        self.animation_name = "no_flag"

    def loop(self):
        sprites = self.finish[self.animation_name]
        sprite_index = int((self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites))
        self.image = sprites[sprite_index]
        self.animation_count += 0.5
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
            if self.animation_name == "unfold_flag":
                self.animation_name = "idle_flag"

