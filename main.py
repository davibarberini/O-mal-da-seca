import pygame
import hantiseca as hanti
import Baleia as lehwa
import botlel as botlasso
from pygame.locals import FULLSCREEN, QUIT, KEYDOWN, K_p, K_f, MOUSEBUTTONDOWN

pygame.init()

scrx = 1024
scry = 768

arial = pygame.font.SysFont("Arial", 64, True, False)

scr = pygame.display.set_mode((scrx, scry), 0, 32)

pygame.display.set_caption ("O mal por trás da seca")

clock = pygame.time.Clock()

def colliderect( obj, mouse, objrender):
    objrect = objrender.get_rect()
    if obj["x"] + objrect.w > mouse[0] > obj["x"] and obj["y"] + objrect.h > mouse[1] > obj["y"]:
        obj["correct"] = (255, 255, 255)
        obj["mcolide"] = True
    else:
        obj["correct"] = (255, 255, 0)
        obj["mcolide"] = False

def bossselect():
    global bossselected
    bossselected = "Hantiseca"

    botlassoimgreal = pygame.image.load("assets/intro/botlassoicon.jpg").convert()
    botlassoimg = pygame.transform.scale(botlassoimgreal, (140, 140))
    hantisecaimgreal = pygame.image.load("assets/intro/hantisecaicon.png").convert()
    hantisecaimg = pygame.transform.scale(hantisecaimgreal, (140, 140))
    lehwaimgreal = pygame.image.load("assets/intro/lehwaicon.png").convert_alpha()
    lehwaimg = pygame.transform.scale(lehwaimgreal, (140, 140))
    sdamareloimgreal = pygame.image.load("assets/intro/hantisecaicon.png").convert()
    sdamareloimg = pygame.transform.scale(sdamareloimgreal, (140, 140))
    hantiseca = {"texto": "Hantiseca", "x": 50, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) ,"mcolide": False}
    lehwa = {"texto": "Lehwa", "x": 400, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    botlasso = {"texto": "Botlasso", "x": 700, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    sdamarelo = {"texto": "Soldado-Amarelo", "x": 400, "y": 400, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    voltar = {"texto": "Voltar", "x": 0, "y": 600, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    voltarrender = arial.render(voltar["texto"], True, voltar["cor"])
    hantisecarect = hantisecaimg.get_rect()
    botlassorect = botlassoimg.get_rect()
    lehwarect = lehwaimg.get_rect()
    sdamarelorect = sdamareloimg.get_rect()
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
                    elif sdamarelo["mcolide"] == True:
                        bossselected = "Soldado-Amarelo"
                    elif voltar["mcolide"] == True:
                        run = False

        mouse = pygame.mouse.get_pos()

        scr.blit(fundo, (0, 0))
        selected = arial.render("Selecionado: " + bossselected, True, (255, 255, 0), (0, 0, 0))
        scr.blit(selected, (10, 300))

        pygame.draw.rect(scr, hantiseca["correct"], [hantiseca["x"] - 5, hantiseca["y"] - 5, hantisecarect.w + 10, hantisecarect.h + 10], 0)
        pygame.draw.rect(scr, lehwa["correct"], [lehwa["x"] - 5, lehwa["y"] - 5, lehwarect.w + 10, lehwarect.h + 10], 0)
        pygame.draw.rect(scr, botlasso["correct"], [botlasso["x"] - 5, botlasso["y"] - 5, botlassorect.w + 10, botlassorect.h + 10], 0)
        pygame.draw.rect(scr, sdamarelo["correct"], [sdamarelo["x"] - 5, sdamarelo["y"] - 5, sdamarelorect.w + 10, sdamarelorect.h + 10], 0)
        pygame.draw.rect(scr, voltar["correct"], [voltar["x"], voltar["y"], voltarrect.w, voltarrect.h], 0)
        scr.blit(hantisecaimg, (hantiseca["x"], hantiseca["y"]))
        scr.blit(lehwaimg, (lehwa["x"], lehwa["y"]))
        scr.blit(botlassoimg, (botlasso["x"], botlasso["y"]))
        scr.blit(sdamareloimg, (sdamarelo["x"], sdamarelo["y"]))
        scr.blit(voltarrender, (voltar["x"], voltar["y"]))

        colliderect(hantiseca, mouse, hantisecaimg)

        colliderect(lehwa, mouse, lehwaimg)

        colliderect(botlasso, mouse, botlassoimg)

        colliderect(sdamarelo, mouse, sdamareloimg)

        colliderect(voltar, mouse, voltarrender)


        clock.tick(60)
        pygame.display.update()

def gameintro():

    start = {"texto": "Start Game", "x": 350, "y": 200, "cor":(0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    boss = {"texto": "Choose Boss", "x": 350, "y": 400, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
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
                                hanti.gameloop(scr, scrx, scry)
                            elif bossselected == "Lehwa":
                                lehwa.gameloop()
                            elif bossselected == "Botlasso":
                                botlasso.gameloop(scr, scrx, scry)
                            intro = False
                        except NameError:
                            print("Não selecionou o boss")

                    elif boss["mcolide"] == True:
                        bossselect()

        startrender = arial.render(start["texto"], True, start["cor"], start["correct"])
        bossrender = arial.render(boss["texto"], True, boss["cor"], boss["correct"])

        mouse = pygame.mouse.get_pos()
        scr.blit(startrender, (start["x"], start["y"]))
        scr.blit(bossrender, (boss["x"], boss["y"]))

        colliderect(start, mouse, startrender)

        colliderect(boss, mouse, bossrender)

        clock.tick(60)
        pygame.display.update()



gameintro()
