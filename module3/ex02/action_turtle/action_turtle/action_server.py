import rclpy
import time
import math
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.executors import MultiThreadedExecutor

from action_turtle_commands.action import MessageTurtleCommands

curr_pose = Pose()


class CommandsActionServer(Node):

    def __init__(self):
        super().__init__('action_server')
        self._action_server = ActionServer(
            self,
            MessageTurtleCommands,
            'execute_turtle_commands',
            self.execute_callback)
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        #self.subscription = self.create_subscription(
        #    Pose,
        #    '/turtle1/pose',
        #    self.listener_callback,
        #    10)
        #self.subscription



    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        
        global curr_pose

        x0, y0 = curr_pose.x, curr_pose.y

        
        twist = Twist()
        
        feedback_msg = MessageTurtleCommands.Feedback()
        feedback_msg.odom = 0
        
        if goal_handle.request.command == 'forward':
        	#twist.linear.x = 1.0
        	twist.linear.x = float(goal_handle.request.s)
        	self.publisher.publish(twist)
        	while feedback_msg.odom != goal_handle.request.s:
        		#self.get_logger().info(f'I heard: "{self.message}"')
        	#	self.publisher.publish(twist)
        		feedback_msg.odom = int(math.sqrt((curr_pose.x - x0)**2+(curr_pose.y - y0)**2))
        		self.get_logger().info(f'I went: {curr_pose.x} {x0} m')
        		goal_handle.publish_feedback(feedback_msg)
        	#	time.sleep(1)
        	#self.publisher.publish(twist)
        	#goal_handle.publish_feedback(feedback_msg)

        else:
        	if goal_handle.request.command == 'turn_left':
        		twist.angular.z = float(goal_handle.request.angle)*2*3.14/360
        	else: twist.angular.z = -1.0 * float(goal_handle.request.angle)*2*3.14/360
        	self.publisher.publish(twist)
        	#time.sleep(1)
        		
        goal_handle.succeed()
        twist.linear.x = 0.0
        self.publisher.publish(twist)
        self.get_logger().info(f'Current position: {curr_pose.x} {curr_pose.y} m')
        		
        
        result = MessageTurtleCommands.Result()
        result.result = True
        return result

class CommandsActionSubscriber(Node):
    """
    Subscriber node to the current battery state
    """     
    def __init__(self):
   
      # Initialize the class using the constructor
      super().__init__('action_subscriber')
     
      # Create a subscriber 
      # This node subscribes to messages of type
      # sensor_msgs/BatteryState
      self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
    	global curr_pose
    	curr_pose = msg


def main(args=None):
    rclpy.init(args=args)
    
    action_server = CommandsActionServer()
    action_subscriber = CommandsActionSubscriber()
    
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(action_server)
    executor.add_node(action_subscriber)



    executor.spin()
    
    executor.shutdown()
    action_server.destroy_node()
    action_subscriber.destroy_node()
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()