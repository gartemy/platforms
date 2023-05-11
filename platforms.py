import pygame

pygame.init()

WIDTH = 1920
HEIGHT = 1200

window = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN)
pygame.display.set_caption('Контр-страйк 2 (оригинал) бета-тест 2')

FPS = 60
clock = pygame.time.Clock()

man_jump = pygame.image.load('man_jump.png')
man_stand = pygame.image.load('man_stand.png')
man_right = pygame.image.load('man_walk.png')
man_left = pygame.transform.flip(man_right, True, False)

speed = 10
change_x = 0
man = man_stand
man_rect = man_stand.get_rect()
man_rect.left = WIDTH // 2
man_rect.bottom = HEIGHT // 2

jump = False

# Максимальная высота прыжка
jump_max = 25

# Изменение прыжка
jump_count = 0

# Игрок находится на платформе
on_platform = False

# Находимся ли в главном меню
main_menu = True

platform_img = pygame.image.load('кирпич шоколадка small.png')

coin = pygame.image.load('coin.png')
coin = pygame.transform.scale(coin, (25, 25))

map = [
    '*******************************',
    '*                            **',
    '*                            **',
    '*    o                       **',
    '*         o                  **',
    '*                            **',
    '*                            **',
    '*            o               **',
    '*                            **',
    '*                 o          **',
    '*                            **',
    '*                            **',
    '*            **              **',
    '*                            **',
    '*                            **',
    '*                            **',
    '*          ******        ******',
    '*****                        **',
    '*                            **',
    '*******************************'
]

# Логотип игры
logo = pygame.image.load('logo.png')
logo_rect = logo.get_rect()
logo_rect.x = WIDTH // 4 - 50
logo_rect.y = HEIGHT // 5

# Кнопка начала игры
start_btn = pygame.image.load('start_btn.png')
start_rect = start_btn.get_rect()
start_rect.x = WIDTH // 2 - 525
start_rect.y = HEIGHT // 2

# Кнопка выхода из игры
exit_btn = pygame.image.load('exit_btn.png')
exit_rect = exit_btn.get_rect()
exit_rect.x = WIDTH // 2 - 75
exit_rect.y = HEIGHT // 2

while True:
    window.fill(pygame.Color('white'))

    man_old = man_rect.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump = True
                jump_count = jump_max
                on_platform = False
            if event.key == pygame.K_ESCAPE:
                main_menu = True

    if main_menu == True:
        window.fill([224, 127, 9])

        # Позиция указателя мыши
        pos = pygame.mouse.get_pos()

        if start_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == True:
            main_menu = False
        
        if exit_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == True:
            exit()

        window.blit(logo, logo_rect)
        window.blit(start_btn, start_rect)
        window.blit(exit_btn, exit_rect)
    else:
        platforms = []

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == '*':
                    platform_rect = platform_img.get_rect()
                    platform_rect.x = platform_rect.width * j
                    platform_rect.y = platform_rect.height * i
                    platforms.append(platform_rect)
                    window.blit(platform_img, platform_rect)
                elif map[i][j] == 'o':
                    coin_rect = coin.get_rect()
                    coin_rect.x = coin_rect.width * j
                    coin_rect.y = coin_rect.height * i
                    window.blit(coin, coin_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            change_x = speed
            man = man_right
        
        if keys[pygame.K_LEFT]:
            change_x = -speed
            man = man_left

        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            man = man_stand
            change_x = 0

        if jump == True:
            man_rect.y -= jump_count
            man = man_jump

        if jump_count > -jump_max or (man_rect.bottom < HEIGHT and on_platform == False):
            jump_count -= 1
            man = man_jump
        else:
            jump = False
            on_platform = True

        if man_rect.bottom > HEIGHT:
            man_rect.bottom = HEIGHT
            jump = False
            on_platform = True
        
        man_rect.x += change_x

        for platform in platforms:
            if man_rect.colliderect(platform):
                if man_rect.left < man_old.left:
                    man_rect.x -= change_x

                if man_rect.right > man_old.right:
                    man_rect.x -= change_x

            if man_rect.colliderect(platform):
                if man_rect.bottom > man_old.bottom:
                    jump = False
                    on_platform = True
                    man_rect.bottom = platform.top

            if man_rect.colliderect(platform) and man_rect.y < platform.height:
                jump = False
                on_platform = True
                man_rect.top = man_old.top

        if on_platform == True:
            manrect_next = man_rect.copy()
            manrect_next.y += 1

            if manrect_next.collidelist(platforms) == -1:
                jump = True
                on_platform = False
                jump_count = -1

        window.blit(man, man_rect)

    pygame.display.update()
    clock.tick(FPS)