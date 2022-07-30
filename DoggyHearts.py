"""Author: Krzysztof Hrybacz <krzysztof@zygtech.pl>"""
"""License: GNU General Public License -- version 3"""

import random, sys, time, pygame
from pygame.locals import *

FPS = 60
WINWIDTH = 800
WINHEIGHT = 600
MOVERATE = 5
ENEMYMOVERATE = 2
SIZEX = 100
SIZEY = 80
HSIZEX = 50
HSIZEY = 50
ESIZEX = 80
ESIZEY = 80
GAMEOVERTIME = 3

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, KITTY_IMG, HEART_IMG, ENEMY_IMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('Doggy.png'))
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Doggy Hearts')

    KITTY_IMG = pygame.image.load('Doggy.png')
    ENEMY_IMG = pygame.image.load('ThePig.png')
    HEART_IMG = pygame.image.load('Heart.png')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    start = pygame.image.load('Start.png')

    while True:
        DISPLAYSURF.blit(start,(0,0))

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    runJump()
                elif event.key == K_2:
                    runCollect()
                elif event.key == K_ESCAPE:
                    terminate()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

class sprite(pygame.sprite.Sprite):

    def __init__(self, image, x, y, layer):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self._layer = layer
        self.rect = self.image.get_rect(x=x, y=y)
        self.mask = pygame.mask.from_surface(self.image,127)


