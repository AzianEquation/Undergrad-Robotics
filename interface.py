import connection
import serial
import struct
import time

# starts the robot, also sets robot to passive mode.
def start():
    connection.write(128)

# resets the robot.
def reset():
    connection.write(7)

# stops the robot.
def stop():
    connection.write(173)

# sets the robot to safe mode.
def safe():
    connection.write(131)

# uses opcode 145 (driveDirect) to drive the robot.
def drive(a, b, c, d):
    connection.write(145)
    connection.write(a)
    connection.write(b)
    connection.write(c)
    connection.write(d)
    if(readButton() == 0):
        return 0
    elif(readButton() == 1):
	return 1
    return 0

# uses the sleep method to wait 0.015 seconds.
def sleep():
    time.sleep(0.015)

# reads the buttons' states, returns 1 when clean button is pressed.
def readButton():
    # requests sensor packet data.
    connection.write(142)
    # waits 0.015 seconds for the code to process.
    sleep()
    # requests button packet data.
    # should read 1 byte which is returned.
    connection.write(18)
    # waits 0.015 seconds for the code to process.
    sleep()
    # reads data from the buttons.
    data = connection.read(1)
    # unpacks the data read to byte.
    byte = struct.unpack('B' ,data)[0]
    return byte 
    
