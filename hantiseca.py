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
        self.count = 0
        self.skill = 1

    def update(self):
        #scr.blit(self.fundo, (0, 0))
        self.draw()
        self.collisions()
        self.boss.update()
        self.p1.update()
        if self.count > 200:
            if self.skill == 1:
                self.boss.skillgs.rect[0] = self.p1.rect[0]
                self.boss.skillgs.alive = True
                self.skill += 1
                self.count = 0
            elif self.skill == 2:
                self.boss.skillsoco.rect[0] = self.boss.rect[0]
                self.boss.skillsoco.rect[1] = self.p1.rect[1]
                self.boss.skillsoco.alive = True
                self.skill += 1
                self.count = 0
            elif self.skill == 3:
                self.boss.skillonda.rect[0] = self.boss.rect[0]
                self.boss.skillonda.alive = True
                self.skill += 1
                self.count = 0
            elif self.skill == 4:
                self.boss.tiros = []
                self.skill += 1
                self.count = 0
            elif self.skill == 5:
                print("chegou aqui")
                self.boss.vulnerable = True
                print(self.count)
                if self.count > 600:
                    self.skill += 1
                    self.boss.vulnerable = False
                    self.count = 0
            if self.skill > 5:
                self.skill = 1
                self.boss.vulnerable = False

        self.count += 1


    def collisions(self):
        p1Rect = pygame.Rect(self.p1.rect)
        if self.boss.skillgs.alive:
            skillRect = pygame.Rect(self.boss.skillgs.rect)
            if self.p1.vulnerable:
                if p1Rect.colliderect(skillRect):
                    self.p1.vulnerable = False
                    self.p1.vida -= 10
            if p1Rect.colliderect(skillRect):
                if self.p1.rect[1] + self.p1.rect[3] > self.boss.skillgs.rect[1]:
                    self.p1.vely = -6
            if self.p1.rect[1] < 0:
                self.p1.rect[1] = 0
        elif self.boss.skillsoco.alive:
            skillRect = pygame.Rect(self.boss.skillsoco.rect)
            if self.p1.vulnerable:
                if p1Rect.colliderect(skillRect):
                    self.p1.vulnerable = False
                    self.p1.vida -= 10
            if p1Rect.colliderect(skillRect):
                if self.p1.rect[0] + self.p1.rect[2] > self.boss.skillsoco.rect[0]:
                    self.p1.rect[0] = self.boss.skillsoco.rect[0] - self.p1.rect[2]
            if self.p1.rect[0] < 0:
                self.p1.rect[0] = 0
        elif self.boss.skillonda.alive:
            skillRect = pygame.Rect(self.boss.skillonda.rect)
            if self.p1.vulnerable:
                if p1Rect.colliderect(skillRect):
                    self.p1.vulnerable = False
                    self.p1.vida -= 10
            if p1Rect.colliderect(skillRect):
                if self.p1.rect[0] > self.boss.skillonda.rect[0] and self.p1.rect[1] >= self.boss.skillonda.rect[1]:
                    self.p1.rect[0] = self.boss.skillonda.rect[0]
                    self.slow = 2
            if self.p1.rect[0] < 0:
                self.p1.rect[0] = 0
        elif len(self.boss.tiros) > 0:
            if self.p1.vulnerable:
                for tiro in self.boss.tiros:
                    (x, y) = tiro.pos
                    tiroRect = pygame.Rect([x - 20, y - 20, 40, 40])
                    if p1Rect.colliderect(tiroRect):
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
        if self.boss.vulnerable:
            bossRect = pygame.Rect(self.boss.rect)
            if self.p1.atacando:
                if p1Rect.colliderect(bossRect):
                    self.boss.vida -= 10
                    self.boss.vulnerable = False
                    self.skill += 1
                    self.count = 0
            if self.p1.tiro.alive:
                p1tiroRect = pygame.Rect(self.p1.tiro.rect)
                if p1tiroRect.colliderect(bossRect):
                    self.boss.vida -= 10
                    self.boss.vulnerable = False
                    self.skill += 1
                    self.count = 0
        self.p1.damage()
        if self.boss.vulnerable:
            self.boss.color = (255, 255, 0)
        else:
            self.boss.color = (255, 0, 0)

    def draw(self):
        self.boss.draw()
        self.p1.draw()


class Boss(object):
    def __init__(self, scr, color, rect, image):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.width = 0
        self.vida = 100
        self.vulnerable = False
        self.image = pygame.image.load(image).convert_alpha()
        self.skillgs = Retangulo(self.scr, (50, 50, 255), [4000, scry, 100, 0])
        self.skillsoco = Retangulo(self.scr, (50, 50, 255), [4000, 0, 0, 100])
        self.skillonda = Retangulo(self.scr, (50, 50, 255), [4000, 100, 0, 800])
        self.tiros = [Circulo(scr, (50, 50, 255), (-500, -500), 20) for e in range (10)]
        self.count = 0

    def draw(self):
        pygame.draw.rect(self.scr, self.color, self.rect, self.width)
        self.scr.blit(self.image, (self.rect[0], self.rect[1]))
        pygame.draw.rect(self.scr, (0, 255, 0), [600, 0, self.vida, 50])

    def update(self):
        self.geiser()
        self.soco()
        self.onda()
        self.bolhas((cenario.p1.rect[0], cenario.p1.rect[1]))
        self.count += 1

    def geiser(self):
        if self.skillgs.alive:
            self.skillgs.draw()
            self.skillgs.rect[3] += 10
            self.skillgs.rect[1] += -10
        if self.skillgs.rect[1] < 200:
            self.skillgs.alive = False
            self.skillgs.rect[3] = 0
            self.skillgs.rect[1] = scry

    def soco(self):
        if self.skillsoco.alive:
            self.skillsoco.draw()
            if not self.skillsoco.rect[0] < 200:
                self.skillsoco.rect[2] += 10
                self.skillsoco.rect[0] += -10
            self.skillsoco.count += 1
            if self.skillsoco.count > 80:
                self.skillsoco.alive = False
                self.skillsoco.count = 0
                self.skillsoco.rect[2] = 0
                self.skillsoco.rect[0] = 4000

    def onda(self):
        if self.skillonda.alive:
            self.skillonda.draw()
            self.skillonda.rect[2] += 5
            self.skillonda.rect[0] += -5
            self.skillonda.rect[1] += 4
            if self.skillonda.rect[0] < -200:
                self.skillonda.alive = False
                self.skillonda.rect[2] = 0
                self.skillonda.rect[1] = 100
                self.skillonda.rect[0] = 4000

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