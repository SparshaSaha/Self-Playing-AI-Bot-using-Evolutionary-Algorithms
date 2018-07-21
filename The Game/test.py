import pygame
from Sprites.Player import Player


def drawGameWindow(player):
    screen.fill(background_colour)
    player.drawCharacter(screen)
    pygame.display.update()


pygame.init()
clock = pygame.time.Clock()
background_colour = (255,255,255)
(width, height) = (1370, 750)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('T-Rex')
screen.fill(background_colour)
pygame.display.flip()

x = 30
y = 600

direction = -1
tRex = Player(x, y, 10, 10);

running = True
jump = False
while running:
    clock.tick(500)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if not jump:
        if keys[pygame.K_SPACE]:
            jump = True
    else:
        tRex.y += 0.75 * direction
        if tRex.y < 550 :
            direction = 1;
        elif tRex.y == y:
            direction = -1;
            jump = False
    drawGameWindow(tRex)
