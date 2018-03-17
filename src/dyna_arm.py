#!/usr/bin/env python

#import necessary libraries
import pypot.dynamixel
import itertools
import rospy
import math
from geometry_msgs.msg import Point, Point32
from time import sleep
from geometry_msgs.msg import Polygon
from sensor_msgs.msg import Joy

#get all available ports your robot is connected to, assume the first one
ports = pypot.dynamixel.get_available_ports()
print('Available ports:', ports)
if not ports:
    raise IOError('No port available.')
port = ports[0]
print('Using the first on the list' + port)

#connect to the port
dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected...')

#find servo_ids
found_ids = dxl_io.scan()
print('Found ids:', found_ids)

#there should be five servos, exit upon failure
if len(found_ids) < 5:
    raise IOError('You should connect at least five motors on the bus for this test.')

#start procedure
print('Ready!')
#
# Type Joy
#
joy_msg = Joy()

#
# Global constants that linear speed
# SPEED = 25
#
SPEED = 25    

#
# Enable servos and set the speed
#
dxl_io.enable_torque(found_ids)
speed = dict(zip(found_ids, itertools.repeat(SPEED)))
newloc = dict(zip(found_ids, itertools.repeat(0)))
dxl_io.set_moving_speed(speed)
dxl_io.set_goal_position(newloc)

#
# Our ps_controller callback, triggered when the joystick is pushed
#
def controllerCallback(data):

    global joy_msg
    joy_msg = data
    global callback_joy_occured
    callback_joy_occured = True

#our main procedure
def listener():

    # initialize our node
    rospy.init_node('controller_to_point_listener', anonymous=True)

    # subscribe to dyna_chatter, listening for controller events
    rospy.Subscriber("joy", Joy, controllerCallback)
 
#run our procedure on startup
if __name__ == '__main__':
    listener()
    mult = 1    
    rate = rospy.Rate(50) # 5hz
    while not rospy.is_shutdown():        
        #print servo_active
        #print joy_msg
        if len(joy_msg.buttons) > 0:
            #print joy_msg        
            #
            # See if button 1 is being pushed use dictionary 
            # function since there is no case in python
            #
            for i in range(0, 6):
                if (joy_msg.buttons[i]==1):    
                    if (i+1 == 6):
			if(callback_joy_occured == True):
                        	print 'I am pushing button 6'
                        	mult = -1*mult
                        	print mult
				button6_pressed = True
                    else:   
                        print 'I am pushing button', i+1
			button6_pressed = False
                        oldpos = dxl_io.get_present_position(found_ids)
                        print oldpos
                        p1 = int(oldpos[i]) + mult*10
                        newpos = {i+1: p1}
                        dxl_io.set_goal_position(newpos)
	callback_joy_occured = False
        rate.sleep()


