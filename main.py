"""Author: Krzysztof Hrybacz <krzysztof@zygtech.pl>"""
"""License: GNU General Public License -- version 3"""

import random, sys, time, pygame
from pygame.locals import *
try:
    import android
except ImportError:
    android = None

FPS = 60
WINWIDTH = 1280
WINHEIGHT = 800
MOVERATE = 7
ENEMYMOVERATE = 3
SIZEX = 100
SIZEY = 80
HSIZEX = 50
HSIZEY = 50
ESIZEX = 80
ESIZEY = 80
GAMEOVERTIME = 3

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, KITTY_IMG, HEART_IMG, ENEMY_IMG, SCREENWIDTH, SCREENHEIGHT

    pygame.init()
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('Doggy.png'))
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    SCREENWIDTH, SCREENHEIGHT = DISPLAYSURF.get_size()
    pygame.display.set_caption('Doggy Hearts')

    KITTY_IMG = pygame.image.load('Doggy.png')
    ENEMY_IMG = pygame.image.load('ThePig.png')
    HEART_IMG = pygame.image.load('Heart.png')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
    start = pygame.transform.smoothscale(pygame.image.load('Start.png'),(SCREENWIDTH, SCREENHEIGHT))

    while True:   
        if android:
            if android.check_pause():
                android.wait_for_resume() 
                 
        DISPLAYSURF.blit(start,(0,0))

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
            if android:
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < SCREENHEIGHT/2:
                        runJump()
                    else:
                        runCollect()
            else:
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        runJump()
                    elif event.key == K_2:
                        runCollect()

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
    gameOverRect.center = (int( SCREENWIDTH / 2 ), int( SCREENHEIGHT / 2 ))

    playerObj = {'surface': pygame.transform.smoothscale(KITTY_IMG, (SIZEX, SIZEY)),
                 'x': 10,
                 'y': 0,
		}

    enemyObj = {'surface': pygame.transform.smoothscale(ENEMY_IMG, (ESIZEX, ESIZEY)),
                'x': SCREENWIDTH+random.randint(0, SCREENWIDTH),
                'y': 0,
	       }
    heartObj = {'surface': pygame.transform.smoothscale(HEART_IMG, (HSIZEX, HSIZEY)),
                'x': SCREENWIDTH+random.randint(0, SCREENWIDTH),
                'y': random.randint(0, 180),
	       }
 
    while True:
        if android:
            if android.check_pause():
                android.wait_for_resume()
                
        DISPLAYSURF.blit(bgOne, (0-(playerObj['x']%bgOne.get_width()), SCREENHEIGHT-bgOne.get_height() ))
        DISPLAYSURF.blit(bgTwo, (bgOne.get_width()-(playerObj['x']%bgOne.get_width()), SCREENHEIGHT-bgOne.get_height() ))
		
        heartSprite = sprite(heartObj['surface'],int( heartObj['x']+100-playerObj['x'] ),SCREENHEIGHT-120-heartObj['y'],1)

        playerSprite = sprite(playerObj['surface'],100,SCREENHEIGHT-120-playerObj['y'],2)

        enemySprite = sprite(enemyObj['surface'],int( enemyObj['x']+100-playerObj['x'] ),SCREENHEIGHT-120,3)

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
                if event.key == K_ESCAPE:
                    return
            if android:
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < SCREENHEIGHT/2  and jump == 0:
                        jump = 1
                    elif x < SCREENWIDTH/2:
                        moveForward = False
                        moveBackward = True
                    else:
                        moveForward = True
                        moveBackward = False
                elif event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    if y > SCREENHEIGHT/2:
                        moveForward = False
                        moveBackward = False
            else:
                if event.type == KEYDOWN:
                    if event.key in (K_RIGHT, K_d):
                        moveForward = True
                        moveBackward = False
                    elif event.key in (K_LEFT, K_a):
                        moveForward = False
                        moveBackward = True
                    elif event.key in (K_UP, K_w) and jump == 0:
                        jump = 1
                elif event.type == KEYUP:
                    if event.key in (K_RIGHT, K_d):
                        moveForward = False
                    elif event.key in (K_LEFT, K_a):
                        moveBackward = False
                                                                    
        if not gameOverMode:
            if moveBackward and playerObj['x']>5:
                playerObj['x'] -= MOVERATE
            if moveForward:
                playerObj['x'] += MOVERATE

            enemyObj['x'] -= ENEMYMOVERATE

            if enemyObj['x'] < playerObj['x']-300:
                enemyObj['x'] = playerObj['x']+SCREENWIDTH+random.randint(0, SCREENWIDTH)           

            if jump>0:
                if jump>36:
                    playerObj['y'] -= round((jump - 36)/3)
                else:
                    playerObj['y'] += round((36 - jump)/3)
                jump += 1
	    
                if playerObj['y'] <= 0: 
                    playerObj['y'] = 0
                    jump = 0 

            if pygame.sprite.collide_mask(playerSprite, heartSprite):
                heartObj['x'] = playerObj['x']+SCREENWIDTH+random.randint(0, SCREENWIDTH)
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
    moving    = False
    PTS = 0

    gameOverMode = False
    gameOverSurf = BASICFONT.render('Game Over', True, (255, 255, 255) )
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (int( SCREENWIDTH / 2 ), int( SCREENHEIGHT / 2 ))

    bowSurf = pygame.image.load('Bow.png')
    bowRect = (SCREENWIDTH-286, SCREENHEIGHT-256)

    playerObj = {'surface': pygame.transform.smoothscale(KITTY_IMG, (SIZEX, SIZEY)),
                 'x': int(SCREENWIDTH / 2),
                 'y': int(SCREENHEIGHT / 2),
		}

    enemyObj = {'surface': pygame.transform.smoothscale(ENEMY_IMG, (ESIZEX, ESIZEY)),
                 'x': random.randint(0, SCREENWIDTH),
                 'y': random.randint(0, SCREENHEIGHT),
		}

    heartObj = {'surface': pygame.transform.smoothscale(HEART_IMG, (HSIZEX, HSIZEY)),
                 'x': random.randint(0, SCREENWIDTH),
                 'y': random.randint(0, SCREENHEIGHT),
		}

    while True:
        if android:
            if android.check_pause():
                android.wait_for_resume()
                
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
                if event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                moving = True                               
            elif event.type == MOUSEBUTTONUP:
                moving = False
                moveLeft = False
                moveRight = False
                moveUp = False
                moveDown = False
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
            
        if moving:
            x, y = pygame.mouse.get_pos()
            if x > playerObj['x'] + 5:
                moveLeft = False
                moveRight = True
            elif x < playerObj['x'] - 5:
                moveLeft = True
                moveRight = False				
            else:
                moveLeft = False
                moveRight = False
            if y > playerObj['y'] + 5: 
                moveUp = False
                moveDown = True
            elif y < playerObj['y'] - 5:
                moveUp = True
                moveDown = False
            else:  
                moveUp = False
                moveDown = False

        if not gameOverMode:
            if moveLeft and playerObj['x'] > 0:
                playerObj['x'] -= MOVERATE
            if moveRight and playerObj['x'] < SCREENWIDTH:
                playerObj['x'] += MOVERATE
            if moveUp and playerObj['y'] > 0:
                playerObj['y'] -= MOVERATE
            if moveDown and playerObj['y'] < SCREENHEIGHT:
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
                heartObj['x'] = random.randint(0, SCREENWIDTH)
                heartObj['y'] = random.randint(0, SCREENHEIGHT)
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
