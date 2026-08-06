


import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
 
from sensor_msgs.msg import BatteryState  


class BatteryVoltage(Node):
    def __init__(self):
        super().__init__('battery_voltage_node')   # node name

        #subscription
        self.subscriber = self.create_subscription(msg_type=BatteryState, topic='/battery_state', callback=self.callback_sub, qos_profile=QoSProfile(depth=10))   
 

    # callback functions for subscription
    def callback_sub(self,msg):
        self.get_logger().info(f'Voltage: {msg.voltage}, Current: {msg.current}, Temperature: {msg.temperature}') 
 

def main(args=None):
    rclpy.init(args=args)

    battery_voltage = BatteryVoltage()   

    try:
        rclpy.spin( battery_voltage )

    except KeyboardInterrupt:
        battery_voltage.get_logger().info('\n\n::: Keyboard Interrupt (SIGINT) ::\n\n')
    
    finally:
        battery_voltage.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    
