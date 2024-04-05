import logging
from flask import Flask, render_template,request
from flask_socketio import SocketIO
from flask import Response
from std_msgs.msg import String
from rclpy.node import Node
import cv2
import rclpy

app = Flask(__name__)
socketio = SocketIO(app)

camera = cv2.VideoCapture(0)

def gen_frames():  
    while True:
        success, frame = camera.read()  
        if not success:
            break
        else:
            resized_frame=cv2.resize(frame,(640,480))
            ret, buffer = cv2.imencode('.jpg', resized_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

class WebNode(Node):
    def __init__(self):
        super().__init__("websocket_node")
        self.publisher_cmd=self.create_publisher(
            String,
            'movement_command',
            10)
    def publish(self,msg):
        self.publisher_cmd.publish(msg)


rclpy.init()
web_node=WebNode()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
     

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('movement_command')
def handle_movement_command(command):
    print('Received command:',command)
    msg = String()
    msg.data=command
    web_node.publish(msg)
    
if __name__=='__main__':
    socketio.run(app)

    