import sys
import serial
ser = serial.Serial(sys.argv[1], 115200, timeout=2)
maxcount = 10
if(len(sys.argv) == 3) :
    maxcount = int(sys.argv[2])
ser.flushInput  # blow away whatever is in the input buffer

count = 0
while( count < maxcount) :
    line = ser.readline()
    print str(count) + " from bot: " + line
    tokens = line.split(' ')
    #print tokens
    if( tokens[0] == 'LE' ) :
        enc_left = int(tokens[1])
        enc_right = int(tokens[3])
        print (enc_left, enc_right)
        count = count + 1
    if( count%10 == 9) :
        # try to reset the encoders
        print "clearing encoders..."
        ser.write( "Z " )

