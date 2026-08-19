# NEURO-ASSISTS ELDERCARE: Safety-Gated High-Level Intent Interface

# Discrete High-Level Command Constants
uint8 INTENT_REST = 0
uint8 INTENT_MOVE_LEFT = 1
uint8 INTENT_MOVE_RIGHT = 2
uint8 INTENT_MOVE_FORWARD = 3
uint8 INTENT_STOP = 4
uint8 INTENT_ASSIST = 5

# Standard ROS2 Header
std_msgs/Header header

# Classification Data
uint8 predicted_intent
float32 confidence_score
bool signal_quality_ok
string model_version