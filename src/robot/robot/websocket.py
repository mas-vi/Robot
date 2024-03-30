from flask import Flask, render_template,request
from flask_socketio import SocketIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

app = Flask(__name__,template_folder="/home/vboxuser/ros2_ws/src/robot/robot/templates")
socketio = SocketIO(app)

class CommandPublisher(Node):
    def __init__(self):
        super().__init__("websocket_node")
        self.publisher=self.create_publisher(
            String,
            'movement_command',
            10)
        
    def publish(self,msg):
        self.publisher.publish(msg)

rclpy.init()
command_publisher=CommandPublisher()

@app.route('/')
def home():
    return render_template("index.html")


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('movement_command')
def handle_movement_command(command):
    print('Received movement command:', command)
    msg = String()
    msg.data = command
    command_publisher.publish(msg)

def main():
    socketio.run(app, host='0.0.0.0', port=5050, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        command_publisher.destroy_node()
        rclpy.shutdown()