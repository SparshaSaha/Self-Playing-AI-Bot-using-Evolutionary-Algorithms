import pygame
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.imageName = "Sprites/tRex.png"

    def drawCharacter(self, canvas):
        canvas.blit(pygame.image.load(self.imageName), (self.x,self.y))
