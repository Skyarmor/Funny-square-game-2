########                                   ########
####                                           ####
##              Funny square game 2              ##
#                                                 #
#            WOAH!! this is VERY messy code!!     #
#    and im not explaining how it works either :D #
#      TRY TO MOD AT YOUR OWN RISK LMAO           #
##              made by: Skyarmor                ##
####                                           ####
########                                   ########
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
#setting up pygame
import pygame
import random
import math
from pygame import mixer
pygame.init()
height = 600
length = 600
scr = pygame.display.set_mode((length,height))
running = True
playerdies = 0
friction = 15
onice = 0
onfriction = 0
multiplenemeies = 0
playerXvelocity = 0
playerYvelocity = 0
youbeatthegame = 0


def restart():
  global level
  global playercolor
  global playerXvelocity
  global playerYvelocity
  global doorhorizontalX
  global doorverticalX
  global wallhorizontalX
  global wallverticalX
  global buttonunpressedX
  global buttonhorizontalunpressedX
  global golemenemyactive
  global buttonpressedX
  global buttonhorizontalpressedX
  global pressingdash
  playerXvelocity = 0
  playerYvelocity = 0
  buttonpressedX += 9000
  buttonhorizontalpressedX += 9000
  buttonunpressedX += 90000
  buttonhorizontalunpressedX += 90000
  doorverticalX += 9000
  doorhorizontalX += 9000
  wallhorizontalX += 9000
  wallverticalX += 9000
  playercolor = green
  golemenemyactive = 0
  level -= 0.5
  pressingdash = 0
  
  
def playerdeath():
  global menuisopen
  global level
  for i in range(80):
    deathparticles.append(deathparticle(random.randint(-25,25), random.randint(-25,25), green, 10))
  restart()

#these are the images for the class tiles that may be spawned
spikedown = pygame.image.load('images/spikeset/spikedown.png')
spikeup = pygame.image.load('images/spikeset/spikeup.png')
spikeleft = pygame.image.load('images/spikeset/spikeleft.png')
spikeright = pygame.image.load('images/spikeset/spikeright.png')
icetiler = pygame.image.load("images/ice tile.png")
frictiontiler= pygame.image.load("images/friction block.png")
voidtiler = pygame.image.load("images/void.png")
enemysprite = pygame.image.load("images/enemy sprite.png")
enemysprite2 = pygame.image.load("images/enemybutbig.png")
enemysprite3 = pygame.image.load("images/enemy sprite 3.png")
endscreen = pygame.image.load("images/endscreen.png")
#ice tile
class icetile():
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.alive = 1
  def draw(self,scr):
    global playercenterX
    global playercenterY
    global friction
    global onice
    if (self.x - playercenterX <= 50 and self.x - playercenterX >= -50 and self.y - playercenterY <= 50 and self.y - playercenterY >= -50 and self.alive == 1):
      onice = 1
    else:
      onice = 0
    if (self.alive == 1):
      scr.blit(icetiler,(self.x, self.y))
      
#friction tile
class frictiontile():
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.alive = 1
  def draw(self,scr):
    global playercenterX
    global playercenterY
    global frictio
    global onfriction
    if (self.x - playercenterX <= 50 and self.x - playercenterX >= -50 and self.y - playercenterY <= 50 and self.y - playercenterY >= -50 and self.alive == 1):
      onfriction = 1
    else:
      onfriction = 0
    if (self.alive == 1):
      scr.blit(frictiontiler,(self.x, self.y))
    
#spike sets
class spike():
  def __init__(self,x,y,face):
    self.x = x
    self.y = y
    self.facing = face
    self.alive = 1
  def draw(self,scr):
    global playercenterX
    global playercenterY
    global playerdies
    if (self.alive == 1):
      if (self.x - playercenterX <= 45 and self.x - playercenterX >= -45 and self.y - playercenterY <= 45 and self.y - playercenterY >= -45):
        playerdies = 1
      scr.blit(self.facing,(self.x, self.y))

class voidtile():
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.alive = 1
  def draw(self,scr):
    if (self.alive == 1):
      scr.blit(voidtiler,(self.x,self.y))
      
      
#defining the particles that trail behind you when you dash 
      
class dashparticle():
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.size = 50
    self.color = cyan
    self.alive = 1
  def draw(self,scr):
    if (self.alive == 1):
      self.size -= 1.5
      self.x += 0.5
      self.y += 0.5
      pygame.draw.rect(scr,self.color,pygame.Rect((self.x,self.y),(self.size, self.size)))
    if (self.size < 0):
      self.alive = 0
      
#particles when you die
#these particles are also reused for other things
      
class deathparticle():
  def __init__(self,xvel,yvel, color,size):
    self.color = color
    self.size = size
    self.x =playercenterX + 25 - self.size
    self.y = playercenterY + 25 - self.size
    self.xvel = xvel
    self.yvel = yvel
    self.alive = 1
  def draw(self,scr):
    if (self.alive == 1):
      self.x += self.xvel
      self.y += self.yvel
      self.size -= 0.5
      pygame.draw.rect(scr,self.color,pygame.Rect((self.x,self.y),(self.size, self.size)))
    if self.size < 0:
      self.alive = 0
      
