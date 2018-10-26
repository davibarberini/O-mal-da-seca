import pygame
from pygame.locals import KEYUP, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_f, FULLSCREEN

pygame.init()
# Variaveis tela e Sprite do Personagem
W = 1280
H = 720
W2 =  1000
H2 = 200

tela = pygame.display.set_mode((W, H), FULLSCREEN)

action = [pygame.image.load("Fly1.png").convert_alpha(),pygame.image.load("Fly2.png").convert_alpha(),pygame.image.load("Fly3.png").convert_alpha(),pygame.image.load("Fly4.png").convert_alpha()
    ,pygame.image.load("Fly5.png").convert_alpha()]

# velocidade do Botlasso
speedx = -10
speedy = -0.5


pygame.display.set_caption("teste")
count =0
start = True
voando = True

def fly():
    global count
    global voando
    if count + 1 >= 120:
        count = 0
    if voando:
        tela.blit(action[count], (W2, H2))
        count +=1
        if count >=5:
            count = 0

while start:
    pygame.time.delay(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_f:
                exit()

    W2 += speedx
    H2 += speedy

    if W2 == 640:
        speedy = -speedy
    if W2 > 1180:
        speedx = -speedx
        if speedy > 0:
            speedy = -speedy
        else:
            continue

    elif W2 < 200:
        speedx = -speedx
        if speedy > 0:
            speedy =- speedy
        else:
            continue


    pygame.display.update()

    tela.fill((0, 0, 0))
    fly()

