import interface
import connection
import serial
import struct
import time
import random

"""
change the interface to include IR distance sensor. (max range is a few inches)
if robot stoped, then clean press initializes wall following behavior.should use PD contoller. 
Goal of controller should be to keep this sensor value at a given set point.  
choose set points and gains to keep robot moving parallel to straight wall without drifting away, 
bumping wall, or oscilation. (in report 'Description' describe process of selecting set points and gain). 
if the robot is moving a clean press stops the robot 
"""
connection.close()
connection.open()
# Starts roomba.
interface.start()
# Sets roomba to safe mode.
interface.full()
# Initializes kp and kd values and the values used in the loop.
kp = 0.05
kd = 0.05
u = 0
setpoint = 250
error0 = 0
error1 = 0
timeT = 0.015
# Initializes gains used in the loop. 
uMax = 75
uMin = -75
rightBiasGain = 40
wallGain = 130 
# This function checks for button press and stops the robot.
def listen():
   if (interface.readButton() == 1):
       interface.driveDirect(0,0,0,0)
       interface.sleep()
       while(1):
           if(interface.readButton() == 1):
               break
# This funtion makes the robot turn 90 degrees clockwise.
def turnClockwise():
    interface.driveDirect(255,56,0,200)
    time.sleep(0.61)
# This funtion makes the robot turn 90 degrees counterclockwise.
def turnCounterClockwise():
    interface.driveDirect(0,200,255,56)
    time.sleep(0.61)
# Makes sure the robot is stopped in the beginning.
interface.driveDirect(0,0,0,0)
# Waits for button press to start the robot.
while(1):
    interface.sleep()
    if (interface.readButton() == 1):
        break
interface.driveDirect(0, 150, 0, 160)
# If the right light bump sensor return value less than 30, the robot drives forward and turns slightly to the right.
while (interface.LBRight < 30):
    print "NO WALL"
    interface.driveDirect(0, 150, 0, 160)
    time.sleep(timeT)
    listen()
# Creates a while loop that keeps the robot running.
while(1):
    # Checks for bump sensor, index 1 = left, index 0 = right 
    # TEST CODE
    # 172 = red && green    161 = force field  168 = red 164 =green
    
    dock = interface.IRCharOmni()
    dockBool = False;
    if (dock == 168):
        print "found red buoy"
        interface.driveDirect(0,200,255,56)
        time.sleep(0.61)
        interface.driveDirect(0,0,0,0)
        interface.sleep()
        dockBool = True;
    while (dockBool == True):
        # read IRCharOmni
        dock1 = interface.IRCharOmni()
        interface.sleep()
        charge = interface.charge()
        interface.sleep()
        bumpRight = interface.bumpWheelDrop(0)
        interface.sleep()
        bumpLeft = interface.bumpWheelDrop(1)
        interface.sleep()
        # move forward slowly
        interface.driveDirect(0, 90, 0, 90)
        # if red (on right) then must turn left
        if (dock1 == 172):
        # drive straight
            print "driving in both buoys"
            interface.driveDirect(0, 100, 0, 100)
            interface.sleep()
        # if green (on left) then must turn right
        elif (dock1 == 164):
            print "found green turning right"
            interface.driveDirect(0,0,0,0)
            interface.sleep()
            interface.driveDirect(0,0,0,90)
            interface.sleep()
        # if both (in middle) go straight
        elif (dock1 == 168):
            print "found red turning left"
            interface.driveDirect(0,0,0,0)
            interface.sleep()
            interface.driveDirect(0,90,0,0)
            interface.sleep()
        if (charge == 2):
            print "arrived at dock (charger)" 
            interface.driveDirect(0,0,0,0)
            interface.sleep()
            interface.song()
            interface.sleep()
            interface.play()
            exit(0)
        if (bumpRight == 1 or bumpLeft == 1):
            print "arrived at dock (bumper)"
            interface.driveDirect(0,0,0,0)
            interface.sleep()
            interface.song()
            interface.sleep()
            interface.play()
            exit(0)

    ## TEST CODE
    bumpRight = interface.bumpWheelDrop(0)
    interface.sleep()
    bumpLeft = interface.bumpWheelDrop(1)
    interface.sleep()
    # If both bumpers are pressed, turn counterclockwise.
    if (bumpRight == 1 and bumpLeft == 1):
        turnCounterClockwise()
    # If right bumper is pressed, turn counterclockwise.
    elif (bumpRight == 1):
        print "ccw"
        turnCounterClockwise()
    # If left bumpter is pressed, turn clockwise.
    elif (bumpLeft == 1):
        print "cw"
        turnClockwise()
   # if right light bumper stops sensing obstacle, turns right.
    if(interface.LBRight() < 20 and error0 != 0):
        print "Turning Right"
        interface.driveDirect(0, 60, 0, 200)
        time.sleep(timeT)
        listen()
    # If the robot senses a wall at wallGain distance, rotate.
    elif (interface.LBFrontLeft() > wallGain):
        # ccw
        print "turning CCW", interface.LBFrontLeft()
        turnCounterClockwise()
        time.sleep(timeT)
        listen()
    # If the robot approaches wall, add u(action) to right speed.
    elif (interface.LBFrontRight() > interface.LBRight()):
        error1 = setpoint - interface.LBRight()
        u =(int)((kp*error1) + kd*((error1 - error0)/timeT))
        if(u > uMax):
            u = uMax
        elif(u < uMin):
            u = uMin
        print "u added to Right wheel, approach wall", u
        interface.driveDirect(0, 150 + u, 0, 150 )
        time.sleep(timeT)
        listen()
        # past error
        error0 = error1
        # general straight line and error
    # If the robot shifts away from the wall, subtract u(action) from right speed.
    elif (interface.LBFrontRight() <= interface.LBRight()):
        error1 = setpoint - interface.LBRight()
        u = (int)((kp*error1) + kd*((error1 - error0)/timeT))
        if(u > uMax):
            u = uMax
        elif(u < uMin):
            u = uMin
        print "u slows right wheel, wall following", u
        interface.driveDirect(0, 150-u , 0, 150 )
        time.sleep(timeT)
        listen()
        error0 = error1
#Stops roomba.
interface.stop()
#Ends connection.
connection.close()
