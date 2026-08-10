


import rclpy
from rclpy.node import Node
#from rclpy.qos import QoSProfile

#from turtlesim.msg import Pose
#from geometry_msgs.msg import Twist
from my_first_package_msgs.srv import CalcData  # defined interface

class ArithServer(Node):
    def __init__(self):
        super().__init__('arith_server')   # node name
        self.server = self.create_service(srv_type=CalcData, srv_name='calc_data', callback=self.callback_service)


    def callback_service(self,request,response):
        response.res = request.x + request.y 

        return response
    
def main(args=None):
    rclpy.init(args=args)

    arith_server_node = ArithServer()

    try: 
        rclpy.spin(arith_server_node)

    except KeyboardInterrupt:
        arith_server_node.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')

    finally:
        arith_server_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()   