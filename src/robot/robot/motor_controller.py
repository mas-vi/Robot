import rclpy
from std_msgs.msg import String
from rclpy.node import Node
from queue import Queue
import threading
from time import sleep
import gpiod
vel = 0
prev_vel=0
queue = Queue()
lock = threading.Lock()  
chip = gpiod.Chip("gpiochip4")


class Motors():
    def __init__(self,en,in1,in2):
        
        self.en=en
        self.in1=in1
        self.in2=in2
        self.en_line = chip.get_line(self.en)
        self.in1_line = chip.get_line(self.in1)
        self.in2_line = chip.get_line(self.in2)
        self.en_line.request(consumer="motor_control", type=gpiod.LINE_REQ_DIR_OUT)
        self.in1_line.request(consumer="motor_control", type=gpiod.LINE_REQ_DIR_OUT)
        self.in2_line.request(consumer="motor_control", type=gpiod.LINE_REQ_DIR_OUT)
    def move(self,vel):
        if vel<0:
            self.in1_line.set_value(0)
            self.in2_line.set_value(1)
        elif vel==0:
            self.in1_line.set_value(0)
            self.in2_line.set_value(0)
        else :
            self.in1_line.set_value(1)
            self.in2_line.set_value(0)
        self.en_line.set_value(vel)
    
class Robot():
    def __init__(self,en1,in1,in2,en2,in3,in4):
        self.motors_left=Motors(en1,in1,in2)
        self.motors_right=Motors(en2,in3,in4)
    def move(self,vel):
        self.motors_left.move(vel)
        self.motors_right.move(vel)
    def command(self,command):
        global vel
        match(command):
                case 'for-left':
                    print(command)
                    self.motors_left.move(-70)
                    self.motors_right.move(70)
                    sleep(0.075)
                    self.move(vel)
                    print('Executed ', command,' success')
                case 'for-right':
                    print(command)
                    self.motors_left.move(70)
                    self.motors_right.move(-70)
                    sleep(0.075)
                    self.move(vel)
                    print('Executed ', command,' success')
                case 'left':
                    self.motors_left.move(-70)
                    self.motors_right.move(70)
                    sleep(0.45)
                    self.move(0)
                    vel=0
                    
                    print('Executed ', command,' success')
                case 'right':
                    self.motors_left.move(70)
                    self.motors_right.move(-70)
                    sleep(0.45)
                    self.move(0)
                    vel=0
                    print('Executed ', command,' success')
    

robot=Robot(14,15,18,10,9,11)

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
            if vel < 20:
                vel += 5

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
            if vel > -20:
                vel -= 5

       
        threading.Thread(target=send_command).start()


def send_command():
    global vel
    global prev_vel
    with lock:
        if(not queue.empty()):
            command=queue.get()
            robot.command(command)


    with lock:
        if prev_vel!=vel:
            prev_vel=vel
            robot.move(prev_vel)
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
