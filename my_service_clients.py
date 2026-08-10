

import rclpy
from rclpy.node import Node 
import numpy as np

from turtlesim.srv import Spawn
from turtlesim.srv import TeleportAbsolute
from my_first_package_msgs.srv import MultiSpawn  # defined interface


class MyServiceClients(Node):
    def __init__(self):
        super().__init__('my_service_clients')   # node name


        # Server
        self.server = self.create_service(srv_type=MultiSpawn, srv_name='multi_spawn', callback=self.callback_service )

        # Clients
        self.teleport = self.create_client(srv_type=TeleportAbsolute, srv_name='/turtle1/teleport_absolute')  # creat_client
        self.spawn = self.create_client(srv_type=Spawn, srv_name='/spawn')
      

        # Request data frame 
        self.req_teleport = TeleportAbsolute.Request()
        self.req_spawn = Spawn.Request()
        self.center_position = 5.54

    def callback_service(self,request,response):
        x, y, theta = self.calc_position(request.num, 3)  
        response.x = x
        response.y = y
        response.theta = theta

        for n in range( len(theta) ):
            self.req_spawn.x = x[n] + self.center_position
            self.req_spawn.y = y[n] + self.center_position
            self.req_spawn.theta = theta[n]

            self.spawn.call_async(self.req_spawn)  #call_async

        return response    

    def calc_position(self,n,r):
        gap_theta = 2*np.pi/n
        theta = [gap_theta*n for n in range(n)]
        x = [ r*np.cos(th) for th in theta]
        y = [ r*np.sin(th) for th in theta]

        return x, y, theta
 

    
def main(args=None):
    rclpy.init(args=args)
    
    my_service_clients_node = MyServiceClients()

    try: 
        rclpy.spin(my_service_clients_node)

    except KeyboardInterrupt:
        my_service_clients_node.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')

    finally:
        my_service_clients_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()  