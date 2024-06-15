import pygame
import sys
import common.globals as globals
import game
import level_creator
import components.button as button
import common.sounds as sounds
from os.path import join

class MainMenu():

    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Set up the screen
        self.screen = pygame.display.set_mode((globals.WIDTH, globals.HEIGHT))
        pygame.display.set_caption("Game Main Menu")
        self.clock = pygame.time.Clock()
        self.current_state = "main_menu"
        self.game_session = None
        self.level_creator_session = level_creator.LevelCreator(self.screen)
        self.sound = sounds.Sound()

        # Font
        self.font = pygame.font.SysFont(None, globals.FONT_SIZE)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False
    # Function to display levels panel
    def display_levels(self):
        clicked = self.events()

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
                if self.current_state == "levels":
                    level_button = (level_button_text, x, y, globals.LEVELS_BUTTON_SIZE, globals.LEVELS_BUTTON_SIZE, globals.GRAY, globals.BLACK, self.run_level, clicked, level_num)
                elif self.current_state == "level_creator_settings":
                    level_button = (level_button_text, x, y, globals.LEVELS_BUTTON_SIZE, globals.LEVELS_BUTTON_SIZE, globals.GRAY, globals.BLACK, self.edit_level, clicked, level_num)
                level_buttons.append(level_button)
        if self.current_state == "level_creator_settings":
            text_surface = self.font.render('Choose level number to edit or:', False, (0, 0, 0))
            self.screen.blit(text_surface, (int(globals.WIDTH * 0.15), (margin_top - globals.FONT_SIZE)//2))
            button.draw_button(self.screen, 'Create new level', int(globals.WIDTH * 0.67), (margin_top - globals.LEVELS_MENU_BUTTON_HEIGHT)//2, globals.LEVELS_MENU_BUTTON_HEIGHT * 6, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, self.edit_level, clicked)
        for button_parameters in level_buttons:
            button.draw_button(self.screen, *button_parameters)
        

        self.display_common_buttons(clicked, display_play_btn = True)


    def display_main_menu(self):
        clicked = self.events()
        buttons_start_x = (globals.WIDTH - globals.MAIN_MENU_BUTTON_WIDTH) // 2
        button_start_y = ((globals.HEIGHT) // 5)
        button.draw_button(self.screen, "Levels", buttons_start_x, button_start_y * 2 - (globals.MAIN_MENU_BUTTON_HEIGHT // 2), globals.MAIN_MENU_BUTTON_WIDTH, globals.MAIN_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, self.start_display_levels, clicked)
        button.draw_button(self.screen, "Settings", buttons_start_x, button_start_y * 3 - (globals.MAIN_MENU_BUTTON_HEIGHT // 2), globals.MAIN_MENU_BUTTON_WIDTH, globals.MAIN_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, self.start_display_settings, clicked)
        button.draw_button(self.screen, "Level Creator", buttons_start_x, button_start_y * 4 - (globals.MAIN_MENU_BUTTON_HEIGHT // 2), globals.MAIN_MENU_BUTTON_WIDTH, globals.MAIN_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, self.start_display_level_creator, clicked)    

    def start_display_level_creator(self):
        self.current_state = "level_creator_settings"

    def start_display_settings(self):
        self.current_state = "settings"

    def start_display_levels(self):
        self.current_state = "levels"

    # Function to display settings panel
    def display_settings(self):
        self.sound.pause()
        clicked = self.events()
        print("Display Settings Panel")  # Placeholder action, replace with your actual implementation

        self.display_common_buttons(clicked, display_play_btn = True)


    # Function to display level creator
    def display_level_creator(self):
        self.level_creator_session.loop()
        self.display_common_buttons(display_main_menu_btn = True, display_play_btn = False)


    def display_common_buttons(self, clicked = None, display_main_menu_btn = True, display_settings_btn = False, display_play_btn = False):
        if not clicked:
            clicked = self.events()

        # Button to return to main menu
        if display_main_menu_btn:
            img = pygame.image.load(join("assets", "Icons", "home.png"))
            button.draw_icon_button(self.screen, globals.LEVELS_MENU_BUTTON_HEIGHT, 0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, img, self.return_to_main_menu, clicked)
        
        if self.game_session and display_play_btn:
            img = pygame.image.load(join("assets", "Icons", "play.png"))
            button.draw_icon_button(self.screen, (globals.WIDTH/2) - (0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT), 0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, img, self.continue_playing, clicked)
        
        # Button to go to settings
        # button.draw_button(screen, "Settings", globals.WIDTH - (globals.LEVELS_MENU_BUTTON_WIDTH * 1.2), 0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_WIDTH, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, display_settings, clicked)
        if display_settings_btn:
            if display_main_menu_btn:
                x_location = globals.WIDTH - (globals.LEVELS_MENU_BUTTON_HEIGHT * 2)
            else:
                x_location = globals.LEVELS_MENU_BUTTON_HEIGHT
            img = pygame.image.load(join("assets", "Icons", "settings.png"))
            button.draw_icon_button(self.screen, x_location, 0.5 * globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, globals.LEVELS_MENU_BUTTON_HEIGHT, img, self.start_display_settings, clicked)
        


    def return_to_main_menu(self):
        self.current_state = "main_menu"

    def run_level(self, level_number):
        self.current_state = "playing_game"
        self.game_session = game.Game(level_number - 1, self.screen)
        self.sound.start()
    
    def edit_level(self, level_number = None):
        print(level_number)
        self.current_state = "level_creator"
        if level_number is not None:
            level_number -= 1
        self.level_creator_session.load_level(level_number)


        

    def continue_playing(self):
        self.current_state = "playing_game"
        self.sound.unpause()

    # Main loop
    def main_loop(self):
        while True:
            self.clock.tick(globals.FPS)
            self.screen.fill(globals.WHITE)
            
            # Draw buttons
            match self.current_state:
                case "main_menu":
                    self.display_main_menu()
                case "levels":
                    self.display_levels()
                case "settings":
                    self.display_settings()
                case "level_creator_settings":
                    self.display_levels()
                case "level_creator":
                    self.display_level_creator()
                case "playing_game":
                    self.game_session.play()
                    self.display_common_buttons(display_main_menu_btn = False, display_settings_btn = True, display_play_btn = False)

            pygame.display.update()


main_menu = MainMenu()
main_menu.main_loop()