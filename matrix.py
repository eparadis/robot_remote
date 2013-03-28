from euclid import *
import math

#marker 290
groundTR = ((-1.72276, 7.38742, 25.6409), (-2.51317, -0.016401, -0.0833841))

#marker 678
robotTR = ((-24.2136, 3.16466, 28.7558), (-1.26046, 0.761938, -1.94073))

matR = Matrix4.new_translate(*robotTR[0]).rotate_euler(*robotTR[1])
print "DEBUG: matR (robot frame to camera frame)"
print matR

matW = Matrix4.new_translate(*groundTR[0]).rotate_euler(*groundTR[1])
print "DEBUG: matW (ground/world frame to camera frame)"
print matW

matX = matW.inverse() * matR
print "DEBUG: xfrm matrix ", matX

point = Point3(0,0,0)
print "point ", matX*point

# the robot thinks its at origin facing up the Y-axis
robotPos = Ray3(Point3(0,0,0), Vector3(0,1,0))
print "position ", matX*robotPos
r = matX*robotPos
zRot = 90 - math.degrees(math.atan2(r.v[1], r.v[0]))
if zRot > 180:
    zRot -= 360
if zRot < -180:
    zRot += 360
print "pos X Y R ", r.p[0], r.p[1], zRot 

