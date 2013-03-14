import sys
import serial
import string
import subprocess

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

def CreatePIDTuningsMessage( (Kp, Ki, Kd) ) :
    """return a string suitable for sending to the robot"""
    # the trailing space is SUUUUPER important! (it tells the robot that we're done >_>
    return "K " + str(Kp) + " " + str(Ki) + " " + str(Kd) + " "

def CreateMotorSpeedMessage( left, right ) :
    """return a string suitable for sending to the robot"""
    # again, don't forget the trailing space 
    return "M " + str(int(left)) + " " + str(int(right)) + " "

def CreateEncoderZeroMessage() :
    """return a string suitable for sending to the robot"""
    return "Z "

def MakeDataRecord( odoPos, imgFile) :
    """given (x,y,theta) and a filename, make an entry into the data log"""
    logfile = "datalog.csv"
    # format is CSV
    # Xpos, Ypos, theta, filename
    # TODO write to the file

def GetPositionsFromLogEntry( line ) :
    """given a line from the CSV logfile, call the ArUco image processor and return the positions of the static marker, the robot marker, and the robot's position as a list of tuples"""
    odoPos = (0,0,0)    # X Y and Theta
    robotMarker = (0,0,0)   # X Y and Theta
    staticMarker = (0,0,0)  # X Y and Theta
    # grab the data from the given line
    #line = "1.0,1.0,5,20130308-231905.jpg" # example data
    lineSplit = line.split(',') 
    odoPos = (lineSplit[0], lineSplit[1], lineSplit[2])
    # call ArUco
    aruco = '/Users/ed/src/opencv/build/aruco-1.2.4/build/utils/aruco_simple'
    image = '/Users/ed/git/robot_remote/test_frames/' + lineSplit[3]
    cal = '/Users/ed/git/robot_remote/htc_one_cal/cal.yml'
    size = '3.622' # side of marker in inches, only counting the black part
    response = subprocess.check_output([aruco, image, cal, size]).splitlines()
    for r in response:
        sp = r.split(',')
        if(len(sp) >= 14) :
            markerID = sp[0]
            T = (sp[9], sp[10], sp[11])
            R = (sp[12], sp[13], sp[14])
            print "marker ",markerID," at T",T," R",R 
            
            # parse the markers of interest
            # call a function to transform/project the Txyz,Rxyz data from a marker to the plane X,Y,Theta of the robot positioning code
            if( int(markerID) == 290) :
                staticMarker = InverseProjection( T, R)
            if( int(markerID) == 678) :
                robotMarket = InverseProjection( T, R)
    # return the properly transformed data
    return (odoPos, robotMarker, staticMarker)

def MeasurePositionOffset( (odoPos, robotMarker, staticMarker) ) :
    """given the positions of the robotMarker and the staticMarker, calculate where the robot is located..."""
    # X and Y: static - robot  (ie: distance to robot from static marker)
    # heading: assume static marker points "north/0deg" so offset the robot's rotation by that much
    return  (staticMarker[0] - robotMarker[0], staticMarker[1] - robotMarker[1], robotMarker[2] - staticMarker[2] )

def CalculateUMBMarkCorrections( cwOffset, ccwOffset, sideLength ) :
    """given difference in robot position from start in one dimension (it doesn't matter which) and the length of the side of the square it traveled, return scaling factors for wheelbase and wheel diameters""" 
    # L = length of the side of the square traveled (4meters in original paper)
    # x_c.g.cw = average x offset of final robot position during clockwise runs
    alpha = math.degrees((cwOffset + ccwOffset) / ( -4*sideLength))  # alpha = ( x_c.g.cw + x_c.g.ccw ) / -4*L * (180deg/pi)     (eq 6.26a)
    beta = math.degrees((cwOffset - ccwOffset) / ( -4*sideLength)) 
    # wb_act = 90deg/(90deg-alpha)*wb_nom     (eq 6.28)
    E_b = 90 / (90 - alpha) # E_b = 90deg/(90deg-alpha)             (eq 6.29)
    R = (sideLength/2) / math.sin(math.radians(beta/2))
    E_d = (R + beta / 2) / (R - beta / 2)
    return ( E_b, E_d)


