import pygame
from pygame.locals import K_UP, K_RIGHT, K_LEFT, K_r, K_x, K_z, K_c, K_f, K_ESCAPE,\
                            KEYDOWN, KEYUP, MOUSEBUTTONDOWN


mortes = [False, False, False, False]
somascore = [0, 0, 0, 0]
videoplayed = False

class Player(object):
    def __init__(self, scr, color, rect, vely):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.vely = vely
        self.velx = 0
        self.width = 0
        self.alive = True
        self.pulo = 0
        self.count = 0
        self.atacando = False
        self.tiro = Retangulo(scr, (0, 0, 255), [-500, 50, 20, 10], "assets/fabiano/bullet.png",
                              "assets/fabiano/bulletsound.wav")
        self.vida = 100
        self.vulnerable = True
        self.countvul = 0
        self.counttiro = 0
        self.slow = 1
        self.estado = 0
        self.imagetiroreal = pygame.image.load("assets/fabiano/projetilfire.png").convert_alpha()
        self.imagetiro = pygame.transform.scale(self.imagetiroreal, (17, 10))
        self.imagewalkingreal =[pygame.image.load("assets/fabiano/fab_walk1.png").convert_alpha(),
                    pygame.image.load("assets/fabiano/fab_walk2.png").convert_alpha(),
                    pygame.image.load("assets/fabiano/fab_walk3.png").convert_alpha(),
                    pygame.image.load("assets/fabiano/fab_walk4.png").convert_alpha()]

        self.imagewalking =[pygame.transform.scale(self.imagewalkingreal[0], (60, 120)),
                         pygame.transform.scale(self.imagewalkingreal[1], (60, 120)),
                         pygame.transform.scale(self.imagewalkingreal[2], (60, 120)),
                         pygame.transform.scale(self.imagewalkingreal[3], (60, 120))]

        self.imagereal = [pygame.image.load("assets/fabiano/fab_idle.png").convert_alpha(),
                     pygame.image.load("assets/fabiano/fab_jump.png").convert_alpha()]

        self.image = [pygame.transform.scale(self.imagereal[0], (60, 120)),
                      pygame.transform.scale(self.imagereal[1], (60, 120))]

        self.imageatacandoreal = [pygame.image.load("assets/fabiano/fab_melee1.png").convert_alpha(),
                                pygame.image.load("assets/fabiano/fab_melee2.png").convert_alpha()]

        self.imageatacando = [pygame.transform.scale(self.imageatacandoreal[0], (60, 120)),
                              pygame.transform.scale(self.imageatacandoreal[1], (60, 120))]

        #self.imgchutereal = pygame.image.load("assets/fabiano/fab_chute.png").convert_alpha()

        #self.imgchute = pygame.transform.scale(self.imgchutereal, (60, 120))

        self.sounds = [pygame.mixer.Sound("assets/fabiano/jumpsound.wav"),
                        pygame.mixer.Sound("assets/fabiano/damagesound.wav"),
                        pygame.mixer.Sound("assets/fabiano/slashsound.wav")]

        self.vidaimagem = pygame.image.load("assets/intro/vidacontorno.png").convert_alpha()
        self.slashimg = pygame.image.load("assets/fabiano/slash.png").convert_alpha()
        self.slashimg = pygame.transform.scale(self.slashimg, (120, 120))
        self.countwalk = 0
        self.spritepersec = 12
        self.countattack = 0
        self.spriteperattack = 20
        self.posslash = (0, 0)
        self.slashalive = False
        self.slashcount = 0
        self.paralisado = False
        self.tutorial = False

    def draw(self):
        if self.alive:
            fabpos = (self.rect[0], self.rect[1])
            #pygame.draw.rect(self.scr, self.color, self.rect, self.width)
            #self.scr.blit(self.image, (self.rect[0], self.rect[1]))
            self.tiro.draw()
            self.tiro.update(self.paralisado)
            # pygame.draw.rect(scr, fabiano["cor"], fabiano["rect"], 0)
            if self.estado == 0:
                self.scr.blit(self.image[0], fabpos)
            elif self.estado == 1:
                self.scr.blit(self.image[1], fabpos)
            elif self.estado == 2:
                self.scr.blit(self.imagewalking[self.countwalk // self.spritepersec], fabpos)
                self.countwalk += 1
                if self.countwalk >= self.spritepersec * 4:
                    self.countwalk = 0
            elif self.estado == 3:
                self.scr.blit(self.imageatacando[self.countattack // self.spriteperattack], fabpos)
                self.countattack += 1
                if self.countattack >= self.spriteperattack * 2:
                    self.countattack = 0
                #elif self.estado == 4:
                #self.scr.blit(self.imgchute, fabpos)
            if not self.tutorial:
                pygame.draw.rect(self.scr, (255 - self.vida * 2, self.vida * 2 , 0), [0, 0, self.vida * 3, 30], 0)
                self.scr.blit(self.vidaimagem, (0, 0))

            if self.counttiro < 60 and self.tiro.alive:
                self.scr.blit(self.imagetiro, (self.rect[0] + 60, self.rect[1] + 45))
            self.counttiro += 1
            if self.paralisado:
                if not self.estado == 1:
                    self.estado = 0

    def update(self):
        if self.alive:
            if self.vida < 0:
                self.vida = 0
            if self.rect[1] + self.vely > 570:
                self.pulo = 0
                self.vely = 0
                if self.estado == 1:
                    if self.velx == 0:
                        self.estado = 0
                    else:
                        self.estado = 2
            if self.rect[0] + self.velx > 1024 - self.rect[2]:
                self.estado = 0
                self.velx = 0
            if self.rect[0] + self.velx < 0:
                self.estado = 0
                self.velx = 0
            if not self.paralisado:
                self.rect[1] += self.vely
                self.vely += 0.20
                self.rect[0] += self.velx
            self.attack()
            if self.vida <= 0:
                pygame.mixer.stop()
                import death
                img = pygame.image.load("assets/intro/deathfundo.png").convert_alpha()
                death.transition(self.scr, img)
                death.mortefab(self.scr)
            self.slash()

    def attack(self):
        if self.atacando:
            self.estado = 3
            self.rect[2] = 100
            self.count += 1
            if self.count > 50:
                self.rect[2] = 60
                self.atacando = False
                self.count = 0
                if self.vely == 0:
                    if self.velx != 0:
                        self.estado = 2
                    else:
                        self.estado = 0
                else:
                    self.estado = 1

    def shoot(self):
        if not self.tiro.alive:
            self.counttiro = 0
            self.tiro.sound.play()
            self.tiro.rect[0] = self.rect[0] + 45
            self.tiro.rect[1] = self.rect[1] + 45
            self.tiro.candraw = True
            self.tiro.alive = True

    def dash(self):
        self.sounds[1].play()
        if self.velx > 0:
            self.rect[0] += 100
            if self.rect[0] + self.rect[2] > 1024:
                self.rect[0] = 1024 - self.rect[2]
        elif self.velx < 0:
            self.rect[0] += -100
            if self.rect[0] < 0:
                self.rect[0] = 0

    def damage(self):
        if not self.vulnerable:
            self.color = (255, 255, 0)
            if self.countvul > 80:
                self.vulnerable = True
                self.countvul = 0
                self.color = (0, 0, 255)
                self.slow = 1
            self.countvul += 1

    def slash(self):
        if self.slashalive:
            self.scr.blit(self.slashimg, self.posslash)
            self.slashcount += 1
            if self.slashcount > 100:
                self.slashalive = False
                self.slashcount = 0

class Retangulo(object):
    def __init__(self, scr, color, rect, image, sound):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.width = 0
        self.alive = False
        self.count = 0
        self.candraw = False
        self.image = pygame.image.load(image).convert_alpha()
        self.sound = pygame.mixer.Sound(sound)
        self.sound2 = pygame.mixer.Sound("assets/fabiano/reloadsound.wav")

    def draw(self):
        if self.candraw:
            #pygame.draw.rect(self.scr, self.color, self.rect, self.width)
            self.scr.blit(self.image, (self.rect[0], self.rect[1]))

    def update(self, paralisado):
        if self.alive:
            if not paralisado:
                self.count += 1
                self.rect[0] += 20
                if self.count == 50:
                    self.sound2.play()
                if self.count > 100:
                    self.rect[0] = -50
                    self.alive = False
                    self.count = 0


def eventos(scr, cenario):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_UP and cenario.p1.pulo <= 1:
                if not cenario.p1.paralisado:
                    cenario.p1.sounds[0].play()
                    cenario.p1.pulo += 1
                    cenario.p1.vely = -9
                    cenario.p1.estado = 1
            if e.key == K_RIGHT:
                if not cenario.p1.paralisado:
                    cenario.p1.velx = 6 // cenario.p1.slow
                    if not cenario.p1.estado == 1:
                        cenario.p1.estado = 2
            elif e.key == K_LEFT:
                if not cenario.p1.paralisado:
                    cenario.p1.velx = -6 // cenario.p1.slow
                    if not cenario.p1.estado == 1:
                        cenario.p1.estado = 2
            elif e.key == K_x:
                if not cenario.p1.atacando:
                    cenario.p1.sounds[2].play()
                if not cenario.p1.paralisado:
                    cenario.p1.countattack = 0
                    cenario.p1.atacando = True
            elif e.key == K_z:
                if not cenario.p1.paralisado:
                    cenario.p1.shoot()
            elif e.key == K_r:
                cenario.p1.vida = 100
            elif e.key == K_c:
                if not cenario.p1.paralisado:
                    cenario.p1.dash()
                    cenario.p1.estado = 1
            if e.key == K_f:
                exit()
            elif e.key == K_ESCAPE:
                pygame.mixer.stop()
                from death import transition
                img = pygame.image.load("assets/intro/introfundo.png").convert_alpha()
                transition(scr, img)
                from main import bossselect
                bossselect()
        elif e.type == KEYUP:
            if e.key == K_RIGHT and cenario.p1.velx > 0:
                cenario.p1.velx = 0
                if not cenario.p1.estado == 1:
                    cenario.p1.estado = 0
            elif e.key == K_LEFT and cenario.p1.velx < 0:
                cenario.p1.velx = 0
                if not cenario.p1.estado == 1:
                    cenario.p1.estado = 0

def mousecolide(dict, mousepos):
    dictrect = pygame.Rect([dict["x"], dict["y"], dict["w"], dict["h"]])
    if dictrect.collidepoint(mousepos):
        return True
    else:
        return False

def eventostuto(scr, p1, voltar):
    mouse = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_UP and p1.pulo <= 1:
                if not p1.paralisado:
                    p1.sounds[0].play()
                    p1.pulo += 1
                    p1.vely = -9
                    p1.estado = 1
            if e.key == K_RIGHT:
                if not p1.paralisado:
                    p1.velx = 6 // p1.slow
                    if not p1.estado == 1:
                        p1.estado = 2
            elif e.key == K_LEFT:
                if not p1.paralisado:
                    p1.velx = -6 // p1.slow
                    if not p1.estado == 1:
                        p1.estado = 2
            elif e.key == K_x:
                if not p1.atacando:
                    p1.sounds[2].play()
                if not p1.paralisado:
                    p1.countattack = 0
                    p1.atacando = True
            elif e.key == K_z:
                if not p1.paralisado:
                    p1.shoot()
            elif e.key == K_r:
                p1.vida = 100
            elif e.key == K_c:
                if not p1.paralisado:
                    p1.dash()
                    p1.estado = 1
            if e.key == K_f:
                exit()
            elif e.key == K_ESCAPE:
                p1.tutorial = False
                from death import transition
                img = pygame.image.load("assets/intro/introfundo.png").convert_alpha()
                transition(scr, img)
                from main import bossselect
                bossselect()
        elif e.type == KEYUP:
            if e.key == K_RIGHT and p1.velx > 0:
                p1.velx = 0
                if not p1.estado == 1:
                    p1.estado = 0
            elif e.key == K_LEFT and p1.velx < 0:
                p1.velx = 0
                if not p1.estado == 1:
                    p1.estado = 0
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if mousecolide(voltar, mouse):
                    p1.tutorial = False
                    from death import transition
                    img = pygame.image.load("assets/intro/introfundo.png").convert_alpha()
                    transition(scr, img)
                    from main import bossselect
                    bossselect()

