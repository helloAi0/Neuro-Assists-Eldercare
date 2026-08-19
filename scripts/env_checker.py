#!/usr/bin/env python3
"""
NEURO-ASSISTS ELDERCARE: System Environment & Dependency Verifier
Author: Principal Robotics Engineer
Description: Verifies software dependencies, ROS2 installation, 
             C++ toolchains, Python scientific packages, and system specs.
"""

import os
import sys
import shutil
import platform
import subprocess
from typing import Tuple, List

class ANSIColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log_header(title: str) -> None:
    print(f"\n{ANSIColors.HEADER}{ANSIColors.BOLD}=== {title} ==={ANSIColors.ENDC}")

def check_status(item_name: str, status: bool, details: str = "") -> None:
    if status:
        print(f"  [{ANSIColors.OKGREEN}PASS{ANSIColors.ENDC}] {item_name} {f'({details})' if details else ''}")
    else:
        print(f"  [{ANSIColors.FAIL}FAIL{ANSIColors.ENDC}] {item_name} {f'({details})' if details else ''}")

def check_command(cmd: str) -> Tuple[bool, str]:
    path = shutil.which(cmd)
    if path:
        try:
            version_output = subprocess.check_output([cmd, "--version"], stderr=subprocess.STDOUT).decode('utf-8').split('\n')[0]
            return True, version_output.strip()
        except Exception:
            return True, f"Located at {path}"
    return False, "Not found in PATH"

def check_python_module(module_name: str) -> Tuple[bool, str]:
    try:
        mod = __import__(module_name)
        version = getattr(mod, '__version__', 'Installed (no version attribute)')
        return True, str(version)
    except ImportError:
        return False, "Module not installed"

def verify_environment() -> bool:
    all_passed = True

    log_header("1. SYSTEM & OPERATING SYSTEM")
    os_name = platform.system()
    os_release = platform.release()
    python_ver = platform.python_version()
    
    is_linux = os_name == "Linux"
    check_status("Operating System (Linux required)", is_linux, f"{os_name} {os_release}")
    if not is_linux:
        all_passed = False

    py_ok = sys.version_info >= (3, 10)
    check_status("Python Version (>= 3.10)", py_ok, f"Python {python_ver}")
    if not py_ok:
        all_passed = False

    log_header("2. ROS 2 & ROBOTICS TOOLCHAIN")
    ros_distro = os.environ.get("ROS_DISTRO", None)
    ros_ok = ros_distro is not None
    check_status("ROS_DISTRO Environment Variable", ros_ok, f"Active: {ros_distro}" if ros_ok else "ROS2 not sourced!")
    if not ros_ok:
        all_passed = False

    colcon_ok, colcon_info = check_command("colcon")
    check_status("Colcon Build Tool", colcon_ok, colcon_info)
    if not colcon_ok:
        all_passed = False

    rosdep_ok, rosdep_info = check_command("rosdep")
    check_status("Rosdep Dependency Tool", rosdep_ok, rosdep_info)

    log_header("3. COMPILERS & BUILD UTILITIES")
    gcc_ok, gcc_info = check_command("g++")
    check_status("C++ Compiler (g++)", gcc_ok, gcc_info)
    
    cmake_ok, cmake_info = check_command("cmake")
    check_status("CMake Build Engine", cmake_ok, cmake_info)

    git_ok, git_info = check_command("git")
    check_status("Git Version Control", git_ok, git_info)

    log_header("4. PYTHON SCIENTIFIC, AI & BCI LIBRARIES")
    py_libraries = [
        ("numpy", "NumPy Numerical Engine"),
        ("scipy", "SciPy Signal Processing"),
        ("mne", "MNE EEG/BCI Signal Processing"),
        ("torch", "PyTorch AI Framework"),
        ("cv2", "OpenCV Computer Vision"),
    ]

    for mod_id, mod_label in py_libraries:
        status, info = check_python_module(mod_id)
        check_status(mod_label, status, info)
        if not status:
            all_passed = False

    log_header("5. WORKSPACE DIRECTORY STRUCTURE")
    required_paths = [
        "ros2_ws/src",
        "scripts",
        "docs/architecture"
    ]
    for rel_path in required_paths:
        full_path = os.path.join(os.getcwd(), rel_path)
        exists = os.path.exists(full_path)
        check_status(f"Directory: {rel_path}", exists)
        if not exists:
            all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print(f"{ANSIColors.OKGREEN}{ANSIColors.BOLD}SUCCESS: Environment verification completed. Ready for Lesson 2!{ANSIColors.ENDC}")
    else:
        print(f"{ANSIColors.FAIL}{ANSIColors.BOLD}WARNING: Some required dependencies are missing. Review errors above.{ANSIColors.ENDC}")
    print("="*60 + "\n")

    return all_passed

if __name__ == "__main__":
    success = verify_environment()
    sys.exit(0 if success else 1)