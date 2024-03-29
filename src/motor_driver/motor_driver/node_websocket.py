from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit
import rclpy
from std_msgs.msg import String

app = Flask(__name__,template_folder="/home/vboxuser/ros2_ws/src/motor_driver/motor_driver/templates")
socketio = SocketIO(app)


rclpy.init()
node = rclpy.create_node('websocket_node')
publisher = node.create_publisher(String, 'movement_command', 10)


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
    publisher.publish(msg)

def main():
    socketio.run(app, host='0.0.0.0', port=5050)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        node.destroy_node()
        rclpy.shutdown()