from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    move_perception_node = Node(
        package = "my_pkg",
        executable = "move_perception_node",
        name = "move_perception",
        output = "screen",
        emulate_tty = True
    )

    use_stamped_config = LaunchConfiguration("use_stamped")

    unstamper_node = Node(
        package = "twist_stamper",
        executable = "twist_unstamper",
        name = "twist_unstamper",
        remappings = [
            ("/cmd_vel_in", "/turtle1/cmd_vel_stamped"),
            ("/cmd_vel_out", "/turtle1/cmd_vel")
        ],
        condition = IfCondition(use_stamped_config)
    )

    use_stamped_arg = DeclareLaunchArgument(
        "use_stamped",
        default_value = "false"
    )

    turtle_sim = Node(
        package = "turtlesim",
        executable = "turtlesim_node",
        name = "sim"
    )

    return LaunchDescription([
        move_perception_node,
        turtle_sim,
        use_stamped_arg,
        unstamper_node
    ])