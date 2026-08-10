import rclpy
from rclpy.node import Node 

#from turtlesim.srv import Spawn
#from turtlesim.srv import TeleportAbsolute
from my_first_package_msgs.srv import CalcData  # defined interface


class ???(Node):
    def __init__(self):
        super().__init__('???')   # node name
        self.client = self.create_client(srv_type=???, srv_name='???')  # creat_client

        while not self.client.wait_for_service(timeout_sec=???):  #wait_for_service
            self.get_logger().error('service not available, waiting again....')

        self.req = ???.Request()

    def send_req(self):
        #self.req.x = 1   #request data
        #self.req.y = 2

        self.future = self.client.call_async(self.req)  #call_async
        return self.future

    
def main(args=None):
    rclpy.init(args=args)
    
    ??? = ???()
    future = ???.send_req()  # call_async, future

    rclpy.spin_until_future_complete(node=???, future=future)  # spin_until_future_complete

    if future.done(): 
        try:
            response = future.result()   # response
        
        except Exception:
            raise RuntimeError('exception while calling service: %r' %future.exception() )
        
        else:
            ???.get_logger().info(f'sum = {response.???}')
        
        finally:
            arith_client_node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()  