---
title: Weekly Breakdown
sidebar_label: Weekly Breakdown
sidebar_position: 2
description: 12-week course structure mapping topics to weekly schedule
keywords: [weekly schedule, course structure, syllabus, Physical AI]
---

# Weekly Breakdown

This 12-week course progresses from foundational ROS 2 concepts through advanced humanoid robotics and VLA integration.

## Week 1: Introduction to Physical AI

**Topics**:
- What is Physical AI and Embodied Intelligence?
- Overview of robotics stack: perception, planning, control
- Introduction to ROS 2 ecosystem
- Development environment setup

**Reading**:
- [Introduction](../index.md)
- [Hardware & Infrastructure](../hardware-infrastructure/index.md)
- [ROS 2 Fundamentals - Introduction](../ros2-fundamentals/index.md)

**Lab Activities**:
1. Install Ubuntu 22.04 LTS (dual boot or VM)
2. Install ROS 2 Humble
3. Run turtlesim demo
4. Create first publisher/subscriber nodes

**Deliverables**:
- Screenshot of turtlesim running
- Git repository with first ROS 2 package

**Estimated Hours**: 8-10 hours

---

## Week 2: ROS 2 Core Concepts

**Topics**:
- ROS 2 architecture and design principles
- Nodes, topics, and message passing
- Services and actions
- Parameters and launch files

**Reading**:
- [Installation & Setup](../ros2-fundamentals/installation.md)
- [Nodes and Topics](../ros2-fundamentals/nodes-topics.md)
- [Services and Actions](../ros2-fundamentals/services-actions.md)
- [Parameters and Launch Files](../ros2-fundamentals/parameters-launch.md)

**Lab Activities**:
1. Create multi-node system for sensor fusion
2. Implement service for robot state queries
3. Write launch file for multi-robot system
4. Debug communication issues

**Deliverables**:
- ROS 2 package with 3+ nodes
- Service client/server implementation
- Launch file with parameters

**Estimated Hours**: 10-12 hours

---

## Week 3: Navigation and Debugging

**Topics**:
- Nav2 navigation stack architecture
- Path planning and obstacle avoidance
- ROS 2 debugging tools (ros2 CLI, rqt, rviz2)
- Performance profiling

**Reading**:
- [Navigation Stack](../ros2-fundamentals/navigation-stack.md)
- [Debugging Tools](../ros2-fundamentals/debugging-tools.md)

**Lab Activities**:
1. Configure Nav2 for mobile robot
2. Implement custom planner plugin
3. Debug navigation failures
4. Optimize navigation performance

**Deliverables**:
- Nav2 configuration for custom robot
- Navigation demo video
- Debug report with solutions

**Estimated Hours**: 10-12 hours

---

## Week 4: Gazebo Simulation

**Topics**:
- Gazebo architecture and world building
- URDF robot modeling
- Sensor plugins (camera, LIDAR, IMU)
- Physics engines and contact simulation

**Reading**:
- [Digital Twin Simulation - Introduction](../digital-twin-simulation/index.md)
- [Gazebo Basics](../digital-twin-simulation/gazebo-basics.md)
- [URDF Modeling](../digital-twin-simulation/urdf-modeling.md)
- [Sensor Integration](../digital-twin-simulation/sensor-integration.md)

**Lab Activities**:
1. Build custom Gazebo world
2. Create URDF model for robot
3. Add camera and LIDAR sensors
4. Simulate sensor noise and failures

**Deliverables**:
- Gazebo world file
- Complete URDF robot description
- Sensor data visualization

**Estimated Hours**: 10-12 hours

---

## Week 5: Unity and Physics Simulation

**Topics**:
- Unity-ROS 2 integration
- Real-time physics simulation
- Visual rendering and lighting
- Sim-to-real gap challenges

**Reading**:
- [Unity Simulation](../digital-twin-simulation/unity-simulation.md)
- [Physics Simulation](../digital-twin-simulation/physics-simulation.md)

**Lab Activities**:
1. Set up Unity-ROS 2 bridge
2. Import robot model into Unity
3. Configure physics materials
4. Compare Gazebo vs Unity performance

**Deliverables**:
- Unity scene with robot
- Physics comparison report
- Video of simulation

**Estimated Hours**: 8-10 hours

---

## Week 6: NVIDIA Isaac Sim

**Topics**:
- Isaac Sim architecture and features
- Omniverse platform overview
- Photorealistic rendering
- Synthetic data generation

**Reading**:
- [NVIDIA Isaac - Introduction](../nvidia-isaac/index.md)
- [Isaac Sim Overview](../nvidia-isaac/isaac-sim-intro.md)
- [Omniverse Setup](../nvidia-isaac/omniverse-setup.md)

**Lab Activities**:
1. Install Isaac Sim
2. Import robot into Omniverse
3. Generate synthetic sensor data
4. Create randomized environments

