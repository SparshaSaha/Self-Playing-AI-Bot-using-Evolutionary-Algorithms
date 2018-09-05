import pygame

class Dashes(object):

    def __init__(self,x ,y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 7, 5)


    def propagate(self, speed):
        self.x -= speed

    def drawCharacter(self, screen):
        self.hitbox = (self.x, self.y, 2, 1)
        pygame.draw.rect(screen, (0, 0, 0), self.hitbox, 2)
         
