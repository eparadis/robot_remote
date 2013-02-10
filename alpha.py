
# pull data from the robot
# calculate its position and target heading to a fixed waypoint

import sys

# my stuff
from robot_util import *
from robot_math import *

serialPort = sys.argv[1]
wheelbase = 16  # centimeters

serialObj = SetupComm()

def Setup() :
    print "doing setup..."
        

def Loop() :
    print "inside loop"
    data = ParseStatusMessage( serialObj.readline())
    print CalcPosition( data['left_enc'], data['right_enc'], wheelbase)



# execution starts here
Setup()

while True :
    Loop()


