

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
 


class HelloWorldSubscriber(Node):

    def __init__(self):
        super().__init__('helloworld_subscriber')

        qos_profile = QoSProfile(depth = 10)
        self.create_subscription(String, '/helloworld', self.callback_sub, qos_profile)

        

    def callback_sub(self, msg):
        self.get_logger().info(f'Recieved message: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = HelloWorldSubscriber()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')

    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