class enemy():
  def __init__(self,x,y,id):
    self.x = x
    self.y = y
    self.xvel = 0
    self.yvel = 0
    self.pressing = [0,0,0,0,0]
    self.alive = 1
    self.cooldown = 0
    self.direction = 0
    self.size = 50
    self.id = id
    self.added = 0
    self.veryadded = 0
    self.distancefromplayer = 0
  def draw(self,scr):
    global playercenterX
    global playercenterY
    global playerXvelocity
    global playerYvelocity
    global dashspeed

    
    if (self.alive == 1):
      
      if (self.size == 50):
        scr.blit(enemysprite,(self.x,self.y))
      if (self.size == 100):
        scr.blit(enemysprite2,(self.x - self.added ,self.y - self.added))
      if (self.size == 100):
        self.added = 25
      elif(self.size == 50):
        self.added = 0
      self.veryadded = 50 + self.added
      if (playercenterX > self.x + self.added):
        self.pressing[4] = "right"
      else:
        self.pressing[4] = 0
      if(playercenterX < self.x + self.added):
        self.pressing[3] = "left"
      else:
        self.pressing[3] = 0
      if(playercenterY > self.y + self.added):
        self.pressing[2] = "down"
      else:
        self.pressing[2] = 0
      if(playercenterY < self.y + self.added):
        self.pressing[1] = "up"
      else:
        self.pressing[1] = 0
        
      if (self.size == 50):
#player getting killed
        if (self.x- playercenterX <= self.size and self.x- playercenterX >= -self.size and self.y- playercenterY <= self.size and self.y- playercenterY >= -self.size and self.alive and playercolor != cyan):
          playerdeath()

#tier 1 enemy getting full killed
        elif(self.x - playercenterX <= 50 and self.x - playercenterX >= -50 and self.y - playercenterY <= 50 and self.y - playercenterY >= -50 and self.alive and playercolor == cyan):
          enemydeath()
          self.alive = 0

#player getting killed
      if (self.size > 50):
        if (self.x- playercenterX <= self.veryadded and self.x- playercenterX >= -self.veryadded and self.y- playercenterY <= self.veryadded and self.y- playercenterY >= -self.veryadded and self.alive and playercolor != cyan):
          playerdeath()


#tier 2 enemy getting damaged
        elif(self.x - playercenterX <= self.veryadded and self.x - playercenterX >= -self.veryadded and self.y - playercenterY <= self.veryadded and self.y - playercenterY >= -self.veryadded and self.alive and playercolor == cyan):            
          enemydeath()
#the code where the enemies knock you back
          if (playerXvelocity < 0 and self.size > 50):
            playerXvelocity = 10
            print("pushing right")
            
          elif (playerXvelocity > 0 and self.size > 50):
            playerXvelocity = -10
            print("pushing left")
            
          if (playerYvelocity < 0 and self.size >50):
            playerYvelocity = 10
            print("pushing up")
            
          elif (playerYvelocity > 0 and self.size > 50):
            playerYvelocity = -10 
            print("pushing down")
          
          self.size -=50
          
        
        
    
      if (self.pressing[4] == 0):
        self.xvel -= self.xvel / friction
      if (self.pressing[3] == 0):
        self.xvel -= self.xvel / friction
      if (self.pressing[2] == 0):
        self.yvel -= self.yvel / friction
      if (self.pressing[1] == 0):
        self.yvel -= self.yvel / friction
      self.y += self.yvel
      self.x += self.xvel
    
      if (self.x >= length - self.size and self.alive==1):
        self.xvel += -bounce
      if (self.x <= 0 and self.alive==1):
        self.xvel += bounce
      if (self.y >= height - self.size and self.alive == 1):
        self.yvel += -bounce
      if (self.y <= 0 and self.alive==1):
        self.yvel += bounce
#wall vertical enemy collision
      if (wallverticalY - self.y <= self.size and wallverticalY - self.y >= -800 and wallverticalX - self.x <= self.size and wallverticalX - self.x >= 15):
        self.xvel -= bounce
      if (wallverticalY - self.y <= self.size and wallverticalY - self.y >= -800 and wallverticalX - self.x >= -self.size and wallverticalX - self.x <= -30):
        self.xvel += bounce
      if (wallverticalX - self.x <= self.size and wallverticalX - self.x >= -self.size and wallverticalY - self.y <= self.size and wallverticalY - self.y >= -25):
        self.yvel -= bounce
      if(wallverticalX - self.x <= self.size and wallverticalX - self.x >= -self.size and wallverticalY - self.y >= -800 and wallverticalY - self.y <= -775):
        self.yvel += bounce
#door vertical enemy collision
      if (doorverticalY - self.y <= self.size and doorverticalY - self.y >= -800 and doorverticalX - self.x <= self.size and doorverticalX - self.x >= 15):
        self.xvel -= bounce
      if (doorverticalY - self.y <= self.size and doorverticalY - self.y >= -800 and doorverticalX - self.x >= -self.size and doorverticalX - self.x <= -30):
        self.xvel += bounce
      if (doorverticalX - self.x <= self.size and doorverticalX - self.x >= -self.size and doorverticalY - self.y <= self.size and doorverticalY - self.y >= -25):
        self.yvel -= bounce
      if (doorverticalX - self.x <= self.size and doorverticalX - self.x >= -50 and doorverticalY - self.y >= -800 and doorverticalY - self.y <= -775):
        self.yvel += bounce
      if(self.pressing[4] == "right"):
        self.xvel += acceleration
      if (self.pressing[3] == "left"):
        self.xvel -= acceleration
      if (self.pressing[1] == "up"):
        self.yvel -= acceleration
      if (self.pressing[2] == "down"):
        self.yvel += acceleration

dashparticles = []
deathparticles = []
spikes = []
icetiles =[]
frictiontiles = []
voidtiles = []
enemies = []
def levelprogress():
  global level
  global multiplenemies
  level += 0.5
  for spike in spikes:
    spike.x = 9000
    spike.alive =0
  for icetile in icetiles:
    icetile.alive = 0
  for frictiontile in frictiontiles:
    frictiontile.alive = 0
  for voidtile in voidtiles:
    voidtile.alive = 0
  for enemy in enemies:
    enemy.alive = 0
  multiplenemies = 0

#creating a library of preset colors to use
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
green = (3, 68, 1)
cyan = (0,255,255)
gray = (100,100,100)

