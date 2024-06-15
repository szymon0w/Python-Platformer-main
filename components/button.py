import pygame
from common import globals


pygame.init()
font = pygame.font.SysFont(None, 50)

def draw_button(screen, text, x, y, width, height, inactive_color, active_color, action=None, clicked = False, parameter = None):
    mouse = pygame.mouse.get_pos()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if clicked and action is not None:
            if parameter:
                action(parameter)
            else:
                action()

    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    text_surface = font.render(text, True, globals.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = ((x + width / 2), (y + height / 2))
    screen.blit(text_surface, text_rect)

def draw_icon_button(screen, x, y, width, height, img, action=None, clicked = False, parameter = None):
    img = pygame.transform.scale(img, (width, height))
    mouse = pygame.mouse.get_pos()
    screen.blit(img, (x, y))
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        if clicked and action is not None:
            if parameter is None:
                action()
            else:
                action(parameter)