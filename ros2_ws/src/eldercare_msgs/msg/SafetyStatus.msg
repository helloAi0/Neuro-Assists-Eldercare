# NEURO-ASSISTS ELDERCARE: System Safety State Interface
# ISO 13849 & ISO 13482 Safety Compliance Definition

# State Machine Constants
uint8 STATE_IDLE = 0
uint8 STATE_USER_DETECTED = 1
uint8 STATE_ASSESSING = 2
uint8 STATE_ASSIST_READY = 3
uint8 STATE_ASSISTING_SIT = 4
uint8 STATE_ASSISTING_STAND = 5
uint8 STATE_PAUSED = 6
uint8 STATE_EMERGENCY_STOP = 7
uint8 STATE_FAULT = 8
uint8 STATE_SAFE_SHUTDOWN = 9

# Standard ROS2 Header
std_msgs/Header header

# Current Operating State
uint8 current_state

# Safety Flags
bool e_stop_triggered
bool manual_override_active
bool watchdog_ok

# Actuator & System Hardware Metrics
float32 max_joint_effort_ratio
string active_fault_code