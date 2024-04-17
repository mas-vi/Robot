source ~/ros2_humble/install/setup.sh
source ~/Projects/Robot/server/virtual/bin/activate
cd server
sudo gunicorn -w 1 -t 100 --worker-class eventlet -b 0.0.0.0 websocket:app
