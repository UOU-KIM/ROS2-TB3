
import rclpy
from rclpy.node import Node
#from rclpy.qos import QoSProfile

#from turtlesim.msg import Pose
#from geometry_msgs.msg import Twist
from my_first_package_msgs.srv import CalcData  # defined interface


class ArithClient(Node):
    def __init__(self):
        super().__init__('arith_client')   # node name
        self.client = self.create_client(srv_type=CalcData, srv_name='/calc_data')  # creat_client

        while not self.client.wait_for_service(timeout_sec=1.0):  #wait_for_service
            self.get_logger().error('service not available, waiting again....')

        self.req = CalcData.Request()

    def send_req(self):
        self.req.x = 1  # request data
        self.req.y = 2

        self.future = self.client.call_async(self.req)  #call_async
        return self.future

    
def main(args=None):
    rclpy.init(args=args)
    
    arith_client_node = ArithClient()
    future = arith_client_node.send_req()  # call_async, future

    rclpy.spin_until_future_complete(node=arith_client_node, future=future)  # spin_until_future_complete

    if future.done(): 
        try:
            response = future.result()   # response
        
        except Exception:
            raise RuntimeError('exception while calling service: %r' %future.exception() )
        
        else:
            arith_client_node.get_logger().info(f'sum = {response.res}')
        
        finally:
            arith_client_node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()  