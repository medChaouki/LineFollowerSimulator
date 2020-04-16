import pygame
import neat
import time
import os
import random
import pickle
import math
import visualize

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans",50)

WIN_WIDTH = 700
WIN_HEIGHT = 700

CAR_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imgs","mustang.png")),(50,100)),-90)
TRACK_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","BG.png")),(700,700))

END_OF_LINE_COLOR =(0,255,0,255)

MAX_OUT_OF_LINE = 10

OUT_OF_LINE_PENALTY = 1

FINISH_BONUS = 1000

MAX_TIME_IN_SECONDS = 10
FPS = 30
MAX_TIME = MAX_TIME_IN_SECONDS*(FPS) 

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
    self.carSensorPositions=[self.getFrontLeftCarSensorPosition(),self.getFrontCenterLeftCarSensorPosition()
                             ,self.getFrontCenterCarSensorPosition(),self.getFrontCenterRightCarSensorPosition(),self.getFrontRightCarSensorPosition()]
    self.lastDistance  =0
    self.nbOfOutOfLineDetection = 0
    self.isActive = True

  def outOfTrack(self):
    trackRect =  TRACK_IMG.get_rect(topleft =(0,0))
    carRect = self.img.get_rect(topleft = ((self.x),(self.y)))
    carRect = carRect.inflate(12,12)
    if trackRect.contains(carRect) == True:
      return False
    else:
      return True

  def incrementOutOfLineDetection(self):

    self.nbOfOutOfLineDetection +=1

  def getOutOfLineDetection(self):

    return self.nbOfOutOfLineDetection 

  def isTheCarActive(self):

    return self.isActive

  def deactivate(self):

    self.isActive = False

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
        if (TRACK_IMG.get_at((x,y))==(0,0,0,255)):
          returnVal = 1
          break

    return returnVal

  def isCarIsOutOfLine(self):
    returnVal = True
    for p in self.carSensorPositions:
      if self.getCarSensorValue(p) == 1:
        returnVal = False
        break
    return returnVal

  def isCarIsAtTheFinishLine(self):
    returnVal = False
    for p in self.carSensorPositions:
      if (TRACK_IMG.get_at(p)== END_OF_LINE_COLOR):
        returnVal = True
        break
    return returnVal

  def getLastDistance(self):

    return self.lastDistance

  def advance(self,distance):
    dx= distance* (math.cos(math.radians(self.rotation)))
    dy= distance* (math.sin(math.radians(self.rotation)))

    if (abs(dx)<0.3):
      dx = 0
    elif (dx >0):
      dx = math.ceil(dx)
    else:
      dx = (math.floor(dx))

    if (abs(dy)<0.3):
      dy = 0
    elif (dy >0):
      dy = math.ceil(dy)
    else:
      dy = (math.floor(dy))
    self.x = round(self.x,2) + round(dx,2)
    self.y = round(self.y,2) + round(dy,2)

  def move(self,dLeft,dRight):
    d= (dLeft+dRight)/2

    if abs(dRight-dLeft)<0.0001:
      turningRadius = 9999999999
    else:
      turningRadius = -(self.trackWidth/2)*((dRight+dLeft)/(dRight-dLeft))

    deltaAngle = math.degrees(-(dRight-dLeft)/self.trackWidth)
    self.rotateCar(deltaAngle)
    self.advance(d)
    self.lastDistance = d
    self.carSensorPositions=[self.getFrontLeftCarSensorPosition(),self.getFrontCenterLeftCarSensorPosition()
                             ,self.getFrontCenterCarSensorPosition(),self.getFrontCenterRightCarSensorPosition(),self.getFrontRightCarSensorPosition()]

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

    



def draw_window(win,cars,timeValue):
  
  text = STAT_FONT.render("Score: "+str(timeValue),1,(0,0,0))
  
  win.blit(TRACK_IMG, (0, 0))
  win.blit(text, (10,10))
  

  for car in cars:
    car.draw(win)

  pygame.display.update()



def trainingFunction(genomes, config):
  win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
  clock = pygame.time.Clock()
  run = True
  ge=[]
  nets=[]
  cars=[]
  timeCounter = 0

  for _,g in genomes:
    net = neat.nn.FeedForwardNetwork.create(g, config)
    nets.append(net)
    cars.append(Car(30,50))
    g.fitness = 0
    ge.append(g)

  while (run == True):
    clock.tick(FPS)
    timeCounter+=1

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
        quit() 
    keyPressed = pygame.key.get_pressed()
    if (keyPressed[pygame.K_ESCAPE] ==True):
      run = False
    if (timeCounter>=MAX_TIME):
      run = False

    if (len(cars)>0):
      for indexC,car in enumerate(cars):
        if(car.outOfTrack()==True):
          car.deactivate()
        else:
          output = nets[indexC].activate((car.getCarSensorValue(car.carSensorPositions[0]),
                    car.getCarSensorValue(car.carSensorPositions[1]),
                    car.getCarSensorValue(car.carSensorPositions[2]),
                    car.getCarSensorValue(car.carSensorPositions[3]),
                    car.getCarSensorValue(car.carSensorPositions[4])))
          car.move(output[0]*10,output[1]*10)
          ge[indexC].fitness += car.getLastDistance()

          if(car.outOfTrack()==True):
            car.deactivate()
          elif (car.isCarIsAtTheFinishLine()== True):
            ge[indexC].fitness += FINISH_BONUS+((MAX_TIME-timeCounter)*10)
            car.deactivate()
          elif (car.isCarIsOutOfLine() == True ):
            car.incrementOutOfLineDetection()
            ge[indexC].fitness -= OUT_OF_LINE_PENALTY
            if(car.getOutOfLineDetection()>MAX_OUT_OF_LINE):
              car.deactivate()
          else:
            #do nothing
            pass

      for indexC,car in enumerate(cars):
        if (car.isTheCarActive() == False):
          cars.pop(indexC)
          nets.pop(indexC)
          ge.pop(indexC)
    else:
      run = False

    draw_window(win,cars,timeCounter)




def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(trainingFunction, 10)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    #node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_file)