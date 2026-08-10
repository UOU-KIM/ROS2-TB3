

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from geometry_msgs.msg import Twist 

from my_first_package_msgs.srv import TurningControl  


class RobotTurnServer(Node):
    def __init__(self):
        super().__init__('robot_turn_server')   # node name

        # Server
        self.server = self.create_service(srv_type=TurningControl, srv_name='/turn_robot', callback=self.callback_service)

        # Publisher
        self.publisher = self.create_publisher(msg_type=Twist, topic='/skidbot/cmd_vel', qos_profile=QoSProfile(depth=10))  
        self.twist_msg = Twist()   # declare a messge object for publishing


        # Variables
        self.start_time = self.get_clock().now().to_msg().sec

        # Message
        self.get_logger().info('==== Robot Turning Server Started, Waiting for Request ====')



    def callback_service(self,request,response):
        
        self.start_time = self.get_clock().now().to_msg().sec   # when REQUEST is received.

        # Publishing
        self.move_robot(request.time_duration, request.linear_vel_x, request.angular_vel_z)       
        self.stop_robot()


        # Response
        response.success = True

        return response 
    
    def move_robot(self, seconds=1, linear_x=0.0, angular_z=0.0):
        self.twist_msg.linear.x = linear_x
        self.twist_msg.angular.z = angular_z

        clock_now = self.get_clock().now().to_msg().sec  # right before Publishing 
        self.get_logger().info('Robot Moves')
        self.get_logger().info(f'Move Commands : linear_x = {linear_x}, angular_z = {angular_z}')
        
        while(clock_now - self.start_time )<seconds:            
            self.publisher.publish(self.twist_msg)
            clock_now = self.get_clock().now().to_msg().sec
    
    def stop_robot(self):
        self.twist_msg.linear.x = 0.0
        self.twist_msg.angular.z = 0.0
        self.publisher.publish(self.twist_msg)
        self.get_logger().info('Robot Stop !!')
    
    
def main(args=None):
    rclpy.init(args=args)

    robot_turn_server = RobotTurnServer()

    try: 
        rclpy.spin(robot_turn_server)

    except KeyboardInterrupt:
        robot_turn_server.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')

    finally:
        robot_turn_server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()   