#setting up the icon for the game
icon= pygame.image.load('images/reallybruh.png')
pygame.display.set_icon(icon)

#player data
playercolor = green
playercenterX = 400
playercenterY = 0

#enemy1data
enemy1 = pygame.image.load('images/enemy sprite.png')
enemy1X = 9000
enemy1Y = 9000
enemy1Xvelocity = 0
enemy1Yvelocity = 0
golemenemy = pygame.image.load("images/golem.png")
golemenemyX = 900
golemenemyY = 900
golemenemyXvelocity = 0
golemenemyYvelocity = 0
golemenemyactive=  0

#floor pattern
floor1 = pygame.image.load("images/floor1.png")
floor1X = 0
floor1Y = 0

#background for menu1
background1= pygame.image.load("images/checkerblue.png")
background1X = 0
background1Y = 0

#wall that is sideways data
wallhorizontal = pygame.image.load("images/wall horizontal.png")
wallhorizontalX = 0
wallhorizontalY = -900

#wall that is standing up data
wallvertical = pygame.image.load("images/wall vertical.png")
wallverticalX = 300
wallverticalY = 200

#door that is sideways data
doorhorizontal = pygame.image.load("images/doorhorizontal.png")
doorhorizontalX = 900
doorhorizontalY = 900

#door that is standing up data
doorvertical = pygame.image.load("images/doorvertical.png")
doorverticalX = 900
doorverticalY = 900

#teleporter data
teleporter = pygame.image.load("images/teleporter.png")
teleporterX = 900
teleporterY = 900

#button pressed texture
buttonpressed = pygame.image.load("images/button pressed.png")
buttonpressedX = 9000
buttonpressedY = 900

#buttonunpressed texture
buttonunpressed = pygame.image.load("images/button unpressed.png")
buttonunpressedX = 900
buttonunpressedY = 900

buttonhorizontalpressed = pygame.image.load("images/button pressed.png")
buttonhorizontalpressedX = 900
buttonhorizontalpressedY = 9000

buttonhorizontalunpressed = pygame.image.load("images/button unpressed.png")
buttonhorizontalunpressedX = 900
buttonhorizontalunpressedY = 900

dashcrystal = pygame.image.load("images/dashdiamond.png")
dashcrystalX = 900
dashcrystalY = 900

deathbox = pygame.image.load("images/deathnode.png")
deathboxX = 900
deathboxY = 900

menuwarning = pygame.image.load("images/warning message.png")
mainmenu = pygame.image.load("images/menu 2.png")

face = pygame.image.load("images/goofy ahh face.png")





level = 0.5
acceleration = 0.2
pressingdash = 0
dashthingy = 0
dashtimer = 0
dashspeed = 6
bounce = 1
dead = 0
menuisopen = 1
warningisopen = 1
mouseX, mouseY = 9000,9000
clicking = False
hasdash = 0

pressing = [0,0,0,0,0,0,0,0,0,0]
enemy1pressing = [0,0,0,0,0,0,0,0,0,0]
enemy1active = 0
fps = 40
pygame.display.set_caption("Funny square game :)")
clock = pygame.time.Clock()
mixer.music.load("musics/Skyarmor - video game track (main).mp3")
mixer.music.play(-1)
def golemAI():
  global playercenterX
  global playercenterY
  global golemenemyX
  global golemenemyY
  global golemenemyactive
  global golemenemyXvelocity
  global golemenemyYvelocity
  global bounce
  global pressing
  global friction
  global acceleration
  if (pressing[1] == "up"):
    golemenemyYvelocity += acceleration
  if (pressing[2] == "down"):
    golemenemyYvelocity -= acceleration
  if (pressing[3] == "left"):
    golemenemyXvelocity += acceleration
  if (pressing[4] == "right"):
    golemenemyXvelocity -= acceleration
  if (pressing[3] == 0):
    golemenemyXvelocity -= golemenemyXvelocity / friction
  if (pressing[4] == 0):
    golemenemyXvelocity -= golemenemyXvelocity / friction
  if (pressing[2] == 0):
    golemenemyYvelocity -= golemenemyYvelocity / friction
  if (pressing[1] == 0):
    golemenemyYvelocity -= golemenemyYvelocity / friction
  #collisions
  if (wallverticalY - golemenemyY <= 50 and wallverticalY - golemenemyY >= -800 and wallverticalX - golemenemyX <= 50 and wallverticalX - golemenemyX >= 15):
    golemenemyXvelocity -= bounce
  if (wallverticalY - enemy1Y <= 50 and wallverticalY - golemenemyY >= -800 and wallverticalX - golemenemyX >= -50 and wallverticalX - golemenemyX <= -30):
    golemenemyXvelocity += bounce
  if (wallverticalX - golemenemyX <= 50 and wallverticalX - golemenemyX >= -50 and wallverticalY - golemenemyY <= 50 and wallverticalY - golemenemyY >= -25):
    golemenemyYvelocity -= bounce
  if (wallverticalX - golemenemyX <= 50 and wallverticalX - golemenemyX >= -50 and wallverticalY - golemenemyY >= -800 and wallverticalY - golemenemyY <= -775):
    golemenemyYvelocity += bounce
  
  if (golemenemyX - playercenterX <= 50 and golemenemyX - playercenterX >= -50 and golemenemyY - playercenterY <= 50 and golemenemyY - playercenterY >= -50 and golemenemyactive):
    playerdeath()
  if (golemenemyX >= length - 50 and golemenemyactive):
    golemenemyXvelocity += -bounce
  if (golemenemyX <= 0 and golemenemyactive):
    golemenemyXvelocity += bounce
  if (golemenemyY >= height - 50 and golemenemyactive):
    golemenemyYvelocity += -bounce
  if (golemenemyY <= 0 and golemenemyactive):
    golemenemyYvelocity += bounce
  golemenemyY += golemenemyYvelocity
  golemenemyX += golemenemyXvelocity

