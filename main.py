
########                                   ########
####                                           ####
##            Funny square game                  ##
#                                                 #
#            WOAH!! this is VERY messy CODE!!     #
#    and im not explaining how it works either :D #
#      TRY TO MOD AT YOUR OWN RISK LMAO           #
##                                               ##
####                                           ####
########                                   ########

#setting up pygame
import pygame
from pygame import mixer
pygame.init()
height = 600
length = 600
scr = pygame.display.set_mode((length,height))
running = True

#creating a library of preset colors to use
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
green = (3, 68, 1)
cyan = (0,255,255)

#setting up the icon for the game
icon= pygame.image.load('reallybruh.png')
pygame.display.set_icon(icon)

#player data
playercolor = green
playercenterX = 400
playercenterY = 0
playerXvelocity = 0
playerYvelocity = 0
#floor pattern
floor1 = pygame.image.load("floor1.png")
floor1X = 0
floor1Y = 0

#wall that is sideways data
wallhorizontal = pygame.image.load("wall horizontal.png")
wallhorizontalX = 0
wallhorizontalY = -900

#wall that is standing up data
wallvertical = pygame.image.load("wall vertical.png")
wallverticalX = 300
wallverticalY = 200

#door that is sideways data
doorhorizontal = pygame.image.load("doorhorizontal.png")
doorhorizontalX = 900
doorhorizontalY = 900

#door that is standing up data
doorvertical = pygame.image.load("doorvertical.png")
doorverticalX = 900
doorverticalY = 900

#teleporter data
teleporter = pygame.image.load("teleporter.png")
teleporterX = 900
teleporterY = 900

#button pressed texture
buttonpressed = pygame.image.load("button pressed.png")
buttonpressedX = 9000
buttonpressedY = 900

#buttonunpressed texture
buttonunpressed = pygame.image.load("button unpressed.png")
buttonunpressedX = 900
buttonunpressedY = 900

buttonhorizontalpressed = pygame.image.load("button pressed.png")
buttonhorizontalpressedX = 900
buttonhorizontalpressedY = 9000

buttonhorizontalunpressed = pygame.image.load("button unpressed.png")
buttonhorizontalunpressedX = 900
buttonhorizontalunpressedY = 900

menuwarning = pygame.image.load("warning message.png")
mainmenu = pygame.image.load("menu 2.png")

face = pygame.image.load("goofy ahh face.png")





level = 0.5
acceleration = 0.2
friction = 15
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

pressing = [0,0,0,0,0,0,0,0,0,0]
fps = 60
pygame.display.set_caption("Funny square game :)")
clock = pygame.time.Clock()
mixer.music.load("Skyarmor - game track 4.mp3")
mixer.music.play(-1)

  
while running:
  mouseX,mouseY = pygame.mouse.get_pos()
  scr = pygame.display.set_mode((length,height))
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
        level += 0.5
      if event.key == pygame.K_w or event.key == pygame.K_UP:
        pressing[1] = "up"
      elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
        pressing[2] = "down"
      elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
        pressing[3] = "left"
      elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        pressing[4] = "right"
      if event.key == pygame.K_SPACE:
        pressingdash = 1
      if (event.key == pygame.K_r or dead == 1):
        buttonpressedX = 9000
        level -= 0.5
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
  else:
    bounce = 2
  if (buttonpressedX == buttonunpressedX and buttonpressedY == buttonunpressedY):
    doorverticalY += 4
  if (buttonhorizontalpressedX == buttonhorizontalunpressedX and buttonhorizontalpressedY == buttonhorizontalunpressedY):
    doorhorizontalX += 4


        
#the players velocity increases based off of acceleration
  if (pressing[1] == "up"):
    playerYvelocity -= acceleration
  if (pressing[2] == "down"):
    playerYvelocity += acceleration
  if (pressing[3] == "left"):
    playerXvelocity -= acceleration
  if (pressing[4] == "right"):
    playerXvelocity += acceleration
  if (pressing[3] == 0):
    playerXvelocity -= playerXvelocity / friction
  if (pressing[4] == 0):
    playerXvelocity -= playerXvelocity / friction
  if (pressing[2] == 0):
    playerYvelocity -= playerYvelocity / friction
  if (pressing[1] == 0):
    playerYvelocity -= playerYvelocity / friction
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
#buttonpressing
  if (buttonunpressedX - playercenterX <= 50 and buttonunpressedX - playercenterX >= -50 and buttonunpressedY - playercenterY <= 50 and buttonunpressedY - playercenterY >= -50):
    buttonpressedX = buttonunpressedX
    buttonpressedY = buttonunpressedY
  if (buttonhorizontalunpressedX - playercenterX <= 50 and buttonhorizontalunpressedX - playercenterX >= -50 and buttonhorizontalunpressedY - playercenterY <= 50 and buttonhorizontalunpressedY - playercenterY >= -50):
    buttonhorizontalpressedX = buttonhorizontalunpressedX
    buttonhorizontalpressedY = buttonhorizontalunpressedY
#warning menu button clicking
  if (clicking == True and mouseX >= 35 and mouseX <= 560 and mouseY >= 480 and mouseY <= 505 and warningisopen == 1):
    warningisopen = 0
  if (clicking == True and mouseX >= 180 and mouseX <= 370 and mouseY >= 380 and mouseY <= 430 and warningisopen == 0 and menuisopen == 1):
    menuisopen = 0
  

#levelloading
  if (level == 0.5 and menuisopen == 0):
    teleporterX =100; teleporterY =400
    playercenterX=400;playercenterY =0
    height = 500; length = 250
    level = 1
  elif (level == 1.5):
    teleporterX =100; teleporterY = 75
    playercenterX=100; playercenterY = 400
    height = 500; length = 250
    level = 2
  elif (level == 2.5):
    playercenterX = 100; playercenterY = 75
    teleporterX = 435; teleporterY = 75
    wallverticalX =270; wallverticalY =100
    height = 250;length = 500
    level = 3
  elif (level == 3.5):
    wallverticalX =270; wallverticalY =100
    wallhorizontalX = 100; wallhorizontalY = 270
    playercenterX = 435; playercenterY = 75
    teleporterX =100; teleporterY =400
    height = 500
    length = 500
    level = 4
  elif (level == 4.5):
    doorverticalX = 400; doorverticalY = -50
    playercenterX = 10; playercenterY = 25
    teleporterX = 500; teleporterY = 25
    height = 100
    length = 800
    buttonunpressedX = 280; buttonunpressedY = 25
    level = 5
  elif (level == 5.5):
    doorverticalX = 900
    length = 100
    height = 600
    buttonunpressedX = 900
    playercenterX = 20; playercenterY = 25
    teleporterX = 10; teleporterY = 550
    doorhorizontalX= -20; doorhorizontalY = 500
    buttonhorizontalunpressedX = 20; buttonhorizontalunpressedY = 450
    level = 6
  elif (level == 6.5):
    length = 500
    height = 500
    playercenterX = 10
    playercenterY = 450
    teleporterX = 447
    teleporterY = 6
    level = 7

  if (menuisopen == 0):
    print(playercenterX, playercenterY)
  if (menuisopen == 1):
    print(mouseX, mouseY, warningisopen, menuisopen)
  scr.fill((white))
    
  
  scr.blit(floor1, (floor1X, floor1Y))
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
  if (menuisopen == 1):
    scr.blit(mainmenu,(0,0))
  if (warningisopen == 1):
    scr.blit(menuwarning, (0,0))
  pygame.display.flip()
pygame.quit()
