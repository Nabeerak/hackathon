---
title: Prerequisites
sidebar_label: Prerequisites
sidebar_position: 3
description: Required background knowledge and setup for the Physical AI course
keywords: [prerequisites, requirements, setup, background knowledge]
---

# Course Prerequisites

To succeed in this Physical AI & Humanoid Robotics course, you should have the following background knowledge and resources.

## Technical Background

### Programming Skills (Required)

**Python 3.8+**:
- Variables, data types, functions, classes
- List comprehensions, dictionaries
- File I/O and exception handling
- Basic understanding of async/await (helpful but not required)

**OR C++17**:
- Classes, inheritance, templates
- Pointers and memory management
- STL containers and algorithms
- Modern C++ features (auto, lambdas, smart pointers)

### Linux Command Line (Required)

- Navigation: `cd`, `ls`, `pwd`, `mkdir`
- File operations: `cp`, `mv`, `rm`, `chmod`
- Process management: `ps`, `kill`, `top`
- Package management: `apt`, `apt-get`
- Text editing: `nano`, `vim`, or `emacs`
- Environment variables and `~/.bashrc`

### Robotics Fundamentals (Recommended)

- Basic understanding of coordinate frames and transformations
- Familiarity with sensors (cameras, LIDAR, IMU)
- Knowledge of robot kinematics (forward/inverse)
- Understanding of control loops (PID control)

### Mathematics (Recommended)

- Linear algebra: vectors, matrices, transformations
- Calculus: derivatives, integrals
- Probability and statistics basics
- Geometry: Euclidean transforms, quaternions

### Machine Learning Basics (Helpful)

- Understanding of neural networks
- Familiarity with PyTorch or TensorFlow
- Knowledge of supervised/unsupervised learning
- Exposure to computer vision concepts

## Hardware Requirements

See the [Hardware & Infrastructure](../hardware-infrastructure/index.md) chapter for detailed specifications. You'll need **one of the following**:

### Option 1: Digital Twin Workstation (Recommended)

- **GPU**: NVIDIA RTX 4070 Ti (12GB VRAM) or higher
- **CPU**: Intel Core i7 13th Gen or AMD Ryzen 9
- **RAM**: 64GB DDR5
- **Storage**: 1TB NVMe SSD
- **OS**: Ubuntu 22.04 LTS

### Option 2: Cloud-Native Setup

- AWS/Azure instance with NVIDIA GPU
- NVIDIA Isaac Sim on Omniverse Cloud
- See [Cloud-Native Alternatives](../hardware-infrastructure/cloud-native-alternatives.md)

### Option 3: Minimal Setup (Limited Labs)

- Any Linux/Mac/Windows machine for theory
- Cloud resources for simulation labs
- Note: Cannot run all labs locally

## Software Installation

Before Week 1, install:

1. **Ubuntu 22.04 LTS**: Dual boot, VM, or WSL2
2. **ROS 2 Humble**: Latest stable release
3. **Git**: For version control
4. **VS Code or PyCharm**: Code editor with Python/C++ support
5. **Docker**: For containerized environments (optional but recommended)

Detailed installation instructions in [ROS 2 Installation](../ros2-fundamentals/installation.md).

## Time Commitment

- **Lectures/Reading**: ~3 hours/week
- **Lab Activities**: ~10-12 hours/week
- **Total**: ~13-15 hours/week for 12 weeks

## Optional but Recommended

- **GitHub Account**: For code repositories and collaboration
- **Discord/Slack**: For course discussions (check with instructor)
- **Physical Robot** (optional): Unitree, Robotis, or similar for real hardware testing

## Self-Assessment Quiz

Before starting, you should be able to:

- [ ] Write a Python class with methods and attributes
- [ ] Navigate a Linux filesystem using terminal commands
- [ ] Explain what a coordinate frame is in robotics
- [ ] Describe the difference between a topic and a service in ROS
- [ ] Calculate a matrix-vector multiplication by hand
- [ ] Install software packages using `apt` on Ubuntu
- [ ] Clone a GitHub repository using Git
- [ ] Explain what a neural network does at a high level

If you checked 6+ boxes, you're ready to begin!

If you need to strengthen your background:

- **Python**: [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- **Linux**: [Linux Command Line Basics](https://ubuntu.com/tutorials/command-line-for-beginners)
- **Robotics**: [Modern Robotics Textbook](http://hades.mech.northwestern.edu/index.php/Modern_Robotics) (free online)
- **Linear Algebra**: [3Blue1Brown Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)

## Ready to Begin?

Proceed to [Hardware & Infrastructure](../hardware-infrastructure/index.md) to set up your development environment!
