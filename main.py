import pygame
#from moviepy.editor import VideoFileClip
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

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=256)

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

def collidelanguage( obj, mouse, objrender):
    objrect = objrender.get_rect()
    if obj["x"] + objrect.w > mouse[0] > obj["x"] and obj["y"] + objrect.h > mouse[1] > obj["y"]:
        obj["scale"] = (120, 120)
        obj["mcolide"] = True
    else:
        obj["scale"] = (100, 100)
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
    pygame.mixer.music.load("assets/musics/intro.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

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
        lehwaimgreal = pygame.image.load("assets/intro/lehwaicondead.png").convert_alpha()
    lehwaimg = pygame.transform.scale(lehwaimgreal, (140, 140))
    if not mortes[3]:
        mckurtimgreal = pygame.image.load("assets/intro/mckurticon.png").convert()
    else:
        mckurtimgreal = pygame.image.load("assets/intro/mckurticondead.png").convert()

    imgseta = pygame.image.load("assets/intro/setacima.png").convert_alpha()
    imgsetalingua = pygame.image.load("assets/intro/botaoirlinguagem.png").convert_alpha()
    mckurtimg = pygame.transform.scale(mckurtimgreal, (140, 140))
    hantiseca = {"texto": "Hantiseca", "x": 130, "y": 150, "cor": (0, 0, 0),"correct": (255, 255, 0) ,"mcolide": False}
    lehwa = {"texto": "Lehwa", "x": 430, "y": 150, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    botlasso = {"texto": "Botlasso", "x": 730, "y": 150, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    mckurt = {"texto": "McKurt", "x": 430, "y": 400, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    start = {"texto": "Start Game", "x": 0, "y": 470, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    startrender = arial.render(start["texto"], True, start["cor"])
    ingles = {"Nome": "Voltar", "x": 860, "y": 360, "w": 100, "h": 70, "scale": (100, 100)}
    inglesimgreal = pygame.image.load("assets/intro/inglesicon.png").convert_alpha()
    portugues = {"Nome": "Voltar", "x": 860, "y": 510, "w": 100, "h": 70, "scale": (100, 100)}
    portuguesimgreal = pygame.image.load("assets/intro/brasilicon.png").convert_alpha()
    hantisecarect = hantisecaimg.get_rect()
    botlassorect = botlassoimg.get_rect()
    lehwarect = lehwaimg.get_rect()
    mckurtrect = mckurtimg.get_rect()
    startrect = startrender.get_rect()
    tuto = pygame.image.load("assets/intro/tutorial.png").convert_alpha()
    tutorect = tuto.get_rect()
    tutodict = {"x": 0, "y": 600, "w": tutorect.w, "h": tutorect.h}
    posseta = (170, 300)
    if death.linguagem == "eng":
        posir = (800, 400)
    else:
        posir = (800, 550)
    run = True
    while run:
        inglesimg = pygame.transform.scale(inglesimgreal, ingles["scale"])
        portuguesimg = pygame.transform.scale(portuguesimgreal, portugues["scale"])
        imgchoose = pygame.image.load("assets/intro/bosschoose" + death.linguagem + ".png").convert_alpha()
        sair = pygame.image.load("assets/intro/sair" + death.linguagem + ".png").convert_alpha()
        mouse = pygame.mouse.get_pos()
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
                    canmckurt = True
                    mortes[0] = True
                    mortes[1] = True
                    mortes[2] = True
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    sairrect = sair.get_rect()
                    sairdict = {"x": 850, "y": 680, "w": sairrect.w, "h": sairrect.h}
                    if hantiseca["mcolide"] == True:
                        bossselected = "Hantiseca"
                        posseta = (170, 300)
                    elif lehwa["mcolide"] == True:
                        bossselected = "Lehwa"
                        posseta = (470, 300)
                    elif botlasso["mcolide"] == True:
                        bossselected = "Botlasso"
                        posseta = (770, 300)
                    elif mckurt["mcolide"] == True:
                        if canmckurt:
                            bossselected = "McKurt"
                            posseta = (470, 550)
                    elif start["mcolide"] == True:
                        try:
                            if bossselected == "Hantiseca":
                                img = pygame.image.load("assets/hantiseca/lore" + death.linguagem + ".png").convert()
                                death.transition(scr, img)
                                lores(bossselected)
                                hanti.gameloop(scr, scrx, scry)
                            elif bossselected == "Lehwa":
                                img = pygame.image.load("assets/baleia/lore" + death.linguagem + ".png").convert()
                                death.transition(scr, img)
                                lores(bossselected)
                                lloop.gameloop()
                            elif bossselected == "Botlasso":
                                img = pygame.image.load("assets/botlasso/lore" + death.linguagem + ".png").convert()
                                death.transition(scr, img)
                                lores(bossselected)
                                bloop.gameloop(scr, scrx, scry)
                            elif bossselected == "McKurt":
                                img = pygame.image.load("assets/mckurt/lore" + death.linguagem + ".png").convert()
                                death.transition(scr, img)
                                lores(bossselected)
                                mkloop.gameloop(scr, scrx, scry)
                                run = False
                        except NameError:
                            print("Não selecionou o boss")
                    elif mousecolide(ingles, mouse):
                        death.linguagem = "eng"
                        posir = (800, 400)
                    elif mousecolide(portugues, mouse):
                        death.linguagem = ""
                        posir = (800, 550)
                    elif mousecolide(tutodict, mouse):
                        tutorial(scr)
                    elif mousecolide(sairdict, mouse):
                        exit()



        scr.blit(fundo, (0, 0))
        scr.blit(imgchoose, (385, 50))
        scr.blit(tuto, (tutodict["x"], tutodict["y"]))
        scr.blit(sair, (850, 680))
        scr.blit(imgseta, posseta)
        scr.blit(imgsetalingua, posir)
        scr.blit(inglesimg, (ingles["x"], ingles["y"]))
        scr.blit(portuguesimg, (portugues["x"], portugues["y"]))
        collidelanguage(ingles, mouse, inglesimg)
        collidelanguage(portugues, mouse, portuguesimg)


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
    from fabiano import Player as ply
    from fabiano import eventostuto

    p1 = ply(scr, (0, 0, 255), [scrx - (scrx - 50), scry - 330, 60, 120], 5)
    p1.tutorial = True

    fundo = pygame.image.load("assets/intro/tuto" + death.linguagem + ".png").convert()

    voltar = {"Nome": "Voltar", "x": 10, "y": 10, "w": 100, "h": 90}

    run = True
    while run:
        clock.tick(120)

        #draw
        scr.blit(fundo, (0, 0))
        p1.draw()

        #update
        p1.update()

        #eventos
        eventostuto(scr, p1, voltar)

        pygame.display.update()


def lores(bosschosed):
    if bosschosed == "Lehwa":
        bosschosed = "baleia"
    elif bosschosed == "Hantiseca":
        bosschosed = "hantiseca"
    elif bosschosed == "McKurt":
        bosschosed = "mckurt"
    elif bosschosed == "Botlasso":
        bosschosed = "botlasso"

    fundo = pygame.image.load("assets/" + bosschosed +"/lore" + death.linguagem + ".png").convert()
    pygame.mixer.music.load("assets/musics/" + bosschosed + ".mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    ir = {"Nome": "Voltar", "x": 800, "y": 30, "w": 100, "h": 90}
    irimg = pygame.image.load("assets/intro/botaoir.png").convert_alpha()

    voltar = {"Nome": "Voltar", "x": 50, "y": 30, "w": 100, "h": 90}
    voltarimg = pygame.image.load("assets/intro/botaovoltar.png").convert_alpha()

    run = True
    while run:
        clock.tick(60)

        # draw
        scr.blit(fundo, (0, 0))
        scr.blit(irimg, (800, 30))
        scr.blit(voltarimg, (50, 30) )

        # update
        mouse = pygame.mouse.get_pos()

        # eventos
        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if mousecolide(ir, mouse):
                        run = False
                    elif mousecolide(voltar, mouse):
                        img = pygame.image.load("assets/intro/introfundo.png").convert_alpha()
                        death.transition(scr, img)
                        bossselect()
                        run = False


        pygame.display.update()

#pygame.display.set_mode((scrx, scry), 0, 32)
bossselect()

