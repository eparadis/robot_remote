import sys
import serial

def SetupComm( ) :
    ser = serial.Serial(sys.argv[1], 115200, timeout=2)
    maxcount = 10
    if(len(sys.argv) == 3) :
        maxcount = int(sys.argv[2])
    ser.flushInput  # blow away whatever is in the input buffer

def ParseStatusMessage( line )
    """given a raw line from the robot that is a status message (starts with LE), return a dict of all the data"""
    tokens = line.rstrip().split(' ')
    # we could loop or do a lot of clever things, but for now its something simple
    dataDict = { 'left_enc' : int(tokens[1]), 'right_enc' : int(tokens[3]) }

def CreatePIDTuningsMessage( Kp, Ki, Kd)
    """return a string suitable for sending to the robot"""
    # the trailing space is SUUUUPER important! (it tells the robot that we're done >_>
    return "K " + str(Kp) + " " + str(Ki) + " " + str(Kd) + " "

def CreateMotorSpeedMessage( left, right )
    """return a string suitable for sending to the robot"""
    # again, don't forget the trailing space 
    return "M " + str(left) + " " + str(right) + " "



