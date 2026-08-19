from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, RegisterEventHandler, EmitEvent
from launch.events import Shutdown
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def launch_setup(context, *args, **kwargs):
    
    use_stamped_str = LaunchConfiguration("use_stamped").perform(context).strip().lower()
    use_stamped = use_stamped_str in ["true", "1"]

    nodes = []

    # 1. Main Teleop Node
    move_perception_node = Node(
        package="my_pkg",
        executable="move_perception_node",
        name="move_perception",
        output="screen",
        emulate_tty=True,
        prefix=["xterm -e"],
        parameters=[{
            'use_stamped': use_stamped,
            'dominant_color_topic': 'dominant_color'
        }]
    )
    nodes.append(move_perception_node)

    # 2. Turtlesim Node
    turtle_sim = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name="sim"
    )
    nodes.append(turtle_sim)

    # 3. Twist Unstamper Node (Dynamically added if use_stamped is True)
    if use_stamped:
        unstamper_node = Node(
            package="twist_stamper",
            executable="twist_unstamper",
            name="twist_unstamper",
            remappings=[
                ("cmd_vel_in", "/turtle1/cmd_vel_stamped"),
                ("cmd_vel_out", "/turtle1/cmd_vel"),
                ("twist_in", "/turtle1/cmd_vel_stamped"),
                ("twist_out", "/turtle1/cmd_vel")
            ]
        )
        nodes.append(unstamper_node)

    # 4. Shutdown Handler (Closes everything when xterm teleop closes)
    shutdown_handler = RegisterEventHandler(
        OnProcessExit(
            target_action=move_perception_node,
            on_exit=[
                EmitEvent(event=Shutdown())
            ]
        )
    )
    nodes.append(shutdown_handler)

    return nodes


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "use_stamped",
            default_value="false",
            description="Whether to run the twist_unstamper bridge"
        ),
        OpaqueFunction(function=launch_setup)
    ])