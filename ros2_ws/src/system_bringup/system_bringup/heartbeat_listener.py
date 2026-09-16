import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HeartbeatListener(Node):
    """Listens for the heartbeat and logs the gap since the last one.

    In the real safety manager, silence here for too long is exactly
    what triggers a FAULT / EMERGENCY_STOP transition later on.
    """

    def __init__(self):
        super().__init__('heartbeat_listener')

        self.subscription_ = self.create_subscription(
            String,
            'system/heartbeat',
            self.on_heartbeat,
            10,
        )
        self.last_time_ = self.get_clock().now()

    def on_heartbeat(self, msg: String):
        now = self.get_clock().now()
        elapsed_sec = (now - self.last_time_).nanoseconds / 1e9
        self.last_time_ = now
        self.get_logger().info(f'Received: "{msg.data}" ({elapsed_sec:.2f}s since last)')


def main(args=None):
    rclpy.init(args=args)
    node = HeartbeatListener()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()