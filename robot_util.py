import sys
import serial

def SetupComm( ) :
    ser = serial.Serial(sys.argv[1], 115200, timeout=2)
    ser.flushInput  # blow away whatever is in the input buffer
    # snarf junk data until we're getting good stuff
    count = 0
    while count < 6 :
        line = ser.readline().rstrip()
        data = ParseStatusMessage(line)
        print data
        if len(data) >= 2 :
            count = count + 1
            print "snarf"
    return ser

def ParseStatusMessage( line ) :
    """given a raw line from the robot that is a status message (starts with LE), return a dict of all the data"""
    line = line.rstrip()
    tokens = line.split(' ')
    # we could loop or do a lot of clever things, but for now its something simple
    if len(tokens) >= 4 : 
        dataDict = { 'left_enc' : int(tokens[1]), 'right_enc' : int(tokens[3]) }
        return dataDict
    return {}

def CreatePIDTuningsMessage( Kp, Ki, Kd) :
    """return a string suitable for sending to the robot"""
    # the trailing space is SUUUUPER important! (it tells the robot that we're done >_>
    return "K " + str(Kp) + " " + str(Ki) + " " + str(Kd) + " "

def CreateMotorSpeedMessage( left, right ) :
    """return a string suitable for sending to the robot"""
    # again, don't forget the trailing space 
    return "M " + str(left) + " " + str(right) + " "



