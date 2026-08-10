

import rclpy
from rclpy.node import Node
#from rclpy.qos import QoSProfile

#from turtlesim.srv import Spawn
#from turtlesim.srv import TeleportAbsolute
from my_first_package_msgs.srv import ??? # defined interface

class ???(Node):
    def __init__(self):
        super().__init__('???')   # node name
        self.server = self.create_service(srv_type=???, srv_name='???', callback=self.callback_service)


    def callback_service(self,request,response):
        #self.get_logger().info(f'Request: {request}')
        #response.x = [1., 2., 3.]
        #response.y = [10.,20.]
        #response.theta = [100., 200., 300.]

        return response
    
def main(args=None):
    rclpy.init(args=args)

    ??? = ???()

    try: 
        rclpy.spin(???)

    except KeyboardInterrupt:
        ???.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')

    finally:
        ???.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()   