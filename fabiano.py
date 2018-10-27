import pygame
from pygame.locals import K_UP, K_RIGHT, K_LEFT, K_r, K_x, K_z


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
        self.count = 0
        self.atacando = False
        self.tiro = Retangulo(scr, (0, 0, 255), [-500, 50, 20, 10])

    def draw(self):
        if self.alive:
            pygame.draw.rect(self.scr, self.color, self.rect, self.width)
            self.scr.blit(self.image, (self.rect[0], self.rect[1]))
            self.tiro.draw()
            self.tiro.update()

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
            self.attack()

    def attack(self):
        if self.atacando:
            self.rect[2] = 100
            self.count += 1
            if self.count > 50:
                self.rect[2] = 60
                self.atacando = False
                self.count = 0

    def shoot(self):
        if not self.tiro.alive:
            self.tiro.rect[0] = self.rect[0]
            self.tiro.rect[1] = self.rect[1]
            self.tiro.alive = True


class Retangulo(object):
    def __init__(self, scr, color, rect):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.width = 0
        self.alive = False
        self.count = 0

    def draw(self):
        if self.alive:
            pygame.draw.rect(self.scr, self.color, self.rect, self.width)

    def update(self):
        if self.alive:
            self.count += 1
            self.rect[0] += 5
            if self.count > 200:
                self.rect[0] = -50
                self.alive = False
                self.count = 0

def ekeydown (e, cenario):
    if e.key == K_UP and cenario.p1.pulo <= 2:
        cenario.p1.pulo += 1
        cenario.p1.vely = -6
    if e.key == K_RIGHT:
        cenario.p1.velx = 6
    elif e.key == K_LEFT:
        cenario.p1.velx = -6
    elif e.key == K_x:
        cenario.p1.atacando = True
    elif e.key == K_z:
        cenario.p1.shoot()
    elif e.key == K_r:
        cenario.p1.vida = 100

def ekeyup(e, cenario):
    if e.key == K_RIGHT and cenario.p1.velx > 0:
        cenario.p1.velx = 0
    elif e.key == K_LEFT and cenario.p1.velx < 0:
        cenario.p1.velx = 0
