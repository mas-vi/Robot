cd server
gunicorn -w 1 -t 100 --worker-class eventlet -b 0.0.0.0 websocket:app
