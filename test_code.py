import pygame
import sys
import os
import random

# Убираем задержку при воспроизведении звуков
pygame.mixer.pre_init(44100, -16, 1, 512)

# Инициализация Pygame
pygame.init()

# Создание экрана
WIDTH, HEIGHT = 900, 700
score = 0
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BEKOSHA RUN")

# Устанавливаем громкость музыки
vol = 0.3

# Загружаем музыку
pygame.mixer.music.load('sounds/main_soundtrek.mp3')
pygame.mixer.music.set_volume(vol)
pygame.mixer.music.play(-1)

carrot_sound = pygame.mixer.Sound('sounds/carrot_sound.ogg')
win_sound = pygame.mixer.Sound("sounds/win_sound.ogg")

background_img = pygame.image.load('images/background2.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

curent_level = 0

# Загружаем картинки
welcome_font = pygame.font.Font(None, 200)
welcome_text = welcome_font.render("BEKOSHA RUN", True, (0, 0, 0))
welcome_text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 700))

start_button_image = pygame.image.load('images/start_button.png')
start_button_image = pygame.transform.scale(start_button_image, (140, 140))
start_button_rect = start_button_image.get_rect(topleft=(WIDTH // 2 - 70, 300))

pause_button_image = pygame.image.load('images/pause_button.png')
pause_button_image = pygame.transform.scale(pause_button_image, (70, 70))
pause_button_rect = pause_button_image.get_rect(topleft=(10, 10))

list_button_image = pygame.image.load('images/list_button.png')
list_button_image = pygame.transform.scale(list_button_image, (140, 140))
list_button_rect = list_button_image.get_rect(topleft=(WIDTH // 2 + 105, 300))

restart_button_image = pygame.image.load('images/return_button.png')
restart_button_image = pygame.transform.scale(restart_button_image, (140, 140))
restart_button_rect = restart_button_image.get_rect(topleft=(WIDTH // 2 - 245, 300))

level_buttons = ['images/back_button.png', 'images/button_1.png', 'images/button_2.png', 'images/button_3.png',
                 'images/button_4.png', 'images/button_5.png']

button_group = []

for i in range(3):
    a = pygame.image.load(level_buttons[i])
    a = pygame.transform.scale(a, (120, 120))
    b = a.get_rect(topleft=(200 + 200 * i, 250))
    button_group.append((a, b))

for i in range(3):
    a = pygame.image.load(level_buttons[i + 3])
    a = pygame.transform.scale(a, (120, 120))
    b = a.get_rect(topleft=(200 + 200 * i, 400))
    button_group.append((a, b))


# Функция по подгрузке файлов
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
welcome_font = pygame.font.Font(None, 140)
welcome_text = welcome_font.render("BEKOSHA RUN", True, (200, 200, 200))
welcome_text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))

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
carrot_counter = 0

pig_img = pygame.image.load('images/pig2.png')
pig_img = pygame.transform.scale(pig_img, (square_size, square_size))
reverse = 'L'
pig_mack = pygame.mask.from_surface(pig_img)

platform_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()
star_sprites = pygame.sprite.Group()
portal_sprites = pygame.sprite.Group()


# Класс еды (моркови)
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
        global carrot_counter
        score += 1
        schet += 1
        carrot_sound.play()
        food_sprites.remove(self)

    def remove(self):
        food_sprites.remove(self)


# Класс портала
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load('images/portal2.png')
        self.image = pygame.transform.scale(original_image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.angle = 0  # Угол вращения портала
        self.original_image = self.image  # Сохраняем оригинальное изображение портала

    def update(self):
        # Обновляем угол вращения портала
        self.angle = (self.angle + 5) % 360  # Увеличиваем угол на 5 градусов в каждом кадре

        # Создаем повернутое изображение портала
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        # Получаем новый прямоугольник с учетом поворота
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        portal_sprites.remove(self)


# Класс эфекта звёзд
class stars_effect(pygame.sprite.Sprite):
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


# Функция по созданию звёзд
def create_stars(position):
    # Количество создаваемых частиц
    particle_count = 20
    # Возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        star_effects = stars_effect(position, random.choice(numbers), random.choice(numbers))
        star_sprites.add(star_effects)


# Класс платформ
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def remove(self):
        platform_sprites.remove(self)


# Класс камеры (для звёзд)
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


# Класс игрока (свинки)
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


# Функция по отрисовке нового уровня
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
            ship_img = 'images/platform.png'
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
    2: 'levels/level_2',
    3: 'levels/level_3',
    4: 'levels/level_4',
    5: 'levels/level_5'
}

curent_level = 1

a = 0

# Основной игровой цикл
running = True
status = 'main_menu'
clock = pygame.time.Clock()

print(f'level - {curent_level}')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if status == 'choosing_levels':
            win_sound.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_group[0][1].collidepoint(event.pos):
                    status = 'main_menu'
                    a = 1
                for i in range(1, 6):
                    if button_group[i][1].collidepoint(event.pos):
                        print(1)
                        curent_level = i
                        new_level(curent_level)
                        print(f'level - {curent_level}')
                        game_over = False
                        pig_rect.rect.x = square_x
                        pig_rect.rect.y = square_y
                        square_y = HEIGHT - square_size
                        square_x = 35
                        falling_speed = 0
                        is_jumping = False
                        jump_count = 10
                        pygame.mixer.music.play(-1)
                        status = 'in_game'
            font = pygame.font.Font(None, 36)
            end_text = font.render("ВЫБЕРИТЕ УРОВЕНЬ", True, (255, 255, 255))
            win.blit(end_text, (400, 450))

        if status == 'main_menu':
            win_sound.stop()
            win.blit(welcome_text, welcome_text_rect)
            win.blit(start_button_image, start_button_rect)
            win.blit(list_button_image, list_button_rect)
            win.blit(restart_button_image, restart_button_rect)
            if event.type == pygame.MOUSEBUTTONDOWN and a == 0:
                if start_button_rect.collidepoint(event.pos):
                    win_sound.stop()
                    status = 'in_game'
                    new_level(curent_level)
                elif list_button_rect.collidepoint(event.pos):
                    win_sound.stop()
                    status = 'choosing_levels'
                elif restart_button_rect.collidepoint(event.pos):
                    curent_level = 1
                    win_sound.stop()
                    status = 'in_game'
            a = 0

        if status == 'in_game':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    game_start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    status = 'pause'

        if status == 'pause':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    win_sound.stop()
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
                    status = 'in_game'
                if start_button_rect.collidepoint(event.pos):
                    win_sound.stop()
                    game_over = False
                    status = 'in_game'
                if list_button_rect.collidepoint(event.pos):
                    win_sound.stop()
                    status = 'choosing_levels'

        if game_over:
            font = pygame.font.Font(None, 36)
            end_text = font.render("ВЫ ПРОШЛИ УРОВЕНЬ!!", True, (255, 255, 255))
            win.blit(end_text, (400, 450))
            if curent_level == 5:
                win_sound.play()
                status = 'game_window'
            else:
                status = 'next_level_window'
            create_stars((0, 0))
            create_stars((100, 0))
            create_stars((200, 0))
            create_stars((400, 0))
            create_stars((600, 0))
            create_stars((800, 0))
            create_stars((300, 0))
            create_stars((500, 0))
            create_stars((700, 0))
            create_stars((900, 0))
            game_over = False

        if status == 'game_window':
            game_over = False
            pig_rect.rect.x = square_x
            pig_rect.rect.y = square_y
            square_y = HEIGHT - square_size
            square_x = 35
            falling_speed = 0
            is_jumping = False
            jump_count = 10
            score = 0

        if status == 'next_level_window':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    win_sound.stop()
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
                    status = 'in_game'
                if start_button_rect.collidepoint(event.pos):
                    win_sound.stop()
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
                    status = 'in_game'
                if list_button_rect.collidepoint(event.pos):
                    win_sound.stop()
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
                    status = 'main_menu'

    if not game_start and not game_over and status == 'in_game':
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

        win.blit(background_img, (0, 0))

        # Обновление и отрисовка порталов
        portal_sprites.update()  # Обновляем порталы
        for portal in portal_sprites:
            win.blit(portal.image, portal.rect)

        # Обработка столкновения с платформами
        collide = pygame.sprite.spritecollide(pig_rect, platform_sprites, False)
        eating = pygame.sprite.spritecollide(pig_rect, food_sprites, False)
        stars = pygame.sprite.spritecollide(pig_rect, portal_sprites, False)

        if stars:
            game_over = True
            pygame.mixer.music.pause()
            win_sound.set_volume(vol)
            if curent_level != 5:
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

    win.fill((0, 0, 0))
    win.blit(background_img, (0, 0))
    if status == 'main_menu':
        win.blit(welcome_text, welcome_text_rect)
        win.blit(start_button_image, start_button_rect)
        win.blit(list_button_image, list_button_rect)
        win.blit(restart_button_image, restart_button_rect)
    if status == 'next_level_window':
        win.blit(start_button_image, start_button_rect)
        win.blit(list_button_image, list_button_rect)
        win.blit(restart_button_image, restart_button_rect)
        font = pygame.font.Font(None, 100)
        text = font.render("ВЫ ПРОШЛИ УРОВЕНЬ!", True, (255, 255, 255))
        win.blit(text, (40, 170))
        font = pygame.font.Font(None, 50)
        for star in star_sprites:
            star.update()
            win.blit(star.image, camera.apply(star))
    if status == 'choosing_levels':
        for i in button_group:
            win.blit(i[0], i[1])
            font = pygame.font.Font(None, 100)
            text = font.render("ВЫБЕРИТЕ УРОВЕНЬ", True, (255, 255, 255))
            win.blit(text, (100, 130))
    if status == 'game_window':
        win.blit(list_button_image, list_button_rect)
        win.blit(restart_button_image, restart_button_rect)
        font = pygame.font.Font(None, 100)
        text = font.render("ВЫ ПРОШЛИ ИГРУ!", True, (255, 255, 255))
        win.blit(text, (100, 170))
        font = pygame.font.Font(None, 50)
        if carrot_counter == 1:
            text = font.render(f"ВЫ СОБРАЛИ {carrot_counter} МОРКОВКУ", True, (255, 255, 255))
        elif carrot_counter == [2, 3, 4]:
            text = font.render(f"ВЫ СОБРАЛИ {carrot_counter} МОРКОВОКИ", True, (255, 255, 255))
        else:
            text = font.render(f"ВЫ СОБРАЛИ {carrot_counter} МОРКОВОК", True, (255, 255, 255))
        win.blit(text, (40, 600))
    if status == 'in_game':
        # Отчистка экрана
        win.blit(pause_button_image, pause_button_rect)
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
            star.update()
            win.blit(star.image, camera.apply(star))

    if status == 'pause':
        win.blit(start_button_image, start_button_rect)
        win.blit(list_button_image, list_button_rect)
        win.blit(restart_button_image, restart_button_rect)

    pygame.display.update()
    clock.tick(30)

# Отрисовываем экран
pygame.quit()
sys.exit()