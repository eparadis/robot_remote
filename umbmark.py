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
squareSize = 1000
wayPoints = [(0, squareSize), (squareSize, squareSize), (squareSize, 0), (0,0)]
wayPoints.reverse() # we pop() the waypoints off, so reverse the order
wp = wayPoints.pop()
testFinished = False

print "doing setup..."
serialObj = SetupComm()
kPID = (7.0, 64.0, 0.18)
serialObj.write( CreatePIDTuningsMessage(kPID ))
serialObj.write( CreateEncoderZeroMessage() )
deltaPos = (0,0,0)
posAcc = (0,0,0)
enc = (0,0)
prevEnc = (0,0)

# setup the visualization stuff
pygame.init()
fpsClock = pygame.time.Clock()
windowSurfaceObj = pygame.display.set_mode( (640,480) )
pygame.display.set_caption( 'Robot Remote Data Visualizer' )
graphScale = 0.5 
redColor = pygame.Color(255,0,0)
whiteColor = pygame.Color(255,255,255)
blackColor = pygame.Color(0,0,0)
blueColor = pygame.Color(0,0,255)
fontObj = pygame.font.SysFont('arial', 16)
lineQueue = deque()

def ControlRobot( pos, waypoint ) :
    #print "nav " + str( TurnTowardsPoint( (posAcc[0],posAcc[1]), posAcc[2], waypoint))
    turn = TurnTowardsPoint( (pos[0],pos[1]), pos[2], waypoint)
    speed = 10
    return (turn[0] + speed, turn[1] + speed)

# drawing loop
while True:
    # grab data from the robot
    data = ParseStatusMessage( serialObj.readline())
    prevEnc = enc
    enc = (data['left_enc'], data['right_enc'])
    deltaPos = CalcPosition( enc[0]-prevEnc[0], enc[1]-prevEnc[1], wheelbase, posAcc[2])
    posAcc = CalcPosAccumulator( deltaPos, posAcc)
    posMsg = "X:{0:.2f}  Y:{1:.2f}  R:{2:.2f}deg".format(*posAcc)
    pidMsg = "Kp:{0:.2f}  Ki:{1:.2f}  Kd:{2:.2f}".format(*kPID)
    scaleMsg = "vis zoom:{0:.0%} (use -/= to change)".format(graphScale)

    # store the position (if its new)
    if deltaPos[0] != 0 or deltaPos[1] != 0 :
        lineQueue.append( posAcc )
    if len(lineQueue) > 300 :
        lineQueue.popleft()

    # control the robot
    if( not testFinished) :
        cmdSpds = ControlRobot( posAcc, wp) 
        print "command speeds", cmdSpds
        serialObj.write( CreateMotorSpeedMessage( cmdSpds[0], cmdSpds[1]))
        if( wp == (0,0)) : 
            wayPointThreshold = 0
        else :
            wayPointThreshold = wheelbase
        if( Distance( (posAcc[0], posAcc[1]), wp) < wayPointThreshold ) :
            if( len( wayPoints) > 0) :
                wp = wayPoints.pop()
            else :
                serialObj.write( CreateMotorSpeedMessage( 0, 0))
                testFinished = True
    else :
        print "final position!"

    ### draw the visualization
    # the background
    windowSurfaceObj.fill( blackColor)

    # draw the text message
    msgSurfaceObj = renderLines( [posMsg, pidMsg, scaleMsg], fontObj, False, whiteColor)
    #msgSurfaceObj = fontObj.render( msg, False, whiteColor)
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (10,10)
    windowSurfaceObj.blit( msgSurfaceObj, msgRectObj)

    # draw the current waypoint
    pygame.draw.circle( windowSurfaceObj, blueColor, (int(wp[0]*graphScale)+320, 240-int(wp[1]*graphScale)), int(wheelbase*graphScale), 0)

    # draw all the lines
    A = (0,0)
    for q in lineQueue :
        B = (q[0]*graphScale,q[1]*graphScale) 
        pygame.draw.line( windowSurfaceObj, redColor, (A[0]+320,240-A[1]), (B[0]+320,240-B[1]), 2)
        A = B

    ### handle events 
    for event in pygame.event.get() :
        if event.type == QUIT:
            print "SHUTTING DOWN..."
            serialObj.write( CreateMotorSpeedMessage( 0, 0) )
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE:
                pygame.event.post( pygame.event.Event(QUIT))
            if event.key == K_z:
                serialObj.write( CreateEncoderZeroMessage() )
                lineQueue.clear()
                posAcc = (0,0,0)
            if event.key == K_SPACE :
                serialObj.write( CreateMotorSpeedMessage( 0, 0))
                testFinished = True

            if event.key == K_MINUS :
                graphScale = graphScale / 2.0
            if event.key == K_EQUALS :
                graphScale = graphScale * 2.0

            #

    pygame.display.update() # draw everything
    #fpsClock.tick(30)   # regulate to 30 fps



