from collections import defaultdict
import pygame
from os.path import join
import common.globals as globals
from components.characters import Character
import components.map_objects as map_objects
import json


pygame.init()
pygame.display.set_caption("Platformer")

pygame.mixer.init()
welcome_sound = pygame.mixer.Sound('assets/Sound/welcome.mp3')
welcome_sound.set_volume(0.1)
music = pygame.mixer.Sound('assets/Sound/Music/Adventurous/Powerful.mp3')
music.set_volume(0.1)
welcome_sound.play()
music.play(loops=-1)

window = pygame.display.set_mode((globals.WIDTH, globals.HEIGHT))
level_number = 0
lava_img = pygame.image.load(join("assets", "Background", "lava.png"))


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(globals.WIDTH // width + 1):
        for j in range(globals.HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, opponents, objects, offset_x, offset_y):
    for tile in background:
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window, offset_x, offset_y)
    
    for opponent in opponents:
        opponent.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)


    darken_surface = pygame.Surface((globals.WIDTH, globals.HEIGHT), pygame.SRCALPHA)
    for i in range(0, globals.HEIGHT, 10):
        darken = min((255 - ((i + offset_y)//4)), 240)
        darken = max(darken, 0)
        pygame.draw.rect(darken_surface, (0, 0, 0, darken), pygame.Rect(0, i, globals.WIDTH, 10))
    
    for obj in objects:
        obj.draw_light(darken_surface, offset_x, offset_y)    
    window.blit(darken_surface, (0, 0))




    for i in range (-5, 10):
        window.blit(lava_img, (i*(767) - offset_x, globals.HEIGHT - offset_y))
    

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0 and (abs(player.rect.bottom - obj.rect.top) < (player.rect.height/4)):
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(character, objects, dx):
    character.move(dx, 0)
    character.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(character, obj):
            collided_object = obj
            break

    character.move(-dx, 0)
    character.update()
    return collided_object

def move_player(player, objects, opponents):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        handle_move(player, objects, "left", globals.PLAYER_VEL)
    elif keys[pygame.K_RIGHT]:
        handle_move(player, objects, "right", globals.PLAYER_VEL)
    else:
        handle_move(player, objects, "", globals.PLAYER_VEL)


    if pygame.sprite.spritecollideany(player, opponents):
        player.make_hit()

def handle_move(character, objects, direction, velocity):
    character.x_vel = 0
    collide_left = collide(character, objects, -velocity * 2)
    collide_right = collide(character, objects, velocity * 2)

    if direction == "left" and not collide_left:
        character.move_left(velocity)
    if direction == "right" and not collide_right:
        character.move_right(velocity)

    vertical_collide = handle_vertical_collision(character, objects, character.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            character.make_hit()
        elif character.is_player and obj and obj.name == "finish":
            global level_number
            level_number += 1
            return(load_level())
        

def load_level(level_index = None):

    global level_number
    if not level_index:
        level_index = level_number
    block_size = 96
    map = None
    with open('assets/maps.json') as f:
        map = json.load(f)["maps"][level_index]

    level_data = defaultdict(list)
    offset_y = 8 - len(map["level"])
    for y in range(len(map["level"])):
        for x in range(len(map["level"][level_index])):
            value = map["level"][y][x]
            match value:
                case 1:
                    level_data["floor"].append(map_objects.Block(x * block_size, (y + offset_y) * block_size, block_size))
                case 2:
                    level_data["fires"].append(map_objects.Fire(x * block_size + 32, (y + offset_y) * block_size + 32, 16, 32, window))
                case 3:
                    level_data["finish"].append(map_objects.Finish(x * block_size, (y + offset_y) * block_size - 32, 64, 64, window))
                case 4:
                    level_data["player"] = Character((x * block_size, (y + offset_y) * block_size), 50, 50, "NinjaFrog", window, True, 100)
                case 5:
                    level_data["opponents"].append(Character((x * block_size, (y + offset_y) * block_size), 50, 50, "MaskDude", window))
                case _:
                    pass 
    return level_data


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Bricks.png")
    level_data = load_level()
    player = level_data["player"]
    opponents = level_data["opponents"]
    floor = level_data["floor"]
    fires = level_data["fires"]
    finish = level_data["finish"]
    
    objects = [*floor, *fires, *finish]

    scroll_area_width = globals.WIDTH//3
    scroll_area_height = globals.HEIGHT//3
    offset_x = player.rect.left - scroll_area_width
    offset_y = player.rect.top - scroll_area_height
    run = True
    while run:
        clock.tick(globals.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()

        
        if player.is_alive():
            player.loop(globals.FPS)
        else:
            player.resurrect()
        [fire.loop() for fire in fires]
        [flag.loop() for flag in finish]
        new_level = move_player(player, objects, opponents)
        for opponent in opponents:
            if opponent.is_alive():
                opponent.loop(globals.FPS)
                if opponent.rect.x > player.rect.x:
                    handle_move(opponent, objects, "left", globals.OPPONENT_VEL)
                else:
                    handle_move(opponent, objects, "right", globals.OPPONENT_VEL)
        
            
        if new_level:
            player = new_level["player"]
            opponents = level_data["opponents"]
            floor = new_level["floor"]
            fires = new_level["fires"]
            finish = new_level["finish"]

            objects = [*floor, *fires, *finish]  
            player.loop(globals.FPS)
            [fire.loop() for fire in fires]
            [flag.loop() for flag in finish]
        draw(window, background, bg_image, player, opponents, objects, offset_x, offset_y)
        
        if ((player.rect.right - offset_x >= globals.WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
        if player.rect.left - offset_x < 0 or player.rect.left - offset_x > globals.WIDTH:
            offset_x = player.rect.left - scroll_area_width

        if ((player.rect.bottom - offset_y >= globals.HEIGHT - scroll_area_height) and player.y_vel > 0) or (
                (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel
        if player.rect.top - offset_y < 0 or player.rect.top - offset_y > globals.HEIGHT:
            offset_y = player.rect.top - scroll_area_height    

        offset_y = min(offset_y, 160)    

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
