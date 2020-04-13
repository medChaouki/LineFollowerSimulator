import pygame
import neat
import time
import os
import random
import pickle
import math

WIN_WIDTH = 1000
WIN_HEIGHT = 1000

CAR_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imgs","mustang.png")),(50,100)),-90)
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","BG.png")),(3000,3000))

class Car:

  def __init__(self,x,y):
    self.x =x
    self.y =y
    self.trackWidth = 50
    self.rotation = 0
    self.img = CAR_IMG
    self.originalImg = self.img

  def rotateCar(self,rotAngle):
    self.rotation += rotAngle
    if (self.rotation >0):
      self.rotation = self.rotation % 360
    else :
      self.rotation = -self.rotation
      self.rotation = self.rotation % 360
      self.rotation = -self.rotation

    rotated_image = pygame.transform.rotate(self.originalImg, -self.rotation)
    old_rect = self.img.get_rect(topleft = (int(self.x),int(self.y)))
    new_rect = rotated_image.get_rect(center=old_rect.center)
    self.img = rotated_image
    self.x = (new_rect.topleft[0])
    self.y = (new_rect.topleft[1])
    #print("self.rotation")
    #print(self.rotation)

  def advance(self,distance):
    self.x += distance* math.cos(math.radians(self.rotation))
    self.y += distance* math.sin(math.radians(self.rotation))

  def move(self,dLeft,dRight):
    d= (dLeft+dRight)/2

    if abs(dRight-dLeft)<0.001:
      turningRadius = 9999999999
    else:
      turningRadius = -(self.trackWidth/2)*((dRight+dLeft)/(dRight-dLeft))

    deltaAngle = math.degrees(-(dRight-dLeft)/self.trackWidth)
    print("deltaAngle")
    print(deltaAngle)

    self.rotateCar(deltaAngle)
    self.advance(d)


  def draw(self,win):
    win.blit(self.img, (self.x, self.y))


def draw_window(win,car):
  
  win.blit(BG_IMG, (0, 0))
  car.draw(win)
  pygame.display.update()

def main():
  car= Car(0,50)
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
      #car.rotateCar(-10)
      car.move(0,10)
    elif (keyPressed[pygame.K_RIGHT] ==True):
      #car.rotateCar(10)
      car.move(10,0)
    if(keyPressed[pygame.K_UP] ==True ):
      #car.advance(10)
      car.move(10,10)
    elif (keyPressed[pygame.K_DOWN] ==True):
      #car.advance(-10)
      car.move(-10,-10)
    elif (keyPressed[pygame.K_SPACE] ==True):
      #car.advance(-10)
      car.move(10,-10)




    draw_window(win,car)

main()