**Deliverables**:
- Isaac Sim scene
- Synthetic dataset (1000+ images)
- Randomization script

**Estimated Hours**: 10-12 hours

---

## Week 7: Perception and SLAM

**Topics**:
- Computer vision for robotics
- Depth sensing and point clouds
- SLAM algorithms (visual, LIDAR)
- Sensor fusion techniques

**Reading**:
- [Robot Brain AI](../nvidia-isaac/robot-brain-ai.md)
- [Perception Systems](../nvidia-isaac/perception-systems.md)
- [SLAM and Navigation](../nvidia-isaac/slam-navigation.md)

**Lab Activities**:
1. Implement visual odometry
2. Run SLAM with LIDAR data
3. Build 3D map of environment
4. Fuse multiple sensor streams

**Deliverables**:
- SLAM-generated map
- Localization demo
- Sensor fusion node

**Estimated Hours**: 12 hours

---

## Week 8: Sim-to-Real Transfer

**Topics**:
- Domain randomization techniques
- Reality gap challenges
- Transfer learning for robotics
- Validation on real hardware

**Reading**:
- [Sim-to-Real Transfer](../nvidia-isaac/sim-to-real-transfer.md)

**Lab Activities**:
1. Train policy in simulation
2. Apply domain randomization
3. Test on real robot (if available)
4. Measure transfer performance

**Deliverables**:
- Trained policy
- Randomization configuration
- Transfer validation report

**Estimated Hours**: 10-12 hours

---

## Week 9: Vision-Language-Action Models

**Topics**:
- VLA architecture and components
- Multimodal foundation models
- Action space representation
- End-to-end learning for manipulation

**Reading**:
- [VLA - Introduction](../vision-language-action/index.md)
- [VLA Overview](../vision-language-action/vla-overview.md)
- [Multimodal Models](../vision-language-action/multimodal-models.md)
- [Action Primitives](../vision-language-action/action-primitives.md)

**Lab Activities**:
1. Set up pre-trained VLA model
2. Test on manipulation tasks
3. Collect demonstration data
4. Analyze action predictions

**Deliverables**:
- VLA inference pipeline
- Task completion videos
- Performance analysis

**Estimated Hours**: 10-12 hours

---

## Week 10: VLA Integration and Fine-Tuning

**Topics**:
- Integrating VLA with robot control
- Fine-tuning for custom tasks
- Data collection strategies
- Evaluation metrics

**Reading**:
- [Integration Patterns](../vision-language-action/integration-patterns.md)
- [Training and Fine-Tuning](../vision-language-action/training-fine-tuning.md)

**Lab Activities**:
1. Integrate VLA with ROS 2 robot
2. Collect task-specific data
3. Fine-tune model
4. Evaluate on test set

**Deliverables**:
- ROS 2-VLA integration
- Fine-tuned model weights
- Evaluation report

**Estimated Hours**: 12 hours

---

## Week 11: Humanoid Robotics Fundamentals

**Topics**:
- Bipedal locomotion and gait control
- Manipulation with humanoid arms
- Balance and stability (ZMP, COM)
- Whole-body control

**Reading**:
- [Humanoid Robotics - Introduction](../humanoid-robotics/index.md)
- [Bipedal Locomotion](../humanoid-robotics/bipedal-locomotion.md)
- [Manipulation Control](../humanoid-robotics/manipulation-control.md)
- [Balance and Stability](../humanoid-robotics/balance-stability.md)

**Lab Activities**:
1. Simulate humanoid walking
2. Implement reaching controller
3. Test balance recovery
4. Coordinate full-body motion

**Deliverables**:
- Walking gait controller
- Manipulation demo
- Stability analysis

**Estimated Hours**: 12 hours

---

## Week 12: Conversational Robotics and HRI

**Topics**:
- Speech recognition and synthesis
- GPT integration for dialogue
- Human-robot interaction design
- Social robotics principles

**Reading**:
- [Conversational Robotics](../humanoid-robotics/conversational-robotics.md)
- [GPT Integration](../humanoid-robotics/gpt-integration.md)
- [HRI Design](../humanoid-robotics/hri-design.md)

**Lab Activities**:
1. Implement speech interface
2. Integrate GPT-4 for conversations
3. Design interaction scenarios
4. User testing and feedback

**Deliverables**:
- Conversational robot system
- Interaction demo video
- User study results

**Final Project**: Integrate all concepts into a complete humanoid robot application

**Estimated Hours**: 12-15 hours

---

## Total Course Load

- **Lecture/Reading**: ~36 hours
- **Lab Activities**: ~120-140 hours
- **Total**: ~156-176 hours over 12 weeks (~13-15 hours/week)

## Prerequisites

Before starting, ensure you meet the [course prerequisites](./prerequisites.md).
