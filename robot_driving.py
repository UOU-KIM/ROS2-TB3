

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
 
from geometry_msgs.msg import Twist 


class RobotDriving(Node):
    def __init__(self):
        super().__init__('driving_node')   # node name        

        # publisher
        self.drv_pub = self.create_publisher(msg_type=Twist, topic='cmd_vel_raw', qos_profile=QoSProfile(depth=10)) 
        self.timer = self.create_timer(timer_period_sec=1.0, callback=self.timer_callback)
        self.drv_msg = Twist()   # declare a messge object for publishing 

        self.drv_msg.linear.x = 0.02
        self.drv_msg.angular.z = 0.0

    # callback functions for publisher
    def timer_callback(self):
        self.drv_pub.publish(self.drv_msg) 

def main(args=None):
    rclpy.init(args=args)

    robot_driving = RobotDriving()   

    try:
        rclpy.spin( robot_driving )

    except KeyboardInterrupt:
        robot_driving.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
    
    finally:
        robot_driving.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main() 

    