def enemydeath():
  global dashtimer
  global enemy1X
  global enemy1Y
  global enemy1active
  global playercolor
  global pressingdash
  for i in range(80):
    deathparticles.append(deathparticle(random.randint(-25,25), random.randint(-25,25), red, 10))
  enemy1X = 9000
  enemy1active = 0
  playercolor = green
  pressingdash = 0


  
while running:
  for i in range(len(enemies)):
    if not enemies[i].alive:
        continue
    for j in range(i+1, len(enemies)):
      if not enemies[j].alive:
        continue
      if (enemies[i].x - enemies[j].x <= 50 and enemies[i].x - enemies[j].x >= -50 and enemies[i].y - enemies[j].y <= 50 and enemies[i].y - enemies[j].y >= -50 and enemies[i].alive == 1 and enemies[j].alive == 1 and enemies[i].size == 50 and enemies[j].size == 50):
        enemies[i].alive = False
        enemies[j].size = 100

      if (enemies[i].x - enemies[j].x <= enemies[j].added and enemies[i].x - enemies[j].x >= -enemies[j].added and enemies[i].y - enemies[j].y <= enemies[j].added and enemies[i].y - enemies[j].y >= -enemies[j].added and enemies[i].alive == 1 and enemies[j].alive == 1 and enemies[i].size == 50 and enemies[j].size == 100):
        enemies[i].alive = False
        enemies[j].size = 150


  for icetile_ in icetiles:
    if (icetile_.x - playercenterX <= 50 and icetile_.x - playercenterX >= -50 and icetile_.y - playercenterY <= 50 and icetile_.y - playercenterY >= -50 and icetile_.alive == 1):
      onice = 1
  for frictiontile_ in frictiontiles:
    if (frictiontile_.x - playercenterX <= 50 and frictiontile_.x - playercenterX >= -50 and frictiontile_.y - playercenterY <= 50 and frictiontile_.y - playercenterY >= -50 and frictiontile_.alive == 1):
      onfriction = 1
  if (onfriction == 1):
    onice = 0
  if(golemenemyactive):
    golemAI()
  mouseX,mouseY = pygame.mouse.get_pos()
  clock.tick(fps)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      #mouse press detector
    if (event.type == pygame.MOUSEBUTTONDOWN):
      clicking = True
    if (event.type == pygame.MOUSEBUTTONUP):
      clicking = False
      #KEY PRESS DETECTOR
    if event.type == pygame.KEYDOWN:
#key detection
      if (event.key == pygame.K_p):
        level += 1
        restart()
      if event.key == pygame.K_w or event.key == pygame.K_UP:
        pressing[1] = "up"
        pressing[2] = 0
      if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        pressing[2] = "down"
        pressing[1] = 0
      if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        pressing[3] = "left"
        pressing[4] = 0
      if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        pressing[4] = "right"
        pressing[3] = 0
      if event.key == pygame.K_SPACE and hasdash == 1:
        pressingdash = 1
      if (event.key == pygame.K_r or dead == 1):
        buttonpressedX = 9000
        enemy1active = 0
        restart()
        playercolor = green
        playerXvelocity = 0
        playerYvelocity = 0
        buttonhorizontalpressedX = 9000
        

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_w or event.key == pygame.K_UP:
        pressing[1] = 0
      if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        pressing[2] = 0
      if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        pressing[3] = 0
      if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        pressing[4] = 0
      if event.key == pygame.K_SPACE:
        pressingdash = 0
    if pressingdash == 1 and pressing[1] == "up" and playercolor == green:
      playerYvelocity -= dashspeed
      dashthingy = 1
    if pressingdash == 1 and pressing[3] == "left" and playercolor == green:
      playerXvelocity -= dashspeed
      dashthingy = 1
    if pressingdash == 1 and pressing[2] == "down" and playercolor == green:
      playerYvelocity += dashspeed
      dashthingy = 1
    if pressingdash == 1 and pressing[4] == "right" and playercolor == green:
      playerXvelocity += dashspeed
      dashthingy = 1

  dashtimer += 1
  if (dashthingy == 1 and playercolor == green):
    playercolor = cyan
    dashtimer = 0
    dashthingy = 0
  if (dashtimer == 20 and playercolor == cyan):
    playercolor = blue
  if (dashtimer >= 120 and playercolor == blue):
    playercolor = green
  if (playercolor == cyan):
    bounce = 10
    dashparticles.append(dashparticle(playercenterX,playercenterY))
    
  else:
    bounce = 2
  if (buttonpressedX == buttonunpressedX and buttonpressedY == buttonunpressedY):
    doorverticalY += 4
  if (buttonhorizontalpressedX == buttonhorizontalunpressedX and buttonhorizontalpressedY == buttonhorizontalunpressedY):
    doorhorizontalX += 4
#organizing functions

  if (playerdies == 1):
    playerdeath()
    playerdies = 0


        
