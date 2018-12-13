import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from fabiano import linguagem

pygame.init()

clock = pygame.time.Clock()

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=256)

def transition(scr, img):

    clock = pygame.time.Clock()

    alpha = 255
    fundo = pygame.Surface((1024, 768))
    fundo.fill((0, 0, 0))
    run = True
    while run:
        clock.tick(120)
        scr.blit(img, (0, 0))
        scr.blit(fundo, (0, 0))
        fundo.set_alpha(alpha)


        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
        alpha -= 3
        if alpha <= 0:
            run = False

        pygame.display.update()



def mousecolide(dict, mousepos):
    dictrect = pygame.Rect([dict["x"], dict["y"], dict["w"], dict["h"]])
    if dictrect.collidepoint(mousepos):
        return True
    else:
        return False


def calculascore(time, fabvida):
    #print(time, fabvida)
    pontos = 2000
    vida = fabvida / 100
    #print(vida)
    pontos -= time * 10
    #print(pontos)
    pontos *= vida
    #print(pontos)
    return int(pontos)



def score(scr, fundo, time, fabvida, bosspos):
    from fabiano import mortes, somascore

    som = pygame.mixer.Sound("assets/musics/vitoria.wav")
    som.play()

    fonte = pygame.font.SysFont("Swis721 Blk BT", 64, True, False)

    voltardict = {"Nome":"Voltar", "x": 30, "y": 600, "w": 390, "h": 100}


    pontos = calculascore(time, fabvida)
    somascore[bosspos] = pontos

    pontofundo = pygame.image.load("assets/intro/pontofundo" + linguagem + ".png").convert_alpha()
    vidarender = fonte.render(str(fabvida), True, (255 ,255 ,0))
    temporender = fonte.render(str(int(time)) + "s", True, (255, 255, 0))
    pontosrender = fonte.render(str(pontos), True, (255 ,255 ,0))

    run = True
    while run:
        clock.tick(60)


        #draw
        scr.blit(fundo, (0, 0))
        scr.blit(pontofundo, (0, 0))
        scr.blit(vidarender, (480, 295))
        scr.blit(temporender, (530, 390))
        scr.blit(pontosrender, (560, 490))



        #update
        mouse = pygame.mouse.get_pos()


        #eventos
        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if mousecolide(voltardict, mouse):
                        if mortes[0] == True and mortes[1] == True and mortes[2] == True:
                            pygame.mixer.music.stop()
                            img = pygame.image.load("assets/intro/fundopreto.png").convert()
                            transition(scr, img)
                            creditos(scr)
                        else:
                            pygame.mixer.music.stop()
                            img = pygame.image.load("assets/intro/introfundo.png").convert_alpha()
                            transition(scr, img)
                            import main
                            main.bossselect()
                            run = False

        pygame.display.update()



def mortefab(scr):
    pygame.mixer.music.load("assets/musics/death.mp3")
    pygame.mixer.music.play(-1)

    fundo = pygame.image.load("assets/intro/deathfundo" + linguagem + ".png").convert()

    simdict = {"Nome": "Voltar", "x": 160, "y": 630, "w": 210, "h": 90}
    naodict = {"Nome": "Voltar", "x": 650, "y": 630, "w": 210, "h": 90}

    run = True
    while run:
        clock.tick(60)

        #draw
        scr.blit(fundo, (0, 0))


        #update
        mouse = pygame.mouse.get_pos()

        # eventos
        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if mousecolide(simdict, mouse):
                        img = pygame.image.load("assets/intro/introfundo.png").convert_alpha()
                        transition(scr, img)
                        import main
                        main.bossselect()
                        run = False
                    elif mousecolide(naodict, mouse):
                        exit()

        pygame.display.update()



def creditos(scr):
    from fabiano import somascore

    scoresoma = 0
    for item in somascore:
        scoresoma += item

    fonte = pygame.font.SysFont("Swis721 Blk BT", 64, True, False)
    scoretotal = fonte.render(str(scoresoma), True, (255, 255, 0))

    pygame.mixer.music.load("assets/musics/death.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    fundo = pygame.image.load("assets/intro/creditos" + linguagem + ".png").convert()

    voltardict = {"Nome": "Voltar", "x": 0, "y": 600, "w": 210, "h": 90}
    voltarimg = pygame.image.load("assets/intro/botaovoltar.png").convert_alpha()
    scoreimg = pygame.image.load("assets/intro/pontosimg" + linguagem + ".png").convert_alpha()

    fundoy = 800
    imgscorey = 2900
    scorey = 2900

    run = True
    while run:
        clock.tick(60)
        scr.fill((0, 0, 0))

        # draw
        scr.blit(fundo, (0, fundoy))
        scr.blit(scoretotal, (600, scorey))
        scr.blit(scoreimg, (300, imgscorey))
        scr.blit(voltarimg, (0, 600))

        # update
        mouse = pygame.mouse.get_pos()

        # eventos
        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if mousecolide(voltardict, mouse):
                        pygame.mixer.music.stop()
                        img = pygame.image.load("assets/intro/introfundo.png").convert_alpha()
                        transition(scr, img)
                        import main
                        main.bossselect()
                        run = False

        fundoy -= 1
        if scorey > 200:
            imgscorey -= 1
            scorey -= 1
        pygame.display.update()