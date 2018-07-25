import pygame
import numpy as np
import tensorflow as tf
class Player(object):
    def __init__(self, x, y):

        # Define the Neural Network
        self.inputNodes = 3
        self.outputNodes = 2
        self.hiddenNodes = 9

        self.inputWeights = np.random.rand(self.inputNodes, self.hiddenNodes)
        self.outputWeights = np.random.rand(self.hiddenNodes, self.outputNodes)

        # Define player properties
        self.x = x
        self.y = [y, y + 20, y]
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
        self.imageName = ["Sprites/GameImages/tRexLeftLeg.png", "Sprites/GameImages/tRexDuck.png", "Sprites/GameImages/tRexRightLeg.png", "Sprites/GameImages/tRexDuckRight.png"]


    def predict(self, userInput):
        hiddenLayer = np.dot(userInput, self.inputWeights)
        hiddenLayer =  1.0 / (1.0 + np.exp(-1.0 * hiddenLayer))
        outputLayer = np.matmul(hiddenLayer, self.outputWeights)
        outputLayer =  1.0 / (1.0 + np.exp(-1.0 * outputLayer))

        return outputLayer.tolist()

    def drawCharacter(self, canvas, index):
        if self.frameCount % 10 == 0 or index != self.index:
            self.currentImageIndex = self.flip(index)
            self.frameCount = 0
            self.index = index

        if index == 0 or index == 2:
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

    def crossOver(parent1, parent2):
        
