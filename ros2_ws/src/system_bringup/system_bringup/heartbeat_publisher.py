import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HeartbeatPublisher(Node):
    """Publishes a simple 'I'm alive' message on a fixed timer.

    This is the seed of what will later become the safety manager's
    watchdog signal: something every subsystem can check to know the
    rest of the system is still responsive.
    """

    def __init__(self):
        super().__init__('heartbeat_publisher')

        self.publisher_ = self.create_publisher(String, 'system/heartbeat', 10)

        self.counter_ = 0
        timer_period_sec = 1.0
        self.timer_ = self.create_timer(timer_period_sec, self.publish_heartbeat)

        self.get_logger().info('Heartbeat publisher started.')

    def publish_heartbeat(self):
        self.counter_ += 1
        msg = String()
        msg.data = f'alive #{self.counter_}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = HeartbeatPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()