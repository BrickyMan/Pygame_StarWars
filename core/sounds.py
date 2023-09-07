import pygame
from utils.constants import *

# Фоновая музыка
pygame.mixer.music.load(f'{AUD}/music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

# Звуки
laser_sound = pygame.mixer.Sound(f'{AUD}/laser.mp3')
laser_sound.set_volume(0.2)