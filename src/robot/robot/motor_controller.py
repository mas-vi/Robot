import rclpy
from std_msgs.msg import String
from rclpy.node import Node
from queue import Queue
import threading
from time import sleep
vel = 0
prev_vel=0
queue = Queue()
lock = threading.Lock()  


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

    def listener_callback(self, msg):
        global vel 
        command = msg.data
        if command == "forward":
            if vel < 100:
                vel += 25

        elif command == "for-left":
            with lock:  
                queue.put('for-left')
        elif command == "for-right":
            with lock:
                queue.put('for-right')
        elif command == "left":
            with lock:
                queue.put('left')
        elif command == "stop":
            vel = 0
            with lock:
                while not queue.empty():
                    queue.get()

        elif command == "right":
            with lock:
                queue.put('right')
        elif command == "backward":
            if vel > -100:
                vel -= 25

       
        threading.Thread(target=send_command).start()


def send_command():
    global vel
    global prev_vel
    with lock:
        if(not queue.empty()):
            command=queue.get()
            match(command):
                case 'for-left':
                    print(command)
                    sleep(1)
                    print('Executed ', command,' success')
                case 'for-right':
                    print(command)
                    sleep(1)
                    print('Executed ', command,' success')
                case 'left':
                    print(command)
                    sleep(1)
                    print('Executed ', command,' success')
                case 'right':
                    print(command)
                    sleep(1)
                    print('Executed ', command,' success')


    with lock:
        if prev_vel!=vel:
            prev_vel=vel
        print(prev_vel)
    

    


def main(args=None):
    try:
        rclpy.init(args=args)
        motor_controller = MotorController()
        rclpy.spin(motor_controller)
    except KeyboardInterrupt:
        pass
    finally:
        motor_controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()