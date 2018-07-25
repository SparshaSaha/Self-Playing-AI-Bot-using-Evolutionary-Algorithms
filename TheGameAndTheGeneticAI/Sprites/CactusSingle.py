import pygame
class CactusSingle(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (0, 0, 0, 0)
        self.imageName = "Sprites/GameImages/smallCactus.png"
        self.loadedImage = pygame.image.load(self.imageName)

    def drawCharacter(self, canvas):
        canvas.blit(self.loadedImage, (self.x,self.y))
        self.hitbox = (self.x + 3, self.y + 3, 15, 30)
        #pygame.draw.rect(canvas, (255, 0, 0), self.hitbox, 2)

    def propagate(self, step):
        self.x -= step
