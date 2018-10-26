import pygame
import fabiano as ply
from pygame.locals import KEYUP,KEYDOWN,K_LEFT,K_RIGHT,K_UP,K_DOWN,K_f,FULLSCREEN, K_ESCAPE

pygame.init()
#Variaveis tela e Sprite do Personagem
W = 1024
H = 768
W2 =  500
H2 = 500

tela = pygame.display.set_mode ((W,H),FULLSCREEN)


#velocidade do Botlasso
speedx =0.00
speedy =5


pygame.display.set_caption ("teste")

start = True
count = 0
voando = True


def botlasso():
    global count
    global voando
    if count + 1 >= 120:
        count = 0
    if voando:
        tela.blit(lasso[count], (W2, H2))
        count +=1
        if count >=5:
            count = 0


def gameloop():
    global H, H2, W, W2
    global speedx, speedy
    global lasso
    lasso = [pygame.image.load("assets/botlasso/Anm1.png").convert_alpha(), pygame.image.load("assets/botlasso/Anm2.png").convert_alpha(),
             pygame.image.load("assets/botlasso/Anm3.png").convert_alpha(), pygame.image.load("assets/botlasso/Anm4.png").convert_alpha(),
             pygame.image.load("assets/botlasso/Anm5.png").convert_alpha()]
    p1 = ply.Player(tela, (0, 0, 255), [H - (W - 50), H - 130, 60, 120], 5, "assets/hantiseca/fabiano.png")
    while start:
        pygame.time.delay(50)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == KEYDOWN:
                if e.key == K_f:
                    exit()
                elif e.key == K_ESCAPE:
                    from main import gameintro
                    gameintro()

        W2 += speedx
        H2 += speedy

        if H2 <= 100:
            speedy = 10
        elif H2 >= 500:
            speedy = -10

        pygame.display.update()

        tela.fill((0, 0, 0))
        p1.update()
        p1.draw()
        botlasso()