#the players velocity increases based off of acceleration
  if (pressing[1] == "up" and onice == 0):
    playerYvelocity -= acceleration
  if (pressing[2] == "down" and onice == 0):
    playerYvelocity += acceleration
  if (pressing[3] == "left" and onice == 0):
    playerXvelocity -= acceleration
  if (pressing[4] == "right" and onice == 0):
    playerXvelocity += acceleration
  if (pressing[3] == 0 and onice == 0):
    playerXvelocity -= playerXvelocity / friction
  elif(onfriction == 1):
    playerXvelocity -= playerXvelocity / friction * 2
  if (pressing[4] == 0 and onice == 0):
    playerXvelocity -= playerXvelocity / friction
  elif(onfriction == 1):
    playerXvelocity -= playerXvelocity / friction * 2
  if (pressing[2] == 0 and onice == 0):
    playerYvelocity -= playerYvelocity / friction
  elif(onfriction == 1):
    playerYvelocity -= playerYvelocity / friction * 2
  if (pressing[1] == 0 and onice == 0):
    playerYvelocity -= playerYvelocity / friction
  elif(onfriction == 1):
    playerYvelocity -= playerYvelocity / friction * 2
  playercenterY += playerYvelocity
  playercenterX += playerXvelocity

  if (playercenterX >= length - 50):
    playerXvelocity += -bounce
  if (playercenterX <= 0):
    playerXvelocity += bounce
  if (playercenterY >= height - 50):
    playerYvelocity += -bounce
  if (playercenterY <= 0):
    playerYvelocity += bounce


#wallhorizontalcollisions
  if (wallhorizontalX - playercenterX <= 50 and wallhorizontalX - playercenterX >= -800 and wallhorizontalY - playercenterY <= 50 and wallhorizontalY - playercenterY >= 15):
    playerYvelocity -= bounce
  if (wallhorizontalX - playercenterX <= 50 and wallhorizontalX - playercenterX >= -800 and wallhorizontalY - playercenterY >= -50 and wallhorizontalY - playercenterY <= -30):
    playerYvelocity += bounce
  if (wallhorizontalY - playercenterY <= 50 and wallhorizontalY - playercenterY >= -50 and wallhorizontalX - playercenterX <= 50 and wallhorizontalX - playercenterX >= -25):
    playerXvelocity -= bounce
  if (wallhorizontalY - playercenterY <= 50 and wallhorizontalY - playercenterY >= -50 and wallhorizontalX - playercenterX >= -800 and wallhorizontalX - playercenterX <= -775):
    playerXvelocity += bounce

#wallverticalcollisions
  if (wallverticalY - playercenterY <= 50 and wallverticalY - playercenterY >= -800 and wallverticalX - playercenterX <= 50 and wallverticalX - playercenterX >= 15):
    playerXvelocity -= bounce
  if (wallverticalY - playercenterY <= 50 and wallverticalY - playercenterY >= -800 and wallverticalX - playercenterX >= -50 and wallverticalX - playercenterX <= -30):
    playerXvelocity += bounce
  if (wallverticalX - playercenterX <= 50 and wallverticalX - playercenterX >= -50 and wallverticalY - playercenterY <= 50 and wallverticalY - playercenterY >= -25):
    playerYvelocity -= bounce
  if (wallverticalX - playercenterX <= 50 and wallverticalX - playercenterX >= -50 and wallverticalY - playercenterY >= -800 and wallverticalY - playercenterY <= -775):
    playerYvelocity += bounce
#doorverticalcollisions
  if (doorverticalY - playercenterY <= 50 and doorverticalY - playercenterY >= -800 and doorverticalX - playercenterX <= 50 and doorverticalX - playercenterX >= 15):
    playerXvelocity -= bounce
  if (doorverticalY - playercenterY <= 50 and doorverticalY - playercenterY >= -800 and doorverticalX - playercenterX >= -50 and doorverticalX - playercenterX <= -30):
    playerXvelocity += bounce
  if (doorverticalX - playercenterX <= 50 and doorverticalX - playercenterX >= -50 and doorverticalY - playercenterY <= 50 and doorverticalY - playercenterY >= -25):
    playerYvelocity -= bounce
  if (doorverticalX - playercenterX <= 50 and doorverticalX - playercenterX >= -50 and doorverticalY - playercenterY >= -800 and doorverticalY - playercenterY <= -775):
    playerYvelocity += bounce
#door horizontal collisions
  if (doorhorizontalX - playercenterX <= 50 and doorhorizontalX - playercenterX >= -800 and doorhorizontalY - playercenterY <= 50 and doorhorizontalY - playercenterY >= 15):
    playerYvelocity -= bounce
  if (doorhorizontalX - playercenterX <= 50 and doorhorizontalX - playercenterX >= -800 and doorhorizontalY - playercenterY >= -50 and doorhorizontalY - playercenterY <= -30):
    playerYvelocity += bounce
  if (doorhorizontalY - playercenterY <= 50 and doorhorizontalY - playercenterY >= -50 and doorhorizontalX - playercenterX <= 50 and doorhorizontalX - playercenterX >= -25):
    playerXvelocity -= bounce
  if (doorhorizontalY - playercenterY <= 50 and doorhorizontalY - playercenterY >= -50 and doorhorizontalX - playercenterX >= -800 and doorhorizontalX - playercenterX <= -775):
    playerXvelocity += bounce
#teleporter colision
  if (teleporterX - playercenterX <= 50 and teleporterX - playercenterX >= -50 and teleporterY - playercenterY <= 50 and teleporterY - playercenterY >= -50):
    level += 0.5
    buttonhorizontalunpressedX += 9000
    buttonunpressedX += 9000
    doorhorizontalX += 9000
    doorverticalX += 9000
    wallhorizontalX += 9000
    wallverticalX += 9000
    buttonpressedX += 9000
    buttonhorizontalpressedX = 9000
    playerXvelocity = 0; playerYvelocity = 0; playercolor = green
  if (dashcrystalX - playercenterX <= 50 and dashcrystalX - playercenterX >= -50 and dashcrystalY - playercenterY <= 50 and dashcrystalY - playercenterY >= -50):
    hasdash = 1
    dashcrystalX = 9000
    for i in range(40):
      deathparticles.append(deathparticle(random.randint(-5,5), random.randint(-5,5), cyan, 20))
