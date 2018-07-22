import pygame
class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 38, 40)
        self.hitboxRect = pygame.Rect(self.x, self.y, 41, 40)
        self.imageName = "Sprites/GameImages/tRex.png"

    def drawCharacter(self, canvas):
        canvas.blit(pygame.image.load(self.imageName), (self.x,self.y))
        self.hitbox = (self.x, self.y, 38, 40)
        self.hitboxRect = pygame.Rect(self.x, self.y, 38, 40)
        pygame.draw.rect(canvas, (255, 0, 0), self.hitbox, 2)

    def jump(self, jump, direction):
        self.y += 2.1 * direction
        if self.y < 510 :
            direction = 1
            return  True, direction
        elif self.y == 600:
            direction = -1
            return False, direction
        else:
            return True, direction

    def detectCollision(self, sprite):
        return self.hitboxRect.colliderect(sprite.hitbox)
