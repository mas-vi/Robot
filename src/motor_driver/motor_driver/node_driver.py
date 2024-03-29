import rclpy
from std_msgs.msg import String

left_motor_pins = (17, 18)
right_motor_pins = (27, 22)

def motor_control_node():
    rclpy.init()
    node = rclpy.create_node('motor_control_node')
    subscriber = node.create_subscription(String, 'movement_command', move_callback, qos_profile=rclpy.qos.qos_profile_sensor_data)
    rclpy.spin(node)

def move_callback(msg):
    command = msg.data
    if command == 'forward':
        move_forward()
    elif command == 'backward':
        move_backward()
    elif command == 'left':
        turn_left()
    elif command == 'right':
        turn_right()

def move_forward():
    print("Moving forward")

def move_backward():
    print("Moving backward")

def turn_left():
    print("Turning left")

def turn_right():
    print("Turning right")
def main():
    try:
        motor_control_node()
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()
if __name__ == '__main__':
    main()
