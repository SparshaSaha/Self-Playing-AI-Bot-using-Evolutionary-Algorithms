import pygame
class CactusDouble(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imageName = "Sprites/GameImages/doubleCactus.png"

    def drawCharacter(self, canvas):
        canvas.blit(pygame.image.load(self.imageName), (self.x,self.y))

    def propagate(self, step):
        self.x -= step
