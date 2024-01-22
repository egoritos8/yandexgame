import pygame
import sys
import os
import random


pygame.mixer.pre_init(44100, -16, 1, 512)
# Инициализация Pygame
pygame.init()

# Создание экрана
WIDTH, HEIGHT = 900, 900
score = 0
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BEKOSHA RUN")

vol = 0.5

pygame.mixer.music.load('sounds/main_soundtrek.mp3')
pygame.mixer.music.set_volume(vol)
pygame.mixer.music.play(-1)

carrot_sound = pygame.mixer.Sound('sounds/carrot_sound.ogg')
win_sound = pygame.mixer.Sound("sounds/win_sound.ogg")


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # Если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# Создание фоновой картинки
background_img = pygame.image.load('images/background2.png')
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
score_text = game_over_font.render(str(score), True, (0, 0, 0))
score_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

# Параметры квадрата персонажа

square_size = 50
square_x = 35
square_y = HEIGHT - square_size
speed = 10
jump_count = 10
is_jumping = False
falling_speed = 0
contact = False
prev_square_y = square_y  # Начальная позиция по вертикали

pig_img = pygame.image.load('images/pig2.png')
pig_img = pygame.transform.scale(pig_img, (square_size, square_size))
reverse = 'L'
pig_mack = pygame.mask.from_surface(pig_img)

platform_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()
star_sprites = pygame.sprite.Group()
portal_sprites = pygame.sprite.Group()


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/carrot.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.food_mack = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        food_sprites.add(self)

    def eat(self):
        global score
        score += 1
        carrot_sound.play()
        food_sprites.remove(self)

    def remove(self):
        food_sprites.remove(self)


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/portal.png')
        self.image = pygame.transform.scale(self.image, (70, 100))
        self.food_mack = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        portal_sprites.add(self)

    def remove(self):
        portal_sprites.remove(self)


class Stars_effect(pygame.sprite.Sprite):
    # Генерируем частицы разного размера
    fire = [load_image("images/star.png")]
    for scale in (5, 10):
        fire.append(pygame.transform.scale(fire[0], (20, 20)))
    fire = fire[1:]

    def __init__(self, pos, dx, dy):
        super().__init__()
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # У каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # И свои координаты
        self.rect.x, self.rect.y = pos

        # Гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        # Движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # Перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


def create_stars(position):
    # Количество создаваемых частиц
    particle_count = 20
    # Возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        star_effects = Stars_effect(position, random.choice(numbers), random.choice(numbers))
        star_sprites.add(star_effects)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def remove(self):
        platform_sprites.remove(self)


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)


camera = Camera(WIDTH // 2, HEIGHT // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pig_img = pygame.image.load('images/pig2.png')
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


def new_level(x):
    platform_sprites.empty()
    food_sprites.empty()
    portal_sprites.empty()

    f = open(level[x], encoding='utf-8')
    lines = f.readlines()

    for line in lines:
        if line.split('-')[0] == 'P':
            obstacle_x = int(line.split('-')[1])
            obstacle_y = int(line.split('-')[2])
            obstacle_width = int(line.split('-')[3])
            obstacle_height = 25
            ship_img = 'images/platforma.png'
            platform = Platform(obstacle_x, obstacle_y, obstacle_width, obstacle_height, ship_img)
            platform_sprites.add(platform)
        if line.split('-')[0] == 'F':
            obstacle_x = int(line.split('-')[1])
            obstacle_y = int(line.split('-')[2])
            food = Food(obstacle_x, obstacle_y)
            food_sprites.add(food)
        if line.split('-')[0] == 'PORT':
            obstacle_x = int(line.split('-')[1])
            obstacle_y = int(line.split('-')[2])
            portal = Portal(obstacle_x, obstacle_y)
            portal_sprites.add(portal)


# Управление персонажем
move_left = False
move_right = False
jump = False

# Флаг окончания и начала игры
game_over = False
game_start = True
contact = False

level = {
    1: 'levels/level_1',
    2: 'levels/level_2'
}

curent_level = 1

new_level(curent_level)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

print(f'level - {curent_level}')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_start:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    game_start = False

        if game_over:
            font = pygame.font.Font(None, 36)
            end_text = font.render("ВЫ ПРОШЛИ УРОВЕНЬ!!", True, (255, 255, 255))
            win.blit(end_text, (400, 450))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print(f'level - {curent_level}')
                game_over = False
                pig_rect.rect.x = square_x
                pig_rect.rect.y = square_y
                square_y = HEIGHT - square_size
                square_x = 35
                falling_speed = 0
                is_jumping = False
                jump_count = 10
                score = 0
                new_level(curent_level)
                pygame.mixer.music.play(-1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                print(f'level - {curent_level}')
                curent_level += 1
                falling_speed = 0
                is_jumping = False
                jump_count = 10
                score = 0
                new_level(curent_level)
                pig_rect.rect.x = square_x
                pig_rect.rect.y = square_y
                square_y = HEIGHT - square_size
                square_x = 35
                game_over = False
                pygame.mixer.music.play(-1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                print(f'level - {curent_level}')
                curent_level += 1
                falling_speed = 0
                is_jumping = False
                jump_count = 10
                score = 0
                new_level(curent_level)
                pig_rect.rect.x = square_x
                pig_rect.rect.y = square_y
                square_y = HEIGHT - square_size
                square_x = 35
                game_over = False
                pygame.mixer.music.play(-1)

    if not game_start and not game_over:
        # Управление персонажем
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
        eating = pygame.sprite.spritecollide(pig_rect, food_sprites, False)
        stars = pygame.sprite.spritecollide(pig_rect, portal_sprites, False)

        if stars:
            create_stars((0, 0))
            create_stars((300, 0))
            create_stars((500, 0))
            create_stars((700, 0))
            create_stars((900, 0))
            game_over = True
            pygame.mixer.music.pause()
            win_sound.set_volume(vol)
            win_sound.play()

        if eating:
            eating[0].eat()
            create_stars((eating[0].x, eating[0].y))

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

            # Обработка движения камеры за персонажем
            if square_x > WIDTH / 2:
                camera_x = square_x - WIDTH / 2

            # Отображение фона
            win.blit(background_img, (0 - camera_x, 0))

            # Отображение персонажа
            pygame.draw.rect(win, (255, 0, 0), (square_x - camera_x, square_y, square_size, square_size))

    win.fill((0, 0, 0))  # Отчистка экрана
    win.blit(background_img, (0, 0))
    platform_sprites.draw(win)
    food_sprites.draw(win)
    font = pygame.font.Font(None, 36)

    # Создание текстового объекта для отображения счета
    text = font.render("Счет: " + str(score), True, (255, 255, 255))

    # Отображение текстового объекта в правом верхнем углу
    win.blit(text, (WIDTH - text.get_width() - 10, 10))
    portal_sprites.draw(win)
    win.blit(pig_img, (pig_rect.rect.x, pig_rect.rect.y))

    for star in star_sprites:
        star.update()  # Обновляем позицию звезды
        win.blit(star.image, camera.apply(star))

    pygame.display.update()  # Обновляем дисплей
    clock.tick(30)

# Отрисовываем экран
pygame.quit()
sys.exit()
