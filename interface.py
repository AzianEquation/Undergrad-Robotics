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

# set the robot to full mode
def full():
    connection.write(132)

# uses opcode 145 (driveDirect) to drive the robot.
def driveDirect(a, b, c, d):
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
# bump and wheel drop sensor read
def bumpWheelDrop(index):
    # requests sensor packet data
    connection.write(142)
    # wait for command to be sent
    sleep()
    # request the bump sensor packet
    connection.write(7)
    sleep()
    data = connection.read(1)
    # interbret data as byte
    byte = struct.unpack('B', data)[0]
    # right bump sensor
    bumpRight = bool(byte & 0x01)
    bumpLeft = bool(byte & 0x02)
    wheelDropRight = bool(byte & 0x04)
    wheelDropLeft = bool(byte & 0x08)
    # return bumpRight
    if (index == 0):
        return bumpRight
    elif (index == 1):
        return bumpLeft
    elif (index == 2):
        return wheelDropRight
    elif (index == 3):
        return wheelDropLeft
    elif (index == 4):
        return bool(byte != 0)
    else:
        return byte
# cliff sensor reading takes param idicating which sensor
def cliffRead():
    # declare array to hold results from cliffArray
    cliffArr = [0,0,0,0,0]
    counter = 0
    for i in range(9,14):
        # requests sensor data
        connection.write(142)
        #requests each cliff sensor
        connection.write(i)
        data = connection.read(1)
        byte = struct.unpack('B', data)[0]
        cliffArr[counter] = byte
        counter += 1
    return cliffArr
# angle
def angleRead():
    connection.write(142)
    # packet 20 is angle 
    sleep()
    connection.write(20)
    # returns signed 2 bytes
    sleep()
    data = connection.read(2)
    byte = struct.unpack(">h", data)[0]
    return byte

def distanceRead():
    connection.write(142)
    sleep()
    connection.write(19)
    sleep()
    data = connection.read(2)
    byte = struct.unpack(">h", data)[0]
    return byte

def song():
    connection.write(140)
    sleep()
    connection.write(0)
    sleep()
    # first 16 notes of "Seek and Destroy"
    connection.write(16)
    sleep()
    # A(110) * 2
    connection.write(45)
    sleep()
    connection.write(14)
    sleep()
    connection.write(45)
    sleep()
    connection.write(14)
    sleep()
    # triplet D(294) D#(311) D(294) @ 9
    connection.write(62)
    sleep()
    connection.write(9)
    sleep()
    connection.write(63)
    sleep()
    connection.write(9)
    sleep()
    connection.write(62)
    sleep()
    # may be 9 || 14
    connection.write(14)
    sleep()
    # A(110)
    connection.write(45)
    sleep()
    connection.write(14)
    sleep()
    #triplet A(220) A#(233) A(220) @ 9
    connection.write(57)
    sleep()
    connection.write(9)
    sleep()
    connection.write(58)
    sleep()
    connection.write(9)
    sleep()
    connection.write(57)
    sleep()
    # may be 14  || 9
    connection.write(14)
    sleep()
    # A(110) F(175) @ 14
    connection.write(45)
    sleep()
    connection.write(14)
    sleep()
    connection.write(53)
    sleep()
    connection.write(14)
    sleep()
    # E(175) G(196)
    connection.write(52)
    sleep()
    connection.write(14)
    sleep()
    connection.write(55)
    sleep()
    connection.write(14)
    sleep()
    # E(165) C(262)
    connection.write(52)
    sleep()
    connection.write(14)
    sleep()
    connection.write(60)
    sleep()
    connection.write(14)
    sleep()
    # A(220)
    connection.write(57)
    sleep()
    connection.write(14)
    sleep()
def play():
    connection.write(141)
    connection.write(0)
# Light Bump sensor range 0-4095

# Light Bump Left
def LBLeft():
    connection.write(142)
    sleep()
    connection.write(46)
    sleep()
    # returns 2 unsigned bytes
    data = connection.read(2)
    byte = struct.unpack(">H", data)
    return int(byte[0])
# Light Bump Front Left
def LBFrontLeft():
    connection.write(142)
    sleep()
    connection.write(47)
    sleep()
    # returns 2 unsigned bytes
    data = connection.read(2)
    byte = struct.unpack(">H", data)
    return int(byte[0])
# Light Bump Center Left
def LBCenterLeft():
    connection.write(142)
    sleep()
    connection.write(48)
    sleep()
    # returns 2 unsigned bytes
    data = connection.read(2)
    byte = struct.unpack(">H", data)
    return int(byte[0])
# Light Bump Center Right
def LBCenterRight():
    connection.write(142)
    sleep()
    connection.write(49)
    sleep()
    # returns 2 unsigned bytes
    data = connection.read(2)
    byte = struct.unpack(">H", data)
    return int(byte[0])
# Light Front Right
def LBFrontRight():
    connection.write(142)
    sleep()
    connection.write(50)
    sleep()
    # returns 2 unsigned bytes
    data = connection.read(2)
    byte = struct.unpack(">H", data)
    return int(byte[0])
# Light Bump Right
def LBRight():
    connection.write(142)
    sleep()
    connection.write(51)
    sleep()
    # returns 2 unsigned bytes
    data = connection.read(2)
    byte = struct.unpack(">H", data)
    return int(byte[0])
# Infrared Character Omni
def IRCharOmni():
    connection.write(142)
    sleep()
    connection.write(17)
    sleep()
    # reads data from the buttons.
    data = connection.read(1)
    # unpacks the data read to byte.
    byte = struct.unpack('B' ,data)[0]
    return int(byte)
# Charing source available (2 ||3)
def charge():
    connection.write(142)
    sleep()
    connection.write(34)
    sleep()
    # reads data from the buttons.
    data = connection.read(1)
    # unpacks the data read to byte.
    byte = struct.unpack('B' ,data)[0]
    return byte

