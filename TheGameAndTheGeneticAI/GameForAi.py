import pygame
import random
import pickle
import numpy as np
import neat
import os
import visualize

from Sprites.CactusSingle import CactusSingle
from Sprites.Player import Player
from Sprites.CactusDouble import CactusDouble
from Sprites.CactusTriple import CactusTriple
from Sprites.Bird import Bird
from Sprites.Clouds import Cloud
from Sprites.Dashes import Dashes


class Game(object):
    
    def __init__(self, tRexArray, config):
        self.obstacleProbability = 0.01
        self.obstaclesOnScreen = []
        self.speed = 3.0
        self.lastQuotient = 0
        self.score = 0
        self.direction = -1
        self.running = True
        self.gameOver = False
        self.jumpSpeed = 3.2
        self.fontName = pygame.font.match_font('arial')
        self.clock = pygame.time.Clock()
        self.background_colour = (255,255,255)
        self.width = 900
        self.height = 600
        self.frameCount = 0
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.trexs = tRexArray
        self.config = config
        self.dashes = []
        self.clouds = []
        cloud1 = Cloud(930, 50, 930, 0.7)
        cloud2 = Cloud(1030, 50, 1030, 0.65)
        cloud3 = Cloud(1030, 100, 1030, 0.5)
        cloud4 = Cloud(1130, 100, 1130, 0.45)
        self.clouds = [cloud1, cloud2, cloud3, cloud4]
        for  trex in self.trexs:
            trex.net = neat.nn.FeedForwardNetwork.create(trex, config)
    

    # Display Score on Screen
    def drawText(self, text, size, x, y):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, (0, 0, 0))
        textRect = textSurface.get_rect()
        textRect.midtop = (x, y)
        self.screen.blit(textSurface, textRect)

    # Draw the game background
    def drawGameBackground(self):
        self.screen.fill(self.background_colour)
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 550, 900, 1), 1)

    
    # Draw obstacles and trexs on screen
    def drawCharacter(self):
        
        for trex in self.trexs:
            if trex.isJumping:
                trex.drawCharacter(self.screen, 0)
            elif trex.alive:
                if trex.predictedAction == 2:
                    trex.drawCharacter(self.screen, 1)
                else:
                    trex.drawCharacter(self.screen, 0)

        for obstacles in self.obstaclesOnScreen:
            obstacles.drawCharacter(self.screen)
        
        for cloud in self.clouds:
            cloud.drawCharacter(self.screen)
    
    # Randomly generate game obstacles depending on obstacle probability
    def generateGameObstacles(self):
        if len(self.obstaclesOnScreen) == 0 or self.obstaclesOnScreen[len(self.obstaclesOnScreen) - 1].x < 600:
            if random.uniform(0,1) < self.obstacleProbability:
                obstacleNumber = random.randint(0, 3)
                if obstacleNumber <= 0:
                    self.obstaclesOnScreen.append(CactusSingle(900, 515))
                elif obstacleNumber <= 1:
                    self.obstaclesOnScreen.append(CactusDouble(900, 515))
                elif obstacleNumber <= 2:
                    self.obstaclesOnScreen.append(CactusTriple(900, 515))
                elif obstacleNumber <= 3:
                    self.obstaclesOnScreen.append(Bird(900, 485))

    
    # Kill trexs on collision
    def detectCollisionAndKillTRex(self):
        for   trex in self.trexs:
            if trex.detectCollision(self.obstaclesOnScreen[0]) and trex.alive:
                trex.fitness = self.score
                trex.alive = False

    # Get Obstacle Info
    def getObstacleIndex(self, name):
        if name == "CactusSingle":
            return (15, 30)

        if name == "CactusDouble":
            return (30, 30)

        if name == "CactusTriple":
            return (45, 30)
        
        else:
            return (45, 27)


    
    # Predict actions for all trexs which are alive
    def predictActionsForTRexs(self):
        
        if len(self.obstaclesOnScreen) > 0:
            obstacleNumber = self.getObstacleIndex(self.obstaclesOnScreen[0].__class__.__name__)
            if obstacleNumber[1] != 27:
                input = (float(obstacleNumber[0]),float(obstacleNumber[1]), 0, float(self.obstaclesOnScreen[0].x - 120), float(self.speed*100))
            else:
                input = (float(obstacleNumber[0]),float(obstacleNumber[1]), 100, float(self.obstaclesOnScreen[0].x - 120), float(self.speed*100))

            for trex in self.trexs:
                if trex.alive:
                    output = trex.net.activate(input)
                    trex.predictedAction = (output.index(max(output)))
        else:
            input = (float(30),float(30), 0, float(9500), float(self.speed*100))
            for trex in self.trexs:
                if trex.alive:
                    output = trex.net.activate(input)
                    trex.predictedAction = (output.index(max(output)))

    

    # Check if generation of Trexs are extinct
    def allDead(self):
        for   trex in self.trexs:
            if trex.alive:
                return False
        self.gameOver = True
        return True

                    
    # Make the TRrexs to jump
    def makeTrexsJump(self):
        
        for trex in self.trexs:
            if trex.alive:
                if not trex.isJumping:
                    if trex.predictedAction == 1:
                        trex.isJumping = True
                else:
                    trex.isJumping, trex.direction = trex.jump(trex.isJumping, trex.direction, self.jumpSpeed)

    
    # Clean obstacles which has passed player
    def cleanDeadObstaclesAndPropagate(self):
        index = 0
        for obstacle in self.obstaclesOnScreen:
            if obstacle.x > 30:
                break
            else:
                self.score += 1
            index += 1

        self.obstaclesOnScreen = self.obstaclesOnScreen[index : ]
        for obstacle in self.obstaclesOnScreen:
            obstacle.propagate(self.speed)
        
        for cloud in self.clouds:
            cloud.propagate()
        
    # Increase Game Speed
    def increaseGameSpeed(self):
        if int(self.score/ 10) != self.lastQuotient:
            self.lastQuotient = int(self.score/ 10)
            self.speed += 0.15
            self.jumpSpeed += 0.05
    
    # Create dashes which signify ground
    def createDashes(self):
        possibleYCoords = [555, 565, 575]
        chosenYCoord = random.choice(possibleYCoords)
        self.dashes.append(Dashes(899, chosenYCoord))
    
    # Remove dashes which have passed the screen and propagate dashes
    def removeDeadDashesAndPropagate(self):
        index = 0
        for dash in self.dashes:
            if dash.x > 0:
                break
            index += 1
        self.dashes = self.dashes[index : ]
        for dash in self.dashes:
            dash.propagate(self.speed)
    
    # Draw dashes on screen
    def drawDashes(self):
        for dash in self.dashes:
            dash.drawCharacter(self.screen)

        
    
    # Run the game
    def game(self):
        pygame.init()
        pygame.display.set_caption('T-Rex Runner')
        self.drawGameBackground()
        pygame.display.flip()

        while self.running:
            self.clock.tick(110)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            self.predictActionsForTRexs()

            self.makeTrexsJump()
            
            self.drawGameBackground()
            self.generateGameObstacles()
            self.cleanDeadObstaclesAndPropagate()
            self.drawCharacter()
            self.drawText('score: ' + str(self.score), 20, 700, 50)
            
            if len(self.dashes) == 0:
                self.createDashes()
            elif self.dashes[0].x < 890:
                self.createDashes()
            
            self.removeDeadDashesAndPropagate()
            self.drawDashes()
            
            pygame.display.update()

            if len(self.obstaclesOnScreen) > 0:
                self.detectCollisionAndKillTRex()
            
            if self.allDead():
                print(self.trexs[0].fitness)
                return
            
            self.increaseGameSpeed()

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(Player, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

player = None

with open('bestTRex_better.pickle', 'rb') as handle:
    player = pickle.load(handle)

print(player)
player.alive = True
visualize.draw_net(config, player, True)

game = Game([player], config)

game.game()
