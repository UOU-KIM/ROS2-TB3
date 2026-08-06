


import math
from geometry_msgs.msg import Twist

class RobotTurnGo():

    def turn(angle, angular_velocity, step):
        twist = Twist()

        if math.fabs(angle) > 0.01:
            if angle >= math.pi:
                twist.angular.z = -angular_velocity
            elif 0 <= angle and angle < math.pi:
                twist.angular.z = angular_velocity
            elif -math.pi <= angle and angle < 0:
                twist.angular.z = -angular_velocity
            elif angle < -math.pi:
                twist.angular.z = angular_velocity
        else:
            step +=1

        return twist, step
    
    def go_straight(distance, linear_velocity, step):
        twist = Twist()

        if distance > 0.01:
            twist.linear.x = linear_velocity
        else:
            step +=1

        return twist, step



"""
import math
from geometry_msgs.msg import Twist

class RobotTurnGo():

    def turn(angle, angular_velocity, step):
        twist = Twist()

        if math.fabs(angle) > 0.01:
            if angle >= math.pi:  # When the target direction is located more than 180deg from the robot's current heading 
                twist.angular.z = -angular_velocity  # rotate clockwise
            elif math.pi > angle and angle >=0: # When the target direction is located between 0deg and 180deg from the robot's current heading.
                twist.angular.z = angular_velocity  # rotate counterclockwisean
            elif 0> angle and angle >= -math.pi:
                twist.angular.z = -angular_velocity  # rotate clockwise
            elif angle < -math.pi:
                twist.angular.z = angular_velocity # rotate counterclockwise
        else: 
            step += 1
        
        #print(step)
        
        return twist, step
    
    def go_straight(distance, linear_velocity, step):
        twist = Twist()

        if distance > 0.01:
            twist.linear.x = linear_velocity
        else:
            step += 1

        return twist, step
"""    