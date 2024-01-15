import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Создание экрана
WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bekosha run")

# Создание фоновой картинки
background_img = pygame.image.load('background 2.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Создание экрана приветствия
welcome_font = pygame.font.Font(None, 50)
welcome_text = welcome_font.render("GAME OVER!", True, (255, 255, 255))
welcome_text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Параметры квадрата (персонажа)
square_size = 35
square_x = 35
square_y = HEIGHT - square_size
speed = 10
jump_count = 10
is_jumping = False
contact = False

pig_img = pygame.image.load('pig.png')
pig_img = pygame.transform.scale(pig_img, (square_size, square_size))
reverse = 'R'
pig_mack = pygame.mask.from_surface(pig_img)

platform_sprites = pygame.sprite.Group()

f = open('carta', encoding='utf-8')
lines = f.readlines()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pig_img = pygame.image.load('pig.png')
        self.pig_img = pygame.transform.scale(pig_img, (square_size, square_size))
        self.rect = pygame.Rect(square_x, square_y, square_size, square_size)

    def update(self, move_left, move_right):
        global square_x
        global square_y
        global reverse
        global pig_img
        global is_jumping, negative, jump_count
        if move_left and square_x > 0:
            square_x -= speed
            if reverse == 'R':
                pig_img = pygame.transform.flip(pig_img, True, False)
            reverse = 'L'
        if move_right and square_x < WIDTH - square_size:
            if reverse == 'L':
                pig_img = pygame.transform.flip(pig_img, True, False)
            reverse = 'R'
            square_x += speed

        self.rect = pygame.Rect(square_x, square_y, square_size, square_size)


pig_rect = Player()

# Создание группы спрайтов для платформ
platform_sprites = pygame.sprite.Group()

# Добавление платформ в группу спрайтов
for line in lines:
    if line.split('-')[0] == 'P':
        obstacle_x = int(line.split('-')[1])
        obstacle_y = int(line.split('-')[2])
        obstacle_width = int(line.split('-')[3])
        obstacle_height = 25
        ship_img = 'platforma.jfif'
        platform = Platform(obstacle_x, obstacle_y, obstacle_width, obstacle_height, ship_img)
        platform_sprites.add(platform)

# Управление персонажем


move_left = False
move_right = False

# Флаг окончания игры
game_over = False
contact = False

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
negative = -1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not is_jumping:
                is_jumping = True
        # Handle player movement
    keys = pygame.key.get_pressed()
    move_left = keys[pygame.K_LEFT]
    move_right = keys[pygame.K_RIGHT]
    collide = 0
    all_rects = [sprite.rect for sprite in platform_sprites]
    for platform_rect in all_rects:

        if pig_rect.rect.bottom >= platform_rect.centery and pig_rect.rect.colliderect(platform_rect):
            is_jumping = False
            contact = True
            square_y = platform_rect.top - square_size + 1
        if pig_rect.rect.colliderect(platform_rect):
            collide = 1
    if not collide and square_y > 365.0 and contact == False:
        is_jumping = True

        if is_jumping:
            if square_y < 365.0 or negative == 1:
                negative = 1
                if jump_count < 0:
                    negative = -1
                if square_y - (jump_count ** 2) * 0.5 * negative > 365.0:
                    square_y = 365.0
                else:
                    square_y -= (jump_count ** 2) * 0.5 * negative
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 8
                negative = 1
        print(jump_count, negative)

        pig_rect.update(move_left, move_right)
        win.fill((0, 0, 0))  # Clear the screen
        win.blit(background_img, (0, 0))  # Draw the background
        win.blit(pig_img, (square_x, square_y))  # Draw the player sprite
        platform_sprites.draw(win)
        pygame.display.update()  # Update the display
        clock.tick(30)

    # Displaying the screen

    pygame.quit()
    sys.exit()
