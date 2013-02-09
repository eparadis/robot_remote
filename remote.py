import sys
import serial
ser = serial.Serial(sys.argv[1], 115200, timeout=2)
maxcount = 10
if(len(sys.argv) == 3) :
    maxcount = int(sys.argv[2])
ser.flushInput  # blow away whatever is in the input buffer

speed = 5 # the speed we want to tell the robot to go

count = 0
while( count < maxcount) :
    line = ser.readline().rstrip()
    print str(count) + " from bot: " + line
    tokens = line.split(' ')
    #print tokens
    if( tokens[0] == 'LE' ) :
        enc_left = int(tokens[1])
        enc_right = int(tokens[3])
        #print (enc_left, enc_right)
        count = count + 1
    if( enc_left > 500) :
        print( "-> L " + str(-speed))
        ser.write( "L " + str(-speed))
    if( enc_left < 0 ) :
        print( "-> L " + str(speed))
        ser.write( "L " + str(speed))