#buttonpressing
  if (buttonunpressedX - playercenterX <= 50 and buttonunpressedX - playercenterX >= -50 and buttonunpressedY - playercenterY <= 50 and buttonunpressedY - playercenterY >= -50 and buttonunpressedX != buttonpressedX):
    buttonpressedX = buttonunpressedX
    buttonpressedY = buttonunpressedY
    for i in range(30):
      deathparticles.append(deathparticle(random.randint(-5,5), random.randint(-5, 5), gray, random.randint(2,20)))
  if (buttonhorizontalunpressedX - playercenterX <= 50 and buttonhorizontalunpressedX - playercenterX >= -50 and buttonhorizontalunpressedY - playercenterY <= 50 and buttonhorizontalunpressedY - playercenterY >= -50 and buttonhorizontalunpressedX != buttonhorizontalpressedX):
    buttonhorizontalpressedX = buttonhorizontalunpressedX
    buttonhorizontalpressedY = buttonhorizontalunpressedY
    for i in range(30):
      deathparticles.append(deathparticle(random.randint(-5,5), random.randint(-5, 5), gray, random.randint(2,20)))
#warning menu button clicking
  if (clicking == True and mouseX >= 35 and mouseX <= 560 and mouseY >= 480 and mouseY <= 505 and warningisopen == 1):
    warningisopen = 0
  if (clicking == True and mouseX >= 180 and mouseX <= 370 and mouseY >= 380 and mouseY <= 430 and warningisopen == 0 and menuisopen == 1): 
    menuisopen = 0
    level = 0.5
    enemy1active = 0
  if (menuisopen == 1):
    height = 600
    width = 600
  if (enemy1active == False):
    enemy1X = 9000
  

