import rclpy, threading
from sshkeyboard import listen_keyboard, stop_listening
from std_msgs.msg import String
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist, TwistStamped
from turtlesim.msg import Color
from rclpy.validate_topic_name import validate_topic_name
from rclpy.exceptions import InvalidTopicNameException

move_bindings = {
    'w': (2.0, 0.0),    # Forward
    's': (-2.0, 0.0),   # Backward
    'a': (0.0, 2.0),    # Turn Left
    'd': (0.0, -2.0),   # Turn Right
}

class Move_PerceptionNode(Node):
    def __init__(self, dominant_color_topic: str):

        
        super().__init__("move_perception_node")

        # self.use_stamped_vel = use_stamped_vel
        self.declare_parameter("use_stamped", False)
        self.use_stamped_vel = self.get_parameter("use_stamped").get_parameter_value().bool_value
        self.declare_parameter("dominant_color_topic", "/dominant_color")
        

        self.dominant_color_topic = "/" + dominant_color_topic
        
        self.latest_dominant_ch = "X"

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
            
            self.keys_publisher = self.create_publisher(TwistStamped, "/turtle1/cmd_vel_stamped", 10)

        else:

            self.keys_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.color_subscriber = self.create_subscription(Color, "/turtle1/color_sensor", self.color_subscribe, 10)
        self.color_publisher = self.create_publisher(String, self.dominant_color_topic, 10)
        
    

    def color_subscribe(self, msg):
        red  = msg.r
        green = msg.g
        blue = msg.b

        if red == green == blue:
            self.latest_dominant_ch = "White"
        elif red > green and red > blue:
            self.latest_dominant_ch = "Red"
        elif green > red and green > blue:
            self.latest_dominant_ch = "Green"
        else:
            self.latest_dominant_ch = "Blue"

        
        

    def keys_publish(self, key):
        if not rclpy.ok():
            return
        
        if key in move_bindings:
            x_move = move_bindings[key][0]
            angular_move = move_bindings[key][1]
            if self.use_stamped_vel:
                msg = TwistStamped()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = "turtle1"
                msg.twist.linear.x = x_move
                msg.twist.angular.z = angular_move
            else:
                msg = Twist()
                msg.linear.x = x_move
                msg.angular.z = angular_move

            self.keys_publisher.publish(msg)
            if self.use_stamped_vel:
                self.get_logger().info(f'Stamped Twist: Linear X = {msg.twist.linear.x}')
                self.get_logger().info(f'Stamped Twist: Angular Z = {msg.twist.angular.z}')
            else:
                self.get_logger().info(f'Standard Twist: Linear X = {msg.linear.x}')
                self.get_logger().info(f'Standard Twist: Angular Z = {msg.angular.z}')

            self.get_logger().info(f"The Dominant Color is {self.latest_dominant_ch}")
            
            dom_color = String()
            dom_color.data = self.latest_dominant_ch[0].lower()
            
            self.color_publisher.publish(dom_color)

        elif key == "q":
            self.get_logger().info("Exit key pressed. Shutting down...")
            stop_listening()
            if self.use_stamped_vel:
                stop_msg = TwistStamped()
            else:
                stop_msg = Twist()
            self.keys_publisher.publish(stop_msg)
            rclpy.shutdown()


    def destroy_node(self):
        stop_listening()
        super().destroy_node()

def is_valid_ros2_topic(topic_name: str):
    try:
        # This will raise an exception if the name is invalid
        validate_topic_name(topic_name)
        return True
    except InvalidTopicNameException as e:
        print(f"Invalid topic name: {e}")
        return False



def main():
    # print("1. Stamped Twist")
    # print("2. Normal Twist")
    # while True:
    #     use_stamped_vel = input("Choose: ").strip()
    #     if use_stamped_vel.isdecimal() and use_stamped_vel in ["1", "2"]:
    #         use_stamped_vel = (int(use_stamped_vel) == 1)
    #         break
    #     else:
    #         print("Invalid Number!!")
    #         continue
    while True:
        dominant_color_topic = input("Choose The Dominant Color Topic Name (For Default, Press Enter): ")
        if not dominant_color_topic:
            dominant_color_topic = "dominant_name"
        if is_valid_ros2_topic(dominant_color_topic):
            break
        else:
            continue

    rclpy.init()
    node  = Move_PerceptionNode(dominant_color_topic)
    
    try:
    
        spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
        spin_thread.start()
        listen_keyboard(on_press=node.keys_publish)
            
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    



if __name__ == "__main__":
    main()
