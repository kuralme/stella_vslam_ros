import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    config_dir = os.path.join(get_package_share_directory('stella_vslam_ros'), 'config', '')
    vocab = config_dir + 'orb_vocab.fbow'
    slam_config = config_dir + 'oakdlite_slam_config.yaml'
    map_db = '/ros2_ws/recordings/map.msg'
    bagfile = '/ros2_ws/recordings/rosbag2_2026_05_06/rosbag2_2026_05_06.mcap'
    left_topic = '/oak/left/image_rect'
    right_topic = '/oak/right/image_rect'

    # Stella VSLAM Node
    vslam_node = Node(
        package='stella_vslam_ros',
        executable='run_slam_offline',
        output='screen',
        arguments=[
            '-v', vocab,
            '-c', slam_config,
            '-b', bagfile,
            '-i', map_db,
            '--storage-id', 'mcap',
            '--left', left_topic,
            '--right', right_topic
        ],
    )

    return LaunchDescription([
        vslam_node
    ])