import pygame
from os.path import join
import common.globals as globals
from components.player import Player
import components.map_objects as map_objects
import json


pygame.init()
pygame.display.set_caption("Platformer")

window = pygame.display.set_mode((globals.WIDTH, globals.HEIGHT))


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(globals.WIDTH // width + 1):
        for j in range(globals.HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
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


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96
    map = None
    with open('assets/maps.json') as f:
        map = json.load(f)["maps"][1]
    player = Player(map["player_position"], 50, 50, window)
    floor = [map_objects.Block(x * block_size, y * block_size, block_size) for y in range(len(map["level"])) for x in range(len(map["level"][0])) if map["level"][y][x] == 1]
    fires = [map_objects.Fire(x * block_size + 32, y * block_size+32, 16, 32, window) for y in range(len(map["level"])) for x in range(len(map["level"][0])) if map["level"][y][x] == 2]
    
    objects = [*floor, *fires]

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(globals.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(globals.FPS)
        [fire.loop() for fire in fires]
            
        
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= globals.WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
