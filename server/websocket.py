from multiprocessing import Process
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO
from std_msgs.msg import String
from rclpy.node import Node
import cv2
import rclpy
from time import sleep
import random
import Adafruit_DHT
app = Flask(__name__)
socketio = SocketIO(app)
#sensor=Adafruit_DHT.DHT11
camera = cv2.VideoCapture(0)



def gen_frames():  
    while True:
        success, frame = camera.read()  
        if not success:
            break
        else:
            resized_frame = cv2.resize(frame, (640, 480))
            ret, buffer = cv2.imencode('.jpg', resized_frame)
            frame = buffer.tobytes()
            sleep(0.0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

class WebNode(Node):
    def __init__(self):
        super().__init__("websocket_node")
        self.publisher_cmd = self.create_publisher(
            String,
            'movement_command',
            10
        )
    def publish(self, msg):
        self.publisher_cmd.publish(msg)     

    

rclpy.init()
web_node = WebNode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('connect', 'You are now connected')

@socketio.on('sensor_data')
def send_data():
    #temperature=sensor.temperature
    #humidity=sensor.humidity
    
    #temperature, humidity = Adafruit_DHT.read_retry(sensor, 4)

    temperature = random.uniform(20.0, 30.0)
    humidity = random.uniform(40.0, 60.0)
    sensor_data = f'Temperature: {"%.2f" %temperature} °C, Humidity: {"%.2f" %humidity} %'
    socketio.emit('sensor_data', sensor_data)
    print(sensor_data)

@socketio.on('movement_command')
def handle_movement_command(command):
    print('Received command:', command)
    msg = String()
    msg.data = command
    web_node.publish(msg)

   
if __name__=='__main__':
   
    socketio.run(app)
    web_node.destroy_node()
    rclpy.shutdown()
    #sensor.exit()
    
