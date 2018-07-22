import pygame
import random
from Sprites.Player import Player
from Sprites.CactusSingle import CactusSingle
from Sprites.CactusDouble import CactusDouble
from Sprites.CactusTriple import CactusTriple

obstacleProbability = 0.01
global obstaclesOnScreen
obstaclesOnScreen = []
speed = 1.5
lastQuotient = 0;
score = 0
font_name = pygame.font.match_font('arial')

def drawText(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def drawGameBackground():
    screen.fill(background_colour)


def drawCharacter():
    tRex.drawCharacter(screen)
    for obstacles in obstaclesOnScreen:
        obstacles.drawCharacter(screen)

def generateGameObstacles():
    if len(obstaclesOnScreen) == 0 or obstaclesOnScreen[len(obstaclesOnScreen) - 1].x < 650:
        if random.uniform(0,1) < obstacleProbability:
            obstacleNumber = random.randint(0,6)
            if obstacleNumber <= 2:
                obstaclesOnScreen.append(CactusSingle(900, 615))
            elif obstacleNumber <= 4:
                obstaclesOnScreen.append(CactusDouble(900, 615))
            else:
                obstaclesOnScreen.append(CactusTriple(900, 615))

def cleanDeadObstaclesAndPropagate(obstacles, score):
    index = 0
    for obstacle in obstacles:
        if obstacle.x >= 70:
            break
        else:
            score += 1
        index+=1

    obstacles = obstacles[index : ]
    for obstacle in obstacles:
        obstacle.propagate(speed)
    return obstacles, score




pygame.init()
clock = pygame.time.Clock()
background_colour = (255,255,255)
(width, height) = (900, 750)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('T-Rex')
drawGameBackground()
pygame.display.flip()

x = 90
y = 600

direction = -1
tRex = Player(x, y)

running = True
jump = False
gameOver = False
while running:
    clock.tick(175)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        gameOver = False
        score = 0
        obstaclesOnScreen = []

    if not jump:
        if keys[pygame.K_SPACE]:
            jump = True
    else:
        jump, direction = tRex.jump(jump, direction)

    if not gameOver:
        drawGameBackground()
        generateGameObstacles()
        obstaclesOnScreen, score = cleanDeadObstaclesAndPropagate(obstaclesOnScreen, score)
        drawCharacter()
        drawText(screen, 'score: ' + str(score), 30, 700, 100)
        pygame.display.update()

    if len(obstaclesOnScreen) > 0 and tRex.detectCollision(obstaclesOnScreen[0]):
        gameOver = True
        speed = 1.5

    if score // 10 > lastQuotient:
        lastQuotient += 1
        speed += 0.2
