import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CirclePublisher(Node):

    def __init__(self):
        super().__init__('publisher')
        self.publisher = self.create_publisher(Twist, '/model/fox/cmd_vel', 10)
        timer_period = 0.5  
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):

        twist = Twist()
        twist.linear.x = 0.5 
        twist.angular.z = 0.1         
        self.publisher.publish(twist)
        
        
def main(args=None):
    rclpy.init(args=args)

    circling = CirclePublisher()

    rclpy.spin(circling)

    circling.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    
