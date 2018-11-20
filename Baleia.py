import pygame
import fabiano as ply
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN, FULLSCREEN, K_f, K_r,K_z,K_x,K_c,K_j,K_SPACE,Rect, K_ESCAPE
from random import randint

pygame.init()
width=1024
height=768
screen=pygame.display.set_mode((width,height))
clock=pygame.time.Clock()
pygame.font.init()
fonte=pygame.font.get_default_font()
fontevitoria=pygame.font.SysFont(fonte, 70, bold=True, italic=False)


class Cenario(object):
    def __init__(self):
        self.cenario=pygame.image.load("./assets/baleia/imagens/fundo.png").convert_alpha()
        self.cenario=pygame.transform.scale(self.cenario,(1024,768))
        self.ba = Enemy(screen, (0,255,0), [780, 450, 270, 270], 0)
        self.velx = 6
        self.count = 0
        self.rect=Rect((0,598),(800,1))

        #self.musica=pygame.mixer.music.load("./assets/baleia/musicas/golden time lover.mp3")
        #self.musicatoca=True
        #self.musicapos=0
        #self.musicapausada=False
        self.p1 = ply.Player(screen, (0, 0, 255), [width - (width - 50), height - 330, 60, 120], 5)

    def atualizarcenario(self):
        screen.blit(self.cenario,(0,0))
        self.ba.draw()
        self.ba.update()
        self.ba.ataque()
        #if self.musicatoca:
         #   self.musicaplay=pygame.mixer.music.play(5)
          #  self.musicatoca=False
        self.p1.update()
        self.p1.draw()
        self.colisao()


    def colisao(self):
        p1Rect = pygame.Rect(self.p1.rect)

        if self.ba.rect.colliderect(self.p1.rect) and self.ba.esperadano==0 and self.ba.invencibilidade:
            self.p1.vida-=20
            self.ba.acerto=True


        elif self.ba.golpe=="preas":
            for i in range(7):
                if self.ba.preasrect[i].colliderect(self.p1.rect) and self.ba.esperadano==0:
                    self.p1.vida-=10
                    self.ba.acerto=True

        elif self.ba.disparorect.colliderect(self.p1.rect) and self.ba.atacar and self.ba.esperadano==0:

            self.p1.vida-=10
            self.ba.acerto=True

        if self.p1.atacando:
            if p1Rect.colliderect(self.ba.rect):
                if(self.ba.protecao==False):
                    self.ba.vida -= 3
                    self.ba.protecao=True



        if self.p1.tiro.alive:
            p1tiroRect = pygame.Rect(self.p1.tiro.rect)
            if p1tiroRect.colliderect(self.ba.rect):
                if(self.ba.protecao==False):
                    self.ba.vida -= 3
                    self.ba.protecao=True

        if self.ba.acerto:
            self.ba.esperadano+=1
            if(self.ba.esperadano>=150):
                self.ba.esperadano=0
                self.ba.acerto=False


