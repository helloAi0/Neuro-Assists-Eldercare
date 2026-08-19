#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "safety_manager/safety_manager_node.hpp"

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<safety_manager::SafetyManagerNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}