import pygame
from button import Button
import os
from win32api import GetSystemMetrics

os.chdir("C:/Users/William/Documents/Clement/Python/Space_Invaders")

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

clock = pygame.time.Clock()

WIDTH, HEIGHT = screen_width - 300, screen_height - 80

pygame.font.init()


def pause(window, bg):
	# load button images
	resume_img = pygame.image.load(os.path.join('button_images','button_resume.png')).convert_alpha()
	control_img = pygame.image.load(os.path.join('button_images', 'ControlsButton.png')).convert_alpha()
	back_img = pygame.image.load(os.path.join('button_images', 'button_back.png')).convert_alpha()
	exit_img = pygame.image.load(os.path.join('button_images', 'button_quit.png')).convert_alpha()

	# create buttons
	resume_button = Button((WIDTH / 2) - resume_img.get_width()/2 + 5, 150, resume_img, 1)
	controls_button = Button((WIDTH /2) - control_img.get_width()/2 + 80, 250, control_img, 0.6)
	back_button = Button(20, HEIGHT - 100, back_img, 1)
	exit_button = Button((WIDTH/2) -  exit_img.get_width()/2, 350, exit_img, 1)

	title_font = pygame.font.SysFont("comicsans", 70)
	instruction_font = pygame.font.SysFont("inkfree", 40)
	paused = True
	menu_state = "main"
	while paused:
		clock.tick(60)
		window.blit(bg, (0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
		if menu_state.lower() == "main":
			resume_button.draw(window)
			resume_button.hover()
			controls_button.draw(window)
			controls_button.hover()
			exit_button.draw(window)
			exit_button.hover()
			if resume_button.get_clicked():
				paused = False
				return True
			if controls_button.get_clicked():
				menu_state = "controls"
			if exit_button.get_clicked():
				paused = False
				return False
		if menu_state.lower() == "controls":
			title = title_font.render("Controls", 1, (0,255,0))
			move_control = instruction_font.render("(A,W,S,D) / (UP,DOWN, LEFT, RIGHT): Move plane", 1, (0,255,0))
			shoot_control = instruction_font.render("SPACE: To shoot lasers", 1, (0,255,0))
			pause_control = instruction_font.render("P: Pause", 1, (0,255,0))
			window.blit(title, (WIDTH/2 - title.get_width()/2, 20))
			window.blit(move_control, (WIDTH/2 - move_control.get_width()/2, 150))
			window.blit(shoot_control, (WIDTH/2 - shoot_control.get_width()/2, 250))
			window.blit(pause_control, (WIDTH/2 - pause_control.get_width()/2,350))
			back_button.draw(window)
			back_button.hover()
			if back_button.get_clicked():
				menu_state = "main"
		
		pygame.display.update()

