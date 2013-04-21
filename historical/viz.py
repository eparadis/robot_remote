import pygame, sys
from pygame.locals import * # get some constants

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode( (640,480) )
pygame.display.set_caption( 'Robot Remote Data Visualizer' )

# a few colors
redColor = pygame.Color(255,0,0)
whiteColor = pygame.Color(255,255,255)
blackColor = pygame.Color(0,0,0)

fontObj = pygame.font.Font('freesansbold.ttf', 16)

msg = "no message yet"

# drawing loop
while True:
    if pygame.key.get_focused() == False:
        print "Lost keyboard focus!"
        pygame.event.setgrab()

    windowSurfaceObj.fill( blackColor)

    msgSurfaceObj = fontObj.render( msg, False, whiteColor)
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (10,20)
    windowSurfaceObj.blit( msgSurfaceObj, msgRectObj)

    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE:
                pygame.event.post( pygame.event.Event(QUIT))

    pygame.display.update() # draw everything
    fpsClock.tick(30)   # regulate to 30 fps



