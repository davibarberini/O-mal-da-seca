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
        self.botlasso = Boss(0.00, 0, 500, 500, True)
        self.p1 = ply.Player(tela, (0, 0, 255), [W - (W - 50), H - 130, 60, 120], 5, "assets/hantiseca/fabiano.png")
        self.count = 0

    def update(self):
        self.botlasso.W += self.botlasso.speedx
        self.botlasso.H += self.botlasso.speedy
        if self.botlasso.H <= 100:
            self.botlasso.speedy = 2
        elif self.botlasso.H >= 500:
            self.botlasso.speedy = -2

        self.p1.update()
        self.draw()

    def draw(self):
        self.p1.draw()
        if self.count + 1 >= 120:
            self.count = 0
        if self.botlasso.voando:
            tela.blit(self.botlasso.lasso[self.count // 8], (self.botlasso.W, self.botlasso.H))
            self.count += 1
            if self.count >= 40:
                self.count = 0


class Boss(object):
    def __init__(self, speedx, speedy, W, H, voando):
        self.lasso = [pygame.image.load("assets/botlasso/Anm1.png").convert_alpha(), pygame.image.load("assets/botlasso/Anm2.png").convert_alpha(),
             pygame.image.load("assets/botlasso/Anm3.png").convert_alpha(), pygame.image.load("assets/botlasso/Anm4.png").convert_alpha(),
             pygame.image.load("assets/botlasso/Anm5.png").convert_alpha()]
        self.speedx = speedx
        self.speedy = speedy
        self.W = W
        self.H = H
        self.voando = voando



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


