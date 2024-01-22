import pygame
import sys
import os
import random

# Инициализация Pygame
pygame.init()

# Создание экрана
WIDTH, HEIGHT = 1000, 750
score = 0
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BEKOSHA RUN")

background_img = pygame.image.load('background2.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

welcome_font = pygame.font.Font(None, 100)
welcome_text = welcome_font.render("BEKOSHA RUN", True, (255, 255, 255))
welcome_text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))

start_button_image = pygame.image.load('start_button.png')
start_button_image = pygame.transform.scale(start_button_image, (140, 140))
start_button_rect = start_button_image.get_rect(topleft=(600, 300))

list_button_image = pygame.image.load('start_button.png')
list_button_image = pygame.transform.scale(list_button_image, (140, 140))
list_button_rect = list_button_image.get_rect(topleft=(425, 300))

restart_button_image = pygame.image.load('start_button.png')
restart_button_image = pygame.transform.scale(restart_button_image, (140, 140))
restart_button_rect = restart_button_image.get_rect(topleft=(250, 300))

level_buttons = ['start_button.png', 'start_button.png', 'start_button.png',
                 'start_button.png', 'start_button.png', 'start_button.png']
button_group = []

for i in range(3):
    a = pygame.image.load('start_button.png')
    a = pygame.transform.scale(restart_button_image, (120, 120))
    b = restart_button_image.get_rect(topleft=(250 + 200 * i, 300))
    button_group.append((a, b))

for i in range(3):
    a = pygame.image.load('start_button.png')
    a = pygame.transform.scale(restart_button_image, (120, 120))
    b = restart_button_image.get_rect(topleft=(250 + 200 * i, 450))
    button_group.append((a, b))

running = True
status = 'главное меню'
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if status == 'главное меню':
            win.blit(welcome_text, welcome_text_rect)
            win.blit(start_button_image, start_button_rect)
            win.blit(list_button_image, list_button_rect)
            win.blit(restart_button_image, restart_button_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    status = 'в игре'
                elif list_button_rect.collidepoint(event.pos):
                    status = 'выбор уровней'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
    win.blit(background_img, (0, 0))
    if status == 'главное меню':
        win.blit(welcome_text, welcome_text_rect)
        win.blit(start_button_image, start_button_rect)
        win.blit(list_button_image, list_button_rect)
        win.blit(restart_button_image, restart_button_rect)
    if status == 'выбор уровней':
        for i in button_group:
            win.blit(i[0], i[1])
    print(status)
    pygame.display.update()
