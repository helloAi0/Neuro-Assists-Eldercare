#ifndef SAFETY_MANAGER__SAFETY_MANAGER_NODE_HPP_
#define SAFETY_MANAGER__SAFETY_MANAGER_NODE_HPP_

#include <memory>
#include <mutex>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/empty.hpp"
#include "eldercare_msgs/msg/safety_status.hpp"
#include "eldercare_msgs/srv/set_safety_mode.hpp"

namespace safety_manager
{

class SafetyManagerNode : public rclcpp::Node
{
public:
  explicit SafetyManagerNode(const rclcpp::NodeOptions & options = rclcpp::NodeOptions());
  virtual ~SafetyManagerNode() = default;

private:
  void publish_safety_status();
  void check_watchdog();
  void heartbeat_callback(const std_msgs::msg::Empty::SharedPtr msg);
  void handle_set_safety_mode(
    const std::shared_ptr<eldercare_msgs::srv::SetSafetyMode::Request> request,
    std::shared_ptr<eldercare_msgs::srv::SetSafetyMode::Response> response);

  // ROS 2 Communication Handles
  rclcpp::Publisher<eldercare_msgs::msg::SafetyStatus>::SharedPtr status_pub_;
  rclcpp::Subscription<std_msgs::msg::Empty>::SharedPtr heartbeat_sub_;
  rclcpp::Service<eldercare_msgs::srv::SetSafetyMode>::SharedPtr service_server_;
  
  // Timers
  rclcpp::TimerBase::SharedPtr status_timer_;
  rclcpp::TimerBase::SharedPtr watchdog_timer_;

  // Thread Safety & Internal State
  std::mutex state_mutex_;
  uint8_t current_state_;
  bool e_stop_triggered_;
  bool manual_override_active_;
  bool watchdog_ok_;
  double watchdog_timeout_sec_;
  std::string active_fault_code_;
  rclcpp::Time last_heartbeat_time_;
};

}  // namespace safety_manager

#endif  // SAFETY_MANAGER__SAFETY_MANAGER_NODE_HPP_