#!/usr/bin/env python3
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from geometry_msgs.msg import Twist
import cv2 # Python OpenCV library
import numpy as np


class NewPublisher(Node):
    def __init__(self):
        super().__init__('new_publisher')
        self.window_name = "Projekt Publisher"
        self.window_size = (700, 700)
        self.window_image = np.zeros((self.window_size[0], self.window_size[1], 3), np.uint8)
        cv2.imshow(self.window_name, self.window_image)
        cv2.waitKey(25)
        self.cords = None

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.25  # seconds
        self.timer = self.create_timer(timer_period, self._timer_callback)
        cv2.setMouseCallback(self.window_name, self.get_mouse_click)
        print("I'm alllive")

    def get_mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.cords = (x, y)

    def _timer_callback(self):
        if self.cords != None:
            cmd_velocity = Twist()
            cmd_velocity.linear.y = 0.0
            velocity = 0.5

            if self.cords[1] <= self.window_size[1] and self.cords[1] > (self.window_size[1]/3)*2:
                cmd_velocity.linear.x = -velocity
            elif self.cords[1] <= (self.window_size[1]/3)*2 and self.cords[1] > self.window_size[1]/3:
                cmd_velocity.linear.x = 0.0
            else:
                cmd_velocity.linear.x = velocity

            self.publisher_.publish(cmd_velocity) #wysylamy do topicu
            self.get_logger().info(f"Publishing: {cmd_velocity.linear.x}")
        cv2.waitKey(25)


def main(args=None):
    rclpy.init(args=args)
    new_publisher = NewPublisher()
    rclpy.spin(new_publisher)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    new_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()