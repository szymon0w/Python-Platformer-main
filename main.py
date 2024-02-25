from collections import defaultdict
import pygame
from os.path import join
import common.globals as globals
from components.player import Player
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


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(-1 ,(globals.WIDTH // width) + 1):
        for j in range(-1, (globals.HEIGHT // height) + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

#effects = [{"offset_x":x, "offset_y":y, "image": image}, [second one]]
def draw(window, background, bg_image, player, objects, offset_x, offset_y, effects = []):
    window.fill((255, 255, 255))
    # for tile in background:
    #     window.blit(bg_image, tile)
    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)

    darken_surface = pygame.Surface((globals.WIDTH, globals.HEIGHT), pygame.SRCALPHA)
    darken_surface.fill((0, 0, 0, 150))
    window.blit(darken_surface, (0, 0))
    for effect in effects:
        for tile in effect["tiles"]:
            window.blit(effect["image"], ((tile[0]+effect["offset_x"])%(globals.WIDTH + (globals.BLOCK_SIZE*2)) - globals.BLOCK_SIZE, (tile[1]+effect["offset_y"])%(globals.HEIGHT + (2 * globals.BLOCK_SIZE)) - globals.BLOCK_SIZE))
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


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -globals.PLAYER_VEL * 2)
    collide_right = collide(player, objects, globals.PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(globals.PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(globals.PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
        elif obj and obj.name == "finish":
            global level_number
            level_number = level_number + 1
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
    level_data["player"] = Player(map["player_position"], 50, 50, window)
    for y in range(len(map["level"])):
        for x in range(len(map["level"][0])):
            value = map["level"][y][x]
            match value:
                case 1:
                    level_data["floor"].append(map_objects.Block(x * block_size, y * block_size, block_size))
                case 2:
                    level_data["fires"].append(map_objects.Fire(x * block_size + 32, y * block_size + 32, 16, 32, window))
                case 3:
                    level_data["finish"].append(map_objects.Finish(x * block_size, y * block_size - 32, 64, 64, window))
                case _:
                    pass 
    return level_data


def main(window):

    clock = pygame.time.Clock()
    background, bg_image = get_background("Brown.png")
    tiles, image = get_background("Effects/rain.png")
    rain = {"offset_x": 0, "offset_y": 0, "tiles": tiles, "image": image}
    print(image)
    level_data = load_level()
    player = level_data["player"]
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
        rain["offset_x"] = (rain["offset_x"] + 5)
        rain["offset_y"] = (rain["offset_y"] + 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()



        player.loop(globals.FPS)
        [fire.loop() for fire in fires]
        [flag.loop() for flag in finish]
        new_level = handle_move(player, objects)
        if new_level:
            player = new_level["player"]
            floor = new_level["floor"]
            fires = new_level["fires"]
            finish = new_level["finish"]
            objects = [*floor, *fires, *finish]  
            player.loop(globals.FPS)
            [fire.loop() for fire in fires]
            [flag.loop() for flag in finish]
        draw(window, background, bg_image, player, objects, offset_x, offset_y, [rain])
        
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

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
