import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import board
import adafruit_dht
import random
# sensor=adafruit_dht.DHT11(board.D4)

class DHTPublisher(Node):
    def __init__(self):
        super().__init__("dht11_publisher")
        self.publisher = self.create_publisher(String, "dht11_topic", 10)
        timer_period = 0.5
        self.timer=self.create_timer(timer_period,self.timer_callback)
    def timer_callback(self):
        # temp=sensor.temperature
        # hum=sensor.humidity
        msg=String()
        temp=random.uniform(20.0, 30.0)
        hum=random.uniform(40.0, 60.0)
        msg.data=f'Temperature: {"%.2f" %temp} °C, Humidity: {"%.2f" %hum} %'
        print("sending ",msg.data)
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    dht_publisher=DHTPublisher()
    rclpy.spin(dht_publisher)
    dht_publisher.destroy_node()
    rclpy.shutdown()
    # sensor.exit()


if __name__=='__main__':
    main()