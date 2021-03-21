import pygame # load pygame keywords
import sys # let python use file system
import os # help python identify your OS
import time
import csv
'''
Variables
'''
ALPHA=(0, 0, 0)
BLUE  = (25, 25, 200)
RED = (255, 0, 0)
BLACK = (23, 23, 23)
PURPLE = (150, 0, 150)
WHITE = (254, 254, 254)
GREEN = (0,128,0,1)
BROWN = (165, 42, 42, 1)
GREEN_BROWN = (165,128,42,1)
ORANGE= (156,45,0,4)
LIGHT_GREEN = (42, 159,0,45)
worldx = 1280
worldy = 704
tx=64
ty=64
steps=10
fps   = 50 # frame rate
ani   = 4   # animation cycles
'''
Mazes
'''
maze1=[[1]*20,
      [1]+[0]*14+[1]+[0]*3+[1],
       [1,1,0,1,0,2,1,0,1,1,1,0,1,1,1,1,1,1,2,1],
       [1,0,0,1,0,0,1,0,0,2,0,0,2,0,0,0,0,0,0,1],
       [1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,0,1,0,1],
       [0,0,0,0,0,2,0,0,1,0,1,0,1,0,0,1,0,1,0,1],
       [1,1,1,0,1,1,1,2,1,0,1,0,2,1,0,1,0,1,0,1],
       [1,2,1,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,0,1],
       [1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,2],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

maze2=[[1]*20,
[1,0,0,0,2,0,1,0,0,0,2,0,0,0,0,0,0,2,0,1],
[1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
[1,0,1,0,0,0,1,2,0,1,0,0,0,0,2,1,1,1,0,0],
[1,0,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0,2,0,1],
[0,0,0,0,0,1,1,1,2,1,1,1,1,1,1,1,1,1,0,1],
[1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,0,0,0,0,0,0,1,1,1,1,1,1,0,1,0,0,1],
[1,0,1,1,1,1,1,1,0,1,0,0,2,0,1,0,1,0,1,1],
[1,0,2,0,0,0,2,0,0,1,0,0,1,0,0,0,1,0,0,1],
[1]*20]
'''
Objects
'''
class Player (pygame.sprite.Sprite):
    def __init__ (self, x, y, imgfile="Elf1.png"):
        (sizex, sizey)=(45,45)
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('Images',imgfile)).convert()
        img = pygame.transform.scale(img,(sizex, sizey))
      # img.convert_alpha()     # optimise alpha
        #img.set_colorkey(ALPHA) # set alpha
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.sizey=sizey
        self.sizex=sizex
        self.movex=0
        self.movey=0
        self.score=lvl*10
        self.collectedchest=False
        self.levelcomplete=False
        
    def control(self,x,y):
        self.movex += x
        self.movey += y
        
    def update(self,wall_list,chest_list,coin_list):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        if self.rect.x < 0:
            self.rect.x =0
        if self.rect.x > worldx-tx:
            if self.collectedchest:
                self.levelcomplete=True
            else:
                self.rect.x =worldx-tx
        collidelist=pygame.sprite.spritecollide(self,wall_list,False)
        for wall in collidelist:
            self.rect.x-=self.movex
            self.rect.y-=self.movey
        collidelist=pygame.sprite.spritecollide(self,chest_list,False)
        for chest in collidelist:
            self.collectedchest=True
            self.score+=100
            chest.disappear()
        collidelist=pygame.sprite.spritecollide(self,coin_list,False)
        for coin in collidelist:
            self.score+=10
            coin.disappear()
            
class Wall(pygame.sprite.Sprite):
    
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
class Chest(pygame.sprite.Sprite):
    
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
    def disappear(self):     
        self.image = pygame.transform.scale(self.image,(int(tx/2),int(ty/2)))
        self.rect  = self.image.get_rect()
        self.rect.x=150
        self.rect.y=10
    
class Coin(pygame.sprite.Sprite):
    
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
    def disappear(self):
        self.rect.x=worldx+100
        self.rect.y=worldy+100
'''
Setup
'''
clock = pygame.time.Clock()
pygame.init()
world    = pygame.display.set_mode([worldx,worldy])
#ball=Ball(600, 50)
#ball_list=pygame.sprite.Group()
#ball_list.add(ball)
lvl=2
if lvl==1:
    px=0
    py=int(5*ty)
    colour=GREEN_BROWN
    chestx=11*tx
    chesty=3*ty
    maze=maze1
if lvl==2:
    px=0
    py=5*ty
    colour=BLACK
    chestx=10*tx
    chesty=6*ty
    maze=maze2
player=Player(px, py)
player_list = pygame.sprite.Group()
player_list.add(player)
img = pygame.image.load(os.path.join('Images','wall.png'))
img = pygame.transform.scale(img,(tx,ty))
img.convert_alpha()     # optimise alpha
img.set_colorkey(ALPHA) # set alpha
wall_list=pygame.sprite.Group()
coin_list=pygame.sprite.Group()
cimg = pygame.image.load(os.path.join('Images','Coin.png'))
cimg = pygame.transform.scale(cimg,(int(tx/2),int(ty/2)))
cimg.convert_alpha()     # optimise alpha
cimg.set_colorkey(ALPHA) # set alpha
for i,row in enumerate(maze):
    for j,pos in enumerate(row):
        x=j*tx
        y=i*ty
        if pos==1:
            wall=Wall(x,y,img)
            wall_list.add(wall)
        elif pos==2:
            coin=Coin(x,y,cimg)
            coin_list.add(coin)
img = pygame.image.load(os.path.join('Images','ChestRed.png'))
img = pygame.transform.scale(img,(tx,ty))
img.convert_alpha()     # optimise alpha
img.set_colorkey(ALPHA) # set alpha
chest_list=pygame.sprite.Group()
chest=Chest(chestx,chesty,img)
chest_list.add(chest)
def playgame():
    main=True
    while main == True:
        if player.levelcomplete:
            pygame.event.post(pygame.event.Event(pygame.QUIT,{}))
        if player.score<0:
            pygame.event.post(pygame.event.Event(pygame.QUIT,{}))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("gameover, your score is " +str(int(player.score)))
                pygame.quit(); sys.exit()
                main = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.control(-steps,0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.control(steps,0)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    player.control(0,-steps)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    player.control(0,steps)
                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                    main=False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.control(steps,0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.control(-steps,0)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    player.control(0,steps)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    player.control(0,-steps)
        world.fill(colour)
        player_list.update(wall_list,chest_list,coin_list)
        player_list.draw(world) # draw player
        wall_list.draw(world)
        chest_list.draw(world)
        coin_list.draw(world)
        largeFont=pygame.font.SysFont("arial",25)
        text=largeFont.render("coins: "+str(int(player.score)),1,WHITE)
        world.blit(text,(10,10))
        
        pygame.display.flip()
        clock.tick(fps)
        player.score-=1/fps
playgame()