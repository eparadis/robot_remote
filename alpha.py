
# pull data from the robot
# calculate its position and target heading to a fixed waypoint

import sys

# my stuff
from robot_util import *
from robot_math import *

serialPort = sys.argv[1]
wheelbase = 99.0 * 16.0 / 15.6  # in encoder ticks 
waypoint = (50, 50) 

print "doing setup..."
serialObj = SetupComm()
prevDeltaPos = (0,0,0)
deltaPos = (0,0,0)
posAcc = (0,0,0)

print "inside loop"
while True :
    data = ParseStatusMessage( serialObj.readline())
    print "{0} {1}".format(data['left_enc'], data['right_enc']) 
    prevDeltaPos = deltaPos 
    deltaPos = CalcPosition( data['left_enc'], data['right_enc'], wheelbase)
    posAcc = CalcPosAccumulator( prevDeltaPos, deltaPos, posAcc)
    print "position " + str(posAcc)
    print "nav " + str( TurnTowardsPoint( (posAcc[0],posAcc[1]), posAcc[2], waypoint))
    print "distance " + str(Distance( (posAcc[0],posAcc[1]), waypoint))


