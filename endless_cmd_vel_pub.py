

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
 
from geometry_msgs.msg import Twist 


class CmdVelPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_pub_node')   # node name 

        # publisher
        self.publisher = self.create_publisher(msg_type=Twist, topic='/skidbot/cmd_vel', qos_profile=QoSProfile(depth=10)) 
        self.timer = self.create_timer(timer_period_sec=0.5, callback=self.callback_timer)
        
 

    # callback functions for publisher
    def callback_timer(self):
        twist_msg = Twist()   # declare a messge object for publishing
        twist_msg.linear.x = 0.5
        twist_msg.angular.z = 1.0        
        self.publisher.publish(twist_msg)

    def stop_robot(self):
        stop_msg = Twist()   # declare a messge object for publishing
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0        
        self.publisher.publish(stop_msg)

def main(args=None):
    rclpy.init(args=args)

    cmd_vel_publisher = CmdVelPublisher()    
  
    try: 
        rclpy.spin( cmd_vel_publisher ) 
    
    except KeyboardInterrupt:
        #cmd_vel_publisher.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
        pass
    
    finally:
        cmd_vel_publisher.stop_robot() 
        cmd_vel_publisher.get_logger().info('\n\n == Stop Publishing == \n\n')
        cmd_vel_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    
