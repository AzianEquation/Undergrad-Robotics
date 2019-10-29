
README:

Project 4 contains three python files: connection.py, interface.py,
 and project4.py is the default interface given for establishing 
serial connection between the computer and the raspberry pi. This interface is
 able to open and close this serial communication as well as read and write
 information from and to the robot. connection.py is not intended to be accessed 
or used by the user. 

interface.py contains all the functions to initialize the
 robots state, read data, move the robot, create and play a song, and read the light
bump sensors. 
start - starts the OI and set the
 robot to passive mode
passive - set the robot to passive mode
reset - hard reset
 of the robot as if you have removed the battery from the robot
stop - close the 
OI 
safe - set the robot to safe mode
drive(a,b,c,d) - makes the robot drive using 
a&b as the high and low bits for the velocity 	of the left wheel and c&d for the 
high and low bits of the velocity of the right 	wheel
sleep - helper function called
 to make the program sleep for 0.015 seconds to prevent errors in writing data 
readButton 
- returns an integer corresponding to what button is being pressed on the robot. 


project4.py is the driver class which contains
 the main function of the program. This is the file intended to be called upon 
and used by the user. This driver class opens the serial connection and initializes
 the robot to both passive and safe mode. It then waits for the initial clean 
button press to start the robots wall following functionality. If at any point the 
clean button is pressed the robot will stop. If the robot finds a dock, it will change
its objectives and track and drive to the dock. After it completes these actions, it will
stop and play a song, and then the program will terminate. The wall following implements 
a PD controller that keeps the robot following the wall around a 'setpoint' value. 
The gains can be adjusted as constants at the top of project4.py