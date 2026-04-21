import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    config_dir = os.path.join(get_package_share_directory('stella_vslam_ros'), 'config', '')
    vocab = config_dir + 'orb_vocab.fbow'
    cam_config = config_dir + 'oakdlite_config.yaml'
    slam_config = config_dir + 'oakdlite_slam_config.yaml'
    joy_config = config_dir + 'f710.config.yaml'

    # Joystick Teleop
    joy_teleop = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('teleop_twist_joy'), 'launch', 'teleop-launch.py')
        ),
        launch_arguments={
            'config_filepath': joy_config,
            'joy_vel': '/fastbot/cmd_vel'
        }.items()
    )

    # DepthAI Driver
    oak_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('depthai_ros_driver'),
                'launch',
                'camera.launch.py',
            ])
        ]),
        launch_arguments={
            'name': 'oak',
            'params_file': cam_config,
            'use_rviz': 'false',
            'rectify_rgb': 'false'
        }.items()
    )

    # Stella VSLAM Node
    vslam_node = Node(
        package='stella_vslam_ros',
        executable='run_slam',
        output='screen',
        arguments=[
            '-v', vocab,
            '-c', slam_config
        ],
        remappings=[
            ('camera/left/image_raw', '/oak/left/image_rect'),
            ('camera/right/image_raw', '/oak/right/image_rect'),
        ]
    )

    delayed_vslam_node = TimerAction(
            period=12.0,
            actions=[vslam_node]
    )

    return LaunchDescription([
        joy_teleop,
        oak_driver,
        delayed_vslam_node
    ])