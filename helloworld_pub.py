

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String


class HelloWorldPublisher(Node):
    def __init__(self):
        super().__init__('helloworld_publisher')
        qos_profile = QoSProfile(depth=10)
        self.publisher = self.create_publisher(String, 'helloworld', qos_profile)
        self.create_timer(1.0, self.callback_timer )
        self.count = 0
        
    def callback_timer(self):
        msg = String()
        msg.data = f'Hello World {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Hello World {self.count}')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = HelloWorldPublisher()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')        

    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
