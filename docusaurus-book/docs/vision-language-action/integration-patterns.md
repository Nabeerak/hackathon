---
title: Integration with Robots
sidebar_label: Integration with Robots
sidebar_position: 5
description: Connecting VLA to robot control
keywords: [integration, ROS 2, deployment]
---

# Integration with Robots

Connect VLA models to robot control systems.

## ROS 2 Integration

```python
# VLA node publishing actions
from geometry_msgs.msg import Twist

class VLANode(Node):
    def __init__(self):
        super().__init__('vla_node')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
```

## Summary

VLA models integrate with ROS 2 for robot control.