class Enemy(object):
    def __init__(self,screen,cor,rect,vely):
        self.screen=screen
        self.cor=cor
        self.rect=Rect(rect)
        self.x=500
        self.y=400
        self.imagem=pygame.image.load("./assets/baleia/imagens/cachorro.png").convert_alpha()
        self.imagem=pygame.transform.scale(self.imagem,(rect[2],rect[3]))
        self.velx=0
        self.vely=vely
        self.width=20
        self.height=30
        self.baleiaalive=True
        self.vida=100
        self.atacar=False
        self.golpe=""
        self.invencibilidade=False
        self.protecao=False
        self.protecaoespera=0
        self.tempo=0
        self.ataques=0


        self.disparo=self.rect[0]+100
        self.disparos=0
        self.disparoy=self.rect[1]+100
        self.disparorect=Rect(self.disparo,rect[1]+100,20,20)
        self.imagemload=[pygame.image.load("./assets/baleia/imagens/cachorro parado.png").convert_alpha(),
                     pygame.image.load("./assets/baleia/imagens/cachorro andando.png").convert_alpha(),
                     pygame.image.load("./assets/baleia/imagens/cachorro andando 2.png").convert_alpha(),
                     pygame.image.load("./assets/baleia/imagens/cachorro atirando.png").convert_alpha(),
                     pygame.image.load("./assets/baleia/imagens/cachorro pulando.png").convert_alpha()]
        self.imagem=[pygame.transform.scale(self.imagemload[0],(rect[2],rect[3])),
                     pygame.transform.scale(self.imagemload[1],(rect[2],rect[3])),
                     pygame.transform.scale(self.imagemload[2],(rect[2],rect[3])),
                     pygame.transform.scale(self.imagemload[3],(rect[2],rect[3])),
                     pygame.transform.scale(self.imagemload[4],(rect[2],rect[3]))]


        self.disparoimagem=pygame.image.load("./assets/baleia/imagens/Tiro.png").convert_alpha()
        self.disparoimagem2=pygame.image.load("./assets/baleia/imagens/alma.png").convert_alpha()


        self.preas=list(range(20))
        self.preasvelx=0
        self.preaload=[pygame.image.load("./assets/baleia/imagens/prea.png").convert_alpha(),
                       pygame.image.load("./assets/baleia/imagens/prea2.png").convert_alpha()]
        self.preasimg=[pygame.transform.scale(self.preaload[0],(120,120)),
                       pygame.transform.scale(self.preaload[1],(120,120))]
        self.vezes=0
        self.preasrect=list(range(20))


        self.pulo=False
        self.pulodevolta=False
        self.cairdevolta=False
        self.esperapulo=0

        self.esperadano=0
        self.acerto=False

        self.countanim=1
        self.countanimprea=0



    def draw(self):
        #pygame.draw.rect(self.screen, self.cor, self.rect, self.width)
        if self.vida<=0:
            self.vida=0
        vidastring=str(self.vida)
        vidastring="Baleia: "+vidastring
        textovida=fontevitoria.render(vidastring,1,(255,255,255))
        self.screen.blit(textovida,(700,50))


        if self.baleiaalive:
            if self.atacar or self.invencibilidade:
                if(self.golpe=="investida"):
                    if(self.countanim<=90):
                        self.screen.blit(self.imagem[self.countanim//30], (self.rect[0], self.rect[1]))
                        self.countanim+=1
                    else:
                        self.countanim=1
                elif(self.golpe=="pulo"):
                    self.screen.blit(self.imagem[4], (self.rect[0], self.rect[1]))
                elif(self.golpe=="disparo" or "disparos"):
                    self.screen.blit(self.imagem[3], (self.rect[0], self.rect[1]))
                elif(self.golpe=="preas"):
                    self.screen.blit(self.imagem[0], (self.rect[0], self.rect[1]))

            else:
                self.screen.blit(self.imagem[0], (self.rect[0], self.rect[1]))

            

        else:
            texto=fontevitoria.render('Você matou mano',1,(255,0,00))
            self.screen.blit(texto,(150,300))


    def update(self):
        if self.baleiaalive:
            if self.rect[1] + self.vely > 300:
                self.vely = 0
            if self.rect[0] + self.velx > 800:
                self.velx = 0
            if self.rect[0] + self.velx < -350:
                self.velx=0
            if self.vida<=0:
                self.baleiaalive=False
                self.vida=0
                self.atacar=False
            if self.protecao:
                self.protecaoespera+=1
                if(self.protecaoespera>=200):
                    self.protecaoespera=0
                    self.protecao=False

            self.disparorect=Rect(self.disparo-12,self.rect[1]+100,20,20)
            self.rect[1] += self.vely
            self.vely += 0.15
            self.rect[0] += self.velx


    def ataque(self):
        if self.baleiaalive:
            r=randint(1,4)
            if(r==1 and self.golpe=="" or self.golpe=="investida"):

                self.velx=0
                self.golpe="investida"
                self.invencibilidade=True
                if (self.rect[0]>=-350):
                    self.velx-=5.5
                    self.rect[0]+=self.velx


                else:
                    self.invencibilidade=False
                    self.rect[0]=730
                    self.golpe=""
                    self.ataques+=1


            elif(r==2 and self.golpe=="" or self.golpe=="disparo"):
                self.atacar=True
                self.golpe="disparo"
                self.invencibilidade=False
                if(self.disparo>=-0):
                    self.disparo-=10
                    self.screen.blit(self.disparoimagem, (self.disparo, self.rect[1]+100))
                else:
                    self.disparo=self.rect[0]+75
                    self.golpe=""
                    self.ataques+=1


            elif(r==3 and self.golpe=="" or self.golpe=="preas"):

                self.velx=0
                self.golpe="preas"
                self.invencibilidade=False
                self.vezes=0


                x=self.rect[0]

                self.preasvelx-=7
                for i in range(7):
                    self.preas[i]=(i*360)+self.preasvelx
                    if(self.preas[i]>=-2000):
                        if(self.countanimprea<=24):
                            self.countanimprea=0
                        self.screen.blit(self.preasimg[self.countanimprea//12], (self.preas[i]-800+2000+0,600))
                        self.countanimprea+=1
                        self.preasrect[i]=Rect(self.preas[i]-1024+2020+0,600+50,80,40)



                    if(self.preas[6]<=-1600):
                        self.golpe=""
                        self.ataques+=1
                        self.preasvelx=0
                        self.countanimprea=0
                        for i in range(7):
                            self.preas[i]=0

            elif(r==4 and self.golpe=="" or self.golpe=="pulo"):
                self.vely=0
                self.velx=0
                self.atacar=False
                self.golpe="pulo"
                self.invencibilidade=True

                if (self.rect[1]>=0 and ((self.pulo==False or self.pulodevolta) and self.cairdevolta==False)and self.esperapulo<=150):
                    self.vely-=4
                    if(self.pulodevolta==False):
                        self.velx-=1.5
                    elif(self.pulodevolta):
                        self.velx+=2.1
                    self.rect[1]+=self.vely
                    self.rect[0]+=self.velx


                elif(self.rect[1]<=0 and (self.pulo==False or self.pulodevolta)):
                    self.pulo=True
                    if(self.pulodevolta):
                        self.cairdevolta=True
                        self.pulodevolta=False
                        print(self.cairdevolta)
                        print(self.rect[1])


                elif((self.pulo or self.cairdevolta) and self.rect[1]<=450 ):
                    self.vely+=2
                    if(self.rect[0]>=0):
                        if(self.cairdevolta==False):
                            self.velx-=1.5
                        elif(self.cairdevolta):
                            if(self.rect[0]<=780):
                                self.velx+=2
                    self.rect[1]+=self.vely
                    self.rect[0]+=self.velx


                elif(self.esperapulo<=150 and self.pulodevolta==False):
                    self.invencibilidade=False
                    self.esperapulo+=1

                elif(self.esperapulo>150 and self.pulodevolta==False):
                    self.pulodevolta=True
                    self.pulo=False
                    self.invencibilidade=True
                    self.esperapulo=0


                else:
                    self.invencibilidade=False
                    self.esperapulo=0
                    self.pulo=False
                    self.pulodevolta=False
                    self.cairdevolta=False
                    self.rect[1]=450
                    self.rect[0]=730
                    self.golpe=""
                    self.ataques+=1


            if(self.ataques>=5 and self.golpe=="" or self.golpe=="disparos"):
                self.atacar=True
                self.golpe="disparos"
                self.invencibilidade=False
                if(self.disparos<=3):
                    if(self.disparos%2==0):
                        if(self.disparo>=-0):
                            self.disparo-=12
                            self.screen.blit(self.disparoimagem2, (self.disparo, self.rect[1]+100))
                        else:
                            self.disparoimagem2=pygame.transform.flip(self.disparoimagem2,True,False)
                            self.disparos+=1
                    elif(self.disparos%2!=0):
                        if(self.disparo<=1024):
                            self.disparo+=12
                            self.screen.blit(self.disparoimagem2, (self.disparo, self.rect[1]+100))
                        else:
                            self.disparoimagem2=pygame.transform.flip(self.disparoimagem2,True,False)
                            self.disparos+=1
                else:
                    self.disparo=self.rect[0]+75
                    self.golpe=""
                    self.ataques=0
                    self.disparos=0





__init__ = "__main__"
cenario = Cenario()
def gameloop():
    global esperafalas, musica, sompausado, espera, acertado, falas

    rodar = True
    espera = 0
    acertado = False
    falas = False
    esperafalas = 0
    musica = False
    sompausado = 0
    #cenario.musicaplay = pygame.mixer.music.play(5)
    while rodar:
        clock.tick(120)
        cenario.atualizarcenario()

        #if cenario.musicapausada == False:
            #cenario.musicapos += 1

        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_f:
                    exit()
                elif e.key == K_ESCAPE:
                    from main import bossselect
                    bossselect()
                ply.ekeydown(e, cenario)
            elif e.type == KEYUP:
                ply.ekeyup(e, cenario)

        pygame.display.update()