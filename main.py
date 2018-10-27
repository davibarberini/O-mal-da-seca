import pygame
import hantiseca as hanti
import baleia as lehwa
import botlel as botlasso
from pygame.locals import FULLSCREEN, QUIT, KEYDOWN, K_p, K_f, MOUSEBUTTONDOWN

pygame.init()

scrx = 1024
scry = 768

scr = pygame.display.set_mode((scrx, scry), FULLSCREEN, 32)

clock = pygame.time.Clock()


def bossselect():
    global bossselected
    bossselected = "Hantiseca"

    botlassoimgreal = pygame.image.load("assets/intro/botlassoicon.jpg").convert()
    botlassoimg = pygame.transform.scale(botlassoimgreal, (140, 140))
    hantisecaimgreal = pygame.image.load("assets/intro/hantisecaicon.jpg").convert()
    hantisecaimg = pygame.transform.scale(hantisecaimgreal, (140, 140))
    lehwaimgreal = pygame.image.load("assets/intro/lehwaicon.png").convert_alpha()
    lehwaimg = pygame.transform.scale(lehwaimgreal, (140, 140))
    arial = pygame.font.SysFont("Arial", 64, True, False)
    hantiseca = {"texto": "Hantiseca", "x": 50, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) ,"mcolide": False}
    lehwa = {"texto": "Lehwa", "x": 400, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    botlasso = {"texto": "Botlasso", "x": 700, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    voltar = {"texto": "Voltar", "x": 0, "y": 600, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    voltarrender = arial.render(voltar["texto"], True, voltar["cor"])
    hantisecarect = hantisecaimg.get_rect()
    botlassorect = botlassoimg.get_rect()
    lehwarect = lehwaimg.get_rect()
    voltarrect = voltarrender.get_rect()
    run = True
    while run:
        scr.fill((0, 0, 0))
        fundo = pygame.image.load("assets/intro/" + bossselected + "fundo.png").convert()

        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_f:
                    exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if hantiseca["mcolide"] == True:
                        bossselected = "Hantiseca"
                    elif lehwa["mcolide"] == True:
                        bossselected = "Lehwa"
                    elif botlasso["mcolide"] == True:
                        bossselected = "Botlasso"
                    elif voltar["mcolide"] == True:
                        run = False
        mouse = pygame.mouse.get_pos()

        scr.blit(fundo, (0, 0))
        selected = arial.render("Selecionado: " + bossselected, True, (255, 255, 0))
        scr.blit(selected, (200, 300))

        pygame.draw.rect(scr, hantiseca["correct"], [hantiseca["x"] - 5, hantiseca["y"] - 5, hantisecarect.w + 10, hantisecarect.h + 10], 0)
        pygame.draw.rect(scr, lehwa["correct"], [lehwa["x"] - 5, lehwa["y"] - 5, lehwarect.w + 10, lehwarect.h + 10], 0)
        pygame.draw.rect(scr, botlasso["correct"], [botlasso["x"] - 5, botlasso["y"] - 5, botlassorect.w + 10, botlassorect.h + 10], 0)
        pygame.draw.rect(scr, voltar["correct"], [voltar["x"], voltar["y"], voltarrect.w, voltarrect.h], 0)
        scr.blit(hantisecaimg, (hantiseca["x"], hantiseca["y"]))
        scr.blit(lehwaimg, (lehwa["x"], lehwa["y"]))
        scr.blit(botlassoimg, (botlasso["x"], botlasso["y"]))
        scr.blit(voltarrender, (voltar["x"], voltar["y"]))

        if hantiseca["x"] - 5 + hantisecarect.w + 10 > mouse[0] > hantiseca["x"] - 5 and\
        hantiseca["y"] - 5 + hantisecarect.h + 10 > mouse[1] > hantiseca["y"] - 5:
            hantiseca["correct"] = (255, 255, 255)
            hantiseca["mcolide"] = True
        else:
            hantiseca["correct"] = (255, 255, 0)
            hantiseca["mcolide"] = False

        if lehwa["x"] - 5 + lehwarect.w + 10 > mouse[0] > lehwa["x"] - 5 and\
                lehwa["y"] - 5 + lehwarect.h + 10 > mouse[1] > lehwa["y"] - 5:
            lehwa["correct"] = (255, 255, 255)
            lehwa["mcolide"] = True
        else:
            lehwa["correct"] = (255, 255, 0)
            lehwa["mcolide"] = False

        if botlasso["x"] - 5 + botlassorect.w + 10 > mouse[0] > botlasso["x"] - 5 and\
                botlasso["y"] - 5 + botlassorect.h + 10 > mouse[1] > botlasso["y"] - 5:
            botlasso["correct"] = (255, 255, 255)
            botlasso["mcolide"] = True
        else:
            botlasso["correct"] = (255, 255, 0)
            botlasso["mcolide"] = False

        if voltar["x"] + voltarrect.w > mouse[0] > voltar["x"] and voltar["y"] + voltarrect.h > mouse[1] > voltar["y"]:
            voltar["correct"] = (255, 255, 255)
            voltar["mcolide"] = True
        else:
            voltar["correct"] = (255, 255, 0)
            voltar["mcolide"] = False


        clock.tick(60)
        pygame.display.update()

def gameintro():
    arial = pygame.font.SysFont("Arial", 64, True, False)
    start = {"texto": "Start Game", "x": 350, "y": 200, "cor":(0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    boss = {"texto": "Choose Boss", "x": 350, "y": 400, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    startrender = arial.render(start["texto"], True, start["cor"])
    bossrender = arial.render(boss["texto"], True, boss["cor"])
    startrect = startrender.get_rect()
    bossrect = bossrender.get_rect()
    intro = True
    while intro:
        scr.fill((0, 0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_p:
                    intro = False
                elif e.key == K_f:
                    exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if start["mcolide"] == True:
                        try:
                            if bossselected == "Hantiseca":
                                hanti.gameloop()
                            elif bossselected == "Lehwa":
                                lehwa.gameloop()
                            elif bossselected == "Botlasso":
                                botlasso.gameloop()
                            intro = False
                        except NameError:
                            None

                    elif boss["mcolide"] == True:
                        bossselect()

        mouse = pygame.mouse.get_pos()

        pygame.draw.rect(scr, start["correct"], [start["x"], start["y"],startrect.w, startrect.h], 0)
        pygame.draw.rect(scr, boss["correct"], [boss["x"], boss["y"], bossrect.w, bossrect.h], 0)
        scr.blit(startrender, (start["x"], start["y"]))
        scr.blit(bossrender, (boss["x"], boss["y"]))

        if start["x"] + startrect.w > mouse[0] > start["x"] and start["y"] + startrect.h > mouse[1] > start["y"]:
            start["correct"] = (255, 255, 255)
            start["mcolide"] = True
        else:
            start["correct"] = (255, 255, 0)
            start["mcolide"] = False
        if boss["x"] + bossrect.w > mouse[0] > boss["x"] and boss["y"] + bossrect.h > mouse[1] > boss["y"]:
            boss["correct"] = (255, 255, 255)
            boss["mcolide"] = True
        else:
            boss["correct"] = (255, 255, 0)
            boss["mcolide"] = False

        clock.tick(60)
        pygame.display.update()

gameintro()
