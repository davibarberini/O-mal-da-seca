def gameloop(tela, W, H):
    import pygame
    from fabiano import Player as ply
    from fabiano import eventos, mortes
    import time
    from random import randint

    pygame.init()

    clock = pygame.time.Clock()

    class Cenario(object):
        def __init__(self):
            self.botlasso = Boss(tela, [780, 0, 150, 170], 0.00, 0, True)
            self.p1 = ply(tela, (0, 0, 255), [W - (W - 50), H - 330, 60, 120], 5)
            self.count = 0
            self.botlassocount = 0
            self.fundo = pygame.image.load("assets/botlasso/botlassofundo.png").convert_alpha()
            self.fundozw = [pygame.image.load("assets/botlasso/ZW1.png").convert(),
                            pygame.image.load("assets/botlasso/ZW2.png").convert(),
                            pygame.image.load("assets/botlasso/ZW3.png").convert(),
                            pygame.image.load("assets/botlasso/ZW4.png").convert(),
                            pygame.image.load("assets/botlasso/ZW5.png").convert()]
            self.inicio = time.time()
            self.countfundo = 0
            self.sentidofundo = True
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=256)
            pygame.mixer.music.load("assets/musics/botlasso.mp3")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            self.zwsound = pygame.mixer.Sound("assets/botlasso/zwsound.wav")
            self.zwsound2 = pygame.mixer.Sound("assets/botlasso/zwsound2.wav")

        def update(self):
            if self.botlasso.skill == 2 and self.botlassocount < 400 and self.botlassocount > 50:
                if self.sentidofundo:
                    self.p1.paralisado = True
                    tela.blit(self.fundozw[self.countfundo // 12], (0, 0))
                    self.countfundo += 1
                    if self.countfundo > 12 * 4:
                        self.sentidofundo = False
                        self.countfundo = 0
                else:
                    if self.botlassocount > 351:
                        tela.blit(self.fundozw[4 - (self.countfundo // 12)], (0, 0))
                        self.countfundo += 1
                        if self.countfundo > 12 * 4:
                            self.countfundo = 0
                    else:
                        tela.blit(self.fundozw[4], (0, 0))
            else:
                tela.blit(self.fundo, (0, 0))
            self.p1.posslash = (self.botlasso.rect[0] + 10, self.botlasso.rect[1] + 10)
            if self.botlassocount > 900:
                if self.botlasso.skill == 1:
                    self.botlasso.skill = 0
                    self.botlasso.rect[0] = 780
                    self.botlasso.rect[1] = 0
                    self.botlasso.speedx = 2
                    self.botlassocount = 0
                elif self.botlasso.skill == 0:
                    self.botlasso.rect[0] = 450
                    self.botlasso.rect[1] = 100
                    self.countfundo = 0
                    self.zwsound.play()
                    self.botlasso.skill = 2
                    self.botlasso.canshoot = False
                    self.botlasso.countzw = 0
                    self.botlasso.tiros3 = []
                    self.botlassocount = 0
                    self.sentidofundo = True
                elif self.botlasso.skill == 2:
                    self.botlasso.rect[0] = 780
                    self.botlasso.rect[1] = 100
                    self.botlasso.tiros3 = []
                    self.botlasso.skill = 1
                    self.botlassocount = 0
            if self.botlasso.skill == 0:
                self.botlasso.rect[1] += self.botlasso.speedy
                if self.botlasso.rect[1] <= 100:
                    self.botlasso.speedy = 2
                elif self.botlasso.rect[1] >= 500:
                    self.botlasso.speedy = -2
            elif self.botlasso.skill == 1:
                self.botlasso.rect[0] += self.botlasso.speedx
                if self.botlasso.rect[0] < 100:
                    self.botlasso.speedx = 2
                elif self.botlasso.rect[0] > 700:
                    self.botlasso.speedx = -2
            if self.botlassocount > 350 and self.botlasso.skill == 2 and not self.botlasso.canshoot:
                self.botlassocount = 700
                self.p1.paralisado = False
                self.zwsound2.play()
                self.botlasso.canshoot = True
                self.botlasso.update()



            if self.botlasso.vida <= 0:
                pygame.mixer.music.stop()
                self.fim = time.time()
                tempo = self.fim - self.inicio
                mortes[2] = True
                import death
                death.score(tela, self.fundo, tempo, self.p1.vida, 1)

            self.botlassocount += 1
            self.p1.damage()
            self.collisions()
            self.draw()
            self.botlasso.update()
            self.p1.update()


        def draw(self):
            self.p1.draw()
            if self.botlasso.voando:
                if self.botlasso.skill == 0:
                    tela.blit(self.botlasso.lasso[self.count // 8], (self.botlasso.rect[0], self.botlasso.rect[1]))
                    self.count += 1
                    if self.count >= 40:
                        self.count = 0
                elif self.botlasso.skill == 1:
                    tela.blit(self.botlasso.fly[self.count // 8], (self.botlasso.rect[0], self.botlasso.rect[1]))
                    self.count += 1
                    if self.count >= 40:
                        self.count = 0
                elif self.botlasso.skill == 2:
                    tela.blit(self.botlasso.zawardo, (self.botlasso.rect[0], self.botlasso.rect[1]))
                pygame.draw.rect(tela, (255 - self.botlasso.vida * 2, self.botlasso.vida * 2, 0), [700, 0, self.botlasso.vida * 3, 30], 0)
                tela.blit(self.p1.vidaimagem, (700, 0))

        def collisions(self):
            p1Rect = pygame.Rect(self.p1.rect)
            if self.botlasso.vulnerable:
                bossRect = pygame.Rect(self.botlasso.rect)
                if self.p1.tiro.alive:
                    p1tirorect = pygame.Rect(self.p1.tiro.rect)
                    if p1tirorect.colliderect(bossRect):
                        self.botlasso.vida -= 10
                        self.botlasso.vulnerable = False
                        self.botlasso.count = 0
                        self.count = 0
                        self.p1.tiro.candraw = False
                if self.p1.atacando:
                    if p1Rect.colliderect(bossRect):
                        self.botlasso.vida -= 10
                        self.botlasso.vulnerable = False
                        self.p1.slashalive = True
                        self.botlasso.count = 0
                        self.count = 0
            if self.p1.vulnerable:
                if len(self.botlasso.tiros) == 3:
                    tiro1Rect = pygame.Rect(self.botlasso.tiros[0].rect)
                    tiro2Rect = pygame.Rect(self.botlasso.tiros[1].rect)
                    tiro3Rect = pygame.Rect(self.botlasso.tiros[2].rect)
                    if p1Rect.colliderect(tiro1Rect):
                        self.p1.sounds[1].play()
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
                    elif p1Rect.colliderect(tiro2Rect):
                        self.p1.sounds[1].play()
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
                    elif p1Rect.colliderect(tiro3Rect):
                        self.p1.sounds[1].play()
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
                elif len(self.botlasso.tiros3) == 6:
                    tiro1Rectzw = pygame.Rect(self.botlasso.tiros3[0].rect)
                    tiro2Rectzw = pygame.Rect(self.botlasso.tiros3[1].rect)
                    tiro3Rectzw = pygame.Rect(self.botlasso.tiros3[2].rect)
                    tiro4Rectzw = pygame.Rect(self.botlasso.tiros3[3].rect)
                    tiro5Rectzw = pygame.Rect(self.botlasso.tiros3[4].rect)
                    tiro6Rectzw = pygame.Rect(self.botlasso.tiros3[5].rect)
                    if p1Rect.colliderect(tiro1Rectzw):
                        self.p1.sounds[1].play()
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
                    elif p1Rect.colliderect(tiro2Rectzw):
                        self.p1.sounds[1].play()
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
                    elif p1Rect.colliderect(tiro3Rectzw):
                        self.p1.sounds[1].play()
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
                    elif p1Rect.colliderect(tiro4Rectzw):
                        self.p1.sounds[1].play()
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
                    elif p1Rect.colliderect(tiro5Rectzw):
                        self.p1.sounds[1].play()
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
                    elif p1Rect.colliderect(tiro6Rectzw):
                        self.p1.sounds[1].play()
                        self.p1.vulnerable = False
                        self.p1.vida -= 10
                elif len(self.botlasso.tiros2) > 0:
                    for tiro in self.botlasso.tiros2:
                        tiroRect = pygame.Rect(tiro.rect)
                        if p1Rect.colliderect(tiroRect):
                            self.p1.sounds[1].play()
                            self.p1.vulnerable = False
                            self.p1.vida -= 10

    class Boss(object):
        def __init__(self, scr, rect, speedx, speedy, voando):
            self.lasso = [pygame.image.load("assets/botlasso/Anm1.png").convert_alpha(),
                          pygame.image.load("assets/botlasso/Anm2.png").convert_alpha(),
                          pygame.image.load("assets/botlasso/Anm3.png").convert_alpha(),
                          pygame.image.load("assets/botlasso/Anm4.png").convert_alpha(),
                          pygame.image.load("assets/botlasso/Anm5.png").convert_alpha()]

            self.fly = [pygame.image.load("assets/botlasso/Fly1.png").convert_alpha(),
                        pygame.image.load("assets/botlasso/Fly2.png").convert_alpha(),
                        pygame.image.load("assets/botlasso/Fly3.png").convert_alpha(),
                        pygame.image.load("assets/botlasso/Fly4.png").convert_alpha(),
                        pygame.image.load("assets/botlasso/Fly5.png").convert_alpha()]

            self.menacing = [pygame.image.load("assets/botlasso/menacing1.png").convert_alpha(),
                             pygame.image.load("assets/botlasso/menacing2.png").convert_alpha(),
                             pygame.image.load("assets/botlasso/menacing3.png").convert_alpha(),
                             pygame.image.load("assets/botlasso/menacing4.png").convert_alpha()]

            self.zawardo = pygame.image.load("assets/botlasso/zeposando.png").convert_alpha()
            self.rect = rect
            self.speedx = speedx
            self.speedy = speedy
            self.voando = voando
            self.scr = scr
            self.skill = 0
            self.tiros = []
            self.tiros2 = []
            self.tiros3 = []
            self.counttiro = 0
            self.vida = 100
            self.count = 0
            self.countzw = 0
            self.vulnerable = True
            self.canshoot = False
            self.mencount = 0

        def update(self):
            if len(self.tiros) == 3:
                self.tiros[0].draw()
                self.tiros[0].rect[0] += -4
                self.tiros[0].rect[1] += -2
                self.tiros[1].rect[0] += -4
                self.tiros[1].draw()
                self.tiros[2].rect[0] += -4
                self.tiros[2].rect[1] += 2
                self.tiros[2].draw()
            for tiro in self.tiros:
                if tiro.rect[0] < 0:
                    self.tiros.remove(tiro)
            for tiro in self.tiros2:
                tiro.draw()
                tiro.rect[1] += 5
                if tiro.rect[1] > 800:
                    self.tiros2.remove(tiro)
            if len(self.tiros3) == 6 and self.countzw > 100:
                if self.countzw > 120:
                    self.tiros3[0].draw()
                if self.countzw > 140:
                    self.tiros3[1].draw()
                if self.countzw > 160:
                    self.tiros3[2].draw()
                if self.countzw > 180:
                    self.tiros3[3].draw()
                if self.countzw > 200:
                    self.tiros3[4].draw()
                if self.countzw > 220:
                    self.tiros3[5].draw()
                if self.canshoot:
                    self.tiros3[0].rect[1] += 4
                    self.tiros3[1].rect[1] += 4
                    self.tiros3[2].rect[1] += 4
                    self.tiros3[3].rect[0] += -6
                    self.tiros3[4].rect[0] += -6
                    self.tiros3[5].rect[0] += -6
            for tiro in self.tiros3:
                if tiro.rect[0] < -100:
                    self.tiros3.remove(tiro)
            self.shoot()
            if not self.vulnerable:
                if self.count > 100:
                    self.vulnerable = True
                self.count += 1
            self.countzw += 1
            if self.skill == 2:
                self.scr.blit(self.menacing[self.mencount // 24], (self.rect[0] + 100, self.rect[1]))
                self.mencount += 1
                if self.mencount > 3 * 24:
                    self.mencount = 0
        def shoot(self):
            if self.skill == 0:
                if 300 < self.rect[1] < 400:
                    if len(self.tiros) < 3:
                        self.tiros.append(Projetil(self.scr, [self.rect[0], self.rect[1], 60, 30], (255, 255, 0),
                                                   "assets/botlasso/tiro.png"))
                        self.tiros.append(Projetil(self.scr, [self.rect[0], self.rect[1], 60, 30], (0, 255, 0),
                                                   "assets/botlasso/tiro.png"))
                        self.tiros.append(Projetil(self.scr, [self.rect[0], self.rect[1], 60, 30], (255, 0, 0),
                                                   "assets/botlasso/tiro.png"))
            elif self.skill == 1:
                if len(self.tiros2) < 3 and self.counttiro > 40:
                    self.tiros2.append(Projetil(self.scr, [self.rect[0], self.rect[1], 30, 60], (255, 255, 0),
                                                "assets/botlasso/tiro2.png"))
                    self.counttiro = 0
                self.counttiro += 1
            elif self.skill == 2 and self.countzw < 100:
                if len(self.tiros3) < 6:
                    x = randint(20, 600)
                    y = randint(300, 500)
                    self.tiros3.append(Projetil(self.scr, [x, 300, 30, 60], (255, 255, 0),
                                               "assets/botlasso/tiro2.png"))
                    self.tiros3.append(Projetil(self.scr, [x + 200, 300, 30, 60], (0, 255, 0),
                                               "assets/botlasso/tiro2.png"))
                    self.tiros3.append(Projetil(self.scr, [x + 400, 300, 30, 60], (255, 0, 0),
                                               "assets/botlasso/tiro2.png"))
                    self.tiros3.append(Projetil(self.scr, [900, y, 60, 30], (255, 255, 0),
                                               "assets/botlasso/tiro.png"))
                    self.tiros3.append(Projetil(self.scr, [900, y + 100, 60, 30], (0, 255, 0),
                                               "assets/botlasso/tiro.png"))
                    self.tiros3.append(Projetil(self.scr, [900, y + 200, 60, 30], (255, 0, 0),
                                               "assets/botlasso/tiro.png"))

    class Projetil(object):
        def __init__(self, scr, rect, color, image):
            self.scr = scr
            self.rect = rect
            self.color = color
            self.image = pygame.image.load(image).convert_alpha()

        def draw(self):
            #pygame.draw.rect(self.scr, self.color, self.rect, 0)
            self.scr.blit(self.image, (self.rect[0], self.rect[1]))

    start = True
    cenario = Cenario()
    while start:
        tela.fill((0, 0, 0))
        clock.tick(120)

        eventos(tela, cenario)

        cenario.update()
        pygame.display.update()


