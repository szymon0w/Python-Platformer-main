from collections import defaultdict
import pygame
from os.path import join
import common.globals as globals
from components.characters import Character
import components.map_objects as map_objects
import sys
import json


# pygame.init()
# pygame.display.set_caption("Platformer")

lava_img = pygame.image.load(join("assets", "Background", "lava.png"))
heart_img = pygame.image.load(join("assets", "MainCharacters", "heart.png"))
heart_img = pygame.transform.scale(heart_img, (20, 20))

class Game:
    def __init__(self, level_number, window):
        self.window = window
        self.level_number = level_number
        self.background, self.bg_image = self.get_background("Bricks.png")
        level_data = self.load_level()
        self.player = level_data["player"]
        self.opponents = level_data["opponents"]
        self.floor = level_data["floor"]
        self.fires = level_data["fires"]
        self.finish = level_data["finish"]
        self.objects = [*self.floor, *self.fires, *self.finish]
        self.scroll_area_width = globals.WIDTH//3
        self.scroll_area_height = globals.HEIGHT//3
        self.offset_x = self.player.rect.left - self.scroll_area_width
        self.offset_y = self.player.rect.top - self.scroll_area_height
    
    
    def get_background(self, name):
        image = pygame.image.load(join("assets", "Background", name))
        _, _, width, height = image.get_rect()
        tiles = []

        for i in range(globals.WIDTH // width + 1):
            for j in range(globals.HEIGHT // height + 1):
                pos = (i * width, j * height)
                tiles.append(pos)

        return tiles, image


    def draw(self, background, bg_image, player, opponents, objects, offset_x, offset_y):
        for tile in background:
            self.window.blit(bg_image, tile)
        
        for obj in objects:
            obj.draw(self.window, offset_x, offset_y)
        
        for opponent in opponents:
            opponent.draw(self.window, offset_x, offset_y)

        player.draw(self.window, offset_x, offset_y)


        darken_surface = pygame.Surface((globals.WIDTH, globals.HEIGHT), pygame.SRCALPHA)
        for i in range(0, globals.HEIGHT, 10):
            darken = min((255 - ((i + offset_y)//4)), 200)
            darken = max(darken, 0)
            pygame.draw.rect(darken_surface, (0, 0, 0, darken), pygame.Rect(0, i, globals.WIDTH, 10))
        
        for obj in objects:
            obj.draw_light(darken_surface, offset_x, offset_y)    
        self.window.blit(darken_surface, (0, 0))




        for i in range (-5, 10):
            self.window.blit(lava_img, (i*(767) - offset_x, globals.HEIGHT - offset_y))

        for i in range (player.lifes):
            self.window.blit(heart_img, (globals.WIDTH - 30 - i * 22, 10))
        



    def handle_vertical_collision(self, character, objects, y_vel):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(character, obj):
                if y_vel > 0 and (abs(character.rect.bottom - obj.rect.top) < (character.rect.height/4)):
                    character.rect.bottom = obj.rect.top
                    character.landed()
                elif y_vel < 0:
                    character.rect.top = obj.rect.bottom
                    character.hit_head()

                collided_objects.append(obj)

        return collided_objects


    def collide(self, character, objects, dx, dy = 0):
        character.move(dx, dy)
        character.update()
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(obj, character):
                collided_objects.append(obj)

        character.move(-dx, -dy)
        character.update()
        return collided_objects

    def move_player(self, player, objects, opponents):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player.jump_count < 2:
            self.player.jump()
        if keys[pygame.K_LEFT]:
            new_level = self.handle_move(player, objects, -globals.PLAYER_VEL)
        elif keys[pygame.K_RIGHT]:
            new_level = self.handle_move(player, objects, globals.PLAYER_VEL)
        else:
            new_level = self.handle_move(player, objects, 0)


        if pygame.sprite.spritecollideany(player, opponents):
            player.make_hit()
        
        return new_level

    def on_the_edge(self, character, objects, velocity):
        if self.collide(character, objects, velocity, 20):
            return False
        else:
            return True

    def handle_move(self, character, objects, velocity):
        character.x_vel = 0

        predicted_collisions = self.collide(character, objects, velocity * 3)
        if not predicted_collisions:
            character.set_x_velocity(velocity)

        vertical_collide = self.handle_vertical_collision(character, objects, character.y_vel)
        if not character.is_player and self.on_the_edge(character, objects, velocity*10):
            character.y_vel = 0
            character.x_vel = 0
        to_check = [*predicted_collisions, *vertical_collide]

        for obj in to_check:
            if obj and obj.name == "fire":
                character.make_hit()
            elif character.is_player and obj and obj.name == "finish":
                self.level_number += 1
                return(self.load_level())
            

    def load_level(self):
        print("Loading level", self.level_number)
        map = None
        with open('assets/maps.json') as f:
            map = json.load(f)["maps"][self.level_number]

        level_data = defaultdict(list)
        offset_y = 8 - len(map["level"])
        for y in range(len(map["level"])):
            for x in range(len(map["level"][self.level_number])):
                value = map["level"][y][x]
                match value:
                    case 1:
                        level_data["floor"].append(map_objects.Block(x * globals.BLOCK_SIZE, (y + offset_y) * globals.BLOCK_SIZE, globals.BLOCK_SIZE))
                    case 2:
                        level_data["fires"].append(map_objects.Fire(x * globals.BLOCK_SIZE + 32, (y + offset_y) * globals.BLOCK_SIZE + 32, 16, 32, self.window))
                    case 3:
                        level_data["finish"].append(map_objects.Finish(x * globals.BLOCK_SIZE, (y + offset_y) * globals.BLOCK_SIZE - 32, 64, 64, self.window))
                    case 4:
                        level_data["player"] = Character((x * globals.BLOCK_SIZE, (y + offset_y) * globals.BLOCK_SIZE), 50, 50, "NinjaFrog", self.window, True, 5)
                    case 5:
                        level_data["opponents"].append(Character((x * globals.BLOCK_SIZE, (y + offset_y) * globals.BLOCK_SIZE + 40), 50, 50, "MaskDude", self.window))
                    case _:
                        pass 
        return level_data


    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        if self.player.is_alive():
            self.player.loop(globals.FPS)
        else:
            self.player.resurrect()
            [opponent.resurrect() for opponent in self.opponents]
        [fire.loop() for fire in self.fires]
        [flag.loop() for flag in self.finish]
        for opponent in self.opponents:
            if opponent.is_alive():
                opponent.loop(globals.FPS)
                if opponent.rect.x > self.player.rect.x:
                    self.handle_move(opponent, self.objects, -globals.OPPONENT_VEL)
                else:
                    self.handle_move(opponent, self.objects, globals.OPPONENT_VEL)
        new_level = self.move_player(self.player, self.objects, self.opponents)

        
            
        if new_level:
            self.player = new_level["player"]
            self.opponents = new_level["opponents"]
            self.floor = new_level["floor"]
            self.fires = new_level["fires"]
            self.finish = new_level["finish"]

            self.objects = [*self.floor, *self.fires, *self.finish]  
            self.player.loop(globals.FPS)
            [fire.loop() for fire in self.fires]
            [flag.loop() for flag in self.finish]
        self.draw(self.background, self.bg_image, self.player, self.opponents, self.objects, self.offset_x, self.offset_y)
        
        if ((self.player.rect.right - self.offset_x >= globals.WIDTH - self.scroll_area_width) and self.player.x_vel > 0) or (
                (self.player.rect.left - self.offset_x <= self.scroll_area_width) and self.player.x_vel < 0):
            self.offset_x += self.player.x_vel
        if self.player.rect.left - self.offset_x < 0 or self.player.rect.left - self.offset_x > globals.WIDTH:
            self.offset_x = self.player.rect.left - self.scroll_area_width

        if ((self.player.rect.bottom - self.offset_y >= globals.HEIGHT - self.scroll_area_height) and self.player.y_vel > 0) or (
                (self.player.rect.top - self.offset_y <= self.scroll_area_height) and self.player.y_vel < 0):
            self.offset_y += self.player.y_vel
        if self.player.rect.top - self.offset_y < 0 or self.player.rect.top - self.offset_y > globals.HEIGHT:
            self.offset_y = self.player.rect.top - self.scroll_area_height    

        self.offset_y = min(self.offset_y, 160)    

    # pygame.quit()
    # quit()
