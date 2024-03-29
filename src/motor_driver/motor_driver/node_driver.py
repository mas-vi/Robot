import rclpy
from std_msgs.msg import String
from rclpy.node import Node

left_motor_pins = (17, 18)
right_motor_pins = (27, 22)

class MotorController(Node):
    def __init__(self):
        super().__init__("motor_controller_node")
        self.subscription = self.create_subscription(
            String,
            'movement_command',
            self.listener_callback,
            10
        )
        self.subscription
    def listener_callback(self,msg):
        command=msg.data
        if command=="forward":
            print("Moving forward")
        elif command=="backward":
            print("Moving backward")
        elif command=="left":
            print("Turn left")
        elif command("right"):
            print("Turn right")


    
def main(args=None):
    try:
        rclpy.init(args=args)
        motor_controller=MotorController()
        rclpy.spin(motor_controller)
    except KeyboardInterrupt:
        pass
        motor_controller.destroy_node()
        rclpy.shutdown()
        
        
if __name__ == '__main__':
    main()
