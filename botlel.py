import pygame
import fabiano as ply
from pygame.locals import KEYUP,KEYDOWN,K_LEFT,K_RIGHT,K_UP,K_DOWN,K_f,FULLSCREEN, K_ESCAPE

pygame.init()

#Variaveis tela e Sprite do Personagem
W = 1024
H = 768

clock = pygame.time.Clock()

tela = pygame.display.set_mode ((W,H),FULLSCREEN)



pygame.display.set_caption ("teste")

class Cenario(object):
    def __init__(self):
        self.botlasso = Boss(tela, [780, 0, 150, 170], 0.00, 0, True)
        self.p1 = ply.Player(tela, (0, 0, 255), [W - (W - 50), H - 330, 60, 120], 5, "assets/hantiseca/fabiano.png")
        self.count = 0
        self.botlassocount = 0
        self.fundo = pygame.image.load("assets/botlasso/botlassofundo.png").convert_alpha()

    def update(self):
        tela.blit(self.fundo, (0, 0))
        self.botlasso.draw()
        self.botlasso.update()
        if self.botlassocount > 900:
            if self.botlasso.skill == 1:
                self.botlasso.skill = 0
                self.botlasso.rect[0] = 780
                self.botlasso.rect[1] = 0
                self.botlasso.speedx = 2
                self.botlassocount = 0
            elif self.botlasso.skill == 0:
                self.botlasso.rect[0] = 780
                self.botlasso.rect[1] = 100
                self.botlasso.skill = 1
                self.botlassocount = 0
        if self.botlasso.skill == 0:
            self.botlasso.rect[1] += self.botlasso.speedy
            if self.botlasso.rect[1] <= 100:
                self.botlasso.speedy = 2
            elif self.botlasso.rect[1] >= 500:
                self.botlasso.speedy = -2
        elif self.botlasso.skill == 1:
                self.botlasso.rect[0] += self.botlasso.speedx
                if self.botlasso.rect[0] < 100:
                    self.botlasso.speedx = 2
                elif self.botlasso.rect[0] > 700:
                    self.botlasso.speedx = -2

        self.botlassocount += 1
        self.p1.update()
        self.draw()

    def draw(self):
        self.p1.draw()
        if self.botlasso.voando:
            if self.botlasso.skill == 0:
                tela.blit(self.botlasso.lasso[self.count // 8], (self.botlasso.rect[0], self.botlasso.rect[1]))
                self.count += 1
                if self.count >= 40:
                    self.count = 0
            elif self.botlasso.skill == 1:
                tela.blit(self.botlasso.fly[self.count // 8], (self.botlasso.rect[0], self.botlasso.rect[1]))
                self.count += 1
                if self.count >= 40:
                    self.count = 0

class Boss(object):
    def __init__(self, scr, rect, speedx, speedy, voando):
        self.lasso = [pygame.image.load("assets/botlasso/Anm1.png").convert_alpha(),
                      pygame.image.load("assets/botlasso/Anm2.png").convert_alpha(),
                      pygame.image.load("assets/botlasso/Anm3.png").convert_alpha(),
                      pygame.image.load("assets/botlasso/Anm4.png").convert_alpha(),
                      pygame.image.load("assets/botlasso/Anm5.png").convert_alpha()]

        self.fly =   [pygame.image.load("assets/botlasso/Fly1.png").convert_alpha(),
                      pygame.image.load("assets/botlasso/Fly2.png").convert_alpha(),
                      pygame.image.load("assets/botlasso/Fly3.png").convert_alpha(),
                      pygame.image.load("assets/botlasso/Fly4.png").convert_alpha(),
                      pygame.image.load("assets/botlasso/Fly5.png").convert_alpha()]
        self.rect = rect
        self.speedx = speedx
        self.speedy = speedy
        self.voando = voando
        self.scr = scr
        self.skill = 0
        self.tiros = []
        self.tiros2 = []
        self.counttiro = 0

    def update(self):
        if len(self.tiros) == 3:
            self.tiros[0].draw()
            self.tiros[0].rect[0] += -4
            self.tiros[0].rect[1] += -2
            self.tiros[1].rect[0] += -4
            self.tiros[1].draw()
            self.tiros[2].rect[0] += -4
            self.tiros[2].rect[1] += 2
            self.tiros[2].draw()
        for tiro in self.tiros:
            if tiro.rect[0] < 0:
                self.tiros.remove(tiro)
        for tiro in self.tiros2:
            tiro.draw()
            tiro.rect[1] += 5
            if tiro.rect[1] > 800:
                self.tiros2.remove(tiro)
        self.shoot()

    def draw(self):
        None
        #pygame.draw.rect(self.scr, (255, 255, 0), self.rect, 0)

    def shoot(self):
        if self.skill == 0:
            if 300  < self.rect[1] < 400:
                if len(self.tiros) < 3:
                    self.tiros.append(Projetil(self.scr, [self.rect[0], self.rect[1], 100, 50], (255, 255, 0), "assets/botlasso/tiro.png"))
                    self.tiros.append(Projetil(self.scr, [self.rect[0], self.rect[1], 100, 50], (0, 255, 0), "assets/botlasso/tiro.png"))
                    self.tiros.append(Projetil(self.scr, [self.rect[0], self.rect[1], 100, 50], (255, 0, 0), "assets/botlasso/tiro.png"))
        else:
            if len(self.tiros2) < 3 and self.counttiro > 40:
                self.tiros2.append(Projetil(self.scr, [self.rect[0], self.rect[1], 50, 100], (255, 255, 0),"assets/botlasso/tiro2.png"))
                self.counttiro = 0
            self.counttiro += 1


class Projetil(object):
    def __init__(self, scr, rect, color, image):
        self.scr = scr
        self.rect = rect
        self.color = color
        self.image = pygame.image.load(image).convert_alpha()

    def draw(self):
        #pygame.draw.rect(self.scr, self.color, self.rect, 0)
        self.scr.blit(self.image, (self.rect[0], self.rect[1]))


def gameloop():
    start = True
    cenario = Cenario()
    while start:
        tela.fill((0, 0, 0))
        clock.tick(120)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == KEYDOWN:
                if e.key == K_f:
                    exit()
                elif e.key == K_ESCAPE:
                    from main import gameintro
                    gameintro()
                ply.ekeydown(e, cenario)
            elif e.type == KEYUP:
                ply.ekeyup(e, cenario)

        cenario.update()
        pygame.display.update()


