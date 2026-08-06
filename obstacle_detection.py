

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data
 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan  # defined interface


class ObstacleDetection(Node):
    def __init__(self):
        super().__init__('obstacle_detection_node')   # node name

        #subscription
        self.scan_sub = self.create_subscription(msg_type=LaserScan, topic='/scan', callback=self.callback_scan, qos_profile=qos_profile_sensor_data)  
        self.cmd_sub = self.create_subscription(msg_type=Twist, topic='/cmd_vel_raw', callback=self.callback_cmd, qos_profile=QoSProfile(depth=10))

        # publisher
        self.cmd_pub = self.create_publisher(msg_type=Twist, topic='/cmd_vel', qos_profile=QoSProfile(depth=10)) 
        self.timer = self.create_timer(timer_period_sec=0.010, callback=self.callback_timer)

        # variables
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.scan_ranges = []

        # states
        self.init_scan_state = False 

        self.get_logger().info('Turtlebot3 obstacle detection nod ehas been initialized.')


    # callback functions for subscription
    def callback_scan(self,msg):
        self.scan_ranges = msg.ranges

        #self.get_logger().info(f"angle_min = {msg.angle_min} \n")
        #self.get_logger().info(f"angle_max = {msg.angle_max} \n")
        #self.get_logger().info(f"angle_increment = {msg.angle_increment} \n")
        #self.get_logger().info(f"data length = {len(msg.ranges)} \n")

        self.init_scan_state = True

    def callback_cmd(self,msg): 
        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z 

    # callback functions for publisher
    def callback_timer(self):
        if self.init_scan_state is True:
            self.move()

    def move(self):
        twist = Twist()

        obstacle_distance = min(self.scan_ranges)
        
        self.get_logger().info(f"distance = {obstacle_distance} \n")

        if obstacle_distance > 0.2:
            twist.linear.x = self.linear_velocity
            twist.angular.z = self.angular_velocity

        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.get_logger().info(f"Obstables are detected nearby. Robot stopped. \n")

        self.cmd_pub.publish(twist)

    """
    def move(self): 
        twist = Twist()

        obstacle_distance = min(self.scan_ranges) 
        #obstacle_distance = self.scan_ranges[0]  # front

        self.get_logger().info(f'distance = {obstacle_distance} \n')

        if obstacle_distance > 0.2:  # if distance < 0.3m, then move....
            twist.linear.x = self.linear_velocity
            twist.angular.z = self.angular_velocity
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.get_logger().info('Obstables are detected nearby. Robot stoppted.')

        self.cmd_pub.publish(twist) 
    """

def main(args=None):
    rclpy.init(args=args)

    obstacle_detection = ObstacleDetection()   

    try:
        rclpy.spin( obstacle_detection )

    except KeyboardInterrupt:
        obstacle_detection.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
    
    finally:
        obstacle_detection.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    
