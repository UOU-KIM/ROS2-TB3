
import os
import rclpy
from rclpy.node import Node 

#from turtlesim.srv import Spawn
#from turtlesim.srv import TeleportAbsolute
from gazebo_msgs.srv import SpawnEntity  # defined interface




from ament_index_python.packages import get_package_share_directory


class SpawnRobot(Node):
    def __init__(self):
        super().__init__('gazebo_model_spawner')   # node name
        self.client = self.create_client(srv_type=SpawnEntity, srv_name='/spawn_entity')  # creat_client

        while not self.client.wait_for_service(timeout_sec=1.0):  #wait_for_service
            self.get_logger().error('service not available, waiting again....')

        self.req = SpawnEntity.Request()

        # directory: home/... /gcamp_gazebo/urdf/skidbot2.urdf
        self.urdf_file_path = os.path.join(
            get_package_share_directory('gcamp_gazebo'),
            'urdf',
            'skidbot2.urdf'
        )


    def send_req(self):
        self.req.name = 'skidbot2' 
        self.req.xml = open(self.urdf_file_path).read()
        self.req.robot_namespace = 'skidbot2'
        self.req.initial_pose.position.x = 1.0
        self.req.initial_pose.position.y = 1.0
        self.req.initial_pose.position.z = 0.3

        self.get_logger().debug('=== Sending service request to `/spawn_entity ===')

        self.future = self.client.call_async(self.req)  #call_async
        return self.future

    
def main(args=None):
    rclpy.init(args=args)
    
    robot_spawn_node = SpawnRobot()
    future = robot_spawn_node.send_req()  # call_async, future

    rclpy.spin_until_future_complete(node=robot_spawn_node, future=future)  # spin_until_future_complete

    if future.done(): 
        try:
            response = future.result()   # response
        
        except Exception:
            raise RuntimeError('exception while calling service: %r' %future.exception() )
        
        else:
            robot_spawn_node.get_logger().info('=== Service Call Done ===')
            robot_spawn_node.get_logger().info(f'Status_message : {response.status_message}')
        
        finally:
            robot_spawn_node.get_logger().warn('=== Shutting down node ===')
            robot_spawn_node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()  