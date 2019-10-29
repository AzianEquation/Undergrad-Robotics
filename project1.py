# coded by John Esco, Adam Kenvin, Changxuan Yao Copyright 2018
import interface
import connection
import serial
import struct
import time

# closes and then opens the connection.
connection.close()
connection.open()

# Starts roomba, which automatically sets it to passive mode.
interface.start()
# Sets roomba to save mode.
interface.safe()

# creates a infinite while loop that breaks the clean button is pressed. 
while(1):
    if (interface.readButton() == 1):
        break

# waits 0.5 for the code to process.
time.sleep(0.5)

# Uses a for loop to run drive and turn codes six times.
for i in range(6):
    # x is an integer that keeps the times that button is pressed.
    # declared to be 0 at the beginning.
    x = 0

    # waits 0.015 seconds for the code to process.
    interface.sleep()

    # Drives straight at a speed of 200 mm per second.
    x = interface.drive(0, 200, 0, 200)

    # time = distance/speed = 30 cm / 20 cm/s = 1.5 s

    # loop is repeated 50 times because the readButton() method sleep 
    # 0.03 seconds in total, and 1.5 seconds/0.03 seconds = 50 times.

    # waits for a total of 1.5 seconds (drives straight for 30 cm)
    # while checking the clean button state.
    for i in range(50):
	if (interface.readButton() == 1):
	    x += 1;

    # checks if the button is pressed once or more than once, if yes 
    # then stop the robot.
    if (x >= 1):
        interface.drive(0, 0, 0, 0)
	interface.sleep()
        x = 0
	interface.sleep()
	# if the button is pressed again, break the loop and continue.
        while (interface.readButton() == 0 ):
            if (interface.readButton() == 1):
                break
    # sleeps and resets x for the next check.
    interface.sleep()
    x = 0
    interface.sleep()

    # drives with the right wheel velocity being 200 mm per second and 
    # left wheel velocity being -200 mm per second.
    x = interface.drive(0, 200, 255, 56)

    # angular speed = (vr - vl)/l = (20 cm - (-20 cm))/23.5cm = 1.0721 
    # radians per second.
    # total turning angle would be 60 degrees, which is pi/3 radians, 
    # since it is in a hexagonal shape.
    # time = total angle/angular speed = pi/3 / 1.0721 = 0.615229 
    # seconds.
    # we need to run 20 times, since the total time needed is 0.615229 
    # seconds, and each button read waits for 0.03 seconds. 0.615229 
    # seconds/0.03 seconds ~ 20 times.
    for i in range(20):
	if (interface.readButton() == 1):
	    x += 1

    # if the button is recorded to be pressed, stop the robot.
    if (x >= 1):
        interface.drive(0, 0, 0, 0)
	interface.sleep()
        x = 0
	interface.sleep()
	# if the button is pressed again, breaks the loop and starts 
	# the robot.
        while (interface.readButton() == 0):
             if (interface.readButton() == 1):
                break
    # waits 0.015 seconds for codes to process.
    interface.sleep()
    # resets the button press count to 0.
    x = 0
    # waits another 0.015 seconds for the codes to process.
    interface.sleep()

# stops the robot from driving.
interface.drive(0, 0, 0, 0)

# stops robot.
interface.stop()
# closes connection.
connection.close()
