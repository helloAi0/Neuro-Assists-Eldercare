cmake_minimum_required(VERSION 3.10)
project(safety_manager)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 20)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(eldercare_msgs REQUIRED)

include_directories(include)

add_library(safety_manager_lib
  src/safety_manager_node.cpp
)
ament_target_dependencies(safety_manager_lib
  rclcpp
  std_msgs
  eldercare_msgs
)

add_executable(safety_manager_node
  src/main.cpp
)
target_link_libraries(safety_manager_node
  safety_manager_lib
)
ament_target_dependencies(safety_manager_node
  rclcpp
  std_msgs
  eldercare_msgs
)

install(TARGETS
  safety_manager_lib
  safety_manager_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include
)

ament_package()