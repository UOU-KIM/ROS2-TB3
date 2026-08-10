

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
 
from geometry_msgs.msg import Twist 


class TurtlesimPublisher(Node):
    def __init__(self):
        super().__init__('turtle_cmd_pose')   # node name
         

        # publisher
        self.publisher = self.create_publisher(msg_type=Twist, topic='/turtle1/cmd_vel', qos_profile=QoSProfile(depth=10)) 
        self.timer = self.create_timer(timer_period_sec=0.5, callback=self.timer_callback) 
 

    # callback functions for publisher
    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 2.0
        self.publisher.publish(msg) 

def main(args=None):
    rclpy.init(args=args)

    turtlesim_publisher = TurtlesimPublisher()   

    try:
        rclpy.spin( turtlesim_publisher )

    except KeyboardInterrupt:
        turtlesim_publisher.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
    
    finally:
        turtlesim_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    
