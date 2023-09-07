# Библиотеки
import pygame
# Модули
from utils.constants import *
from core.classes import *

# Инициализация игрока
player = Player(
	x = WIDTH // 2,
	y = HEIGHT - 100,
	w = 50,
	h = 50,
	image_normal = f'{IMG}/battleship.png',
	image_super = f'{IMG}/battleship_neon.png',
	speed = 5,
	hp = 100,
	shoot_cd = FPS // 4)

# Надписи
lose_text = Label('gAme oveR', 100, WIDTH // 2, HEIGHT // 2)