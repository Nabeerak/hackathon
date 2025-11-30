#!/usr/bin/env python3
"""
Generate ALL remaining Physical AI textbook content - MVP edition
This creates comprehensive but concise content for rapid deployment
"""

import os

BASE_DIR = "docusaurus-book/docs/physical-ai-textbook"

# ALL REMAINING CONTENT
ALL_PAGES = {
    # Complete ROS 2 Fundamentals (remaining 4 pages)
    "ros2-fundamentals/services-actions.md": """---
title: Services and Actions
sidebar_label: Services and Actions
sidebar_position: 4
description: Request-response and goal-based communication
keywords: [ROS 2, services, actions]
---

# Services and Actions

ROS 2 provides services for request-response and actions for long-running tasks.

## Services

```python
# Service server
from example_interfaces.srv import AddTwoInts

class ServiceNode(Node):
    def __init__(self):
        super().__init__('service_node')
        self.srv = self.create_service(
            AddTwoInts, 'add_two_ints', self.callback)

    def callback(self, request, response):
        response.sum = request.a + request.b
        return response
```

## Actions

```python
from action_msgs.msg import GoalStatus
from example_interfaces.action import Fibonacci

# Action server with feedback
```

## Summary

Use services for quick requests, actions for long-running goals with feedback.
""",

    "ros2-fundamentals/parameters-launch.md": """---
title: Parameters and Launch Files
sidebar_label: Parameters and Launch Files
sidebar_position: 5
description: Configuration and multi-node startup
keywords: [ROS 2, parameters, launch files]
---

# Parameters and Launch Files

Configure nodes at runtime and launch multiple nodes together.

## Parameters

```python
class ParameterNode(Node):
    def __init__(self):
        super().__init__('param_node')
        self.declare_parameter('my_param', 'default')
        value = self.get_parameter('my_param').value
```

## Launch Files

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='my_node',
            parameters=[{'param': 'value'}]
        )
    ])
```

## Summary

Parameters enable flexible configuration, launch files streamline multi-node systems.
""",

    "ros2-fundamentals/navigation-stack.md": """---
title: Navigation Stack
sidebar_label: Navigation Stack
sidebar_position: 6
description: Nav2 for autonomous robot navigation
keywords: [ROS 2, Nav2, navigation]
---

# Navigation Stack

Nav2 provides autonomous navigation for mobile robots.

## Setup

```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
```

## Configuration

Nav2 requires:
- **Map**: Occupancy grid of environment
- **Localization**: AMCL for robot pose
- **Planner**: Global and local path planning
- **Controller**: DWB for trajectory tracking

## Launch Navigation

```bash
ros2 launch nav2_bringup navigation_launch.py
```

## Summary

Nav2 enables autonomous navigation with obstacle avoidance and path planning.
""",

    "ros2-fundamentals/debugging-tools.md": """---
title: Debugging Tools
sidebar_label: Debugging Tools
sidebar_position: 7
description: ros2 CLI, rqt, and rviz2 for troubleshooting
keywords: [ROS 2, debugging, tools]
---

# Debugging Tools

Essential tools for ROS 2 development and troubleshooting.

## CLI Tools

```bash
# List nodes
ros2 node list

# List topics
ros2 topic list
ros2 topic echo /topic_name

# Check node info
ros2 node info /node_name
```

## RQt

```bash
ros2 run rqt_graph rqt_graph  # Visualize node graph
ros2 run rqt_console rqt_console  # View logs
```

## RViz2

```bash
ros2 run rviz2 rviz2  # 3D visualization
```

## Summary

Use CLI for quick checks, RQt for analysis, RViz2 for visualization.
""",

    # Complete Digital Twin Simulation (6 pages)
    "digital-twin-simulation/index.md": """---
title: Introduction to Digital Twins
sidebar_label: Introduction to Digital Twins
sidebar_position: 1
description: Physics simulation for robot development
keywords: [simulation, digital twin, Gazebo]
---

# Introduction to Digital Twins

Digital twins are virtual replicas of physical robots for safe, fast development.

## Benefits

- **Safe testing**: No hardware damage
- **Rapid iteration**: 10-100x faster than real-world
- **Synthetic data**: Generate unlimited training data
- **Cost effective**: Test before building

## Simulation Platforms

- **Gazebo**: Open-source, ROS 2 integrated
- **Unity**: Real-time rendering, game engine
- **Isaac Sim**: NVIDIA's photorealistic simulator

## Summary

Digital twins accelerate development and reduce costs.
""",

    "digital-twin-simulation/gazebo-basics.md": """---
title: Gazebo Basics
sidebar_label: Gazebo Basics
sidebar_position: 2
description: World building and robot simulation in Gazebo
keywords: [Gazebo, simulation, ROS 2]
---

# Gazebo Basics

Gazebo is the standard open-source robot simulator.

## Installation

```bash
sudo apt install ros-humble-gazebo-ros-pkgs
```

## Launch Gazebo

```bash
ros2 launch gazebo_ros gazebo.launch.py
```

## Add Robot Model

```xml
<!-- robot.urdf -->
<robot name="my_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.1"/>
      </geometry>
    </visual>
  </link>
</robot>
```

## Summary

Gazebo provides physics-based simulation for ROS 2 robots.
""",

    "digital-twin-simulation/unity-simulation.md": """---
title: Unity Simulation
sidebar_label: Unity Simulation
sidebar_position: 3
description: Real-time physics with Unity-ROS 2 integration
keywords: [Unity, simulation, ROS 2]
---

# Unity Simulation

Unity game engine for high-fidelity robot simulation.

## Unity Robotics Hub

- Real-time graphics
- Unity physics engine
- ROS 2 TCP connector

## Setup

1. Install Unity 2022 LTS
2. Import Robotics packages
3. Configure ROS 2 connection

## Summary

Unity offers photorealistic simulation with game-quality graphics.
""",

    "digital-twin-simulation/urdf-modeling.md": """---
title: URDF Robot Modeling
sidebar_label: URDF Robot Modeling
sidebar_position: 4
description: Creating robot descriptions with URDF/Xacro
keywords: [URDF, robot modeling, Xacro]
---

# URDF Robot Modeling

URDF (Unified Robot Description Format) defines robot kinematics.

## Basic URDF

```xml
<robot name="simple_robot">
  <link name="base_link"/>

  <link name="wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </visual>
  </link>

  <joint name="wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel"/>
    <origin xyz="0 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>
</robot>
```

## Summary

URDF defines robot structure for simulation and visualization.
""",

    "digital-twin-simulation/sensor-integration.md": """---
title: Sensor Integration
sidebar_label: Sensor Integration
sidebar_position: 5
description: Virtual cameras, LIDAR, and IMU sensors
keywords: [sensors, LIDAR, camera, IMU]
---

# Sensor Integration

Add virtual sensors to simulated robots.

## Camera Sensor

```xml
<gazebo reference="camera_link">
  <sensor type="camera" name="camera1">
    <update_rate>30.0</update_rate>
    <camera>
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>800</height>
      </image>
    </camera>
  </sensor>
</gazebo>
```

## LIDAR Sensor

Provides 2D/3D point cloud data for navigation.

## Summary

Virtual sensors generate realistic data for algorithm development.
""",

    "digital-twin-simulation/physics-simulation.md": """---
title: Physics Simulation
sidebar_label: Physics Simulation
sidebar_position: 6
description: Collision, friction, and dynamics modeling
keywords: [physics, simulation, dynamics]
---

# Physics Simulation

Accurate physics for realistic robot behavior.

## Physics Engines

- **ODE**: Default in Gazebo
- **Bullet**: Fast collision detection
- **PhysX**: NVIDIA accelerated

## Material Properties

```xml
<collision>
  <surface>
    <friction>
      <ode>
        <mu>0.6</mu>
        <mu2>0.6</mu2>
      </ode>
    </friction>
  </surface>
</collision>
```

## Summary

Physics simulation models real-world robot dynamics.
""",

    # Complete NVIDIA Isaac Platform (7 pages) - continuing next...
}

# Write all pages
total = 0
for filepath, content in ALL_PAGES.items():
    full_path = os.path.join(BASE_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    total += 1
    print(f"[{total}] {filepath}")

print(f"\n==> Generated {total} pages!")
