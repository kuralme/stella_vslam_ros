import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class KittiPublisher(Node):
    def __init__(self):
        super().__init__('kitti_publisher')
        self.left_pub = self.create_publisher(Image, 'camera/left/image_raw', 10)
        self.right_pub = self.create_publisher(Image, 'camera/right/image_raw', 10)
        self.bridge = CvBridge()
        
        # Path to sequence 00
        self.base_path = '/ros2_ws/src/stella_vslam_ros/kitti_data_odometry/dataset/sequences/00/'
        
        # 10Hz is standard for KITTI
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.frame_id = 0

    def timer_callback(self):
        # KITTI filenames are 000000.png, 000001.png, etc.
        img_name = f"{self.frame_id:06d}.png"
        left_path = os.path.join(self.base_path, 'image_0', img_name)
        right_path = os.path.join(self.base_path, 'image_1', img_name)

        if not os.path.exists(left_path):
            self.get_logger().info('End of sequence reached.')
            self.timer.cancel()
            return

        # Load images
        cv_left = cv2.imread(left_path)
        cv_right = cv2.imread(right_path)

        # Add these lines to force-match the YAML config
        # KITTI Stereo 00-02 expects 1241x376
        target_size = (1241, 376) 
        cv_left = cv2.resize(cv_left, target_size)
        cv_right = cv2.resize(cv_right, target_size)

        # If the YAML says the images should be Grayscale:
        cv_left = cv2.cvtColor(cv_left, cv2.COLOR_BGR2GRAY)
        cv_right = cv2.cvtColor(cv_right, cv2.COLOR_BGR2GRAY)

        # Get current ROS time to stamp BOTH images exactly the same
        now = self.get_clock().now().to_msg()

        # Convert to ROS message using "mono8" if you converted to gray, 
        # or keep "bgr8" if you didn't.
        left_msg = self.bridge.cv2_to_imgmsg(cv_left, encoding="mono8")
        right_msg = self.bridge.cv2_to_imgmsg(cv_right, encoding="mono8")

        # Set headers
        left_msg.header.stamp = now
        left_msg.header.frame_id = "camera_link"
        right_msg.header.stamp = now
        right_msg.header.frame_id = "camera_link"

        # Publish
        self.left_pub.publish(left_msg)
        self.right_pub.publish(right_msg)
        
        if self.frame_id % 50 == 0:
            self.get_logger().info(f'Publishing frame: {self.frame_id}')
        
        self.frame_id += 1

def main(args=None):
    rclpy.init(args=args)
    node = KittiPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()