import pygame
import neat
import time
import os
import random
import pickle
import math

WIN_WIDTH = 700
WIN_HEIGHT = 700

CAR_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imgs","mustang.png")),(50,100)),-90)
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","BG.png")),(700,700))

class Car:

  def __init__(self,x,y):
    self.x =x
    self.y =y
    self.length = 100
    self.SensorsWidth = 50
    self.trackWidth = 50
    self.rotation = 0
    self.img = CAR_IMG
    self.originalImg = self.img
    self.distanceTraveled  =0

  def rotateCar(self,rotAngle):
    self.rotation += rotAngle
    if (self.rotation >0):
      self.rotation = self.rotation % 360
    else :
      self.rotation = -self.rotation
      self.rotation = self.rotation % 360
      self.rotation = -self.rotation

    rotated_image = pygame.transform.rotate(self.originalImg, -self.rotation)
    old_rect = self.img.get_rect(topleft = ((self.x),(self.y)))
    new_rect = rotated_image.get_rect(center=old_rect.center)
    self.img = rotated_image
    self.x = float(new_rect.topleft[0])
    self.y = float(new_rect.topleft[1])

  def getCenter(self):

    return self.img.get_rect(topleft = (int(self.x),int(self.y))).center

  def getFrontLeftCarSensorPosition(self):
    returnVal=(0,0)
    x=  (self.length)/2
    y= -(self.SensorsWidth)/2
    teta = math.radians(self.rotation)
    x1=(x*math.cos(teta)-y*math.sin(teta))
    y1=(x*math.sin(teta)+y*math.cos(teta)) 
    x1+=self.getCenter()[0]
    y1+=self.getCenter()[1]
    returnVal=int(x1),int(y1)
    return returnVal

  def getFrontCenterLeftCarSensorPosition(self):
    returnVal=(0,0)
    x=  (self.length)/2
    y= -(self.SensorsWidth)*1/4
    teta = math.radians(self.rotation)
    x1=(x*math.cos(teta)-y*math.sin(teta))
    y1=(x*math.sin(teta)+y*math.cos(teta)) 
    x1+=self.getCenter()[0]
    y1+=self.getCenter()[1]
    returnVal=int(x1),int(y1)
    return returnVal

  def getFrontRightCarSensorPosition(self):
    returnVal=(0,0)
    x=  (self.length)/2
    y=  (self.SensorsWidth)/2
    teta = math.radians(self.rotation)
    x1=(x*math.cos(teta)-y*math.sin(teta))
    y1=(x*math.sin(teta)+y*math.cos(teta)) 
    x1+=self.getCenter()[0]
    y1+=self.getCenter()[1]
    returnVal=int(x1),int(y1)
    return returnVal

  def getFrontCenterRightCarSensorPosition(self):
    returnVal=(0,0)
    x=  (self.length)/2
    y=  (self.SensorsWidth)*1/4
    teta = math.radians(self.rotation)
    x1=(x*math.cos(teta)-y*math.sin(teta))
    y1=(x*math.sin(teta)+y*math.cos(teta)) 
    x1+=self.getCenter()[0]
    y1+=self.getCenter()[1]
    returnVal=int(x1),int(y1)
    return returnVal

  def getFrontCenterCarSensorPosition(self):
    returnVal=(0,0)
    x=  (self.length)/2
    y=  0
    teta = math.radians(self.rotation)
    x1=(x*math.cos(teta)-y*math.sin(teta))
    y1=(x*math.sin(teta)+y*math.cos(teta)) 
    x1+=self.getCenter()[0]
    y1+=self.getCenter()[1]
    returnVal=int(x1),int(y1)
    return returnVal

  def getCarSensorValue(self,sensorPosition):
    returnVal=0
    startX = sensorPosition[0]-3
    endX = sensorPosition[0]+3
    startY = sensorPosition[1]-3
    endY = sensorPosition[1]+3
    for x in range(startX,endX):
      for y in range(startY,endY):
        if (BG_IMG.get_at((x,y))==(0,0,0,255)):
          returnVal = 1
          break

    return returnVal

  def getDistance(self):

    return self.distanceTraveled

  def advance(self,distance):
    dx= distance* (math.cos(math.radians(self.rotation)))
    dy= distance* (math.sin(math.radians(self.rotation)))
    if (dx >0):
      dx = math.ceil(dx)
    else:
      dx = - (math.ceil(-dx))
    if (dy >0):
      dy = math.ceil(dy)
    else:
      dy = - (math.ceil(-dy))
    self.x = round(self.x,2) + round(dx,2)
    self.y = round(self.y,2) + round(dy,2)
    print(self.x)
    print(self.y)

  def move(self,dLeft,dRight):
    d= (dLeft+dRight)/2

    if abs(dRight-dLeft)<0.0001:
      turningRadius = 9999999999
    else:
      turningRadius = -(self.trackWidth/2)*((dRight+dLeft)/(dRight-dLeft))

    deltaAngle = math.degrees(-(dRight-dLeft)/self.trackWidth)
    self.rotateCar(deltaAngle)
    self.advance(d)
    self.distanceTraveled += d

  def drawSensors(self,win):
    pygame.draw.line(win,(255,25,0),self.getFrontLeftCarSensorPosition(),self.getFrontRightCarSensorPosition(),10)
    pygame.draw.circle(win,(0,0,255),self.getFrontLeftCarSensorPosition(),3,3)
    pygame.draw.circle(win,(0,0,255),self.getFrontRightCarSensorPosition(),3,3)
    pygame.draw.circle(win,(0,0,255),self.getFrontCenterCarSensorPosition(),3,3)
    pygame.draw.circle(win,(0,0,255),self.getFrontCenterLeftCarSensorPosition(),3,3)
    pygame.draw.circle(win,(0,0,255),self.getFrontCenterRightCarSensorPosition(),3,3)

  def draw(self,win):
    win.blit(self.img, (self.x, self.y))
    self.drawSensors(win)

    



def draw_window(win,car):
  
  win.blit(BG_IMG, (0, 0))
  pygame.draw.rect(win,(50,0,0),car.img.get_rect(topleft=(car.x,car.y)))
  car.draw(win)
  #print("------------")
  #print(pygame.mouse.get_pos())
  #print((car.x,car.y))
  pygame.display.update()



def main():
  car= Car(0.0,50.0)
  win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
  clock = pygame.time.Clock()
  run = True
  keyNotPressedBefore = False
  while run :
    clock.tick(40)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          run = False
          pygame.quit()
          quit()

    keyPressed = pygame.key.get_pressed()
    if (keyPressed[pygame.K_LEFT] ==True):
      car.move(0,5)
    elif (keyPressed[pygame.K_RIGHT] ==True):
      car.move(5,0)
    if(keyPressed[pygame.K_UP] ==True ):
      car.move(2,2)
    elif (keyPressed[pygame.K_DOWN] ==True):
      car.move(-2,-2)
    elif (keyPressed[pygame.K_SPACE] ==True):
      car.move(5,-5)




    draw_window(win,car)

main()