import pygame
from random import randint

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

# Игрок находится на земле
on_ground = False

# Игрок находится на платформе
on_platform = False

platform_img = pygame.image.load('кирпич шоколадка small.png')

map = [
    '******************************',
    '*                            *',
    '*                            *',
    '*                            *',
    '*                            *',
    '*                            *',
    '*                            *',
    '*                            *',
    '*                            *',
    '*                            *',
    '*                            *',
    '*                            *',
    '*            **              *',
    '*                            *',
    '*                            *',
    '*                            *',
    '*          ******        *****',
    '*****                        *',
    '*                            *',
    '******************************'
]

while True:
    window.fill(pygame.Color('pink'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump = True
                jump_count = jump_max
                on_ground = False
                on_platform = False

    platforms = []

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '*':
                platform_rect = platform_img.get_rect()
                platform_rect.x = platform_rect.width * j
                platform_rect.y = platform_rect.height * i
                platforms.append(platform_rect)
                window.blit(platform_img, platform_rect)

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

    man_rect.x += change_x

    if jump == True:
        man_rect.y -= jump_count
        man = man_jump

    if jump_count > -jump_max or (man_rect.bottom < HEIGHT and on_ground == False):
        jump_count -= 1
        man = man_jump
    else:
        jump = False
        on_ground = True

    if man_rect.bottom > HEIGHT:
        man_rect.bottom = HEIGHT
        jump = False
        on_ground = True

    man_old = man_rect.copy()

    for platform in platforms:
        if man_rect.colliderect(platform):
            if man_rect.left < man_old.left:
                man_rect.x -= change_x

            if man_rect.right > man_old.right:
                man_rect.x += change_x

        if man_rect.colliderect(platform):
            if man_rect.bottom > man_old.bottom:
                jump = False
                on_ground = True
                man_rect.bottom = platform.top

    window.blit(man, man_rect)

    pygame.display.update()
    clock.tick(FPS)