from flask import Flask, render_template,request
from flask_socketio import SocketIO
from flask import Response
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import threading
import time

app = Flask(__name__,template_folder="/home/vboxuser/Robot/src/robot/robot/templates")
socketio = SocketIO(app)

class WebNode(Node):
    def __init__(self):
        super().__init__("websocket_node")
        self.publisher_cmd=self.create_publisher(
            String,
            'movement_command',
            10)
        self.subscription=self.create_subscription(
            Image,
            "video_frames",
            self.listener_callback,
            10
        )
        self.br=CvBridge()
        self.latest_frame = None
        self.lock = threading.Lock()
        
        
    def publish(self,msg):
        self.publisher_cmd.publish(msg)
    def listener_callback(self, data):
        self.get_logger().info("Receiving video frame")
        with self.lock:
            self.latest_frame = self.br.imgmsg_to_cv2(data)
    def gen_frames(self):  
        while True:
            with self.lock:  
                frame = self.latest_frame
                if frame is not None:
                    resized_frame = cv2.resize(frame, (640, 480))
                    ret, buffer = cv2.imencode('.jpg', resized_frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

rclpy.init()
web_node=WebNode()

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/video_feed')
def video_feed():
    return Response(web_node.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('movement_command')
def handle_movement_command(command):
    print('Received movement command:', command)
    msg = String()
    msg.data = command
    web_node.publish(msg)

def main():
    
    flask_thread = threading.Thread(target=socketio.run, args=(app,), kwargs={"host": '0.0.0.0', "port": 5050, "allow_unsafe_werkzeug": True})
    flask_thread.start()
    rclpy.spin(web_node)
    flask_thread.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        web_node.destroy_node()
        rclpy.shutdown()