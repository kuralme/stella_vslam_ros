#!/bin/bash
set -e

# export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
source "/opt/ros/$ROS_DISTRO/setup.bash"

# Source local ws if it exists
if [ -f "/ros2_ws/install/setup.bash" ]; then
    source "/ros2_ws/install/setup.bash"
    echo "Sourced local workspace: /ros2_ws"
else
    echo "No local workspace found at /ros2_ws, skipping..."
fi

# Execute the command passed from compose
exec "$@"