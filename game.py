# Библиотеки
import pygame
import random
# Собственные модули
from core.window import *
from core.sprites_manager import *
from core.classes import *
from core.sounds import *
from utils.constants import * 

# Режим разработчика
developer_mode = True

# Инициализация часов
clock = pygame.time.Clock()

# ==== УПРАВЛЯЮЩИЕ ПЕРЕМЕННЫЕ ====
game = GameControl()

# Игровой цикл
while game.run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN and not game.game_over:
				paused = not paused
			elif event.key == pygame.K_RETURN and game.paused and game.game_over:
				game.game_over = False
				game.paused = False

	if not game.paused:
		# Отрисовка
		window.fill(BLACK)

		# Обновление
		player.update()
		player_lasers.update()
		game.spawn_enemy()
		enemies.update()
		if pygame.sprite.spritecollideany(player, enemies):
			game.defeat()

		shot_enemies = pygame.sprite.groupcollide(enemies, player_lasers, False, True)
		for e in shot_enemies:
			e.get_damage(shot_enemies[e][0].damage)
			if e.is_dead():
				e.kill()

		# Отрисовка
		player.draw()
		player_lasers.draw(window)
		enemies.draw(window)

	# Экран проигрыша
	if game.paused and game.game_over:
		window.fill(BLACK)
		lose_text.draw()

	# Последние изменения
	pygame.display.flip()
	clock.tick(FPS)

# Завершение Pygame
pygame.quit()
