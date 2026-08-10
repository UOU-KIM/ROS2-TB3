

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from my_first_package_msgs.msg import CmdAndPoseVel  # defined interface


class CmdAndPose(Node):
    def __init__(self):
        super().__init__('turtle_cmd_pose')   # node name

        #subscription
        self.sub_pose = self.create_subscription(msg_type=Pose, topic='/turtle1/pose', callback=self.callback_pos, qos_profile=QoSProfile(depth=10))  
        self.sub_cmdvel = self.create_subscription(msg_type=Twist, topic='/turtle1/cmd_vel', callback=self.callback_cmd, qos_profile=QoSProfile(depth=10))

        # publisher
        self.publisher = self.create_publisher(msg_type=CmdAndPoseVel, topic='/cmd_and_pose', qos_profile=QoSProfile(depth=10)) 
        self.timer = self.create_timer(timer_period_sec=1.0, callback=self.timer_callback)
        self.cmd_pose = CmdAndPoseVel()   # declare a messge object for publishing

    # callback functions for subscription
    def callback_pos(self,msg):
        self.cmd_pose.pose_x = msg.x
        self.cmd_pose.pose_y = msg.y
        self.cmd_pose.linear_vel = msg.linear_velocity
        self.cmd_pose.angular_vel = msg.angular_velocity

    def callback_cmd(self,msg):
        self.cmd_pose.cmd_vel_linear = msg.linear.x
        self.cmd_pose.cmd_vel_angular = msg.angular.z

    # callback functions for publisher
    def timer_callback(self):
        self.publisher.publish(self.cmd_pose) 

def main(args=None):
    rclpy.init(args=args)

    cmd_and_pose = CmdAndPose()   

    try:
        rclpy.spin( cmd_and_pose )

    except KeyboardInterrupt:
        cmd_and_pose.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
    
    finally:
        cmd_and_pose.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    
