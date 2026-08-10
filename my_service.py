

import rclpy
from rclpy.node import Node
#from rclpy.qos import QoSProfile

#from turtlesim.msg import Pose
#from geometry_msgs.msg import Twist
from my_first_package_msgs.srv import MultiSpawn  # defined interface

class MyService(Node):
    def __init__(self):
        super().__init__('my_service')   # node name
        self.server = self.create_service(srv_type=MultiSpawn, srv_name='/multi_spawn', callback=self.callback_service)


    def callback_service(self,request,response):
        self.get_logger().info(f'Request: {request}')
        response.x = [1., 2., 3.]
        response.y = [10.,20.]
        response.theta = [100., 200., 300.]
        return response
    
def main(args=None):
    rclpy.init(args=args)

    my_service_node = MyService()

    try: 
        rclpy.spin(my_service_node)

    except KeyboardInterrupt:
        my_service_node.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')

    finally:
        my_service_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()   