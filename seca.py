import pygame
from pygame.locals import FULLSCREEN, QUIT, KEYDOWN, K_g, K_UP, \
                         K_DOWN, K_LEFT, K_RIGHT, KEYUP, K_s, K_o, K_r, K_b, K_p, K_f, MOUSEBUTTONDOWN
pygame.init()

scrx = 1024
scry = 768

scr = pygame.display.set_mode((scrx, scry), 0, 32)

clock = pygame.time.Clock()

bolha = pygame.image.load("assets/hantiseca/bolha1.png").convert_alpha()


class Cenario(object):
    def __init__(self):
        self.boss = Boss(scr, (255, 0, 0), [scrx - 300, scry - 500, 250, 500], "assets/hantiseca/boss1.png")
        self.p1 = Player(scr, (0, 0, 255), [scrx - (scrx - 50), scry - 130, 60, 120], 5, "assets/hantiseca/fabiano.png")
        #self.fundo = pygame.image.load("assets/hantiseca/fundo.png").convert()

    def update(self):
        #scr.blit(self.fundo, (0, 0))
        self.draw()
        self.boss.update()
        self.p1.update()

    def draw(self):
        self.boss.draw()
        self.p1.draw()


class Player(object):
    def __init__(self, scr, color, rect ,vely, image):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.vely = vely
        self.velx = 0
        self.width = 0
        self.image = pygame.image.load(image).convert_alpha()
        self.alive = True
        self.pulo = 0

    def draw(self):
        if self.alive:
            #pygame.draw.rect(self.scr, self.color, self.rect, self.width)
            self.scr.blit(self.image, (self.rect[0], self.rect[1]))

    def update(self):
        if self.alive:
            if self.rect[1] + self.vely > 650:
                self.pulo = 0
                self.vely = 0
            if self.rect[0] + self.velx > 500:
                self.velx = 0
            if self.rect[0] + self.velx < 0:
                self.velx = 0
            self.rect[1] += self.vely
            self.vely += 0.15
            self.rect[0] += self.velx


class Boss(object):
    def __init__(self, scr, color, rect, image):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.width = 0
        self.image = pygame.image.load(image).convert_alpha()
        self.skillgs = Retangulo(self.scr, (50, 50, 255), [4000, scry, 100, 0])
        self.skillsoco = Retangulo(self.scr, (50, 50, 255), [4000, 0, 0, 100])
        self.skillonda = Retangulo(self.scr, (50, 50, 255), [4000, 300, 0, 500])
        self.tiros = []
        self.count = 0

    def draw(self):
        #pygame.draw.rect(self.scr, self.color, self.rect, self.width)
        self.scr.blit(self.image, (self.rect[0], self.rect[1]))

    def update(self):
        self.geiser()
        self.soco()
        self.onda()
        self.bolhas((cenario.p1.rect[0], cenario.p1.rect[1]))
        self.count += 1
    def geiser(self):
        if self.skillgs.alive:
            self.skillgs.draw()
            self.skillgs.rect[3] += -10
        if self.skillgs.rect[3] < -500:
            self.skillgs.alive = False
            self.skillgs.rect[3] = 0

    def soco(self):
        if self.skillsoco.alive:
            self.skillsoco.draw()
            if not self.skillsoco.rect[2] < -500:
                self.skillsoco.rect[2] += -10
            self.skillsoco.count += 1
            if self.skillsoco.count > 80:
                self.skillsoco.alive = False
                self.skillsoco.count = 0
                self.skillsoco.rect[2] = 0

    def onda(self):
        if self.skillonda.alive:
            self.skillonda.draw()
            self.skillonda.rect[2] += -5
            self.skillonda.rect[1] += 3
            if self.skillonda.rect[2] < -800:
                self.skillonda.alive = False
                self.skillonda.rect[2] = 0
                self.skillonda.rect[1] = 300

    def bolhas(self, posp):
        (xp, yp) = posp
        cad = int(self.rect[0] - xp)
        cop = int(yp - self.rect[1])
        h = ((cad ** 2) + (cop ** 2)) ** 0.5
        #pygame.draw.line(self.scr, (255, 255, 0), (750, 300), (750 - cad, 300 + cop), 5)

        if len(self.tiros) < 10 and self.count % 20 == 0:
            self.tiros.append(Circulo(scr, (50, 50, 255), (750, 300), 20))

        #bolhasdrawandupdate
        for tiro in self.tiros:
            tiro.draw()
            (x, y) = tiro.pos
            x += -(h / 150)
            y += tiro.vely
            tiro.vely += 0.2
            tiro.pos = (x, y)



class Retangulo(object):
    def __init__(self, scr, color, rect):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.width = 0
        self.alive = False
        self.count = 0

    def draw(self):
        pygame.draw.rect(self.scr, self.color, self.rect, self.width)


class Circulo(object):
    def __init__(self, scr, color, pos, raio):
        self.scr = scr
        self.color = color
        self.pos = pos
        self.raio = raio
        self.width = 0
        self.alive = False
        self.count = 0
        self.vely = -10

    def draw(self):
        self.scr.blit(bolha, self.pos)


