import rclpy
from rclpy.node import Node 
 
from my_first_package_msgs.srv import TurningControl  # defined interface


class RobotTurningClient(Node):
    def __init__(self):
        super().__init__('robot_turn_client')   # node name
        self.client = self.create_client(srv_type=TurningControl, srv_name='/turn_robot')  # creat_client

        while not self.client.wait_for_service(timeout_sec=1.0):  #wait_for_service
            self.get_logger().error('service not available, waiting again....')

        self.req = TurningControl.Request()
        self.get_logger().info('=== Robot Turn Service Client === ')

    def send_req(self):

        while True:

            try:
                td = input('> Type turning time duration: ')
                vel_x = input('> Type turning linear velocity: ')
                vel_z = input('> Typy turning angular velocity: ')

                if float(vel_z) > 1.5707 or float(vel_x) >3:
                    raise ArithmeticError('Velocity too high !!')
                
                self.req.time_duration = int(td)
                self.req.linear_vel_x = float(vel_x)
                self.req.angular_vel_z = float(vel_z)

                self.get_logger().info(f'linear_x = {self.req.linear_vel_x}, angular_z = {self.req.angular_vel_z}')
                
                break

            except ArithmeticError as e:
                self.get_logger().warn(str(e))

            except Exception as e:
                self.get_logger().warn(str(e))
                self.get_logger().warn('PLZ type number again')
 
        self.future = self.client.call_async(self.req)  #call_async
        self.get_logger().info(' Request Sended ')        

        return self.future

    
def main(args=None):
    rclpy.init(args=args)
    
    robot_turn_client = RobotTurningClient()
    future = robot_turn_client.send_req()  # call_async, future

    rclpy.spin_until_future_complete(node=robot_turn_client, future=future)  # spin_until_future_complete

    if future.done(): 
        try:
            response = future.result()   # response
        
        except Exception:
            raise RuntimeError('exception while calling service: %r' %future.exception() )
        
        else:
            robot_turn_client.get_logger().info(f"Response : {'Success' if response.success == True else 'Fail'}" )
        
        finally:
            robot_turn_client.get_logger().warn('=== Shutting down node ===')
            robot_turn_client.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()  