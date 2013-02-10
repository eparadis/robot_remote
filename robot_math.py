# some functions to do some math
import math

def CalcPosition( left_enc, right_enc, wheel_base )
    """give encoder ticks and the robot's wheel base, return X Y position and heading in degrees
    note! has some non-obvious assumptions: see notebook for Feb 9th 2013
    X and Y position units depend on wheel_base units"""
    distance = ( left_enc + right_enc ) / 2.0
    theta = ( left_enc - right_enc) / wheel_base    # we say 0 is straight ahead, positive theta is to the RIGHT!
    headingDeg = math.degrees(theta)
    xPos = distance * math.sin(theta)   # note unusual sin/cos usage
    yPos = distance * math.cos(theta)

    return (xPos, yPos, headingDeg)


