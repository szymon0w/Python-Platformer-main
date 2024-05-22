import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.welcome_sound = pygame.mixer.Sound('assets/Sound/welcome.mp3')
        self.welcome_sound.set_volume(0.1)
        self.music = pygame.mixer.Sound('assets/Sound/Music/Adventurous/Powerful.mp3')
        self.music.set_volume(0.1)

    def start(self):
        self.welcome_sound.play()
        self.music.play(loops=-1)

    def pause(self):
        self.welcome_sound.set_volume(0)
        pygame.mixer.pause()
        

    def unpause(self):
        pygame.mixer.unpause()


    