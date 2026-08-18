import rclpy
from sshkeyboard import listen_keyboard, stop_listening
import sys
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist, TwistStamped

MOVE_BINDINGS = {
    'w': (2.0, 0.0),    # Forward
    's': (-2.0, 0.0),   # Backward
    'a': (0.0, 2.0),    # Turn Left
    'd': (0.0, -2.0),   # Turn Right
}

class Move_PerceptionNode(Node):
    def __init__(self):
        super().__init__("move_perception_node")

        self.use_stamped_vel = False

        self.get_logger().info(
            "\nControl Your Turtle!\n"
            "---------------------------\n"
            "   w: Forward\n"
            "   s: Backward\n"
            "   a: Turn Left\n"
            "   d: Turn Right\n"
            "   q: Quit\n"
        )

        if self.use_stamped_vel:
        
            #self.keys_subscriber = self.create_subscription(TwistStamped, "/cmd_vel", self.stamped_keys_publish, 10)
            
            self.keys_publisher = self.create_publisher(TwistStamped, "/cmd_vel", 10)

        else:
            #self.keys_subscriber = self.create_subscription(Twist, "/cmd_vel", self.keys_publish, 10)

            self.keys_publisher = self.create_publisher(Twist, "/cmd_vel", 10)
        

        

    # def press(self, key):
    #     print(f"'{key}' pressed")
    #     stop_listening()
    #     return key
    
    def key_capture(self):
        listen_keyboard(on_press=self.keys_publish)
        


    def keys_publish(self, key):
        if not rclpy.ok():
            return
        
        if key in MOVE_BINDINGS:
            x_move = MOVE_BINDINGS[key][0]
            angular_move = MOVE_BINDINGS[key][1]
            msg = Twist()

            msg.linear.x = x_move
            msg.angular.z = angular_move

            self.keys_publisher.publish(msg)
            self.get_logger().info(f'Forwarded standard Twist: Linear X={msg.linear.x}')
            self.get_logger().info(f'Forwarded standard Twist: Angular Z={msg.angular.z}')
        elif key == "q":
            self.get_logger().info("Exit key pressed. Shutting down...")
            stop_listening()
            stop_msg = Twist()
            self.keys_publisher.publish(stop_msg)
            rclpy.shutdown()
            #sys.exit(0)

    def stamped_keys_publish(self, msg):
        actual_msg = TwistStamped()

        actual_msg.twist.linear.x = msg.twist.linear.x
        actual_msg.twist.linear.y = msg.twist.linear.y    


        actual_msg.twist.angular.x = msg.twist.angular.x
        actual_msg.twist.angular.y = msg.twist.angular.y

        self.keys_publisher.publish(actual_msg)
        self.get_logger().info(f'Forwarded standard Twist: Linear X={actual_msg.twist.linear.x}')

    def destroy_node(self):
        stop_listening()
        super().destroy_node()


def main():
    rclpy.init()
    node  = Move_PerceptionNode()

    try:
        listen_keyboard(on_press=node.keys_publish)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    



if __name__ == "__main__":
    main()
