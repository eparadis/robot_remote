Mobile Robot Remote Control
by Ed Paradis

Interfaces with the Arduino code (elsewhere) to read sensor values and send commands.

usage:
  python2.7 remote.py /dev/tty.usbmodem1a21

notes:
- if using the USB serial port, remember to unplug the bluetooth module (specifically pin 0, RX, orange wire)

TODO
1. compute robot position (in global coordinates) using encoder data: L&Renc -> theta+mag -> X&Y
2. write TurnTowardsPoint; given CurPos and TargetPos, return L&R speeds to turn towards TargetPos
3. write ReachedPoint; return true if close enough to the target point
4. simple waypoint program
    1. read a list of waypoints from a file
    2. set the first waypoint as the target point
    3. go forwards at a speed proportional to distance to target point
    4. turn towards the target point
    - write data 
    5. if not ReachedPoint, goto 3
    6. if ReachedPoint and not the last waypoint, set the next waypoint as the target point and goto 3
    7. if ReachedPoint and the last waypoint, stop going forwards


