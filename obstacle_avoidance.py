
import math
import numpy
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data
 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan  # defined interface
from nav_msgs.msg import Odometry

class ObstacleDetection(Node):
    def __init__(self):
        super().__init__('obstacle_detection_node')   # node name

        #subscription
        self.scan_sub = self.create_subscription(msg_type=LaserScan, topic='/scan', callback=self.callback_scan, qos_profile=qos_profile_sensor_data)
        self.odom_sub = self.create_subscription(msg_type=Odometry, topic='/odom', callback=self.callback_odom, qos_profile=QoSProfile(depth=10) )

        # publisher
        self.cmd_pub = self.create_publisher(msg_type=Twist, topic='/cmd_vel', qos_profile=QoSProfile(depth=10)) 
        self.timer = self.create_timer(timer_period_sec=0.010, callback=self.callback_timer)

        # variables: velocity
        self.linear_velocity = 0.05
        self.angular_velocity = 0.1

        # variables: robot information
        self.scan_ranges = []  
        self.last_pose_theta = 0.0

        # variables: robot goal 
        self.goal_pose_theta = 0.0

        # variables: states
        self.scan_state = False 
        self.odom_state = False
        self.step = 1

        self.get_logger().info('Turtlebot3 obstacle detection nod ehas been initialized.')


    # callback functions for subscription
    def callback_scan(self,msg):
        self.scan_ranges = msg.ranges
        self.scan_state = True 
    
    def callback_odom(self,msg):
        self.last_pose_x = msg.pose.pose.position.x
        self.last_pose_y = msg.pose.pose.position.y
        _, _, self.last_pose_theta = self.euler_from_quaternion( msg.pose.pose.orientation )  # roll, pitch, yaw
        self.odom_state = True 
    

    # callback functions for publisher
    def callback_timer(self):
        if self.scan_state is True and self.odom_state is True:
            self.move()

    def move(self):
        twist = Twist()

        if self.step == 1:
            robot_front_distance = self.scan_ranges[0]         
            self.get_logger().info(f"distance = {robot_front_distance} \n")

            twist = self.go_straight(robot_front_distance)

        elif self.step == 2: 

            twist.linear.x = 0.0
            twist.angular.z = 0.0       

            self.goal_pose_theta = self.last_pose_theta + math.pi/2
            self.step += 1 # next step

        elif self.step == 3:
            angle_diff = self.goal_pose_theta - self.last_pose_theta
            self.get_logger().info(f"angle difference = {angle_diff} \n")

            twist = self.turn(angle_diff)        

        self.cmd_pub.publish(twist)
    
    def go_straight(self,dist):
        twist = Twist()        

        if dist > 0.2:
            twist.linear.x = self.linear_velocity
            twist.angular.z = 0.0
            #self.get_logger().info(f"Go straight: Obstacles are not detected. \n")

        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.step += 1 # next step

        return twist      
    
    def turn(self,angle_diff):
        twist = Twist()

        twist.linear.x = 0.0

        if  0.0005 < angle_diff and angle_diff <= math.pi:
            twist.angular.z = self.angular_velocity
        elif -math.pi < angle_diff and angle_diff < -0.0005:
            twist.angular.z = -self.angular_velocity 
        else:
            twist.angular.z = 0.0
            self.step = 1

        return twist


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

    
