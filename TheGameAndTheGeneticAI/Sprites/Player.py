import pygame
import numpy as np
import random
import neat
class Player(neat.DefaultGenome):
    def __init__(self, key):
        
        super().__init__(key)

        # Define player properties
        self.x = 90
        self.y = [500, 500 + 20, 500]
        self.hitbox = (self.x, self.y[0], 38, 40)
        self.hitboxRectStanding = pygame.Rect(self.x, self.y[0], 41, 40)
        self.hitboxRectDucking = pygame.Rect(self.x, self.y[1], 58, 30)
        self.frameCount = 0
        self.index = 0
        self.currentImageIndex = 0
        self.score = 0
        self.alive = True
        self.isJumping = False
        self.direction = -1
        self.predictedAction = 0
        self.net = None
        self.imageName = ["Sprites/GameImages/tRexLeftLeg.png", "Sprites/GameImages/tRexDuck.png", "Sprites/GameImages/tRexRightLeg.png", "Sprites/GameImages/tRexDuckRight.png"]

    def configure_new(self, config):
        super().configure_new(config)
    

    def configure_crossover(self, genome1, genome2, config):
        super().configure_crossover(genome1, genome2, config)
    
    def mutate(self, config):
        super().mutate(config)
    
    def distance(self, other, config):
        return super().distance(other, config)
        


    def drawCharacter(self, canvas, index):
        if self.frameCount % 10 == 0 or index != self.index:
            self.currentImageIndex = self.flip(index)
            self.frameCount = 0
            self.index = index

        if index == 0 or index == 2 or self.isJumping:
            self.hitbox = (self.x, self.y[0], 38, 40)
            self.hitboxRectStanding = pygame.Rect(self.x, self.y[0], 41, 40)
            self.hitboxRect = self.hitboxRectStanding
        else:
            self.hitboxRectDucking = pygame.Rect(self.x, self.y[1], 58, 30)
            self.hitbox = (self.x, self.y[1], 58, 30)
            self.hitboxRect = self.hitboxRectDucking

        self.frameCount += 1

        canvas.blit(pygame.image.load(self.imageName[self.currentImageIndex]), (self.x,self.y[index]))

        #pygame.draw.rect(canvas, (255, 0, 0), self.hitbox,2)

    def jump(self, jump, direction, jumpSpeed):
        self.y[0] += jumpSpeed * direction
        if self.y[0] < 410 :
            direction = 1
            return  True, direction
        elif self.y[0] >= 500:
            direction = -1
            return False, direction
        else:
            return True, direction

    def detectCollision(self, sprite):
        return self.hitboxRect.colliderect(sprite.hitbox)

    def flip(self, index):
        if index == 0:
            if self.currentImageIndex == 0:
                return 2
            else:
                return 0
        else:
            if self.currentImageIndex == 1:
                return 3
            else:
                return 1