cenario = Cenario()

def bossselect():
    global bossselected
    bossselected = "hantiseca"

    arial = pygame.font.SysFont("Arial", 64, True, False)
    hantiseca = {"texto": "Hantiseca", "x": 50, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) ,"mcolide": False}
    lehwa = {"texto": "Lehwa", "x": 400, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    botlasso = {"texto": "Botlasso", "x": 600, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) , "mcolide": False}
    voltar = {"texto": "Voltar", "x": 0, "y": 600, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    hantisecarender = arial.render(hantiseca["texto"], True, hantiseca["cor"])
    lehwarender = arial.render(lehwa["texto"], True, lehwa["cor"])
    botlassorender = arial.render(botlasso["texto"], True, botlasso["cor"])
    voltarrender = arial.render(voltar["texto"], True, voltar["cor"])
    hantisecarect = hantisecarender.get_rect()
    lehwarect = lehwarender.get_rect()
    botlassorect = botlassorender.get_rect()
    voltarrect = voltarrender.get_rect()
    run = True
    while run:
        scr.fill((0, 0, 0))

        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_f:
                    exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if hantiseca["mcolide"] == True:
                        bossselected = "hantiseca"
                    elif lehwa["mcolide"] == True:
                        bossselected = "lehwa"
                    elif botlasso["mcolide"] == True:
                        bossselected = "botlasso"
                    elif voltar["mcolide"] == True:
                        run = False
        mouse = pygame.mouse.get_pos()

        selected = arial.render("Selecionado: " + bossselected, True, (255, 255, 0))
        scr.blit(selected, (300, 300))

        pygame.draw.rect(scr, hantiseca["correct"], [hantiseca["x"], hantiseca["y"], hantisecarect.w, hantisecarect.h], 0)
        pygame.draw.rect(scr, lehwa["correct"], [lehwa["x"], lehwa["y"], lehwarect.w, lehwarect.h], 0)
        pygame.draw.rect(scr, botlasso["correct"], [botlasso["x"], botlasso["y"], botlassorect.w, botlassorect.h], 0)
        pygame.draw.rect(scr, voltar["correct"], [voltar["x"], voltar["y"], voltarrect.w, voltarrect.h], 0)
        scr.blit(hantisecarender, (hantiseca["x"], hantiseca["y"]))
        scr.blit(lehwarender, (lehwa["x"], lehwa["y"]))
        scr.blit(botlassorender, (botlasso["x"], botlasso["y"]))
        scr.blit(voltarrender, (voltar["x"], voltar["y"]))

        if hantiseca["x"] + hantisecarect.w > mouse[0] > hantiseca["x"] and\
        hantiseca["y"] + hantisecarect.h > mouse[1] > hantiseca["y"]:
            hantiseca["correct"] = (255, 255, 255)
            hantiseca["mcolide"] = True
        else:
            hantiseca["correct"] = (255, 255, 0)
            hantiseca["mcolide"] = False

        if lehwa["x"] + lehwarect.w > mouse[0] > lehwa["x"] and lehwa["y"] + lehwarect.h > mouse[1] > lehwa["y"]:
            lehwa["correct"] = (255, 255, 255)
            lehwa["mcolide"] = True
        else:
            lehwa["correct"] = (255, 255, 0)
            lehwa["mcolide"] = False

        if botlasso["x"] + botlassorect.w > mouse[0] > botlasso["x"] and botlasso["y"] + botlassorect.h > mouse[1] > botlasso["y"]:
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
                if e.key == K_f:
                    exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if start["mcolide"] == True:
                        intro = False
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


def gameloop():
    run = True
    while run:
        clock.tick(120)
        scr.fill((255, 255, 255))

        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            if e.type == KEYDOWN:
                if e.key == K_p:
                    exit()
                if e.key == K_g:
                    cenario.boss.skillgs.rect[0] = cenario.p1.rect[0]
                    cenario.boss.skillgs.alive = True
                if e.key == K_s:
                    cenario.boss.skillsoco.rect[0] = cenario.boss.rect[0]
                    cenario.boss.skillsoco.rect[1] = cenario.p1.rect[1]
                    cenario.boss.skillsoco.alive = True
                if e.key == K_o:
                    cenario.boss.skillonda.rect[0] = cenario.boss.rect[0]
                    cenario.boss.skillonda.alive = True
                if e.key == K_UP and cenario.p1.pulo <= 2:
                    cenario.p1.pulo += 1
                    cenario.p1.vely = -6
                if e.key == K_RIGHT:
                    cenario.p1.velx = 6
                if e.key == K_LEFT:
                    cenario.p1.velx = -6
                if e.key == K_r:
                    cenario.p1.vida = 100
                if e.key == K_b:
                    cenario.boss.tiros = []
            if e.type == KEYUP:
                if e.key == K_RIGHT and cenario.p1.velx > 0:
                    cenario.p1.velx = 0
                if e.key == K_LEFT and cenario.p1.velx < 0:
                    cenario.p1.velx = 0

        cenario.update()
        pygame.display.update()


gameintro()
gameloop()
