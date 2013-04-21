import sys
sys.path.append( 'lib')
# some functions to do some math
import math
from euclid import *

def CalcPosition( left_enc, right_enc, wheel_base, curr_rot ) :
    """give encoder ticks and the robot's wheel base, return X Y position and heading in degrees
    note! has some non-obvious assumptions: see notebook for Feb 9th 2013
    X and Y position units depend on wheel_base units"""
    distance = ( left_enc + right_enc ) / 2.0
    theta = ( left_enc - right_enc) / wheel_base    # we say 0 is straight ahead, positive theta is to the RIGHT!
    theta = theta + math.radians(curr_rot)
    xPos = distance * math.sin(theta)   # note unusual sin/cos usage
    yPos = distance * math.cos(theta)
    return (xPos, yPos, math.degrees(theta))

def TurnTowardsPoint( curPos, curHeading, targetPos ) :
    """given the current robot position and heading, return wheel speeds to turn the robot towards a given target
    point. positions are pairs/tuples"""
    diffPos = ( targetPos[0] - curPos[0], targetPos[1] - curPos[1])
    bearing = math.degrees(math.atan2( diffPos[1], diffPos[0]))   # atan2(y,x)
    bearing = 90 - bearing # we heading/bearing in a non-standard way
    if bearing > 180.0 : 
        bearing = bearing - 360.0
    elif bearing < -180 :
        bearing = bearing + 360.0
    turnRequired = bearing - curHeading
    if turnRequired > 180.0 :
        turnRequired = turnRequired - 360.0
    if turnRequired < -180.0 :
        turnRequired = turnRequired + 360.0
    speed = abs( turnRequired / 18.0)
    print "bearing: ", bearing, "turnReq: ", turnRequired
    if( turnRequired < 1) :
        return ( 0 - speed, speed)
    elif( turnRequired > 1) :
        return ( speed, 0 - speed)
    else :
        return (speed, speed)

def CalcPosAccumulator( curr, acc) :
    heading = curr[2]  
    if( heading < -180.0) :
        heading = heading + 360.0
    if( heading > 180.0) :
        heading = heading - 360.0
    return ( curr[0] + acc[0], curr[1] + acc[1], heading )

def Distance( pos, waypoint) :
    return math.sqrt( math.pow((pos[0]-waypoint[0]),2) + math.pow(pos[1]-waypoint[1],2))

#def InverseProjection( Vt, Vr ) :
#    """TODO given a translation and rotation vector, calculate position and orientation on a horizontal plane"""
#    X = 0
#    Y = 0
#    R = 0
#    return (X, Y, R)

def CalcPositionFromMarkers( robotTR, groundTR):
    # matR = robot frame in reference to camera frame
    matR = Matrix4.new_identity()
    matR.translate(*robotTR[0])
    matRq = Quaternion(*robotTR[1]).get_matrix()
    matR = matR * matRq
    # matW = world/ground marker in refernce to camera frame
    matW = Matrix4.new_identity()
    matW.translate(*groundTR[0])
    matWq = Quaternion(*groundTR[1]).get_matrix()
    matW = matW * matWq
    # matX = robot frame in refernce to world/ground frame
    matX = matW.inverse() * matR
    robotPos = Ray3(Point3(0,0,0), Vector3(1,0,0)) # the robot thinks its at origin and aligned with x-axis of marker
    r = matX*robotPos # robot position
    #print "DEBUG robot marker height", r.p[2] 
    zRot = 90 - math.degrees(math.atan2(r.v[1], r.v[0])) # we do robot 'rotation' a little weird, 
                                                         # so handle that and clamp values
                                                         # also note marker axes may be goofy depending on CV processing 
    if zRot > 180:
        zRot -= 360
    if zRot < -180:
        zRot += 360
    #print "pos X Y R ", r.p[0], r.p[1], zRot
    return ( r.p[0], r.p[1], zRot)  

