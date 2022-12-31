import random

import pygame


class Controller:
    def __init__(self, screen, head):
        self.screen = screen
        self.body_parts = [head]
        self.head = head
        self.apple = pygame.image.load('images/apple.png')
        self.apple = pygame.transform.scale(self.apple, (15, 15))
        self.apple_rect = self.apple.get_rect()
        self.head_rect = self.head.get_rect()
        self.set_apple()
        self.add = False

    def key_handle(self, rect):
        self.check_if_eaten(rect)
        x, y = 0, 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            x, y = 0, -1
        elif key[pygame.K_DOWN]:
            x, y = 0, 1
        elif key[pygame.K_LEFT]:
            x, y = -1, 0
        elif key[pygame.K_RIGHT]:
            x, y = 1, 0
        elif key[pygame.K_SPACE]:
            x, y = -1, -1
        return x, y

    def check_position_limits(self, rect):
        if rect.x <= -15:
            rect.x = 315
        elif rect.y <= -15:
            rect.y = 315
        elif rect.x >= 315:
            rect.x = -15
        elif rect.y >= 315:
            rect.y = -15
        return rect

    def set_apple(self):
        while True:
            x, y = random.randint(5, 280), random.randint(5, 280)
            is_ok = True
            for part in self.body_parts:
                rect = part.get_rect()
                if rect.x <= x <= rect.x + 15 and rect.y <= y <= rect.y + 15:
                    is_ok = not is_ok
                    break
            if is_ok:
                self.apple_rect.center = x, y
                return

    def check_if_eaten(self, rect):
        apple_rect = self.apple_rect
        if apple_rect.x - 10 <= rect.x <= apple_rect.x + 10 and apple_rect.y - 10 <= rect.y <= apple_rect.y + 10:
            score = int((str(pygame.display.get_caption()).split(' = ')[1].split('\'')[0])) + 1
            pygame.display.set_caption('Score = ' + str(score))
            self.add = True
            self.set_apple()
