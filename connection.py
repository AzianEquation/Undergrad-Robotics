import serial
import struct
import time
#This connects the program with the roomba
connection = serial.Serial('/dev/ttyUSB0', baudrate=115200)

#This method sends the command to the roomba
def write(a):
    connection.write(chr(a))
    pass

#This method reads in the inputs from the rooba
def read(a):
    output = connection.read(int(a))
    return output
    pass

#This closes the connection
def close():
    connection.close()
    pass

#This opens the connection
def open():
    connection.open()
    pass



