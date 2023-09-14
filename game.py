# Библиотеки
import pygame
import random
import sys
# Собственные модули
from core.base import *
from core.sprites_manager import *
from core.classes import *
from core.sounds import *
from utils.constants import * 

game = GameControl()

# Игровой цикл
while game.run:
	keys = pygame.key.get_pressed()
	events = pygame.event.get()
	for event in events:
		# Закрытие окна
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			# if event.key == pygame.K_RETURN and :
			# 	game.paused = not game.spaused
			# elif event.key == pygame.K_RETURN and game.paused and game.game_over:
			# 	game.game_over = False
			# 	game.paused = False
			if event.key == pygame.K_l:
				game.set_state('game_over')

	if game.state == 'runs':
		# Отрисовка
		window.fill(BLACK)

		# Обновление
		player.update(keys)
		player_lasers.update()
		game.spawn_enemy()
		enemies.update()
		if pygame.sprite.spritecollideany(player, enemies):
			# game.defeat()
			game.set_state('game_over')


		shot_enemies = pygame.sprite.groupcollide(enemies, player_lasers, False, True)
		for e in shot_enemies:
			e.get_damage(shot_enemies[e][0].damage)
			if e.is_dead():
				e.kill()

		# Отрисовка
		player.draw(window)
		player_lasers.draw(window)
		enemies.draw(window)

	# Главное меню
	elif game.state == 'menu':
		main_menu.update(events)
		main_menu.draw(window)

	# Экран проигрыша
	elif game.state == 'game_over':
		window.fill(BLACK)
		lose_text.draw(window)

	# Последние изменения
	pygame.display.flip()
	game.clock.tick(FPS)

# Завершение Pygame
pygame.quit()
