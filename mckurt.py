import pygame
import time
from random import randint
from fabiano import Player as ply
from fabiano import eventos, mortes

clock = pygame.time.Clock()

class Cenario(object):
    def __init__(self, scr, W, H):
        self.scr = scr
        self.p1 = ply(scr, (0, 0, 255), [W - (W - 50), H - 330, 60, 120], 5)
        self.p1.vida = 100
        self.p1.rect[0] = 50
        self.mckurt = Boss([700, 270, 250, 500])
        self.fundo = pygame.image.load("assets/mckurt/fundo.png").convert_alpha()
        self.bolas = []
        self.bolaimgreal = pygame.image.load("assets/mckurt/ball.png").convert_alpha()
        self.bolaimg1 = pygame.transform.scale(self.bolaimgreal, (30, 30))
        self.bolaimg2 = pygame.transform.scale(self.bolaimgreal, (40, 40))
        self.bolavel = -10
        self.count = 0
        self.countanim = 0
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=256)
        pygame.mixer.music.load("assets/musics/mckurt.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.inicio = time.time()

    def update(self):
        self.mckurt.update()
        self.p1.update()
        self.p1.damage()
        if self.mckurt.skill == 1:
            if len(self.bolas) < 10 and self.count > 15:
                if self.mckurt.cannon == 1:
                    bola = {"pos": (850, 380),
                            "raio": 15,
                            "vely": self.bolavel,
                            "image": self.bolaimg1}
                else:
                    bola = {"pos": (880, 380),
                            "raio": 15,
                            "vely": self.bolavel,
                            "image": self.bolaimg1}
                self.bolas.append(bola)
                self.mckurt.sounds.play()
                self.count = 0
                if self.mckurt.cannon == 1:
                    self.mckurt.cannon = 2
                else:
                    self.mckurt.cannon = 1
        else:
            x = randint(30, 800)
            if len(self.bolas) < 20 and self.count > 20:
                bola = {"pos": (x, -50),
                        "raio": 20,
                        "vely": self.bolavel,
                        "image": self.bolaimg2}
                self.bolas.append(bola)
                self.count = 0

        for ball in self.bolas:
            (bx, by) = ball["pos"]
            pygame.draw.circle(self.scr, (0, 0, 0), ball["pos"], ball["raio"])
            self.scr.blit(ball["image"], (bx - ball["raio"], by - ball["raio"]))
            by += ball["vely"]
            if self.mckurt.skill == 1:
                if by < -50:
                    self.bolas.remove(ball)
            else:
                if by > 810:
                    self.bolas.remove(ball)
            ball["pos"] = (bx, by)

        if self.mckurt.count > 300:
            if self.mckurt.skill == 1:
                self.mckurt.skill = 2
                self.bolavel = 10
                self.mckurt.count = 0
            elif self.mckurt.skill == 2 and self.mckurt.count > 500:
                self.mckurt.skill = 1
                self.bolavel = -10
                self.mckurt.count = 0
        fabRect = pygame.Rect(self.p1.rect)
        tiroRect = pygame.Rect(self.p1.tiro.rect)
        if self.mckurt.vulnerable:
            if tiroRect.colliderect(self.mckurt.rect) and self.p1.tiro.alive:
                self.mckurt.vida -= 5
                self.p1.tiro.candraw = False
                self.mckurt.vulnerable = False
            if self.p1.atacando:
                if fabRect.colliderect(self.mckurt.rect):
                    self.mckurt.vida -= 5
                    self.mckurt.vulnerable = False
                    self.p1.slashalive = True
                    self.p1.posslash = (self.mckurt.rect[0] + 60, self.p1.rect[1] + 30)

        for ball in self.bolas:
            (bx, by) = ball["pos"]
            ballside = ball["raio"] * 2
            ballRect = pygame.Rect([bx, by, ballside, ballside])
            if fabRect.colliderect(ballRect):
                if self.p1.vulnerable:
                    self.p1.vida -= 20
                    self.p1.sounds[1].play()
                    self.p1.vulnerable = False

        if self.mckurt.vida <= 0:
            pygame.mixer.music.stop()
            self.fim = time.time()
            tempo = self.fim - self.inicio
            mortes[3] = True
            import death
            death.score(self.scr, self.fundo, tempo, self.p1.vida, 2)

        self.count += 1
        self.mckurt.count += 1

    def draw(self):
        self.scr.blit(self.fundo, (0, 0))
        self.p1.draw()
        if self.mckurt.skill == 1:
            self.scr.blit(self.mckurt.image, (self.mckurt.rect[0], self.mckurt.rect[1]))
        else:
            self.scr.blit(self.mckurt.reloading[self.countanim // 24], (self.mckurt.rect[0], self.mckurt.rect[1]))
            self.countanim += 1
            if self.countanim >= 4 * 24:
                self.countanim = 0
        pygame.draw.rect(self.scr, (255 - self.mckurt.vida * 2, self.mckurt.vida * 2, 0), [700, 0, self.mckurt.vida * 3, 30], 0)
        self.scr.blit(self.p1.vidaimagem, (700, 0))


class Boss(object):
    def __init__(self, rect):
        self.rect = rect
        self.count = 0
        self.skill = 1
        self.vida = 100
        self.imagereal = [pygame.image.load("assets/mckurt/mckurt.png").convert_alpha(),
                          pygame.image.load("assets/mckurt/shoot1.png").convert_alpha(),
                          pygame.image.load("assets/mckurt/shoot2.png").convert_alpha(),
                          pygame.image.load("assets/mckurt/shoot3.png").convert_alpha(),
                          pygame.image.load("assets/mckurt/shoot4.png").convert_alpha()]

        self.image = pygame.transform.scale(self.imagereal[0], (250, 500))

        self.reloading = [pygame.transform.scale(self.imagereal[1], (250, 500)),
                          pygame.transform.scale(self.imagereal[2], (250, 500)),
                          pygame.transform.scale(self.imagereal[3], (250, 500)),
                          pygame.transform.scale(self.imagereal[4], (250, 500))]

        self.sounds = pygame.mixer.Sound("assets/mckurt/bulletsound.wav")
        self.cannon = 1
        self.vulnerable = True
        self.vulcount = 0

    def update(self):
        if not self.vulnerable:
            self.vulcount += 1
            if self.vulcount > 100:
                self.vulnerable = True
                self.vulcount = 0




def gameloop(scr, W, H):

    cenario = Cenario(scr, W, H)
    run = True
    while run:
        clock.tick(120)

        #draw
        cenario.draw()

        #update
        cenario.update()


        #eventos
        eventos(scr, cenario)


        pygame.display.update()
