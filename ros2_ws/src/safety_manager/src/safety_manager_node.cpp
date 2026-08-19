#include "safety_manager/safety_manager_node.hpp"

namespace safety_manager
{

using namespace std::chrono_literals;

SafetyManagerNode::SafetyManagerNode(const rclcpp::NodeOptions & options)
: Node("safety_manager_node", options),
  current_state_(eldercare_msgs::msg::SafetyStatus::STATE_IDLE),
  e_stop_triggered_(false),
  manual_override_active_(false),
  watchdog_ok_(true),
  watchdog_timeout_sec_(2.0),
  active_fault_code_("NONE"),
  last_heartbeat_time_(this->now())
{
  // Declare parameters
  this->declare_parameter<double>("watchdog_timeout_sec", 2.0);
  this->get_parameter("watchdog_timeout_sec", watchdog_timeout_sec_);

  // Create Publisher
  status_pub_ = this->create_publisher<eldercare_msgs::msg::SafetyStatus>(
    "/eldercare/safety/status", rclcpp::QoS(10).reliable());

  // Create Heartbeat Subscriber
  heartbeat_sub_ = this->create_subscription<std_msgs::msg::Empty>(
    "/eldercare/heartbeat", rclcpp::QoS(10).best_effort(),
    std::bind(&SafetyManagerNode::heartbeat_callback, this, std::placeholders::_1));

  // Create Service Server
  service_server_ = this->create_service<eldercare_msgs::srv::SetSafetyMode>(
    "/eldercare/safety/set_mode",
    std::bind(&SafetyManagerNode::handle_set_safety_mode, this, std::placeholders::_1, std::placeholders::_2));

  // Timers: Status publishing at 10 Hz, Watchdog checking at 5 Hz
  status_timer_ = this->create_wall_timer(
    100ms, std::bind(&SafetyManagerNode::publish_safety_status, this));
  
  watchdog_timer_ = this->create_wall_timer(
    200ms, std::bind(&SafetyManagerNode::check_watchdog, this));

  RCLCPP_INFO(this->get_logger(), "Safety Manager Node Initialized successfully in STATE_IDLE.");
}

void SafetyManagerNode::heartbeat_callback(const std_msgs::msg::Empty::SharedPtr /*msg*/)
{
  std::lock_guard<std::mutex> lock(state_mutex_);
  last_heartbeat_time_ = this->now();
  watchdog_ok_ = true;
}

void SafetyManagerNode::check_watchdog()
{
  std::lock_guard<std::mutex> lock(state_mutex_);
  
  // Skip watchdog monitoring if in Emergency Stop or Fault state already
  if (current_state_ == eldercare_msgs::msg::SafetyStatus::STATE_EMERGENCY_STOP ||
      current_state_ == eldercare_msgs::msg::SafetyStatus::STATE_FAULT)
  {
    return;
  }

  double elapsed_sec = (this->now() - last_heartbeat_time_).seconds();
  if (elapsed_sec > watchdog_timeout_sec_)
  {
    watchdog_ok_ = false;
    current_state_ = eldercare_msgs::msg::SafetyStatus::STATE_FAULT;
    active_fault_code_ = "ERR_WATCHDOG_TIMEOUT";
    RCLCPP_ERROR(
      this->get_logger(),
      "WATCHDOG TIMEOUT EXCEEDED (%.2f s > %.2f s)! Transitioned to STATE_FAULT.",
      elapsed_sec, watchdog_timeout_sec_);
  }
}

void SafetyManagerNode::publish_safety_status()
{
  std::lock_guard<std::mutex> lock(state_mutex_);

  eldercare_msgs::msg::SafetyStatus status_msg;
  status_msg.header.stamp = this->now();
  status_msg.header.frame_id = "base_link";
  status_msg.current_state = current_state_;
  status_msg.e_stop_triggered = e_stop_triggered_;
  status_msg.manual_override_active = manual_override_active_;
  status_msg.watchdog_ok = watchdog_ok_;
  status_msg.max_joint_effort_ratio = (current_state_ == eldercare_msgs::msg::SafetyStatus::STATE_EMERGENCY_STOP) ? 0.0f : 1.0f;
  status_msg.active_fault_code = active_fault_code_;

  status_pub_->publish(status_msg);
}

void SafetyManagerNode::handle_set_safety_mode(
  const std::shared_ptr<eldercare_msgs::srv::SetSafetyMode::Request> request,
  std::shared_ptr<eldercare_msgs::srv::SetSafetyMode::Response> response)
{
  std::lock_guard<std::mutex> lock(state_mutex_);

  response->previous_state = current_state_;

  // Handle Emergency Stop Request
  if (request->target_state == eldercare_msgs::msg::SafetyStatus::STATE_EMERGENCY_STOP)
  {
    current_state_ = eldercare_msgs::msg::SafetyStatus::STATE_EMERGENCY_STOP;
    e_stop_triggered_ = true;
    active_fault_code_ = "E_STOP_USER_REQUEST";
    response->success = true;
    response->new_state = current_state_;
    response->message = "Emergency stop engaged successfully.";
    RCLCPP_WARN(this->get_logger(), "EMERGENCY STOP ENGAGED via Service call: %s", request->reason.c_str());
    return;
  }

  // Prevent leaving E-Stop without explicit force_override
  if (e_stop_triggered_ && !request->force_override)
  {
    response->success = false;
    response->new_state = current_state_;
    response->message = "Cannot transition out of E-STOP without force_override=true.";
    RCLCPP_ERROR(this->get_logger(), "Rejected transition attempt out of E-STOP without override flag.");
    return;
  }

  // Clear E-stop if force_override is granted
  if (e_stop_triggered_ && request->force_override)
  {
    e_stop_triggered_ = false;
    active_fault_code_ = "NONE";
    last_heartbeat_time_ = this->now(); // Reset heartbeat timestamp
  }

  current_state_ = request->target_state;
  response->success = true;
  response->new_state = current_state_;
  response->message = "State updated successfully.";

  RCLCPP_INFO(
    this->get_logger(), "Safety state updated to: %u. Reason: %s",
    current_state_, request->reason.c_str());
}

}  // namespace safety_manager