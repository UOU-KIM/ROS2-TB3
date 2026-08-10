

import numpy 
import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist  
from nav_msgs.msg import Odometry
  

class AbsoluteMove(Node):
    def __init__(self):
        super().__init__('absolute_move_node')   # node name

        print('TurtleBot3 Absolute Move')
        print('----------------------------------------------')
        print('Enter absolute coordinates in odometry frame')
        print('goal x: absolute x position (unit: m)')
        print('goal y: absolute y position (unit: m)')
        print('goal heading: absolute orientation (range: -180 ~ 180, unit: deg)')
        print('----------------------------------------------')

        #subscription
        self.odom_sub = self.create_subscription(msg_type=Odometry, topic='/odom', callback=self.callback_odom_sub, qos_profile=QoSProfile(depth=10))   

        # publisher
        self.cmd_pub = self.create_publisher(msg_type=Twist, topic='/cmd_vel', qos_profile=QoSProfile(depth=10)) 
        self.timer = self.create_timer(timer_period_sec=0.05, callback=self.callback_timer)
        self.cmd_twist = Twist()   # declare a messge object for publishing

        # variables
        self.position = Point()
        self.position_error = Point()
        self.goal_position = Point()

        self.heading = 0.0
        self.goal_heading = 0.0
        self.heading_error = 0.0

        self.angular_speed = 0.15
        self.linear_speed = 0.5

        self.odom_state = False

        self.get_logger().info('Ready to receive goal inputs.')
        self.get_key()

    # inputs
    def get_key(self):
        self.goal_position.x = float(input('goal x(absolute): '))
        self.goal_position.y = float(input('goal y(absolute): '))
        self.goal_heading = float(input('goal heading (absolute, degrees): '))

        self.goal_heading = math.radians( self.goal_heading ) 

        # range: (-pi ~ pi )
        if self.goal_heading > math.pi:
            self.goal_heading -= 2*math.pi
        elif self.goal_heading < -math.pi:
            self.goal_heading += 2*math.pi 

        self.get_logger().info(
            f'New goal: '
            f'x: {self.goal_position.x:.2f},'
            f'y: {self.goal_position.y:.2f},'
            f'heading: '
            f'{math.degrees(self.goal_heading):.2f}'
        )

    # callback functions for subscription
    def callback_odom_sub(self,msg):
        self.position = msg.pose.pose.position   #Point (x,y,z)
        _, _, self.heading = self.euler_from_quaternion(msg.pose.pose.orientation)

        self.odom_state = True

  

    # callback functions for publisher
    def callback_timer(self):

        if self.odom_state is True:
            self.robot_move()
        else:
            self.get_logger().info('Odom information is not received!')


    def robot_move(self):
        self.position_error.x = self.goal_position.x - self.position.x
        self.position_error.y = self.goal_position.y - self.position.y

        distance = math.sqrt( pow(self.position_error.x,2) + pow(self.position_error.y,2) )
        direction = math.atan2( self.position_error.y, self.position_error.x  )

        if distance > 0.05:

            path_angle = direction - self.heading

            if path_angle > math.pi:
                path_angle -= 2*math.pi
            elif path_angle < -math.pi:
                path_angle += 2*math.pi
            
            self.cmd_twist.linear.x = min(  self.linear_speed*distance, 0.1 )  # 0 ~ 0.1
            self.cmd_twist.angular.z = max( min( path_angle, 1.5 ), -1.5 )  #-1.5 ~ 1.5

            self.get_logger().info(
                f'Moving to x: {self.goal_position.x:.2f}, y: {self.goal_position.y:.2f} '
                f'(current: {self.position.x:.2f}, {self.position.y:.2f})'
            )

            self.cmd_pub.publish(self.cmd_twist) 
        
        else:
            self.cmd_twist.linear.x = 0.0

            self.heading_error = self.goal_heading - self.heading

            if self.heading_error > math.pi:
                self.heading_error -= 2*math.pi
            if self.heading_error < -math.pi:
                self.heading_error += 2*math.pi

            if abs( math.degrees( self.heading_error ) ) <1.0:

                self.cmd_twist.angular.z = 0.0

                self.cmd_pub.publish(self.cmd_twist) 
                self.get_key()

            else:
                turn_speed = max( min( abs(self.heading_error)*1.0, 1.0), 0.0)  #0.1 ~ 1.0 
                self.cmd_twist.angular.z = turn_speed if self.heading_error >0 else -turn_speed 

                self.get_logger().info(
                    f'Rotating to heading: {math.degrees(self.goal_heading):.2f}°'
                    f'(current: {math.degrees(self.heading):.2f}°)'
                )
                self.cmd_pub.publish(self.cmd_twist)     


    def euler_from_quaternion(self, quat): 

        x = quat.x
        y = quat.y
        z = quat.z
        w = quat.w

        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = numpy.arctan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        pitch = numpy.arcsin(sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = numpy.arctan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw
    

def main(args=None):
    rclpy.init(args=args)

    absolute_move = AbsoluteMove()   

    try:
        rclpy.spin( absolute_move )

    except KeyboardInterrupt:
        absolute_move.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
    
    finally:
        absolute_move.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    