def runJump():

    bgOne = pygame.image.load('Background.png')
    bgTwo = pygame.image.load('Background.png')

    moveForward = False
    moveBackward = False
    jump = 0
    PTS = 0

    gameOverMode = False
    gameOverSurf = BASICFONT.render('Game Over', True, (255, 255, 255) )
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (int( WINWIDTH / 2 ), int( WINHEIGHT / 2 ))

    playerObj = {'surface': pygame.transform.smoothscale(KITTY_IMG, (SIZEX, SIZEY)),
                 'x': 10,
                 'y': 0,
		}

    enemyObj = {'surface': pygame.transform.smoothscale(ENEMY_IMG, (ESIZEX, ESIZEY)),
                'x': WINWIDTH+random.randint(0, WINWIDTH),
                'y': 0,
	       }
    heartObj = {'surface': pygame.transform.smoothscale(HEART_IMG, (HSIZEX, HSIZEY)),
                'x': WINWIDTH+random.randint(0, WINWIDTH),
                'y': random.randint(0, 180),
	       }
 
    while True:
        DISPLAYSURF.blit(bgOne, (0-(playerObj['x']%bgOne.get_width()), WINHEIGHT-bgOne.get_height() ))
        DISPLAYSURF.blit(bgTwo, (bgOne.get_width()-(playerObj['x']%bgOne.get_width()), WINHEIGHT-bgOne.get_height() ))


        heartSprite = sprite(heartObj['surface'],int( heartObj['x']+100-playerObj['x'] ),WINHEIGHT-120-heartObj['y'],1)

        playerSprite = sprite(playerObj['surface'],100,WINHEIGHT-120-playerObj['y'],2)

        enemySprite = sprite(enemyObj['surface'],int( enemyObj['x']+100-playerObj['x'] ),WINHEIGHT-120,3)

        sprites = pygame.sprite.LayeredUpdates(heartSprite, playerSprite, enemySprite)
        sprites.draw(DISPLAYSURF)

        PTSdisp = BASICFONT.render(str(PTS), True, (255, 255, 255))
        PTSrect = PTSdisp.get_rect()
        PTSrect.left=10
        PTSrect.top=10
        DISPLAYSURF.blit(PTSdisp, PTSrect)

        for event in pygame.event.get(): 
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moveForward = True
                    moveBackward = False
                elif event.key == K_LEFT:
                    moveForward = False
                    moveBackward = True

                elif event.key == K_SPACE and jump == 0:
                    jump = 1

            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    moveForward = False
                elif event.key == K_LEFT:
                    moveBackward = False

                elif event.key == K_ESCAPE:
                    return

        if not gameOverMode:
            if moveBackward and playerObj['x']>5:
                playerObj['x'] -= MOVERATE
            if moveForward:
                playerObj['x'] += MOVERATE

            enemyObj['x'] -= ENEMYMOVERATE

            if enemyObj['x'] < playerObj['x']-300:
                enemyObj['x'] = playerObj['x']+WINWIDTH+random.randint(0, WINWIDTH)           

            if jump>0:
                if jump>36:
                    playerObj['y'] -= 5
                else:
                    playerObj['y'] += 5
                    jump += 1
	    
                if playerObj['y'] == 0: 
                    jump = 0 

            if pygame.sprite.collide_mask(playerSprite, heartSprite):
                heartObj['x'] = playerObj['x']+WINWIDTH+random.randint(0, WINWIDTH)
                heartObj['y'] = random.randint(0, 180)
                PTS += 1
            if pygame.sprite.collide_mask(playerSprite, enemySprite):
                gameOverMode = True
                gameOverStartTime = time.time()

        else:
            DISPLAYSURF.blit(gameOverSurf, gameOverRect)
            if time.time() - gameOverStartTime > GAMEOVERTIME:
                return

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def runCollect():

    moveLeft  = False
    moveRight = False
    moveUp    = False
    moveDown  = False
    PTS = 0

    gameOverMode = False
    gameOverSurf = BASICFONT.render('Game Over', True, (255, 255, 255) )
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (int( WINWIDTH / 2 ), int( WINHEIGHT / 2 ))

    bowSurf = pygame.image.load('Bow.png')
    bowRect = (WINWIDTH-286, WINHEIGHT-256)

    playerObj = {'surface': pygame.transform.smoothscale(KITTY_IMG, (SIZEX, SIZEY)),
                 'x': int(WINWIDTH / 2),
                 'y': int(WINHEIGHT / 2),
		}

    enemyObj = {'surface': pygame.transform.smoothscale(ENEMY_IMG, (ESIZEX, ESIZEY)),
                 'x': random.randint(0, WINWIDTH),
                 'y': random.randint(0, WINHEIGHT),
		}

    heartObj = {'surface': pygame.transform.smoothscale(HEART_IMG, (HSIZEX, HSIZEY)),
                 'x': random.randint(0, WINWIDTH),
                 'y': random.randint(0, WINHEIGHT),
		}

    while True:
        DISPLAYSURF.fill( (200, 200, 255) )
        DISPLAYSURF.blit(bowSurf, bowRect)

        heartSprite = sprite(heartObj['surface'],int( heartObj['x'] - (HSIZEX / 2) ),int( heartObj['y'] - (HSIZEY / 2) ),1)

        playerSprite = sprite(playerObj['surface'],int( playerObj['x'] - (SIZEX / 2) ),int( playerObj['y'] - (SIZEY / 2) ),2)

        enemySprite = sprite(enemyObj['surface'],int( enemyObj['x'] - (ESIZEX / 2) ),int( enemyObj['y'] - (ESIZEY / 2) ),3)

        sprites = pygame.sprite.LayeredUpdates(heartSprite, playerSprite, enemySprite)
        sprites.draw(DISPLAYSURF)

        PTSdisp = BASICFONT.render(str(PTS), True, (255, 255, 255))
        PTSrect = PTSdisp.get_rect()
        PTSrect.left=10
        PTSrect.top=10
        DISPLAYSURF.blit(PTSdisp, PTSrect)

        for event in pygame.event.get(): 
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
                elif event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False

                elif event.key == K_ESCAPE:
                    return
        if not gameOverMode:
            if moveLeft and playerObj['x'] > 0:
                playerObj['x'] -= MOVERATE
            if moveRight and playerObj['x'] < WINWIDTH:
                playerObj['x'] += MOVERATE
            if moveUp and playerObj['y'] > 0:
                playerObj['y'] -= MOVERATE
            if moveDown and playerObj['y'] < WINHEIGHT:
                playerObj['y'] += MOVERATE

            if playerObj['x'] < enemyObj['x']:
                enemyObj['x'] -= ENEMYMOVERATE
            if playerObj['x'] > enemyObj['x']:
                enemyObj['x'] += ENEMYMOVERATE
            if playerObj['y'] < enemyObj['y']:
                enemyObj['y'] -= ENEMYMOVERATE
            if playerObj['y'] > enemyObj['y']:
                enemyObj['y'] += ENEMYMOVERATE

            if pygame.sprite.collide_mask(playerSprite, heartSprite):
                heartObj['x'] = random.randint(0, WINWIDTH)
                heartObj['y'] = random.randint(0, WINHEIGHT)
                PTS += 1

            if pygame.sprite.collide_mask(playerSprite, enemySprite):
                gameOverMode = True
                gameOverStartTime = time.time()
        else:
            DISPLAYSURF.blit(gameOverSurf, gameOverRect)
            if time.time() - gameOverStartTime > GAMEOVERTIME:
                return

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
