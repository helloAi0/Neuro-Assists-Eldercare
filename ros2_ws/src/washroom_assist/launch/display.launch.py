import os
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # Traverse upwards dynamically to find workspace root containing simulation/
    current_dir = os.path.abspath(os.path.dirname(__file__))
    repo_root = current_dir
    
    while repo_root != os.path.dirname(repo_root):
        candidate = os.path.join(repo_root, "simulation", "robots", "washroom_arm.urdf.xacro")
        if os.path.exists(candidate):
            xacro_file_path = candidate
            break
        repo_root = os.path.dirname(repo_root)
    else:
        xacro_file_path = "/mnt/c/Users/user/Documents/Neuro-Assists-Eldercare/simulation/robots/washroom_arm.urdf.xacro"

    # Evaluate Xacro to produce raw URDF XML string parameter
    robot_description_content = ParameterValue(
        Command(['xacro ', xacro_file_path]),
        value_type=str
    )

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )

    # Joint State Publisher GUI Node (Interactive Sliders)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # RViz2 Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])