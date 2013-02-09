import sys
import serial
ser = serial.Serial(sys.argv[1], 115200, timeout=2)
maxcount = 10
if(len(sys.argv) == 3) :
    maxcount = sys.argv[2]


count = 0
while( count < sys.argv[2]) :
    line = ser.readline()
    print str(count) + " from bot: " + line
    tokens = line.split(' ')
    print tokens
    if( tokens[0] == 'LE' ) :
        enc_left = int(tokens[1])
        enc_right = int(tokens[3])
        print (enc_left, enc_right)
        count = count + 1



