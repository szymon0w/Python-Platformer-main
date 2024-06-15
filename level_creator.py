import pygame
import json
from common import globals
from common.image_handler import ImageHandler
import components.button as button
# Initialize Pygame
# pygame.init()

class LevelCreator():
    def __init__(self, window):
        self.level_number = None
        self.window = window
        self.image_handler = ImageHandler()
        self.ROWS, self.COLS = int(globals.HEIGHT * 0.8) // globals.GRID_SIZE, int(globals.WIDTH * 0.8) // globals.GRID_SIZE
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.OBJECTS = ['empty', 'floor', 'fire', 'finish', 'start', 'opponent']
        self.OBJECT_IMAGES = {
            'empty': self.image_handler.background,
            'floor': self.image_handler.floor,
            'fire': self.image_handler.fire,
            'finish': self.image_handler.finish,
            'start': self.image_handler.start,
            'opponent': self.image_handler.opponent
        }
        # Create a grid filled with 'empty'
        self.grid = [['empty' for _ in range(self.COLS)] for _ in range(self.ROWS)]

        self.unique_locations = {"start": None, "finish": None}
        # Current selected object
        self.current_object = 'empty'
        self.mouse_clicked = False

    def load_level(self, level_number):
        self.current_object = 'empty'
        self.level_number = level_number
        if level_number is None:
            self.grid = [['empty' for _ in range(self.COLS)] for _ in range(self.ROWS)]
        else:
            with open("assets/maps.json", "r") as jsonFile:
                data = json.load(jsonFile)
            self.grid = data["maps"][self.level_number]["level"]
            self.ROWS = len(self.grid)
            self.COLS = len(self.grid[0])


    def draw_selection(self):
        x_location = globals.WIDTH * 0.25
        y_location = globals.HEIGHT * 0.1
        for key, value in self.OBJECT_IMAGES.items():
            size = int(globals.GRID_SIZE * 1.5)
            if key == self.current_object:
                size *= 2
            button.draw_icon_button(self.window, int(x_location - (0.5 * size)), (y_location - (0.5 * size)), size, size, value, self.set_current_object, pygame.mouse.get_pressed()[0], key)
            x_location += int((globals.WIDTH * 0.5) / (len(self.OBJECT_IMAGES)))
        size = int(globals.GRID_SIZE * 1.5)
        button.draw_button(self.window, "Save",  int(x_location - (0.5 * size)), (y_location - (0.5 * globals.MAIN_MENU_BUTTON_HEIGHT)), globals.MAIN_MENU_BUTTON_WIDTH // 2, globals.MAIN_MENU_BUTTON_HEIGHT, globals.GRAY, globals.BLACK, self.save_grid_to_json, pygame.mouse.get_pressed()[0])
        

    def set_current_object(self, value_to_set):
        self.current_object = value_to_set
    def draw_grid(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                rect = pygame.Rect(int(globals.WIDTH * 0.1) + col * globals.GRID_SIZE, int(globals.HEIGHT * 0.2) + row * globals.GRID_SIZE, globals.GRID_SIZE, globals.GRID_SIZE)
                self.window.blit(self.OBJECT_IMAGES[self.grid[row][col]], rect)
                pygame.draw.rect(self.window, self.BLACK, rect, 1)

    def validate_grid(self):
        return (any('start' in sublist for sublist in self.grid) and any('finish' in sublist for sublist in self.grid))


    def save_grid_to_json(self):
        if self.validate_grid():
            print('saving grid')
            with open("assets/maps.json", "r") as jsonFile:
                data = json.load(jsonFile)
            if self.level_number is None:
                data["maps"].append({"level": self.grid})
            else: 
                data["maps"][self.level_number] = ({"level": self.grid})
                self.level_number = None
            with open('assets/maps.json', 'w') as f:
                json.dump(data, f, indent=4)
            self.ROWS, self.COLS = int(globals.HEIGHT * 0.8) // globals.GRID_SIZE, int(globals.WIDTH * 0.8) // globals.GRID_SIZE
            self.grid = [['empty' for _ in range(self.COLS)] for _ in range(self.ROWS)]
            


    def loop(self):
        self.draw_grid()
        self.draw_selection()
        
        keys = pygame.key.get_pressed()    
        
        if keys[pygame.K_1]:
            self.current_object = 'empty'
        elif keys[pygame.K_2]:
            self.current_object = 'floor'
        elif keys[pygame.K_3]:
            self.current_object = 'fire'
        elif keys[pygame.K_4]:
            self.current_object = 'finish'
        elif keys[pygame.K_5]:
            self.current_object = 'start'
        elif keys[pygame.K_6]:
            self.current_object = 'opponent'
            
            
    
        self.mouse_clicked = pygame.mouse.get_pressed()[0]

        if self.mouse_clicked:     
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = (mouse_x - int(globals.WIDTH * 0.1)) // globals.GRID_SIZE
            row = (mouse_y - int(globals.HEIGHT * 0.2)) // globals.GRID_SIZE
            if 0 <= col < len(self.grid[0]) and 0 <= row < len(self.grid):
                if self.current_object in self.unique_locations.keys():
                    if self.unique_locations[self.current_object]:
                        current_location = self.unique_locations[self.current_object]
                        self.grid[current_location[0]][current_location[1]] = 'empty'
                    self.unique_locations[self.current_object] = (row, col)
                self.grid[row][col] = self.current_object