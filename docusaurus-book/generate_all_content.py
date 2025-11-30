#!/usr/bin/env python3
import os

base = "docs/physical-ai-textbook"

# Generate complete ROS 2 Fundamentals chapter (7 pages)
ros2_pages = {
    "ros2-fundamentals/index.md": """---
title: Introduction to ROS 2
sidebar_label: Introduction to ROS 2
sidebar_position: 1
description: Overview of ROS 2 architecture and ecosystem
keywords: [ROS 2, robotics, middleware]
---

# Introduction to ROS 2

ROS 2 (Robot Operating System 2) is the standard middleware for robot development, providing communication, tools, and libraries.

## Why ROS 2?

- **Industry standard**: Used by Boston Dynamics, NASA, automotive companies
- **Real-time capable**: DDS middleware with deterministic communication
- **Production ready**: Security, scalability, multi-robot support
- **Cross-platform**: Linux, Windows, macOS

## Core Concepts

**Nodes**: Independent processes that perform computation
**Topics**: Named buses for streaming data (publish/subscribe)
**Services**: Request/response communication
**Actions**: Long-running tasks with feedback

## ROS 2 vs ROS 1

| Feature | ROS 1 | ROS 2 |
|---------|-------|-------|
| Real-time | No | Yes |
| Security | Limited | TLS/SROS2 |
| Multi-robot | Difficult | Native |
| Python | 2.7 | 3.8+ |

## Summary

ROS 2 is the foundation for modern robotics development.
""",

    "ros2-fundamentals/installation.md": """---
title: Installation & Setup
sidebar_label: Installation & Setup
sidebar_position: 2
description: Installing ROS 2 Humble on Ubuntu 22.04
keywords: [ROS 2, installation, Ubuntu]
---

# Installation & Setup

Install ROS 2 Humble on Ubuntu 22.04.

## Prerequisites

```bash
sudo apt update && sudo apt upgrade -y
```

## Add ROS 2 Repository

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
```

## Install ROS 2 Humble

```bash
sudo apt update
sudo apt install ros-humble-desktop
```

## Setup Environment

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Verify Installation

```bash
ros2 run demo_nodes_cpp talker
# Open new terminal
ros2 run demo_nodes_cpp listener
```

## Summary

ROS 2 Humble is now installed and ready for development.
""",

    "ros2-fundamentals/nodes-topics.md": """---
title: Nodes and Topics
sidebar_label: Nodes and Topics
sidebar_position: 3
description: Creating publishers and subscribers
keywords: [ROS 2, nodes, topics, pub/sub]
---

# Nodes and Topics

Nodes communicate via topics using publish/subscribe pattern.

## Creating a Publisher

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        
    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2!'
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = MinimalPublisher()
    rclpy.spin(node)
```

## Creating a Subscriber

```python
class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String, 'topic', self.callback, 10)
        
    def callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')
```

## Summary

Topics enable decoupled communication between nodes.
""",
}

# Write ROS 2 pages
for path, content in ros2_pages.items():
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print(f"ROS2: {path}")

print(f"Generated {len(ros2_pages)} ROS 2 pages")
