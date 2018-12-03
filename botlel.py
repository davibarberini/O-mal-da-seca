def gameloop(tela, W, H):
    import pygame
    import fabiano as ply
    import time

    pygame.init()

    clock = pygame.time.Clock()

    class Cenario(object):
        def __init__(self):
            self.botlasso = Boss(tela, [780, 0, 150, 170], 0.00, 0, True)
            self.p1 = ply.Player(tela, (0, 0, 255), [W - (W - 50), H - 330, 60, 120], 5)
            self.count = 0
            self.botlassocount = 0
            self.fundo = pygame.image.load("assets/botlasso/botlassofundo.png").convert_alpha()
            self.inicio = time.time()

        def update(self):
            tela.blit(self.fundo, (0, 0))
            self.botlasso.update()
            if self.botlassocount > 900:
                if self.botlasso.skill == 1:
                    self.botlasso.skill = 0
                    self.botlasso.rect[0] = 780
                    self.botlasso.rect[1] = 0
                    self.botlasso.speedx = 2
                    self.botlassocount = 0
                elif self.botlasso.skill == 0:
                    self.botlasso.rect[0] = 780
                    self.botlasso.rect[1] = 100
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



            if self.botlasso.vida < 0:
                pygame.mixer.music.stop()
                self.fim = time.time()
                tempo = self.fim - self.inicio
                ply.mortes[2] = True
                import death
                death.score(tela, self.fundo, tempo, self.p1.vida, 1)

            self.botlassocount += 1
            self.p1.update()
            self.p1.damage()
            self.collisions()
            self.draw()


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
                pygame.draw.rect(tela, (0, 255, 0), [600, 0, self.botlasso.vida * 3, 50])

        def collisions(self):
            if self.botlasso.vulnerable:
                bossRect = pygame.Rect(self.botlasso.rect)
                if self.p1.tiro.alive:
                    p1tirorect = pygame.Rect(self.p1.tiro.rect)
                    if p1tirorect.colliderect(bossRect):
                        self.botlasso.vida -= 10
                        self.botlasso.vulnerable = False
                        self.botlasso.count = 0
                        self.count = 0
            if self.p1.vulnerable:
                p1Rect = pygame.Rect(self.p1.rect)
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
            self.rect = rect
            self.speedx = speedx
            self.speedy = speedy
            self.voando = voando
            self.scr = scr
            self.skill = 0
            self.tiros = []
            self.tiros2 = []
            self.counttiro = 0
            self.vida = 100
            self.count = 0
            self.vulnerable = True

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
            self.shoot()
            if not self.vulnerable:
                if self.count > 100:
                    self.vulnerable = True
                self.count += 1

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
            else:
                if len(self.tiros2) < 3 and self.counttiro > 40:
                    self.tiros2.append(Projetil(self.scr, [self.rect[0], self.rect[1], 30, 60], (255, 255, 0),
                                                "assets/botlasso/tiro2.png"))
                    self.counttiro = 0
                self.counttiro += 1

    class Projetil(object):
        def __init__(self, scr, rect, color, image):
            self.scr = scr
            self.rect = rect
            self.color = color
            self.image = pygame.image.load(image).convert_alpha()

        def draw(self):
            pygame.draw.rect(self.scr, self.color, self.rect, 0)
            self.scr.blit(self.image, (self.rect[0], self.rect[1]))

    start = True
    cenario = Cenario()
    while start:
        tela.fill((0, 0, 0))
        clock.tick(120)

        ply.eventos(tela, cenario)

        cenario.update()
        pygame.display.update()


