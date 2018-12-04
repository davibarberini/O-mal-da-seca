import pygame
from moviepy.editor import VideoFileClip
import hantiseca as hanti
import Baleia as lloop
import botlel as bloop
import mckurt as mkloop
import death
from pygame.locals import FULLSCREEN, QUIT, KEYDOWN, K_p, K_ESCAPE, MOUSEBUTTONDOWN, K_9
from fabiano import mortes, somascore, videoplayed

pygame.init()

scrx = 1024
scry = 768

arial = pygame.font.SysFont("Arial", 64, True, False)

scr = pygame.display.set_mode((scrx, scry), 0, 32)

pygame.display.set_caption ("O mal por trás da seca")

clock = pygame.time.Clock()

canmckurt = False

def colliderect( obj, mouse, objrender):
    objrect = objrender.get_rect()
    if obj["x"] + objrect.w > mouse[0] > obj["x"] and obj["y"] + objrect.h > mouse[1] > obj["y"]:
        obj["correct"] = (255, 255, 255)
        obj["mcolide"] = True
    else:
        obj["correct"] = (255, 255, 0)
        obj["mcolide"] = False

def mousecolide(dict, mousepos):
    dictrect = pygame.Rect([dict["x"], dict["y"], dict["w"], dict["h"]])
    if dictrect.collidepoint(mousepos):
        return True
    else:
        return False

