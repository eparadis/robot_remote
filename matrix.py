from euclid import *
import math

def dist3( A, B) : 
    '''given two points (as triples), return the distance between them'''
    C = ( A[0]-B[0],A[1]-B[1],A[2]-B[2])
    return math.sqrt( C[0]**2 + C[1]**2 + C[2]**2)

#marker 290
#groundTR = ((-1.72276, 7.38742, 25.6409), (-2.51317, -0.016401, -0.0833841))
groundTR = ((1.88763, 3.77743, 50.1638), (-2.33674, 0.00150832, 0.00458851)) # 20130308-231905.jpg w/ logitech_640

#marker 678
#robotTR = ((-24.2136, 3.16466, 28.7558), (-1.26046, 0.761938, -1.94073))
robotTR = ((-14.9905, -1.07214, 46.2836), (-1.72942, 0.781333, -1.89458)) # 20130308-231905.jpg w/ logitech_640

print "original distance =", dist3(groundTR[0], robotTR[0])

#matR = Matrix4.new_translate(*robotTR[0]).rotate_euler(*robotTR[1])
matR = Matrix4.new_identity()
matR.translate(*robotTR[0])
matR.rotate_euler(*robotTR[1])
print "DEBUG: matR (robot frame to camera frame)"
print matR

matW = Matrix4.new_identity()
matW.translate(*groundTR[0])
matW.rotate_euler(*groundTR[1])
print "DEBUG: matW (ground/world frame to camera frame)"
print matW

matX = matW.inverse() * matR
#matX = matR.inverse() * matW
###matX = matW * matR.inverse() # wrong!
###matX = matR * matW.inverse() # also wrong!
print "DEBUG: xfrm matrix ", matX


# where the robot is aligned in its coordinate system
robotPos = Ray3(Point3(0,0,0), Vector3(1,0,0))
r = matX*robotPos
print "position ", r
print "final distance =", dist3( (0,0,0), r.p)

zRot = 90 - math.degrees(math.atan2(r.v[0], r.v[2]))
if zRot > 180:
    zRot -= 360
if zRot < -180:
    zRot += 360
print "pos X Y R ", 0-r.p[2], 0-r.p[0], zRot 

