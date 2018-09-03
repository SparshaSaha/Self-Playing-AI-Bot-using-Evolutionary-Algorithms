import pygame
import random
import pickle
import numpy as np
import neat
import os
from Sprites.CactusSingle import CactusSingle
from Sprites.Player import Player
from Sprites.CactusDouble import CactusDouble
from Sprites.CactusTriple import CactusTriple
from Sprites.Bird import Bird
import pickle

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
        for trexId, trex in self.trexs:
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

    
    # Draw obstacles and trexs on screen
    def drawCharacter(self):
        
        for trexId, trex in self.trexs:
            if trex.alive:
                if trex.predictedAction == 2:
                    trex.drawCharacter(self.screen, 1)
                else:
                    trex.drawCharacter(self.screen, 0)

        for obstacles in self.obstaclesOnScreen:
            obstacles.drawCharacter(self.screen)
    
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
        for trexId, trex in self.trexs:
            if trex.detectCollision(self.obstaclesOnScreen[0]) and trex.alive:
                trex.fitness = self.score
                trex.alive = False

    
    def getObstacleIndex(self, name):
        if name == "CactusSingle":
            return 1

        if name == "CactusDouble":
            return 2

        if name == "CactusTriple":
            return 3
        
        else:
            return 4

    
    # Predict actions for all trexs which are alive
    def predictActionsForTRexs(self):
        
        if len(self.obstaclesOnScreen) > 0:
            obstacleNumber = self.getObstacleIndex(self.obstaclesOnScreen[0].__class__.__name__)
            if obstacleNumber != 4:
                input = (float(obstacleNumber), 0, float(self.obstaclesOnScreen[0].x - 120), float(self.speed*100))
            else:
                input = (float(obstacleNumber), 100, float(self.obstaclesOnScreen[0].x - 120), float(self.speed*100))

            for trexId, trex in self.trexs:
                if trex.alive:
                    output = trex.net.activate(input)
                    trex.predictedAction = (output.index(max(output)))
    

    # Check if generation of Trexs are extinct
    def allDead(self):
        for trexId, trex in self.trexs:
            if trex.alive:
                return False
        self.gameOver = True
        return True

                    
                
                

    
    def makeTrexsJump(self):
        
        for trexId, trex in self.trexs:
            if trex.alive:
                if not trex.isJumping:
                    if trex.predictedAction == 1:
                        trex.isJumping = True
                else:
                    trex.isJumping, trex.direction = trex.jump(trex.isJumping, trex.direction, self.jumpSpeed)

    

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
        
    
    def increaseGameSpeed(self):
        if int(self.score/ 5) != self.lastQuotient:
            self.lastQuotient = int(self.score/ 5)
            self.speed += 0.15
            self.jumpSpeed += 0.05
            
        
    

    def game(self):
        pygame.init()
        pygame.display.set_caption('T-Rex Runner')
        self.drawGameBackground()
        pygame.display.flip()

        while self.running:
            self.clock.tick(100)

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
            
            pygame.display.update()

            if len(self.obstaclesOnScreen) > 0:
                self.detectCollisionAndKillTRex()
            
            if self.allDead():
                return
            
            self.increaseGameSpeed()
                        


def eval_genomes(genomes, config):
    g = Game(genomes, config)
    g.game()


            
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(Player, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)

winner = pop.run(eval_genomes, 100)

# Save winner in a file
with open('bestTRex.pickle', 'wb') as handle:
    pickle.dump(winner, handle, protocol = pickle.HIGHEST_PROTOCOL)

