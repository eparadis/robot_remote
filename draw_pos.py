import pygame, sys
from pygame.locals import * # get some constants
from collections import deque

# setup the robot stuff
from robot_util import *
from robot_math import *
from renderlines import *   # a nice way to render multiline text off the pygame font docs comments

serialPort = sys.argv[1]
#wheelbase = 99.0 * 16.0 / 15.6  # in encoder ticks, flat slick wheels 
wheelbase = 95.0 * 162.5 / 170.0  # in encoder ticks, knobby round wheels
waypoint = (50, 50)

print "doing setup..."
serialObj = SetupComm()
kPID = (14.0, 7.0, 0.02)
serialObj.write( CreatePIDTuningsMessage(kPID ))
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
fontObj = pygame.font.SysFont('arial', 16)
msg = "no message yet"
lineQueue = deque()

# drawing loop
while True:
    # grab data from the robot
    data = ParseStatusMessage( serialObj.readline())
    print "enc {0} {1}".format(data['left_enc'], data['right_enc'])
    prevEnc = enc
    enc = (data['left_enc'], data['right_enc'])
    print "deltaEnc ", ( enc[0]-prevEnc[0], enc[1]-prevEnc[1])
    deltaPos = CalcPosition( enc[0]-prevEnc[0], enc[1]-prevEnc[1], wheelbase, posAcc[2])
    posAcc = CalcPosAccumulator( deltaPos, posAcc)
    print "position " + str(posAcc)
    print "nav " + str( TurnTowardsPoint( (posAcc[0],posAcc[1]), posAcc[2], waypoint))
    print "distance " + str(Distance( (posAcc[0],posAcc[1]), waypoint))   
    posMsg = "X:{0:.2f}  Y:{1:.2f}  R:{2:.2f}deg".format(*posAcc)
    pidMsg = "Kp:{0:.2f}  Ki:{1:.2f}  Kd:{2:.2f}".format(*kPID)

    # store the position (if its new)
    if deltaPos[0] != 0 or deltaPos[1] != 0 :
        lineQueue.append( posAcc )
    if len(lineQueue) > 300 :
        lineQueue.popleft()

    ### draw the visualization
    # the background
    windowSurfaceObj.fill( blackColor)

    # draw the text message
    msgSurfaceObj = renderLines( [posMsg, pidMsg], fontObj, False, whiteColor)
    #msgSurfaceObj = fontObj.render( msg, False, whiteColor)
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (10,10)
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
            print "SHUTTING DOWN..."
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE:
                pygame.event.post( pygame.event.Event(QUIT))
            if event.key == K_z:
                serialObj.write( CreateEncoderZeroMessage() )
                lineQueue.clear()
                posAcc = (0,0,0)
            if event.key == K_UP :
                serialObj.write( CreateMotorSpeedMessage( 10, 10))
            if event.key == K_DOWN :
                serialObj.write( CreateMotorSpeedMessage( -10, -10))
            if event.key == K_RIGHT :
                serialObj.write( CreateMotorSpeedMessage( 10, -10))
            if event.key == K_LEFT :
                serialObj.write( CreateMotorSpeedMessage( -10, 10))
            if event.key == K_SPACE :
                serialObj.write( CreateMotorSpeedMessage( 0, 0))

            if event.key == K_w :
                kPID = (kPID[0]+0.1, kPID[1], kPID[2])
                serialObj.write( CreatePIDTuningsMessage(kPID) )
            if event.key == K_s :
                kPID = (kPID[0]-0.1, kPID[1], kPID[2])
                serialObj.write( CreatePIDTuningsMessage(kPID) )
            if event.key == K_e :
                kPID = (kPID[0], kPID[1]+0.1, kPID[2])
                serialObj.write( CreatePIDTuningsMessage(kPID) )
            if event.key == K_d :
                kPID = (kPID[0], kPID[1]-0.1, kPID[2])
                serialObj.write( CreatePIDTuningsMessage(kPID) )
            if event.key == K_r :
                kPID = (kPID[0], kPID[1], kPID[2]+0.01)
                serialObj.write( CreatePIDTuningsMessage(kPID) )
            if event.key == K_f :
                kPID = (kPID[0], kPID[1], kPID[2]-0.01)
                serialObj.write( CreatePIDTuningsMessage(kPID) )









    pygame.display.update() # draw everything
    #fpsClock.tick(30)   # regulate to 30 fps


