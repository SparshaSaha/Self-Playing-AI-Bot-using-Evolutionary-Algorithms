import pygame
import numpy as np
import random
class Player(object):
    def __init__(self, x, y):

        # Define the Neural Network
        self.inputNodes = 4
        self.outputNodes = 2
        self.hiddenNodes = 13

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
        temp = userInput[1] * 0.8
        outputLayer = np.append(outputLayer,temp)
        outputLayer =  1.0 / (1.0 + np.exp(-1.0 * outputLayer))

        return outputLayer.tolist()

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

    def crossOver(self, parent1, parent2):
        parent1InputWeights = parent1.inputWeights.tolist()
        parent2InputWeights = parent2.inputWeights.tolist()

        parent1OutputWeights = parent1.outputWeights.tolist()
        parent2OutputWeights = parent1.outputWeights.tolist()

        # Fix Input inputWeights
        self.inputWeights = []

        for i in range(0, self.inputNodes):
            arrayChooser = random.randint(0, 1)
            if arrayChooser == 0:
                self.inputWeights.append(parent1InputWeights[i])
            else:
                self.inputWeights.append(parent2InputWeights[i])


        self.inputWeights = np.array(self.mutate(self.inputWeights))

        # Fix Output Weights

        self.outputWeights = []

        for i in range(0, self.hiddenNodes):
            arrayChooser = random.randint(0, 1)
            if arrayChooser == 0:
                self.outputWeights.append(parent1OutputWeights[i])
            else:
                self.outputWeights.append(parent2OutputWeights[i])

        self.outputWeights = np.array(self.mutate(self.outputWeights))

    def mutate(self, array):
        mutateProb = 0.7
        if random.uniform(0, 1) > mutateProb:
            first = random.randint(0, len(array)-1)
            second = random.randint(0, len(array)-1)
            temp = array[first]
            array[first] = array[second]
            array[second] = temp


            first = random.randint(0, len(array)-1)
            second = random.randint(0, len(array)-1)
            temp = array[first]
            array[first] = array[second]
            array[second] = temp
        return array
