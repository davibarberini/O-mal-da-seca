import pygame
from pygame.locals import KEYDOWN, K_UP, K_RIGHT, K_LEFT, K_r, KEYUP


class Player(object):
    def __init__(self, scr, color, rect ,vely, image):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.vely = vely
        self.velx = 0
        self.width = 0
        self.image = pygame.image.load(image).convert_alpha()
        self.alive = True
        self.pulo = 0

    def draw(self):
        if self.alive:
            #pygame.draw.rect(self.scr, self.color, self.rect, self.width)
            self.scr.blit(self.image, (self.rect[0], self.rect[1]))

    def update(self):
        if self.alive:
            if self.rect[1] + self.vely > 650:
                self.pulo = 0
                self.vely = 0
            if self.rect[0] + self.velx > 500:
                self.velx = 0
            if self.rect[0] + self.velx < 0:
                self.velx = 0
            self.rect[1] += self.vely
            self.vely += 0.15
            self.rect[0] += self.velx



def ekeydown (e, cenario):
    if e.key == K_UP and cenario.p1.pulo <= 2:
        cenario.p1.pulo += 1
        cenario.p1.vely = -6
    if e.key == K_RIGHT:
        cenario.p1.velx = 6
    elif e.key == K_LEFT:
        cenario.p1.velx = -6
    elif e.key == K_r:
        cenario.p1.vida = 100

def ekeyup(e, cenario):
    if e.key == K_RIGHT and cenario.p1.velx > 0:
        cenario.p1.velx = 0
    elif e.key == K_LEFT and cenario.p1.velx < 0:
        cenario.p1.velx = 0
