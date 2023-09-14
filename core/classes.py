# Библиотеки
import pygame
import random
# Модули
from utils.constants import *
from core.base import *
from core.groups_manager import *
from core.sounds import *

# Управление игрой
class GameControl():
	def __init__(self):
		self.run = True
		self.state = 'menu'
		self.stopped = True
		self.pause = False
		self.main_menu = True
		self.game_over = False
		# Инициализация часов
		self.clock = pygame.time.Clock()
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

	def set_state(self, state):
		self.state = state

	def defeat(self):
		self.paused = True
		self.game_over = True

	def switch_pause(self):
		self.pause = not self.pause

class Menu():
	def __init__(self):
		x = WIDTH // 2
		y = HEIGHT // 5
		btns_text = ['play', 'records', 'settings', 'exit']
		self.current_btn = 0
		self.menu_btns = []
		for i in range(len(btns_text)):
			self.menu_btns.append(Label(x, y * (i + 1), btns_text[i], 75))

	def draw(self, parent):
		for i, b in enumerate(self.menu_btns):
			if i == self.current_btn:
				b.change_color(YELLOW)
			b.draw(parent)

	def update(self, events):
		for e in events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_UP and self.current_btn > 0:
					self.menu_btns[self.current_btn].change_color(WHITE)
					self.current_btn -= 1
				elif e.key == pygame.K_DOWN and self.current_btn < len(self.menu_btns) - 1:
					self.menu_btns[self.current_btn].change_color(WHITE)
					self.current_btn += 1

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

	def draw(self, parent):
		parent.blit(self.image, self.rect.topleft)

	def get_damage(self, damage):
		self.hp -= damage
		if self.hp < 0:
			self.hp = 0

	def is_dead(self):
		return self.hp <= 0


class Player(Sprite):
	def __init__(self, x, y, w, h, image_normal, image_super, speed, hp, shoot_cd):
		super().__init__(x, y, w, h, image_normal, speed, hp)
		self.image_normal = self.image
		self.image_super = pygame.image.load(image_super)
		self.image_super = pygame.transform.scale(self.image_super, self.size)
		self.base_shoot_cd = shoot_cd
		self.shoot_cd = shoot_cd
		self.super_mode = False

	def switch_super(self):
		if self.super_mode:
			self.super_mode = False
			self.image = self.image_normal
		else:
			self.super_mode = True
			self.image = self.image_super


	def shoot(self):
		if self.shoot_cd <= 0:
			self.shoot_cd = self.base_shoot_cd
			player_lasers.add(Laser(*self.rect.topleft, 0, -10, 0, 5))
			player_lasers.add(Laser(*self.rect.topright, 0, -10, 0, 5))
			if self.super_mode:
				player_lasers.add(Laser(*self.rect.topleft, -7, -7, 45, 5))
				player_lasers.add(Laser(*self.rect.topright, 7, -7, -45, 5))
			laser_sound.play()

	def update(self, keys):
		if self.shoot_cd > 0:
			self.shoot_cd -= 1
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
			self.switch_super()

		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH


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
		if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > WIDTH:
			self.kill()


class Label():
	def __init__(self, x, y, text, size, color = WHITE):
		self.text = text
		self.font = pygame.font.Font(f'{FNT}/starjedi/Starjedi.ttf', size)
		self.rendered_text = self.font.render(self.text, True, color)
		self.rect = self.rendered_text.get_rect(center = (x, y))

	def draw(self, parent):
		parent.blit(self.rendered_text, self.rect.topleft)

	def change_color(self, color):
		self.rendered_text = self.font.render(self.text, True, color)