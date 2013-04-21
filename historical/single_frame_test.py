from robot_util import *
import os

expRes = []
for line in open("more_test_frames/results.txt", 'r'):
    if line[0] != '#' and len(line) > 7:
        sp = line.split()
        a = GetPositionsFromLogEntry("1.0,1.0,5,../more_test_frames/" + sp[0])
        a = a[1] # we don't care about the first half of the returned pair
        b = (float(sp[1]), float(sp[2]), float(sp[3]))
        print "calc results", a, "exp results", b

#for f in [filename for filename in os.listdir("more_test_frames") if filename[-4:] == ".jpg"]:
#    print f, GetPositionsFromLogEntry("1.0,1.0,5,../more_test_frames/" + f)

#print GetPositionsFromLogEntry("1.0,1.0,5,20130308-231925.jpg")
