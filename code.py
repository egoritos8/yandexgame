import pygame
import sys
import time

# Инициализация Pygame
pygame.init()

# Создание экрана
WIDTH, HEIGHT = 900, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BEKOSHA RUN")

# Создание фоновой картинки
background_img = pygame.image.load('img.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Создание экрана приветствия
welcome_font = pygame.font.Font(None, 50)
welcome_text = welcome_font.render("BEKOSHA RUN", True, (0, 0, 0))
welcome_text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

instructions_font = pygame.font.Font(None, 36)
instructions_text = instructions_font.render("Press SPACE or UP to jump", True, (0, 0, 0))
instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# Создание экрана окончания игры
game_over_font = pygame.font.Font(None, 50)
game_over_text = game_over_font.render("GAME OVER!", True, (0, 0, 0))
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

score_font = pygame.font.Font(None, 36)

# Параметры квадрата (персонажа)
square_size = 35
square_x = 35
square_y = HEIGHT - square_size
speed = 10
jump_count = 10
is_jumping = False
falling_speed = 0
contact = False
prev_square_y = square_y  # Начальная позиция по вертикали

pig_img = pygame.image.load('pig2.png')
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
        self.pig_img = pygame.image.load('pig2.png')
        self.pig_img = pygame.transform.scale(self.pig_img, (square_size, square_size))
        self.rect = pygame.Rect(square_x, square_y, square_size, square_size)

    def update(self, move_left, move_right, jump):
        global square_x
        global square_y
        global reverse
        global pig_img
        global is_jumping, jump_count, falling_speed, prev_square_y
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

        # Обработка прыжка
        if jump and not is_jumping:
            is_jumping = True
            falling_speed = 0
            prev_square_y = square_y  # Запоминаем предыдущую высоту

        # Логика прыжка
        if is_jumping:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                square_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Физика падения
        if square_y < HEIGHT - square_size:
            square_y += falling_speed
            falling_speed += 0.7  # Увеличиваем скорость падения
        else:
            square_y = HEIGHT - square_size
            falling_speed = 0

        # Обработка столкновения с платформами
        collide = pygame.sprite.spritecollide(self, platform_sprites, False)
        if collide:
            if prev_square_y < collide[0].rect.top and falling_speed > 0:
                square_y = collide[0].rect.top - square_size
                falling_speed = 0
                is_jumping = False
                jump_count = 10
            elif prev_square_y > collide[0].rect.bottom and falling_speed > 0:
                # Персонаж стоит на платформе
                is_jumping = False
                square_y = collide[0].rect.top - square_size + 1

        # Предотвращение выпрыгивания сверху за границы
        if square_y < 0:
            square_y = 0

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
        ship_img = 'platforma.png'
        platform = Platform(obstacle_x, obstacle_y, obstacle_width, obstacle_height, ship_img)
        platform_sprites.add(platform)

# Управление персонажем
move_left = False
move_right = False
jump = False

# Флаг окончания и начала игры
game_over = False
game_start = True
contact = False

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_start:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    game_start = False

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    pig_rect.rect.x = square_x
                    pig_rect.rect.y = square_y
                    square_y = HEIGHT - square_size
                    falling_speed = 0
                    is_jumping = False
                    jump_count = 10

    if not game_start and not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]

        # Обработка прыжка
        if not is_jumping:
            jump = keys[pygame.K_SPACE] or keys[pygame.K_UP]
        else:
            jump = False

        pig_rect.update(move_left, move_right, jump)

        # Обработка столкновения с платформами
        collide = pygame.sprite.spritecollide(pig_rect, platform_sprites, False)
        if collide:
            if pig_rect.rect.bottom <= collide[0].rect.centery:
                # Персонаж прыгает на платформу
                pig_rect.rect.y = collide[0].rect.top - square_size
                falling_speed = 0
                is_jumping = False
                jump_count = 10
            elif pig_rect.rect.centery >= collide[0].rect.bottom:
                # Персонаж стоит на платформе
                pig_rect.rect.y = collide[0].rect.bottom
                falling_speed = 0

        # Предотвращение выпрыгивания сверху за границы
        if pig_rect.rect.y < 0:
            pig_rect.rect.y = 0

        # Проверка на окончание игры (падение вниз)
        if pig_rect.rect.y > HEIGHT:
            game_over = True

    win.fill((0, 0, 0))  # Clear the screen
    win.blit(background_img, (0, 0))  # Draw the background
    platform_sprites.draw(win)
    win.blit(pig_img, (pig_rect.rect.x, pig_rect.rect.y))  # Draw the player sprite

    if game_start:
        win.blit(welcome_text, welcome_text_rect)
        win.blit(instructions_text, instructions_rect)

    if game_over:
        win.blit(game_over_text, game_over_rect)
        score_text = score_font.render("Your Score: {}".format(pig_rect.rect.y), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        win.blit(score_text, score_rect)

    pygame.display.update()  # Update the display
    clock.tick(30)

# Displaying the screen
pygame.quit()
sys.exit()
