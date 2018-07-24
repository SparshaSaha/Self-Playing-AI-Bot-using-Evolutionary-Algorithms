import pygame
class Bird(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (0, 0, 0, 0)
        self.frameCount = 0;
        self.images = ["Sprites/GameImages/birdUp.png", "Sprites/GameImages/birdDown.png"]
        self.flipState = 0

    def drawCharacter(self, canvas):
        if self.frameCount % 50 == 0:
            self.flipState = self.flip(self.flipState)

        canvas.blit(pygame.image.load(self.images[self.flipState]), (self.x,self.y))
        self.hitbox = (self.x, self.y, 45, 27)
        self.frameCount += 1

    def propagate(self, step):
        self.x -= step

    def flip(self, index):
        if index == 0:
            return 1
        else:
            return 0
