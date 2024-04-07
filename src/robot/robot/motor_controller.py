import rclpy
from std_msgs.msg import String
from rclpy.node import Node
from queue import Queue
import threading
from time import sleep
import RPi.GPIO as GPIO
vel = 0
prev_vel=0
queue = Queue()
lock = threading.Lock()  

class Motors():
    def __init__(self,en,in1,in2):
        self.en=en
        self.in1=in1
        self.in2=in2
        GPIO.setmode(GPIO.BCM)
        GPIO.setmode(self.en,GPIO.OUTPUT)
        GPIO.setmode(self.in1,GPIO.OUTPUT)
        GPIO.setmode(self.in2,GPIO.OUTPUT)
        self.pwm=GPIO.PWM(en,1000)
        self.pwm.start(0)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
    def move(self,vel):
        if vel<0:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in1,GPIO.HIGH)
        if vel==0:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in1,GPIO.LOW)
        else :
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in1,GPIO.LOW)
        self.pwm.ChangeDutyCycle(abs(vel))

class Robot():
    def __init__(self,en1,in1,in2,en2,in3,in4):
        self.motors_left=Motors(en1,in1,in2)
        self.motors_right=Motors(en2,in3,in4)
    def move(self,vel):
        self.motors_left.move(vel)
        self.motors_right.move(vel)
    def command(self,command):
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
    

robot=Robot(0,0,0,0,0,0)

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