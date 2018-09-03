import pygame

class Cloud(object):

    def __init__(self, x, y, regenarate, speed):
        self.speed = speed
        self.y = y
        self.x = regenarate
        self.regenarate = regenarate
        self.image = pygame.image.load("Sprites/GameImages/Cloud.png")

    def propagate(self):
        if self.x < -10:
            self.x = self.regenarate

        self.x -= self.speed 
    
    def drawCharacter(self, canvas):
        canvas.blit(self.image, (self.x,self.y))

        
