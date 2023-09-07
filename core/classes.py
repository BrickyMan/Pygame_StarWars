# Библиотеки
import pygame
import random
# Модули
from utils.constants import *
from core.window import *
from core.groups_manager import *
from core.sounds import *

# Управление игрой
class GameControl():
	def __init__(self):
		self.run = True
		self.paused = False
		self.game_over = False
		# Управление спавном врагов
		self.base_enemy_spawn_cd = FPS
		self.enemy_spawn_cd = FPS

	def spawn_enemy(self):
		if self.enemy_spawn_cd <= 0:
			self.enemy_spawn_cd = self.base_enemy_spawn_cd
			enemies.add(Enemy(
				x = random.randint(50, WIDTH - 50),
				y = -100,
				w = 35,
				h = 35,
				image = f'{IMG}/aircraft.png',
				speed = 2,
				hp = 10)
			)
		else:
			self.enemy_spawn_cd -= 1

	def defeat():
		paused = True
		game_over = True


class Sprite(pygame.sprite.Sprite):
	def __init__(self, x, y, w, h, image, speed, hp):
		super().__init__()
		# Переменнные свойства
		self.hp = hp
		self.speed = speed
		# Базовые свойства
		self.base_pos = (x, y)
		self.size = (w, h)
		# Изображение
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image, self.size)
		# Хитбокс
		self.rect = self.image.get_rect(center = self.base_pos)

	def draw(self):
		window.blit(self.image, self.rect.topleft)

	def get_damage(self, damage):
		self.hp -= damage
		if self.hp < 0:
			self.hp = 0

	def is_dead(self):
		return self.hp <= 0


class Player(Sprite):
	def __init__(self, x, y, w, h, image_normal, image_super, speed, hp, shoot_cd):
		super().__init__(x, y, w, h, image_normal, speed, hp)
		self.image_super = pygame.image.load(image_super)
		self.image_super = pygame.transform.scale(self.image_super, self.size)
		self.base_shoot_cd = shoot_cd
		self.shoot_cd = shoot_cd
		self.super_mode = False

	def shoot(self):
		if self.shoot_cd <= 0:
			self.shoot_cd = self.base_shoot_cd
			player_lasers.add(Laser(*self.rect.topleft, 0, -10, 0, 5))
			player_lasers.add(Laser(*self.rect.topright, 0, -10, 0, 5))
			if self.super_mode:
				player_lasers.add(Laser(*self.rect.topleft, -7, -7, 45, 5))
				player_lasers.add(Laser(*self.rect.topright, 7, -7, -45, 5))
			laser_sound.play()

	def update(self):
		if self.shoot_cd > 0:
			self.shoot_cd -= 1
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.rect.y -= self.speed
		if keys[pygame.K_s]:
			self.rect.y += self.speed
		if keys[pygame.K_a]:
			self.rect.x -= self.speed
		if keys[pygame.K_d]:
			self.rect.x += self.speed
		if keys[pygame.K_SPACE]:
			self.shoot()
		# Режим разработчика
		if keys[pygame.K_k] and developer_mode:
			self.super_mode = not self.super_mode
		if keys[pygame.K_l] and developer_mode:
			defeat()

		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH

	def draw(self):
		if self.super_mode:
			window.blit(self.image_super, self.rect.topleft)
		else:
			window.blit(self.image, self.rect.topleft)


class Enemy(Sprite):
	def __init__(self, x, y, w, h, image, speed, hp):
		super().__init__(x, y, w, h, image, speed, hp)


	def update(self):
		self.rect.y += self.speed
		if self.rect.top > HEIGHT:
			self.rect.bottom = 0
			self.rect.centerx = random.randint(100, WIDTH - 100)


class Laser(pygame.sprite.Sprite):
	def __init__(self, x, y, dx, dy, angle, damage):
		super().__init__()
		self.image = pygame.Surface((2, 20), pygame.SRCALPHA)
		self.image.fill(RED)
		self.image = pygame.transform.rotate(self.image, angle)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.dx = dx
		self.dy = dy
		self.damage = damage

	def update(self):
		self.rect.centerx += self.dx
		self.rect.centery += self.dy
		if self.rect.bottom < 0:
			self.kill()


class Label():
	def __init__(self, text, size, x, y):
		self.font = pygame.font.Font(f'{FNT}/starjedi/Starjedi.ttf', size)
		self.text = self.font.render(text, True, WHITE)
		self.rect = self.text.get_rect()
		self.rect.center = (x, y)

	def draw(self):
		window.blit(self.text, self.rect.topleft)