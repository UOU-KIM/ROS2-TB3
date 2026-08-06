
import math
import numpy
import sys
import termios
import rclpy


from rclpy.node import Node
from rclpy.qos  import QoSProfile
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


from my_tb3_pkg.robot_turn_go import RobotTurnGo

terminal_msg = """Turtlebot3 Position Control
-------------------------------------------------
From the current pose,

x: goal position x (unit: m)
y: goal position y (unit: m)
theta: goal orientation (range: -180 ~ 180, unit: deg)

-----------------------------------------------------
"""



class RobotPositionControl(Node):
    def __init__(self):
        super().__init__('position_control_node')   # node name

        # subscription
        self.odom_sub = self.create_subscription(msg_type=Odometry, topic='odom', callback=self.callback_sub, qos_profile=QoSProfile(depth=10))   

        # publisher
        self.cmd_pub = self.create_publisher(msg_type=Twist, topic='cmd_vel', qos_profile=QoSProfile(depth=10)) 
        self.timer = self.create_timer(timer_period_sec=0.01, callback=self.callback_timer)
        
        self.get_logger().info("\n\n Turtlebot3 position control node has been initialized.\n\n")

        # variables
        self.odom = Odometry()
        self.last_pose_x = 0.0
        self.last_pose_y = 0.0
        self.last_pose_theta = 0.0

        self.goal_pose_x = 0.0
        self.goal_pose_y = 0.0
        self.goal_pose_theta = 0.0

        self.step = 1
        self.get_key_state = False
        self.init_odom_state = False
     
    
    def callback_sub(self,msg):
        self.last_pose_x = msg.pose.pose.position.x
        self.last_pose_y = msg.pose.pose.position.y
        _, _, self.last_pose_theta = self.euler_from_quaternion( msg.pose.pose.orientation )

        self.init_odom_state = True
    
    """ # Core 1
    # callback functions for subscription
    def callback_sub(self,msg):  #Odometry
        self.last_pose_x = msg.pose.pose.position.x
        self.last_pose_y = msg.pose.pose.position.y

        _, _, self.last_pose_theta = self.euler_from_quaternion( msg.pose.pose.orientation ) 

        self.init_odom_state = True   
    """


    # callback functions for publisher
    def callback_timer(self):  
        if self.init_odom_state is True:
            self.generate_path()

    def generate_path(self):
        twist = Twist()

        if self.get_key_state is False:
            input_x, input_y, input_theta = self.get_key()

            self.goal_pose_x = self.last_pose_x + input_x
            self.goal_pose_y = self.last_pose_y + input_y
            self.goal_pose_theta = self.last_pose_theta + input_theta

            self.get_key_state = True

        else:
            if self.step == 1:
                path_theta = math.atan2( self.goal_pose_y - self.last_pose_y, self.goal_pose_x - self.last_pose_x )
                angle = path_theta - self.last_pose_theta
                angular_velocity = 0.1

                twist, self.step = RobotTurnGo.turn( angle, angular_velocity, self.step )

            elif self.step == 2:
                distance = math.sqrt( (self.goal_pose_x-self.last_pose_x) ** 2 + (self.goal_pose_y-self.last_pose_y) ** 2 )
                linear_velocity = 0.1

                twist, self.step = RobotTurnGo.go_straight( distance, linear_velocity, self.step )

            elif self.step == 3:
                angle = self.goal_pose_theta - self.last_pose_theta
                angular_velocity = 0.1

                twist, self.step = RobotTurnGo.turn(angle, angular_velocity, self.step)

            elif self.step == 4:
                self.step = 1
                self.get_key_state = False
            
            self.cmd_pub.publish(twist)

    

    """  # Core 2
    def generate_path(self):
        twist = Twist()

        if self.get_key_state is False:
            
            input_x, input_y, input_theta = self.get_key()

            self.goal_pose_x = self.last_pose_x + input_x
            self.goal_pose_y = self.last_pose_y + input_y
            self.goal_pose_theta = self.last_pose_theta + input_theta

            self.get_key_state = True

            print(self.get_key_state)

        else:
            if self.step == 1:  

                path_theta = math.atan2(
                    self.goal_pose_y - self.last_pose_y,
                    self.goal_pose_x - self.last_pose_x
                )

                angle = path_theta - self.last_pose_theta
                angular_velocity = 0.1

                twist, self.step = RobotTurnGo.turn(angle, angular_velocity, self.step )

                #print("Step = ", self.step)                


            elif self.step == 2:        

                distance = math.sqrt(
                    (self.goal_pose_x - self.last_pose_x) ** 2 +
                    (self.goal_pose_y - self.last_pose_y) ** 2
                )

                linear_velocity = 0.1

                twist, self.step = RobotTurnGo.go_straight(distance, linear_velocity, self.step )

            elif self.step == 3: 

                angle = self.goal_pose_theta - self.last_pose_theta
                angular_velocity = 0.1

                twist, self.step = RobotTurnGo.turn(angle, angular_velocity, self.step )

            elif self.step == 4:
                self.step  = 1
                self.get_key_state = False

            # Publishing
            self.cmd_pub.publish(twist) 
    """

    def get_key(self):
        print(terminal_msg)

        input_x = float( input("Input x[m]: ") )
        input_y = float( input("Input y[m]: ") )
        input_theta = float( input("Input theta[deg]: ") )

        while input_theta > 180 or input_theta < -180:
            self.get_logger().input("Enter a value for theta between -180 and 180.")
            input_theta = float( input("Input theta[deg]:") )

        input_theta = numpy.deg2rad(input_theta)    #rad

        settings = termios.tcgetattr(sys.stdin)
        termios.tcsetattr( sys.stdin, termios.TCSADRAIN, settings )

        return input_x, input_y, input_theta
        

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

    robot_position_control = RobotPositionControl()   

    try:
        rclpy.spin( robot_position_control )

    except KeyboardInterrupt:
        robot_position_control.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
    
    finally:
        robot_position_control.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    
