import pygame, sys
from pygame.locals import * # get some constants
from collections import deque

# setup the robot stuff
from robot_util import *
from robot_math import *

serialPort = sys.argv[1]
wheelbase = 99.0 * 16.0 / 15.6  # in encoder ticks 
waypoint = (50, 50)

print "doing setup..."
serialObj = SetupComm()
deltaPos = (0,0,0)
posAcc = (0,0,0)
enc = (0,0)
prevEnc = (0,0)

# setup the visualization stuff
pygame.init()
fpsClock = pygame.time.Clock()
windowSurfaceObj = pygame.display.set_mode( (640,480) )
pygame.display.set_caption( 'Robot Remote Data Visualizer' )
redColor = pygame.Color(255,0,0)
whiteColor = pygame.Color(255,255,255)
blackColor = pygame.Color(0,0,0)
fontObj = pygame.font.Font('freesansbold.ttf', 16)
msg = "no message yet"
lineQueue = deque()

# drawing loop
while True:
    # grab data from the robot
    data = ParseStatusMessage( serialObj.readline())
    print "{0} {1}".format(data['left_enc'], data['right_enc'])
    prevEnc = enc
    enc = (data['left_enc'], data['right_enc'])
    print ( enc[0]-prevEnc[0], enc[1]-prevEnc[1])
    deltaPos = CalcPosition( enc[0]-prevEnc[0], enc[1]-prevEnc[1], wheelbase, posAcc[2])
    posAcc = CalcPosAccumulator( deltaPos, posAcc)
    print "position " + str(posAcc)
    print "nav " + str( TurnTowardsPoint( (posAcc[0],posAcc[1]), posAcc[2], waypoint))
    print "distance " + str(Distance( (posAcc[0],posAcc[1]), waypoint))   

    # store the position (if its new)
    if deltaPos[0] != 0 or deltaPos[1] != 0 :
        lineQueue.append( posAcc )
    if len(lineQueue) > 300 :
        lineQueue.popleft()

    ### draw the visualization
    # the background
    windowSurfaceObj.fill( blackColor)

    # draw the text message
    msgSurfaceObj = fontObj.render( msg, False, whiteColor)
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (10,20)
    windowSurfaceObj.blit( msgSurfaceObj, msgRectObj)

    # draw all the lines
    A = (0,0)
    for q in lineQueue :
        B = (q[0],q[1]) 
        pygame.draw.line( windowSurfaceObj, redColor, (A[0]+320,240-A[1]), (B[0]+320,240-B[1]), 2)
        A = B

    ### handle events 
    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE or event.key == K_q:
                pygame.event.post( pygame.event.Event(QUIT))
            if event.key == K_z:
                serialObj.write( CreateEncoderZeroMessage() )
                lineQueue.clear()

    pygame.display.update() # draw everything
    #fpsClock.tick(30)   # regulate to 30 fps



