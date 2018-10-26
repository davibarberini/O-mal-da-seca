import pygame
from pygame.locals import KEYUP, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_f, FULLSCREEN

pygame.init()
# Variaveis tela e Sprite do Personagem
W = 1024
H = 768
W2 =  W/2 -30
H2 = H/6

tela = pygame.display.set_mode((W, H))

lasso = [pygame.image.load("wry.png"),pygame.image.load("wry2.png"),pygame.image.load("wry3.png")]
#fundo = pygame.image.load("Fundo2.png")
#TOKIWO TOMARE
ZW = [pygame.image.load("Fundo2.png"),pygame.image.load("ZW1.png"),pygame.image.load("ZW2.png"),pygame.image.load("ZW3.png"),pygame.image.load("ZW4.png"),pygame.image.load("ZW5.png")
      ,pygame.image.load("ZW4.png"),pygame.image.load("ZW3.png"),pygame.image.load("ZW2.png"),pygame.image.load("ZW1.png")]
pygame.mixer.music.load ('OMUNDO.mp3')
# velocidade do Botlasso
speedx = -5
speedy = -3.5

count=0
transac=0

pygame.display.set_caption("teste")

start = True

dio = 0
wry = 0
timestop = True
def timetostop():
    global wry

    global dio
    global timestop

    if timestop == True:
        tela.blit(ZW[dio], (0,0))
        tela.blit(lasso[wry], (W2, H2))
        dio+=1
        if dio == 1:
            pygame.mixer.music.play(0)
        if dio == 2:
            wry = 1
        if dio == 5:
            wry = 2
        if dio >= 10:
            dio = 0

            timestop = False
        #ocorre a animação,---Fazer codigo para setar a velocidade do jogador pra 0 e criar projeteis












while start:
    # botlasso
    tela.blit(lasso[wry], (W2, H2))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_f:
                exit()

    H2 += speedy
    if H2 <=-100:
        count +=1
    if count>100:
        speedy = 0

        W2 = 480
        H2 = 50
        timetostop()

        pygame.display.update()

    pygame.display.update()
    tela.blit(ZW[0], (0, 0))



