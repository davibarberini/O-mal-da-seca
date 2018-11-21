def gameloop(scr, scrx, scry):
    import pygame
    import fabiano as ply
    from random import randint
    from pygame.locals import FULLSCREEN, QUIT, KEYDOWN, K_g, KEYUP, K_s, K_o, K_r, K_b, K_p, K_f, MOUSEBUTTONDOWN, \
        K_ESCAPE
    pygame.init()

    clock = pygame.time.Clock()

    class Cenario(object):
        def __init__(self):
            self.boss = Boss(scr, (255, 0, 0), [scrx - 300, scry - 550, 250, 500])
            self.p1 = ply.Player(scr, (0, 0, 255), [scrx - (scrx - 50), scry - 330, 60, 120], 5)
            self.fundo = pygame.image.load("assets/soldado-amarelo/fundo.png").convert()
            self.count = 0

        def update(self):
            scr.blit(self.fundo, (0, 0))
            self.draw()
            self.collisions()
            self.boss.update()
            self.boss.bolhas((self.p1.rect[0], self.p1.rect[1]))
            self.p1.update()
            if self.count > 300:
                if self.boss.skill == 1:
                    self.boss.anim = 3
                    self.boss.tiros = []
                    self.boss.skill = 2
                    self.count = 0
                    self.boss.count = 0
                elif self.boss.skill == 3:
                    self.boss.estado = 0
                    self.boss.vulnerable = True
                    if self.count > 900:
                        self.boss.count = 0
                        self.boss.skill = 1
                        self.boss.vulnerable = False
                        self.count = 0
            self.count += 1

        def collisions(self):
            p1Rect = pygame.Rect(self.p1.rect)

            if len(self.boss.tiros) > 0:
                if self.p1.vulnerable:
                    for tiro in self.boss.tiros:
                        (x, y) = tiro.pos
                        tiroRect = pygame.Rect([x - 20, y - 20, 40, 40])
                        if p1Rect.colliderect(tiroRect):
                            self.p1.vulnerable = False
                            self.p1.vida -= 10
            if self.boss.vulnerable:
                bossRect = pygame.Rect(self.boss.rect)
                if self.p1.atacando:
                    if p1Rect.colliderect(bossRect):
                        self.boss.vida -= 10
                        self.boss.vulnerable = False
                        self.boss.count = 0
                        self.boss.skill = 1
                        self.count = 0
                if self.p1.tiro.alive:
                    p1tiroRect = pygame.Rect(self.p1.tiro.rect)
                    if p1tiroRect.colliderect(bossRect):
                        self.boss.vida -= 10
                        self.boss.vulnerable = False
                        self.boss.count = 0
                        self.boss.skill = 1
                        self.count = 0
            self.p1.damage()
            if self.boss.vulnerable:
                self.boss.color = (255, 255, 0)
            else:
                self.boss.color = (255, 0, 0)

        def draw(self):
            self.boss.draw()
            self.p1.draw()

    class Boss(object):
        def __init__(self, scr, color, rect):
            self.scr = scr
            self.color = color
            self.rect = rect
            self.width = 0
            self.vida = 100
            self.vulnerable = False
            self.imagereal = pygame.image.load("assets/soldado-amarelo/sdamarelo.png").convert_alpha()
            self.image = pygame.transform.scale(self.imagereal, (250, 500))
            self.tiros = [Circulo(scr, (50, 50, 255), (-500, -500), 20, -12) for e in range(10)]
            self.count = 0
            self.countanim = 0
            self.anim = 0
            self.estado = 0
            # estado 0 = idle
            # estado 1 = not idle
            self.hand = True
            self.canskill = False
            self.skill = 1

        def draw(self):
            # pygame.draw.rect(self.scr, self.color, self.rect, self.width)
            self.scr.blit(self.image, (self.rect[0], self.rect[1]))
            pygame.draw.rect(self.scr, (0, 255, 0), [600, 0, self.vida, 50])

        def update(self):
            self.count += 1

        def bolhas(self, posp):
            if self.skill == 1:
                if len(self.tiros) < 10 and self.count % 20 == 0:
                    if self.hand:
                        self.tiros.append(Circulo(scr, (50, 50, 255), (870, 300), 20, -12))
                        self.hand = False
                    else:
                        self.tiros.append(Circulo(scr, (50, 50, 255), (900, 300), 20, -12))
                        self.hand = True


            if self.skill == 2:
                if len(self.tiros) < 10 and self.count % 20 == 0:
                    posx = randint(0, 700)
                    self.tiros.append(Circulo(scr, (50, 50, 255), (posx, -60), 20, 8))

            if self.count > 300:
                if self.skill == 1:
                    self.skill = 2
                    self.count = 0
                elif self.skill == 2:
                    self.skill = 3
                    self.count = 0

            for tiro in self.tiros:
                tiro.draw()
                (x, y) = tiro.pos
                y += tiro.vely
                if y < -60 and self.skill == 1:
                    self.tiros.remove(tiro)
                elif y > 900 and self.skill == 2:
                    self.tiros.remove(tiro)
                tiro.pos = (x, y)

    class Circulo(object):
        def __init__(self, scr, color, pos, raio, vely):
            self.scr = scr
            self.color = color
            self.pos = pos
            self.raio = raio
            self.width = 0
            self.alive = False
            self.count = 0
            self.vely = vely
            self.bolhaoriginal = pygame.image.load("assets/hantiseca/bolha1.png").convert_alpha()
            self.bolha = pygame.transform.scale(self.bolhaoriginal, (40, 40))

        def draw(self):
            self.scr.blit(self.bolha, self.pos)


    cenario = Cenario()
    run = True
    while run:
        clock.tick(120)
        scr.fill((255, 255, 255))

        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_p:
                    exit()
                elif e.key == K_b:
                    cenario.boss.tiros = []
                elif e.key == K_ESCAPE:
                    from main import bossselect
                    bossselect()
                ply.ekeydown(e, cenario)
            elif e.type == KEYUP:
                ply.ekeyup(e, cenario)

        cenario.update()
        pygame.display.update()
