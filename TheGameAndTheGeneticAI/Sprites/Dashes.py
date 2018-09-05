import pygame

class Dashes(object):

    def __init__(self,x ,y):
        self.x = x
        self.y = y

    def propagate(self, speed):
        self.x -= speed

    def drawCharacter(self, screen):
        hitbox = (self.x, self.y, 7, 5)
        pygame.draw.rect(screen, (0, 0, 0), hitbox, 2)
         
