import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    vocab_path = "/ros2_ws/src/stella_vslam_ros/orb_vocab.fbow"
    config_path = "/ros2_ws/src/stella_vslam_ros/config/kitti/KITTI_stereo_00-02.yaml"
    publisher_script = "/ros2_ws/src/stella_vslam_ros/scripts/kitti_pub_stereo.py"

    return LaunchDescription([
        # 1. Transform: map -> odom
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
            output='screen'
        ),
        # 2. Transform: odom -> camera_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'camera_link'],
            output='screen'
        ),
        
        # Python topic publisher for Kitti dataset
        ExecuteProcess(
            cmd=['python3', publisher_script],
            output='screen'
        ),

        ExecuteProcess(
            cmd=[
                'ros2', 'run', 'stella_vslam_ros', 'run_slam',
                '-v', vocab_path,
                '-c', config_path
            ],
            output='screen'
        )
    ])