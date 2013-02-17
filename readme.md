Mobile Robot Remote Control
by Ed Paradis

Arduino + Python + pygame + openCV

draw_pos.py - creates a pygame window to let you see the computed path and drive using the arrow keys
umbmark.py - lets you run umbmark-style squares for calibrating your odometry system

setup:
I developed this on a Mac running OS X 10.7.5
I used homebrew to install all the goodies: python, pygame (and its requirements), and openCV (and its requirements)

usage:
  python remote.py /dev/tty.usbmodem1a21

note to self:
- if using the USB serial port, remember to unplug the bluetooth module (specifically pin 0, RX, orange wire)

TODO
- port ArUco to python openCV bindings
- mount a fiducial to the bot to measure its end position when running umbmark squares so I can avoid using rulers


