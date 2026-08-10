


import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from sensor_msgs.msg import LaserScan 


class LaserSubscriber(Node):
    def __init__(self):
        super().__init__('laser_sub_node')   # node name

        #subscription
        self.subscriber = self.create_subscription(msg_type=LaserScan, topic='/skidbot/scan', callback=self.callback_scan, qos_profile=QoSProfile(depth=10))   
 

    # callback functions for subscription
    def callback_scan(self,msg):
        self.get_logger().info(f'Distance from Front Object: {msg.ranges[360]}')    
 
 

def main(args=None):
    rclpy.init(args=args)

    laser_subscriber = LaserSubscriber()   

    try:
        rclpy.spin( laser_subscriber )

    except KeyboardInterrupt:
        laser_subscriber.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
    
    finally:
        laser_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    
