import pygame
import random
import pickle
import numpy as np
from Sprites.Player import Player
from Sprites.CactusSingle import CactusSingle
from Sprites.CactusDouble import CactusDouble
from Sprites.CactusTriple import CactusTriple
from Sprites.Bird import Bird

class Game(object):

    def __init__(self):
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
        self.trex = Player(90, 500)
    

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

    
    def drawCharacter(self):
        
        self.trex.drawCharacter(self.screen)

        for obstacles in self.obstaclesOnScreen:
            obstacles.drawCharacter(self.screen)
    
    # Randomly generate game obstacles depending on obstacle probability
    def generateGameObstacles(self):
        if len(self.obstaclesOnScreen) == 0 or self.obstaclesOnScreen[len(self.obstaclesOnScreen) - 1].x < 600:
            if random.uniform(0,1) < self.obstacleProbability:
                obstacleNumber = random.randint(0, 9)
                if obstacleNumber <= 4:
                    self.obstaclesOnScreen.append(CactusSingle(900, 515))
                elif obstacleNumber <= 6:
                    self.obstaclesOnScreen.append(CactusDouble(900, 515))
                elif obstacleNumber <= 8:
                    self.obstaclesOnScreen.append(CactusTriple(900, 515))
    
    def detectCollisionAndKillTRex(self):
        if self.trex.detectCollision(self.obstaclesOnScreen[0]) and self.trex.alive:
            self.trex.score = score
            self.trex.alive = False

    
    def makeTrexsJump(self):
        
        if not self.trex.isJumping:
            if self.trex.predictedAction == 1:
                self.trex.isJumping = True
        else:
            self.trex.isJumping, self.trex.direction = self.trex.jump(self.trex.isJumping, self.trex.direction, self.jumpSpeed)
    

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
            
            

g = Game()
g.game()   
    


    
    
    
    
