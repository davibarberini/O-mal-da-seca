import pygame
from pygame.locals import K_UP, K_RIGHT, K_LEFT, K_r, K_x, K_z, K_c


class Player(object):
    def __init__(self, scr, color, rect, vely):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.vely = vely
        self.velx = 0
        self.width = 0
        self.alive = True
        self.pulo = 0
        self.count = 0
        self.atacando = False
        self.tiro = Retangulo(scr, (0, 0, 255), [-500, 50, 20, 10], "assets/fabiano/bullet.png",
                              "assets/fabiano/bulletsound.wav")
        self.vida = 100
        self.vulnerable = True
        self.countvul = 0
        self.slow = 1
        self.estado = 0
        self.imagewalkingreal =[pygame.image.load("assets/fabiano/fab_walk1.png").convert_alpha(),
                    pygame.image.load("assets/fabiano/fab_walk2.png").convert_alpha(),
                    pygame.image.load("assets/fabiano/fab_walk3.png").convert_alpha(),
                    pygame.image.load("assets/fabiano/fab_walk4.png").convert_alpha()]

        self.imagewalking =[pygame.transform.scale(self.imagewalkingreal[0], (60, 120)),
                         pygame.transform.scale(self.imagewalkingreal[1], (60, 120)),
                         pygame.transform.scale(self.imagewalkingreal[2], (60, 120)),
                         pygame.transform.scale(self.imagewalkingreal[3], (60, 120))]

        self.imagereal = [pygame.image.load("assets/fabiano/fab_idle.png").convert_alpha(),
                     pygame.image.load("assets/fabiano/fab_jump.png").convert_alpha()]

        self.image = [pygame.transform.scale(self.imagereal[0], (60, 120)),
                     pygame.transform.scale(self.imagereal[1], (60, 120))]

        self.sounds = [pygame.mixer.Sound("assets/fabiano/jumpsound.wav"),
                        pygame.mixer.Sound("assets/fabiano/damagesound.wav")]
        self.countwalk = 0
        self.spritepersec = 12

    def draw(self):
        if self.alive:
            fabpos = (self.rect[0], self.rect[1])
            #pygame.draw.rect(self.scr, self.color, self.rect, self.width)
            #self.scr.blit(self.image, (self.rect[0], self.rect[1]))
            self.tiro.draw()
            self.tiro.update()
            # pygame.draw.rect(scr, fabiano["cor"], fabiano["rect"], 0)
            if self.estado == 0:
                self.scr.blit(self.image[0], fabpos)
            elif self.estado == 1:
                self.scr.blit(self.image[1], fabpos)
            elif self.estado == 2:
                self.scr.blit(self.imagewalking[self.countwalk // self.spritepersec], fabpos)
                self.countwalk += 1
                if self.countwalk >= self.spritepersec * 4:
                    self.countwalk = 0
            pygame.draw.rect(self.scr, (0, 255, 0), [0, 0, self.vida * 3, 30], 0)

    def update(self):
        if self.alive:
            if self.rect[1] + self.vely > 570:
                self.pulo = 0
                self.vely = 0
                if self.estado == 1:
                    if self.velx == 0:
                        self.estado = 0
                    else:
                        self.estado = 2
            if self.rect[0] + self.velx > 1024 - self.rect[2]:
                self.estado = 0
                self.velx = 0
            if self.rect[0] + self.velx < 0:
                self.estado = 0
                self.velx = 0
            self.rect[1] += self.vely
            self.vely += 0.20
            self.rect[0] += self.velx
            self.attack()
            if self.vida < 0:
                from main import gameintro
                gameintro()

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
            self.tiro.sound.play()
            self.tiro.rect[0] = self.rect[0] + 45
            self.tiro.rect[1] = self.rect[1] + 45
            self.tiro.alive = True

    def dash(self):
        self.sounds[1].play()
        if self.velx > 0:
            self.rect[0] += 100
            if self.rect[0] + self.rect[2] > 1024:
                self.rect[0] = 1024 - self.rect[2]
        elif self.velx < 0:
            self.rect[0] += -100
            if self.rect[0] < 0:
                self.rect[0] = 0

    def damage(self):
        if not self.vulnerable:
            self.color = (255, 255, 0)
            if self.countvul > 80:
                self.vulnerable = True
                self.countvul = 0
                self.color = (0, 0, 255)
                self.slow = 1
            self.countvul += 1


class Retangulo(object):
    def __init__(self, scr, color, rect, image, sound):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.width = 0
        self.alive = False
        self.count = 0
        self.image = pygame.image.load(image).convert_alpha()
        self.sound = pygame.mixer.Sound(sound)

    def draw(self):
        if self.alive:
            pygame.draw.rect(self.scr, self.color, self.rect, self.width)
            self.scr.blit(self.image, (self.rect[0], self.rect[1]))

    def update(self):
        if self.alive:
            self.count += 1
            self.rect[0] += 10
            if self.count > 200:
                self.rect[0] = -50
                self.alive = False
                self.count = 0


def ekeydown(e, cenario):
    if e.key == K_UP and cenario.p1.pulo <= 1:
        cenario.p1.sounds[0].play()
        cenario.p1.pulo += 1
        cenario.p1.vely = -9
        cenario.p1.estado = 1
    if e.key == K_RIGHT:
        cenario.p1.velx = 6 // cenario.p1.slow
        if not cenario.p1.estado == 1:
            cenario.p1.estado = 2
    elif e.key == K_LEFT:
        cenario.p1.velx = -6 // cenario.p1.slow
        if not cenario.p1.estado == 1:
            cenario.p1.estado = 2
    elif e.key == K_x:
        cenario.p1.atacando = True
    elif e.key == K_z:
        cenario.p1.shoot()
    elif e.key == K_r:
        cenario.p1.vida = 100
    elif e.key == K_c:
        cenario.p1.dash()
        cenario.p1.estado = 1


def ekeyup(e, cenario):
    if e.key == K_RIGHT and cenario.p1.velx > 0:
        cenario.p1.velx = 0
        if not cenario.p1.estado == 1:
            cenario.p1.estado = 0
    elif e.key == K_LEFT and cenario.p1.velx < 0:
        cenario.p1.velx = 0
        if not cenario.p1.estado == 1:
            cenario.p1.estado = 0
