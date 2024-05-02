from multiprocessing import Process
from flask import Flask, render_template, request, Response, redirect
from flask_socketio import SocketIO
from serial import Serial
import cv2
from time import sleep
import random
app = Flask(__name__)
socketio = SocketIO(app)
camera = cv2.VideoCapture(0)
arduino = Serial('/dev/ttyACM0', 9600)
arduino.timeout = 1


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
    
    sensor_data = arduino.readline()
    decoded = sensor_data[0:len(sensor_data)].decode("utf-8")
    socketio.emit('sensor_data', decoded)


@socketio.on('movement_command')
def handle_movement_command(command):
    print('Received command:', command)
    
    arduino.write(str(command).encode())


   
if __name__=='__main__':
   
    socketio.run(app)
    
