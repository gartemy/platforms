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
platform = pygame.image.load('кирпич шоколадка small.png')

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

    platforms = []

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '*':
                platform_rect = platform.get_rect()
                platform_rect.x = platform_rect.width * j
                platform_rect.y = platform_rect.height * i
                platforms.append(platform_rect)
                window.blit(platform, platform_rect)

    pygame.display.update()
    clock.tick(FPS)