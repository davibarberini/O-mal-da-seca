import pygame
import fabiano as ply
from pygame.locals import FULLSCREEN, QUIT, KEYDOWN, K_g, KEYUP, K_s, K_o, K_r, K_b, K_p, K_f, MOUSEBUTTONDOWN, K_ESCAPE
pygame.init()

scrx = 1024
scry = 768

scr = pygame.display.set_mode((scrx, scry), FULLSCREEN, 32)

clock = pygame.time.Clock()

bolha = pygame.image.load("assets/hantiseca/bolha1.png").convert_alpha()


class Cenario(object):
    def __init__(self):
        self.boss = Boss(scr, (255, 0, 0), [scrx - 300, scry - 500, 250, 500], "assets/hantiseca/boss1.png")
        self.p1 = ply.Player(scr, (0, 0, 255), [scrx - (scrx - 50), scry - 130, 60, 120], 5, "assets/hantiseca/fabiano.png")
        #self.fundo = pygame.image.load("assets/hantiseca/fundo.png").convert()

    def update(self):
        #scr.blit(self.fundo, (0, 0))
        self.draw()
        self.boss.update()
        self.p1.update()

    def draw(self):
        self.boss.draw()
        self.p1.draw()


class Boss(object):
    def __init__(self, scr, color, rect, image):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.width = 0
        self.image = pygame.image.load(image).convert_alpha()
        self.skillgs = Retangulo(self.scr, (50, 50, 255), [4000, scry, 100, 0])
        self.skillsoco = Retangulo(self.scr, (50, 50, 255), [4000, 0, 0, 100])
        self.skillonda = Retangulo(self.scr, (50, 50, 255), [4000, 300, 0, 500])
        self.tiros = []
        self.count = 0

    def draw(self):
        #pygame.draw.rect(self.scr, self.color, self.rect, self.width)
        self.scr.blit(self.image, (self.rect[0], self.rect[1]))

    def update(self):
        self.geiser()
        self.soco()
        self.onda()
        self.bolhas((cenario.p1.rect[0], cenario.p1.rect[1]))
        self.count += 1
    def geiser(self):
        if self.skillgs.alive:
            self.skillgs.draw()
            self.skillgs.rect[3] += -10
        if self.skillgs.rect[3] < -500:
            self.skillgs.alive = False
            self.skillgs.rect[3] = 0

    def soco(self):
        if self.skillsoco.alive:
            self.skillsoco.draw()
            if not self.skillsoco.rect[2] < -500:
                self.skillsoco.rect[2] += -10
            self.skillsoco.count += 1
            if self.skillsoco.count > 80:
                self.skillsoco.alive = False
                self.skillsoco.count = 0
                self.skillsoco.rect[2] = 0

    def onda(self):
        if self.skillonda.alive:
            self.skillonda.draw()
            self.skillonda.rect[2] += -5
            self.skillonda.rect[1] += 3
            if self.skillonda.rect[2] < -800:
                self.skillonda.alive = False
                self.skillonda.rect[2] = 0
                self.skillonda.rect[1] = 300

    def bolhas(self, posp):
        (xp, yp) = posp
        cad = int(self.rect[0] - xp)
        cop = int(yp - self.rect[1])
        h = ((cad ** 2) + (cop ** 2)) ** 0.5
        #pygame.draw.line(self.scr, (255, 255, 0), (750, 300), (750 - cad, 300 + cop), 5)

        if len(self.tiros) < 10 and self.count % 20 == 0:
            self.tiros.append(Circulo(scr, (50, 50, 255), (750, 300), 20))

        #bolhasdrawandupdate
        for tiro in self.tiros:
            tiro.draw()
            (x, y) = tiro.pos
            x += -(h / 150)
            y += tiro.vely
            tiro.vely += 0.2
            tiro.pos = (x, y)



class Retangulo(object):
    def __init__(self, scr, color, rect):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.width = 0
        self.alive = False
        self.count = 0

    def draw(self):
        pygame.draw.rect(self.scr, self.color, self.rect, self.width)


class Circulo(object):
    def __init__(self, scr, color, pos, raio):
        self.scr = scr
        self.color = color
        self.pos = pos
        self.raio = raio
        self.width = 0
        self.alive = False
        self.count = 0
        self.vely = -10

    def draw(self):
        self.scr.blit(bolha, self.pos)


cenario = Cenario()

def gameloop():
    run = True
    while run:
        clock.tick(120)
        scr.fill((255, 255, 255))

        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_p:
                    exit()
                elif e.key == K_g:
                    cenario.boss.skillgs.rect[0] = cenario.p1.rect[0]
                    cenario.boss.skillgs.alive = True
                elif e.key == K_s:
                    cenario.boss.skillsoco.rect[0] = cenario.boss.rect[0]
                    cenario.boss.skillsoco.rect[1] = cenario.p1.rect[1]
                    cenario.boss.skillsoco.alive = True
                elif e.key == K_o:
                    cenario.boss.skillonda.rect[0] = cenario.boss.rect[0]
                    cenario.boss.skillonda.alive = True
                elif e.key == K_b:
                    cenario.boss.tiros = []
                elif e.key == K_ESCAPE:
                    from main import gameintro
                    gameintro()
                ply.ekeydown(e, cenario)
            elif e.type == KEYUP:
                ply.ekeyup(e, cenario)
        cenario.update()
        pygame.display.update()
