import pygame
import time
from os import listdir
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1280, 720
pygame.display.set_caption("Arcade game")

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
AQUA = 0, 255, 255
GREEN = 0, 255, 0

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen) # , pygame.RESIZABLE)

IMGS_PATH = 'images'

# player = pygame.Surface((20, 20))
# player.fill(WHITE)
player_images = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player = player_images[0] # pygame.image.load("player.png").convert_alpha()
player_rect = player.get_rect()
player_speed = 7

game_over = pygame.transform.scale(pygame.image.load("gameover.jpg").convert_alpha(), (width // 2, height // 2))
game_over_rect = pygame.Rect((200, 200, 400, 400))
# line = pygame.Surface((20, height))
# line.fill(AQUA)
# line_rect = pygame.Rect(100, 0, *line.get_size())


def create_enemy():
    # enemy = pygame.Surface((20, 20))
    # enemy.fill(RED)
    enemy = pygame.transform.scale(pygame.image.load("enemy.png").convert_alpha(), (100, 50)) # pygame.image.load("enemy.png").convert_alpha()
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(4, 7)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    # bonus = pygame.Surface((15, 15))
    # bonus.fill(GREEN)
    bonus = pygame.transform.scale(pygame.image.load("bonus.png").convert_alpha(), (250, 220)) # pygame.image.load("bonus.png").convert_alpha()
    bonus_rect = pygame.Rect(random.randint(0, width - 250), -300, *bonus.get_size())
    bonus_speed = random.randint(2, 3)
    return [bonus, bonus_rect, bonus_speed]


bg = pygame.transform.scale(pygame.image.load("background.png").convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0

scores = 0

enemies = []
bonuses = []

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_images):
                img_index = 0
            player = player_images[img_index]


    pressed_keys = pygame.key.get_pressed()

    # if ball_rect.bottom >= height or ball_rect.top <= 0:
    #     ball.fill(AQUA)
    #     ball_speed[1] = -ball_speed[1]
    # if ball_rect.right >= width or ball_rect.left <= 0:
    #     ball.fill(RED)
    #     ball_speed[0] = -ball_speed[0]

    # main_surface.fill(WHITE)
    # main_surface.blit(bg, (0, 0))

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, player_rect)
    main_surface.blit(font.render(str(scores), True, RED), (width - 30, 0))
    # main_surface.blit(line, line_rect)


    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            main_surface.blit(game_over, game_over_rect)
            time.sleep(3)
            is_working = False

        if scores >= 5:
            enemy[2] = random.randint(15, 20)


    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)


    # main_surface.fill((155, 155, 155))
    pygame.display.flip()


