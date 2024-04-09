import pygame
import common.globals as globals
import common.image_handler as image_handler


class Character(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 5

    def __init__(self, position, width, height, character_name, window, is_player = False, lifes = 1):
        super().__init__()
        self.health = 100
        self.start_position = position
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.SPRITES = image_handler.load_sprite_sheets(32, 32, True, window, "MainCharacters", character_name)
        self.is_player = is_player
        self.lifes = lifes

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.health -= 10


    def set_x_velocity(self, velocity):
        self.x_vel = velocity
        if velocity < 0 and self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        if velocity > 0 and self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.y_vel = min(self.y_vel, self.GRAVITY * 8)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def is_alive(self):
        return (self.health > 0 and self.rect.y < globals.HEIGHT)
    
    def resurrect(self):
        self.lifes -= 1
        if self.lifes > 0:
            self.rect.x = self.start_position[0]
            self.rect.y = self.start_position[1]
            self.health = 100
            self.y_vel = 0

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel = abs(self.y_vel)

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y- offset_y))

