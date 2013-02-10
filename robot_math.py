# some functions to do some math
import math

def CalcPosition( left_enc, right_enc, wheel_base ) :
    """give encoder ticks and the robot's wheel base, return X Y position and heading in degrees
    note! has some non-obvious assumptions: see notebook for Feb 9th 2013
    X and Y position units depend on wheel_base units"""
    distance = ( left_enc + right_enc ) / 2.0
    theta = ( left_enc - right_enc) / wheel_base    # we say 0 is straight ahead, positive theta is to the RIGHT!
    headingDeg = math.degrees(theta)
    xPos = distance * math.sin(theta)   # note unusual sin/cos usage
    yPos = distance * math.cos(theta)

    return (xPos, yPos, headingDeg)

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
    turnRequired = bearing - heading
    if( turnRequired < 0) :
        return (-10.0, 10.0)
    elif( turnRequired > 0) :
        return (10.0, -10.0)
    else :
        return (0.0, 0.0)