#levelloading
  if (level == 0.5 and menuisopen == 0):
    teleporterX =100; teleporterY =400
    playercenterX=400;playercenterY =0
    height = 500; length = 250
    levelprogress()
  elif (level == 1.5):
    teleporterX =100; teleporterY = 75
    playercenterX=100; playercenterY = 400
    height = 500; length = 250
    levelprogress()
  elif (level == 2.5):
    playercenterX = 100; playercenterY = 75
    teleporterX = 435; teleporterY = 75
    wallverticalX =270; wallverticalY =100
    height = 250;length = 500
    levelprogress()
  elif (level == 3.5):
    wallverticalX =270; wallverticalY =100
    wallhorizontalX = 100; wallhorizontalY = 270
    playercenterX = 435; playercenterY = 75
    teleporterX =100; teleporterY =400
    levelprogress()
    voidtiles.append(voidtile(450,450))
    voidtiles.append(voidtile(400,450))
    voidtiles.append(voidtile(450,400))
    voidtiles.append(voidtile(400,400))
    voidtiles.append(voidtile(350,400))
    voidtiles.append(voidtile(400,350))
    voidtiles.append(voidtile(350,350))
    voidtiles.append(voidtile(350,450))
    voidtiles.append(voidtile(450,350))
    voidtiles.append(voidtile(300,300))
    voidtiles.append(voidtile(300,350))
    voidtiles.append(voidtile(300,400))
    voidtiles.append(voidtile(300,450))
    voidtiles.append(voidtile(350,300))
    voidtiles.append(voidtile(400,300))
    voidtiles.append(voidtile(450,300))
    height = 500
    length = 500
  elif (level == 4.5):
    doorverticalX = 400; doorverticalY = -50
    playercenterX = 10; playercenterY = 25
    teleporterX = 500; teleporterY = 25
    height = 100
    length = 800
    buttonunpressedX = 280; buttonunpressedY = 25
    levelprogress()
  elif (level == 5.5):
    doorverticalX = 900
    length = 100
    height = 600
    buttonunpressedX = 900
    playercenterX = 20; playercenterY = 25
    teleporterX = 10; teleporterY = 550
    doorhorizontalX= -20; doorhorizontalY = 500
    buttonhorizontalunpressedX = 20; buttonhorizontalunpressedY = 450
    levelprogress()
  elif (level == 6.5):
    levelprogress()
    length = 500
    height = 500
    playercenterX = 10
    playercenterY = 450
    teleporterX = 447
    teleporterY = 6
    enemies.append(enemy(337,100,0))
  elif(level == 7.5):
    length = 500
    height = 250
    playercenterX = 447
    playercenterY = 6
    teleporterX = 0
    teleporterY = 126
    levelprogress()
    enemies.append(enemy(0,126,0))
  elif(level == 8.5):
    length =400
    height = 600
    playercenterX = 0
    playercenterY = 176
    enemy1X = 0
    enemy1Y = 26
    enemy1active = 1
    wallverticalX = 150
    wallverticalY = -270
    teleporterX = 310
    teleporterY = 44
    levelprogress()
    enemies.append(enemy(0,26,0))
  elif(level == 9.5):
    length =400
    height =600
    doorverticalX = 150
    doorverticalY = -50
    playercenterX = 310
    playercenterY = 44
    buttonunpressedX = 240
    buttonunpressedY = 430
    teleporterX=0
    teleporterY = 500
    enemy1X = 0
    enemy1Y = 176
    enemy1active = 1
    levelprogress()
    enemies.append(enemy(0,176,0))
  elif(level == 10.5):
    height = 100
    length = 600
    playercenterX =0
    playercenterY = 0
    enemy1active = 0
    teleporterX = 550
    teleporterY = 27
    hasdash = 0
    dashcrystalX = 313
    dashcrystalY = 20
    levelprogress()
  elif(level == 11.5):
    height =100
    length = 600
    playercenterX = 550
    playercenterY = 27
    teleporterX = 0
    teleporterY = 0
    hasdash = 1
    enemy1active = 1
    enemy1X = 0
    enemy1Y = 0
    levelprogress()
    enemies.append(enemy(0,0,0))
  elif(level == 12.5):
    levelprogress()
    height = 600
    length = 600
    playercenterX = 0
    playercenterY = 0
    doorverticalX = 75
    doorverticalY = 0
    buttonunpressedX = 0
    buttonunpressedY = 550
    teleporterX = 550
    teleporterY = 550
    enemies.append(enemy(550,0,0))
    enemies.append(enemy(0,550,0))
    multiplenemies = 1
    icetiles.append(icetile(0,540))
    icetiles.append(icetile(0,490))
    icetiles.append(icetile(0,440))
    icetiles.append(icetile(0,390))
    icetiles.append(icetile(0,340))
    icetiles.append(icetile(0,290))
    icetiles.append(icetile(0,240))
    icetiles.append(icetile(0,190))
    icetiles.append(icetile(0,140))
    icetiles.append(icetile(0,90))
  elif(level == 13.5):
    level = 14.5
  elif(level == 14.5):
    height =600
    length = 600
    playercenterX = 0
    playercenterY = 0
    golemenemyX = 533 
    golemenemyY = 319
    enemy1active = 0
    golemenemyactive = 1
    teleporterX =550
    teleporterY = 550
    levelprogress()
  elif(level == 15.5):
    height = 600
    length = 110
    playercenterX =0
    playercenterY = 0
    golemenemyactive = 1
    golemenemyX = 0
    golemenemyY = 420
    teleporterX=0
    teleporterY = 420
    wallverticalX = 60
    wallverticalY = -260
    levelprogress()
  elif(level == 16.5):
    height = 600
    length = 455
    playercenterX = 0
    playercenterY = 0
    wallverticalX = 250
    wallverticalY = -275
    golemenemyactive = 0
    golemenemyX = 9000
    teleporterX =352; teleporterY =0
    levelprogress()
    spikes.append(spike(200,0,spikeleft))
    spikes.append(spike(200,50,spikeleft))
    spikes.append(spike(200,100,spikeleft))
    spikes.append(spike(200,150,spikeleft))
    spikes.append(spike(200,200,spikeleft))
    spikes.append(spike(200,250,spikeleft))
    spikes.append(spike(200,300,spikeleft))
    spikes.append(spike(200,350,spikeleft))
    spikes.append(spike(200,400,spikeleft))
    spikes.append(spike(200,450,spikeleft))
    spikes.append(spike(200,470,spikeleft))

    spikes.append(spike(300,0,spikeright))
    spikes.append(spike(300,50,spikeright))
    spikes.append(spike(300,100,spikeright))
    spikes.append(spike(300,150,spikeright))
    spikes.append(spike(300,200,spikeright))
    spikes.append(spike(300,250,spikeright))
    spikes.append(spike(300,300,spikeright))
    spikes.append(spike(300,350,spikeright))
    spikes.append(spike(300,400,spikeright))
    spikes.append(spike(300,450,spikeright))
    spikes.append(spike(300,470,spikeright))

    spikes.append(spike(405,0,spikeleft))
    spikes.append(spike(405,50,spikeleft))
    spikes.append(spike(405,100,spikeleft))
    spikes.append(spike(405,150,spikeleft))
    spikes.append(spike(405,200,spikeleft))
    spikes.append(spike(405,250,spikeleft))
    spikes.append(spike(405,300,spikeleft))
    spikes.append(spike(405,350,spikeleft))
    spikes.append(spike(405,400,spikeleft))
    spikes.append(spike(405,450,spikeleft))
    spikes.append(spike(405,500,spikeleft))
  
  elif(level == 17.5):
    length = 600
    height = 625
    wallverticalX = 250
    wallverticalY = -275
    doorverticalX = 250
    doorverticalY = -150
    playercenterX =352
    playercenterY = 0
    teleporterX = 0
    teleporterY = 0
    buttonunpressedX = 505
    buttonunpressedY=5
    levelprogress()
    spikes.append(spike(200,0,spikeleft))
    spikes.append(spike(200,50,spikeleft))
    spikes.append(spike(200,100,spikeleft))
    spikes.append(spike(200,150,spikeleft))
    spikes.append(spike(200,200,spikeleft))
    spikes.append(spike(200,250,spikeleft))
    spikes.append(spike(200,300,spikeleft))
    spikes.append(spike(200,350,spikeleft))
    spikes.append(spike(200,400,spikeleft))
    spikes.append(spike(200,450,spikeleft))
    spikes.append(spike(200,470,spikeleft))

    spikes.append(spike(300,0,spikeright))
    spikes.append(spike(300,50,spikeright))
    spikes.append(spike(300,100,spikeright))
    spikes.append(spike(300,150,spikeright))
    spikes.append(spike(300,200,spikeright))
    spikes.append(spike(300,250,spikeright))
    spikes.append(spike(300,300,spikeright))
    spikes.append(spike(300,350,spikeright))
    spikes.append(spike(300,400,spikeright))
    spikes.append(spike(300,450,spikeright))
    spikes.append(spike(300,470,spikeright))

    spikes.append(spike(405,0,spikeleft))
    spikes.append(spike(405,50,spikeleft))
    spikes.append(spike(405,100,spikeleft))
    spikes.append(spike(405,150,spikeleft))
    spikes.append(spike(405,200,spikeleft))
    spikes.append(spike(405,250,spikeleft))
    spikes.append(spike(405,300,spikeleft))
    spikes.append(spike(405,350,spikeleft))
    spikes.append(spike(405,400,spikeleft))
    spikes.append(spike(405,450,spikeleft))
    spikes.append(spike(405,500,spikeleft))

    spikes.append(spike(455,-1,spikeright))
    spikes.append(spike(455,49,spikeright))
    spikes.append(spike(455,99,spikeright))
    spikes.append(spike(455,149,spikeright))
    spikes.append(spike(455,199,spikeright))
    spikes.append(spike(455,249,spikeright))
    spikes.append(spike(455,299,spikeright))
    spikes.append(spike(455,349,spikeright))
    spikes.append(spike(455,399,spikeright))
    spikes.append(spike(455,449,spikeright))
    spikes.append(spike(455,499,spikeright))

    icetiles.append(icetile(455,0))
    icetiles.append(icetile(455,50))
    icetiles.append(icetile(455,100))
    icetiles.append(icetile(455,150))
    icetiles.append(icetile(455,200))
    icetiles.append(icetile(455,250))
    icetiles.append(icetile(455,300))
    icetiles.append(icetile(455,350))
    icetiles.append(icetile(455,400))
    icetiles.append(icetile(455,450))
    icetiles.append(icetile(455,500))

    icetiles.append(icetile(505,0))
    icetiles.append(icetile(505,50))
    icetiles.append(icetile(505,100))
    icetiles.append(icetile(505,150))
    icetiles.append(icetile(505,200))
    icetiles.append(icetile(505,250))
    icetiles.append(icetile(505,300))
    icetiles.append(icetile(505,350))
    icetiles.append(icetile(505,400))
    icetiles.append(icetile(505,450))
    icetiles.append(icetile(505,500))

    icetiles.append(icetile(555,0))
    icetiles.append(icetile(555,50))
    icetiles.append(icetile(555,100))
    icetiles.append(icetile(555,150))
    icetiles.append(icetile(555,200))
    icetiles.append(icetile(555,250))
    icetiles.append(icetile(555,300))
    icetiles.append(icetile(555,350))
    icetiles.append(icetile(555,400))
    icetiles.append(icetile(555,450))
    icetiles.append(icetile(555,500))

    frictiontiles.append(frictiontile(455,550))
    frictiontiles.append(frictiontile(505,550))
    frictiontiles.append(frictiontile(555,550))
  elif(level==18.5):
    length = 600
    height = 150
    playercenterX= 1
    playercenterY = 1
    teleporterX = 500
    teleporterY = 100
    levelprogress()
    spikes.append(spike(550,0, spikeleft))
    icetiles.append(icetile(100,0))
    icetiles.append(icetile(150,0))
    icetiles.append(icetile(200,0))
    icetiles.append(icetile(250,0))
    icetiles.append(icetile(300,0))
    icetiles.append(icetile(350,0))
    icetiles.append(icetile(400,0))
    icetiles.append(icetile(450,0))
    icetiles.append(icetile(500,0))
    icetiles.append(icetile(550,0))
    icetiles.append(icetile(100,50))
    icetiles.append(icetile(150,50))
    icetiles.append(icetile(200,50))
    icetiles.append(icetile(250,50))
    icetiles.append(icetile(300,50))
    icetiles.append(icetile(350,50))
    icetiles.append(icetile(400,50))
    icetiles.append(icetile(450,50))
    icetiles.append(icetile(500,50))
    icetiles.append(icetile(550,50))
    icetiles.append(icetile(100,100))
    icetiles.append(icetile(150,100))
    icetiles.append(icetile(200,100))
    icetiles.append(icetile(250,100))
    icetiles.append(icetile(300,100))
    spikes.append(spike(300,100,spikeup))
    icetiles.append(icetile(350,100))
    icetiles.append(icetile(400,100))
    icetiles.append(icetile(450,100))
    icetiles.append(icetile(550,100))
  elif(level == 19.5):
    playercenterX =0 ;playercenterY = 0
    teleporterX = 300
    teleporterY = 1
    height = 95
    length = 500
    golemenemyactive = 1
    golemenemyX = 450
    golemenemyY = 1
    levelprogress()
  elif(level == 20.5):
    teleporterX = 2000
    teleporterY = 2000
    youbeatthegame = 1
    length = 300
    height = 300
    levelprogress()
    

  scr.fill((white))
    
  
  scr.blit(floor1, (floor1X, floor1Y))
  for voidtile_ in voidtiles:
    voidtile_.draw(scr)
  for icetile_ in icetiles:
    icetile_.draw(scr)
  for frictiontile_ in frictiontiles:
    frictiontile_.draw(scr)
  for spike_ in spikes:
    spike_.draw(scr)
  for dashparticle_ in dashparticles:
    dashparticle_.draw(scr)  
  for deathparticle_ in deathparticles:
    deathparticle_.draw(scr)
  scr.blit(buttonunpressed,(buttonunpressedX,buttonunpressedY))
  scr.blit(buttonpressed, (buttonpressedX, buttonpressedY))
  scr.blit(buttonhorizontalunpressed,(buttonhorizontalunpressedX,buttonhorizontalunpressedY))
  scr.blit(buttonhorizontalpressed, (buttonhorizontalpressedX, buttonhorizontalpressedY))
  pygame.draw.rect(scr,playercolor,(playercenterX,playercenterY,50,50))
  scr.blit(face,(playercenterX, playercenterY))
  scr.blit(wallhorizontal,(wallhorizontalX,wallhorizontalY))
  scr.blit(wallvertical, (wallverticalX, wallverticalY))
  scr.blit(doorvertical,(doorverticalX,doorverticalY))
  scr.blit(doorhorizontal, (doorhorizontalX,doorhorizontalY))
  scr.blit(teleporter, (teleporterX, teleporterY))
  scr.blit(dashcrystal, (dashcrystalX, dashcrystalY))
  for enemy_ in enemies:
    enemy_.draw(scr)
  scr.blit(golemenemy,(golemenemyX,golemenemyY))
  if (menuisopen == 1):
    scr.blit(mainmenu,(0,0))
  if (warningisopen == 1):
    scr.blit(menuwarning, (0,0))
  if (youbeatthegame == 1):
    scr.blit(endscreen, (0,0))
  pygame.display.flip()
  pygame.display.update()
pygame.quit()