def bossselect():
    global bossselected, canmckurt
    bossselected = "Hantiseca"

    if not mortes[2]:
        botlassoimgreal = pygame.image.load("assets/intro/botlassoicon.jpg").convert()
    else:
        botlassoimgreal = pygame.image.load("assets/intro/botlassoicondead.jpg").convert()
    botlassoimg = pygame.transform.scale(botlassoimgreal, (140, 140))
    if not mortes[0]:
        hantisecaimgreal = pygame.image.load("assets/intro/hantisecaicon.png").convert()
    else:
        hantisecaimgreal = pygame.image.load("assets/intro/hantisecaicondead.png").convert()
    hantisecaimg = pygame.transform.scale(hantisecaimgreal, (140, 140))
    if not mortes[1]:
        lehwaimgreal = pygame.image.load("assets/intro/lehwaicon.png").convert_alpha()
    else:
        lehwaimgreal = pygame.image.load("assets/intro/lehwaicon.png").convert_alpha()
    lehwaimg = pygame.transform.scale(lehwaimgreal, (140, 140))
    if not mortes[3]:
        mckurtimgreal = pygame.image.load("assets/intro/mckurticon.png").convert()
    else:
        mckurtimgreal = pygame.image.load("assets/intro/mckurticondead.png").convert()
    mckurtimg = pygame.transform.scale(mckurtimgreal, (140, 140))
    hantiseca = {"texto": "Hantiseca", "x": 50, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) ,"mcolide": False}
    lehwa = {"texto": "Lehwa", "x": 400, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    botlasso = {"texto": "Botlasso", "x": 700, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    mckurt = {"texto": "McKurt", "x": 400, "y": 400, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    start = {"texto": "Start Game", "x": 0, "y": 600, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    startrender = arial.render(start["texto"], True, start["cor"])
    hantisecarect = hantisecaimg.get_rect()
    botlassorect = botlassoimg.get_rect()
    lehwarect = lehwaimg.get_rect()
    mckurtrect = mckurtimg.get_rect()
    startrect = startrender.get_rect()
    run = True
    while run:
        scr.fill((0, 0, 0))
        fundo = pygame.image.load("assets/intro/" + bossselected + "fundo.png").convert()
        if mortes[0] and mortes[1] and mortes[2]:
            canmckurt = True

        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    exit()
                if e.key == K_9:
                    mortes[0] = True
                    mortes[1] = True
                    mortes[2] = True
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if hantiseca["mcolide"] == True:
                        bossselected = "Hantiseca"
                    elif lehwa["mcolide"] == True:
                        bossselected = "Lehwa"
                    elif botlasso["mcolide"] == True:
                        bossselected = "Botlasso"
                    elif mckurt["mcolide"] == True:
                        bossselected = "McKurt"
                    elif start["mcolide"] == True:
                        try:
                            if bossselected == "Hantiseca":
                                img = pygame.image.load("assets/hantiseca/lore.png").convert()
                                death.transition(scr, img)
                                lores(bossselected)
                                hanti.gameloop(scr, scrx, scry)
                            elif bossselected == "Lehwa":
                                img = pygame.image.load("assets/baleia/lore.png").convert()
                                death.transition(scr, img)
                                lores(bossselected)
                                lloop.gameloop()
                            elif bossselected == "Botlasso":
                                img = pygame.image.load("assets/botlasso/lore.png").convert()
                                death.transition(scr, img)
                                lores(bossselected)
                                bloop.gameloop(scr, scrx, scry)
                            if canmckurt:
                                if bossselected == "McKurt":
                                    img = pygame.image.load("assets/mckurt/lore.png").convert()
                                    death.transition(scr, img)
                                    lores(bossselected)
                                    mkloop.gameloop(scr, scrx, scry)
                                    run = False
                        except NameError:
                            print("Não selecionou o boss")

        mouse = pygame.mouse.get_pos()

        scr.blit(fundo, (0, 0))
        selected = arial.render("Selecionado: " + bossselected, True, (255, 255, 0), (0, 0, 0))
        scr.blit(selected, (10, 300))

        pygame.draw.rect(scr, hantiseca["correct"], [hantiseca["x"] - 5, hantiseca["y"] - 5, hantisecarect.w + 10, hantisecarect.h + 10], 0)
        pygame.draw.rect(scr, lehwa["correct"], [lehwa["x"] - 5, lehwa["y"] - 5, lehwarect.w + 10, lehwarect.h + 10], 0)
        pygame.draw.rect(scr, botlasso["correct"], [botlasso["x"] - 5, botlasso["y"] - 5, botlassorect.w + 10, botlassorect.h + 10], 0)
        if canmckurt:
            pygame.draw.rect(scr, mckurt["correct"], [mckurt["x"] - 5, mckurt["y"] - 5, mckurtrect.w + 10, mckurtrect.h + 10], 0)
        pygame.draw.rect(scr, start["correct"], [start["x"], start["y"], startrect.w, startrect.h], 0)
        scr.blit(hantisecaimg, (hantiseca["x"], hantiseca["y"]))
        scr.blit(lehwaimg, (lehwa["x"], lehwa["y"]))
        scr.blit(botlassoimg, (botlasso["x"], botlasso["y"]))
        if canmckurt:
            scr.blit(mckurtimg, (mckurt["x"], mckurt["y"]))
        scr.blit(startrender, (start["x"], start["y"]))

        colliderect(hantiseca, mouse, hantisecaimg)

        colliderect(lehwa, mouse, lehwaimg)

        colliderect(botlasso, mouse, botlassoimg)

        if canmckurt:
            colliderect(mckurt, mouse, mckurtimg)

        colliderect(start, mouse, startrender)


        clock.tick(60)
        pygame.display.update()


#def video():
    #clip = VideoFileClip('assets/intro/introvideo.mp4')
    #clip.preview()


def tutorial(scr):

    fundo = pygame.image.load("assets/intro/tutorial.png").convert()

    voltar = {"Nome": "Voltar", "x": 20, "y": 800, "w": 100, "h": 90}
    voltarimg = pygame.image.load("assets/intro/botaovoltar.png").convert_alpha()

    run = True
    while run:
        clock.tick(60)

        #draw
        scr.blit(fundo, (0, 0))
        scr.blit(voltarimg,(20, 800))


        #update
        mouse = pygame.mouse.get_pos()

        #eventos
        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if mousecolide(voltar, mouse):
                        exit()

        pygame.display.update()


def lores(bosschosed):
    if bosschosed == "Lehwa":
        bosschosed = "baleia"

    fundo = pygame.image.load("assets/" + bosschosed +"/lore.png").convert()

    voltar = {"Nome": "Voltar", "x": 800, "y": 30, "w": 100, "h": 90}
    voltarimg = pygame.image.load("assets/intro/botaoir.png").convert_alpha()

    run = True
    while run:
        clock.tick(60)

        # draw
        scr.blit(fundo, (0, 0))
        scr.blit(voltarimg, (800, 30))

        # update
        mouse = pygame.mouse.get_pos()

        # eventos
        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if mousecolide(voltar, mouse):
                        run = False

        pygame.display.update()

pygame.display.set_mode((scrx, scry), 0, 32)
bossselect()

