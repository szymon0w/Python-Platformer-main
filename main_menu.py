import pygame
import sys
import common.globals as globals
import game
import level_creator
import components.button as button
import common.sounds as sounds
# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((globals.WIDTH, globals.HEIGHT))
pygame.display.set_caption("Game Main Menu")
clock = pygame.time.Clock()
current_state = "main_menu"
game_session = None
level_creator_session = level_creator.LevelCreator(screen)
sound = sounds.Sound()

# Font
font = pygame.font.SysFont(None, 50)

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
    return False
# Function to display levels panel
def display_levels():
    global current_state
    current_state = "levels"
    clicked = events()

    # Draw buttons for levels
    level_buttons = []
    margin_top = 100
    margin_sides = 20
    levels_per_row = 10
    number_of_rows = 7
    button_padding = (globals.WIDTH - (2 * margin_sides) - (levels_per_row * globals.LEVELS_BUTTON_SIZE)) // (levels_per_row - 1)
    

    for row in range(number_of_rows):
        for col in range(levels_per_row):
            level_num = row * levels_per_row + col + 1
            x = margin_sides + col * (globals.LEVELS_BUTTON_SIZE + button_padding)
            y = margin_top + row * (globals.LEVELS_BUTTON_SIZE + button_padding)
            level_button_text = f"{level_num}"
            level_button = (level_button_text, x, y, globals.LEVELS_BUTTON_SIZE, globals.LEVELS_BUTTON_SIZE, globals.GRAY, globals.BLACK, run_level, clicked, level_num)
            level_buttons.append(level_button)

    for button_parameters in level_buttons:
        button.draw_button(screen, *button_parameters)

    display_common_buttons(clicked)


def display_main_menu():
    clicked = events()
    buttons_start_x = (globals.WIDTH - globals.MAIN_MENU_BUTTON_WIDTH) // 2
    button_start_y = ((globals.HEIGHT) // 5)
    button.draw_button(screen, "Levels", buttons_start_x, button_start_y * 2 - (globals.MAIN_MENU_BUTTON_HEIGHT // 2), globals.MAIN_MENU_BUTTON_WIDTH, globals.MAIN_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, display_levels, clicked)
    button.draw_button(screen, "Settings", buttons_start_x, button_start_y * 3 - (globals.MAIN_MENU_BUTTON_HEIGHT // 2), globals.MAIN_MENU_BUTTON_WIDTH, globals.MAIN_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, display_settings, clicked)
    button.draw_button(screen, "Level Creator", buttons_start_x, button_start_y * 4 - (globals.MAIN_MENU_BUTTON_HEIGHT // 2), globals.MAIN_MENU_BUTTON_WIDTH, globals.MAIN_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, display_level_creator, clicked)    

# Function to display settings panel
def display_settings():
    global current_state
    current_state = "settings"
    global sound
    sound.pause()
    clicked = events()
    print("Display Settings Panel")  # Placeholder action, replace with your actual implementation

    display_common_buttons(clicked)


# Function to display level creator
def display_level_creator():
    global current_state
    current_state = "level_creator"
    level_creator_session.loop()
    display_common_buttons(display_main_menu_btn = True, display_play_btn = False)


def display_common_buttons(clicked = None, display_main_menu_btn = True, display_settings_btn = False, display_play_btn = True):
    global game_session

    if not clicked:
        clicked = events()

    # Button to return to main menu
    # button.draw_button(screen, "Main Menu", globals.LEVELS_MENU_BUTTON_WIDTH * 0.2, 0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_WIDTH, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, return_to_main_menu, clicked)
    if display_main_menu_btn:
        button.draw_icon_button(screen, globals.LEVELS_MENU_BUTTON_HEIGHT, 0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, "home.png", return_to_main_menu, clicked)
    
    if game_session and display_play_btn:
        button.draw_icon_button(screen, (globals.WIDTH/2) - (0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT), 0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, "play.png", continue_playing, clicked)
    
    # Button to go to settings
    # button.draw_button(screen, "Settings", globals.WIDTH - (globals.LEVELS_MENU_BUTTON_WIDTH * 1.2), 0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_WIDTH, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, display_settings, clicked)
    if display_settings_btn:
        if display_main_menu_btn:
            x_location = globals.WIDTH - (globals.LEVELS_MENU_BUTTON_HEIGHT * 2)
        else:
            x_location = globals.LEVELS_MENU_BUTTON_HEIGHT
        button.draw_icon_button(screen, x_location, 0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, "settings.png", display_settings, clicked)
    


def return_to_main_menu():
    global current_state
    current_state = "main_menu"

def run_level(level_number):
    global game_session
    game_session = game.Game(level_number - 1, screen)
    global sound
    sound.start()
    global current_state
    current_state = "playing_game"

def continue_playing():
    global current_state
    current_state = "playing_game"
    global sound
    sound.unpause()

# Main loop
def main_loop():
    while True:
        clock.tick(globals.FPS)
        screen.fill(globals.WHITE)
        # display_levels()
        # Draw buttons
        match current_state:
            case "main_menu":
                display_main_menu()
            case "levels":
                display_levels()
            case "settings":
                display_settings()
            case "level_creator":
                display_level_creator()
            case "playing_game":
                game_session.play()
                display_common_buttons(display_main_menu_btn = True, display_settings_btn = True, display_play_btn = True)

        pygame.display.update()

# Run the main loop
main_loop()
