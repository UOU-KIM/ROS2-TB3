

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from my_first_package_msgs.msg import CmdAndPoseVel  # defined interface


class ???(Node):
    def __init__(self):
        super().__init__('???')   # node name

        #subscription
        self.??? = self.create_subscription(msg_type=???, topic='???', callback=self.callback_???, qos_profile=QoSProfile(depth=10))  
        self.??? = self.create_subscription(msg_type=???, topic='???', callback=self.callback_???, qos_profile=QoSProfile(depth=10))

        # publisher
        self.??? = self.create_publisher(msg_type=???, topic='???', qos_profile=QoSProfile(depth=10)) 
        self.timer = self.create_timer(timer_period_sec=1.0, callback=self.timer_callback)
        self.??? = ???()   # declare a messge object for publishing

    # callback functions for subscription
    def callback_pos(self,msg):
        #self.cmd_pose.pose_x = msg.x
        #self.cmd_pose.pose_y = msg.y
        #self.cmd_pose.linear_vel = msg.linear_velocity
        #self.cmd_pose.angular_vel = msg.angular_velocity

    def callback_cmd(self,msg):
        #self.cmd_pose.cmd_vel_linear = msg.linear.x
        #self.cmd_pose.cmd_vel_angular = msg.angular.z

    # callback functions for publisher
    def timer_callback(self):
        self.???.publish(self.cmd_pose) 

def main(args=None):
    rclpy.init(args=args)

    ??? = ???()   

    try:
        rclpy.spin( ??? )

    except KeyboardInterrupt:
        ???.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
    
    finally:
        ???.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    
