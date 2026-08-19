# NEURO-ASSISTS ELDERCARE: Upper-Limb Tremor Analysis Interface

# Standard ROS2 Header
std_msgs/Header header

# Spectral Analysis Metrics
float32 tremor_frequency_hz
float32 tremor_amplitude_mm
float32 dominant_axis_power
bool tremor_detected

# Active Suppression Parameters
float32 suppression_gain