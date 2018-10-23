import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN, FULLSCREEN, K_f, K_r,K_z,K_x,K_c,K_j,K_SPACE,Rect
from random import randint

pygame.init()
width=1024
height=720
screen=pygame.display.set_mode((width,height))
clock=pygame.time.Clock()
pygame.font.init()
fonte=pygame.font.get_default_font()
fontevitoria=pygame.font.SysFont(fonte, 70, bold=True, italic=False)


class Cenario(object):
    def __init__(self):
        self.cenario=pygame.image.load("./assets/baleia/imagens/deserto.jpg")
        self.cenario=pygame.transform.scale(self.cenario,(1024,720))
        self.ba = Enemy(screen, (0,255,0), [780, 450, 270, 270], 0)
        self.velx = 6
        self.count = 0
        self.rect=Rect((0,598),(800,1))

        self.musica=pygame.mixer.music.load("./assets/baleia/musicas/golden time lover.mp3")
        self.musicaplay=pygame.mixer.music.play(5)
        self.musicatoca=True
        self.musicapos=0
        self.musicapausada=False

    def atualizarcenario(self):
        screen.blit(self.cenario,(0,0))
        'self.pl.draw()'
        self.ba.draw()
        'self.pl.update()'
        self.ba.update()
        if self.musicatoca:
            self.musicaplay=pygame.mixer.music.play(5)
            self.musicatoca=False


class Enemy(object):
    def __init__(self,screen,cor,rect,vely):
        self.screen=screen
        self.cor=cor
        self.rect=Rect(rect)
        self.x=500
        self.y=400
        self.imagem=pygame.image.load("./assets/baleia/imagens/cachorro.png")
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
        self.tempo=0
        self.ataques=0


        self.disparo=self.rect[0]+100
        self.disparos=0
        self.disparoy=self.rect[1]+100
        self.disparorect=Rect(self.disparo,rect[1]+100,20,20)
        self.disparoimagem=pygame.image.load("./assets/baleia/imagens/bola.png")
        self.disparoimagem2=pygame.image.load("./assets/baleia/imagens/bola2.png")



        self.disparoimagem=pygame.transform.scale(self.disparoimagem,(20,20))
        self.disparoimagem2=pygame.transform.scale(self.disparoimagem2,(20,20))


        self.preas=list(range(20))
        self.preasvelx=0
        self.preasimg=pygame.image.load("./assets/baleia/imagens/prea.jpg")
        self.preasimg=pygame.transform.scale(self.preasimg,(120,120))
        self.vezes=0
        self.preasrect=list(range(20))


        self.pulo=False
        self.pulodevolta=False
        self.cairdevolta=False
        self.esperapulo=0




    def draw(self):
        #pygame.draw.rect(self.screen, self.cor, self.rect, self.width)
        if self.vida<=0:
            self.vida=0
        vidastring=str(self.vida)
        vidastring="Baleia: "+vidastring
        textovida=fontevitoria.render(vidastring,1,(255,255,255))
        self.screen.blit(textovida,(700,50))


        if self.baleiaalive:
            self.screen.blit(self.imagem, (self.rect[0], self.rect[1]))

            

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
                    self.velx-=3
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
                    self.disparo-=6
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

                self.preasvelx-=5
                for i in range(7):
                    self.preas[i]=(i*360)+self.preasvelx
                    if(self.preas[i]>=-2000):
                        self.screen.blit(self.preasimg, (self.preas[i]-800+2000+0,600))
                        self.preasrect[i]=Rect(self.preas[i]-1024+2020+0,600+50,80,40)



                    if(self.preas[6]<=-1600):
                        self.golpe=""
                        self.ataques+=1
                        self.preasvelx=0
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
                            self.disparo-=8
                            self.screen.blit(self.disparoimagem2, (self.disparo, self.rect[1]+100))
                        else:
                            self.disparos+=1
                    elif(self.disparos%2!=0):
                        if(self.disparo<=1024):
                            self.disparo+=8
                            self.screen.blit(self.disparoimagem2, (self.disparo, self.rect[1]+100))
                        else:
                            self.disparos+=1
                else:
                    self.disparo=self.rect[0]+75
                    self.golpe=""
                    self.ataques=0
                    self.disparos=0


            '''if(self.ataques==5 and self.golpe=="" or self.golpe=="espera"):
               self.golpe="espera"
                self.invencibilidade=False
                self.atacar=False

                if(self.tempo<=300):
                    self.tempo+=1
                else:
                    tempo=0
                    self.golpe=""
                    self.ataques=0
                 self.tempo=0 '''














__init__="__main__"

rodar=True
cenario=Cenario()
clock.tick(120)
espera=0
acertado=False
falas=False
esperafalas=0
musica=True
sompausado=0


while rodar:
    cenario.atualizarcenario()

    if cenario.musicapausada==False:
        cenario.musicapos+=1

    for e in pygame.event.get():
        if e.type == QUIT:
            exit()

    cenario.ba.ataque()
    pygame.display.update()
'''colisão
    if(cenario.pl.rect.colliderect(cenario.rect)):
        cenario.pl.pulo=0

    if cenario.ba.rect.colliderect(cenario.pl.rect) and espera==0 and cenario.ba.invencibilidade:

        cenario.pl.vida-=1
        acertado=True


    elif cenario.ba.golpe=="preas":
        for i in range(7):
            if cenario.ba.preasrect[i].colliderect(cenario.pl.rect) and espera==0:
                cenario.pl.vida-=1
                acertado=True

    elif cenario.ba.disparorect.colliderect(cenario.pl.rect) and cenario.ba.atacar and espera==0:

        cenario.pl.vida-=1
        acertado=True

    if acertado:
        espera+=1
        if(espera>=150):
            espera=0
            acertado=False '''




