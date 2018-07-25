import pygame
import random
import pickle
import numpy as np
from Sprites.Player import Player
from Sprites.CactusSingle import CactusSingle
from Sprites.CactusDouble import CactusDouble
from Sprites.CactusTriple import CactusTriple
from Sprites.Bird import Bird

# Game Variables
obstacleProbability = 0.01
obstaclesOnScreen = []
speed = 3.0
lastQuotient = 0
score = 0
tRexIndex = 0
direction = -1
running = True
gameOver = False
jumpSpeed = 3.2
fontName = pygame.font.match_font('arial')
clock = pygame.time.Clock()
background_colour = (255,255,255)
(width, height) = (900, 600)
frameCount = 0
generation = 1

# Display Score on Screen
def drawText(surf, text, size, x, y):
    font = pygame.font.Font(fontName, size)
    textSurface = font.render(text, True, (0, 0, 0))
    textRect = textSurface.get_rect()
    textRect.midtop = (x, y)
    surf.blit(textSurface, textRect)

# Draw the game background
def drawGameBackground():
    screen.fill(background_colour)

# Draw TRex and all obstacles on Screen
def drawCharacter():
    for trex in tRex:
        if trex.alive == True:
            trex.drawCharacter(screen, 0)
    for obstacles in obstaclesOnScreen:
        obstacles.drawCharacter(screen)

# Randomly generate game obstacles depending on obstacle probability
def generateGameObstacles():
    if len(obstaclesOnScreen) == 0 or obstaclesOnScreen[len(obstaclesOnScreen) - 1].x < 650:
        if random.uniform(0,1) < obstacleProbability:
            obstacleNumber = random.randint(0, 9)
            if obstacleNumber <= 4:
                obstaclesOnScreen.append(CactusSingle(900, 515))
            elif obstacleNumber <= 6:
                obstaclesOnScreen.append(CactusDouble(900, 515))
            elif obstacleNumber <= 8:
                obstaclesOnScreen.append(CactusTriple(900, 515))


# Remove dead obstacles from obstacle array
def cleanDeadObstaclesAndPropagate(obstacles, score):
    index = 0
    for obstacle in obstacles:
        if obstacle.x > 30:
            lastDistance = 900
            break
        else:
            score += 1
        index+=1

    obstacles = obstacles[index : ]
    for obstacle in obstacles:
        obstacle.propagate(speed)
    return obstacles, score

def getObstacleIndex(name):
    if name == "CactusSingle":
        return 1

    if name == "CactusDouble":
        return 2

    return 3

def detectCollisionAndKillTRex():
    for trex in tRex:
        if trex.detectCollision(obstaclesOnScreen[0]) and trex.alive:
            trex.score = score
            trex.alive = False

def makeTrexsJump():
    for trex in tRex:
        if not trex.isJumping:
            if trex.predictedAction == 1:
                trex.isJumping = True
        else:
            trex.isJumping, trex.direction = trex.jump(trex.isJumping, trex.direction, jumpSpeed)

def countAlive():
    count = 0
    for trex in tRex:
        if trex.alive:
            count += 1

    if count == 0:
        return True
    else:
        return False

def BuildNextGeneration():
    newTrexs = []
    tRex.sort(key=lambda x: x.score, reverse=True)

    # Keep 3 top scorers as it is
    newTrexs.append(tRex[0])
    newTrexs.append(tRex[1])
    newTrexs.append(tRex[2])

    # Saving best weights
    with open('inputWts', 'wb') as fp:
        pickle.dump(tRex[0].inputWeights.tolist(), fp)

    with open('outputWts', 'wb') as fp:
        pickle.dump(tRex[0].outputWeights.tolist(), fp)



    bestTwo = Player(90, 500)
    bestTwo.crossOver(tRex[0], tRex[1])
    newTrexs.append(bestTwo)

    bestAndWorst = Player(90, 500)
    bestAndWorst.crossOver(tRex[0], tRex[len(tRex) - 1])
    newTrexs.append(bestAndWorst)

    for i in range(0, len(tRex) - 20):
        par1 = tRex[random.randint(0, len(tRex)-1)]
        par2 = tRex[random.randint(0, len(tRex)-1)]

        child = Player(90, 500)
        child.crossOver(par1, par2)
        newTrexs.append(child)

    return newTrexs


def aliveCount():
    cnt = 0;
    for i in tRex:
        if i.alive:
            cnt+=1
    return cnt





# 0 - jump
# 1 - duck
# 2 - nothing

pygame.init()
action = 0;
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('T-Rex Runner')
drawGameBackground()
pygame.display.flip()

tRex = [Player(90, 500) for i in range(0, 1000)]

while running:
    clock.tick(100)

    if len(obstaclesOnScreen) > 0 and frameCount > 1:
        obstacleNumber = getObstacleIndex(obstaclesOnScreen[0].__class__.__name__)
        for trex in tRex:
            action = trex.predict(np.array([float(obstacleNumber), float(obstaclesOnScreen[0].x - 120), float(speed)]))
            frameCount = 0
            if action[0] > action[1]:
                trex.predictedAction = 0
            else:
                trex.predictedAction = 1
    frameCount += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        gameOver = False
        score = 0
        obstaclesOnScreen = []

    #if keys[pygame.K_DOWN] and not jump:
        #tRexIndex = 1

    #else:
        #tRexIndex = 0


    makeTrexsJump()

    if countAlive() :
        tRex = BuildNextGeneration()
        generation += 1
        obstaclesOnScreen.clear()
        score = 0




    if not gameOver:
        drawGameBackground()
        generateGameObstacles()
        obstaclesOnScreen, score = cleanDeadObstaclesAndPropagate(obstaclesOnScreen, score)
        drawCharacter()
        drawText(screen, 'score: ' + str(score), 20, 700, 50)
        drawText(screen, 'Generation Count: ' + str(len(tRex)), 10, 100, 50)
        drawText(screen, 'Generation: ' + str(generation), 10, 100, 70)
        drawText(screen, 'Generation Alive: ' + str(aliveCount()),10 ,200, 50)

        pygame.display.update()

    if len(obstaclesOnScreen) > 0:
        detectCollisionAndKillTRex()

    if score // 10 > lastQuotient:
        lastQuotient += 1
        speed += 0.5
        jumpSpeed += 0.1
