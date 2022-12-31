import sys
import time
import pygame
from pygame.locals import *
from gameController import Controller

pygame.init()
pygame.display.set_caption('Score = 0')
w = h = 300
screen = pygame.display.set_mode((w, h))
img = pygame.image.load('images/body_vertical.png')
apple = pygame.image.load('images/apple.png')
img = pygame.transform.scale(img, (15, 15))
apple = pygame.transform.scale(apple, (18, 18))
img.fill((110, 110, 255))
rect = img.get_rect()
rect.center = w / 2, h / 2
isPaused = False
x = y = 0
clock = pygame.time.Clock()
game = Controller(screen, img)
pygame.display.update()
body_parts = [rect]


def add():
    global x, y
    rec = img.get_rect()
    rec.center = body_parts[-1].center
    rec.x -= x * 15
    rec.y -= y * 15
    body_parts.append(rec)


def self_eat():
    i = 0
    for rct in body_parts:
        if i != 0 and rct == body_parts[0]:
            return True
        i += 1
    return False


def get_head():
    w = h = 19
    if x == 1:
        direction = 'right'
        w += 5
    elif x == -1:
        direction = 'left'
        w += 5
    elif y == -1:
        direction = 'up'
        h += 5
    else:
        direction = 'down'
        h += 5
    head = pygame.image.load('images/head_' + direction + '.png')
    head = pygame.transform.scale(head, (w, h))
    return head


while True:
    if game.add:
        game.add = False
        add()
    if self_eat():
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    x1, y1 = game.key_handle(body_parts[0])

    if x1 == y1 == -1:
        isPaused = not isPaused
        time.sleep(.2)
    elif not (x1 == y1 == 0 or (x == -x1 and x != 0) or (y == -y1 and y != 0)):
        x, y = x1, y1

    if isPaused:
        continue
    screen.fill((255, 255, 0))
    body_parts[-1].move_ip(body_parts[0].x - body_parts[-1].x + x * 15, body_parts[0].y - body_parts[-1].y + y * 15)
    body_parts.insert(0, body_parts[-1])
    del body_parts[-1]

    for rect in body_parts:
        rect = game.check_position_limits(rect)
        if body_parts.index(rect) == 0:
            a, b = rect.center
            if x != 0:
                rect.y -= 2
                if x == -1:
                    rect.x -= 7
            elif y != 0:
                rect.x -= 2
                if y == -1:
                    rect.y -= 7
            screen.blit(get_head(), rect)
            rect.center = a, b
        else:
            screen.blit(img, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    screen.blit(game.apple, game.apple_rect)
    pygame.display.update()
    clock.tick(10)
