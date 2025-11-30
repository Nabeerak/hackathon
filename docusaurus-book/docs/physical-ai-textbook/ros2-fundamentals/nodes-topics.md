---
title: Nodes and Topics
sidebar_label: Nodes and Topics
sidebar_position: 3
description: Creating publishers and subscribers in ROS 2
keywords: [ROS 2, nodes, topics, pub/sub, publish, subscribe]
---

# Nodes and Topics

## Introduction

Nodes and topics form the backbone of ROS 2's distributed communication architecture. Understanding how nodes communicate through topics is essential for building any robotic system. In this chapter, you'll learn how to create publishers and subscribers, understand the publish-subscribe pattern, and build your first ROS 2 applications.

## What are Nodes?

A **node** is a fundamental unit of computation in ROS 2. Think of nodes as individual processes that perform specific tasks in your robot system. Each node should have a single, well-defined purpose. For example:

- A camera node that publishes image data
- A motor controller node that sends velocity commands
- A navigation node that processes sensor data and plans paths

### Node Design Principles

When designing nodes, follow these best practices:

1. **Single Responsibility**: Each node should do one thing well
2. **Loose Coupling**: Nodes communicate through well-defined interfaces
3. **Modularity**: Nodes can be reused across different robots
4. **Testability**: Individual nodes can be tested in isolation

## Understanding Topics

**Topics** are named buses over which nodes exchange messages. The publish-subscribe pattern enables:

- **Decoupling**: Publishers don't need to know about subscribers
- **Scalability**: Multiple publishers and subscribers per topic
- **Flexibility**: Add/remove nodes without changing existing code

### Topic Naming Conventions

Follow these conventions for topic names:

- Use lowercase with underscores: `/sensor_data`
- Organize hierarchically: `/robot/sensors/camera/image`
- Avoid spaces and special characters
- Be descriptive: `/cmd_vel` not `/c`

## Creating a Publisher Node

Let's create a complete publisher node that demonstrates best practices:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class VelocityPublisher(Node):
    """
    A publisher node that sends velocity commands to a robot.
    Demonstrates timer-based publishing and proper node structure.
    """

    def __init__(self):
        # Initialize the node with a descriptive name
        super().__init__('velocity_publisher')

        # Create a publisher on the /cmd_vel topic
        # Queue size of 10 means keep last 10 messages if subscriber is slow
        self.publisher = self.create_publisher(
            Twist,           # Message type
            '/cmd_vel',      # Topic name
            10               # Queue size
        )

        # Create a timer that calls our callback every 0.5 seconds
        self.timer = self.create_timer(0.5, self.timer_callback)

        # Counter to track published messages
        self.count = 0

        self.get_logger().info('Velocity Publisher has been started')

    def timer_callback(self):
        """
        Called every 0.5 seconds by the timer.
        Publishes velocity commands to make robot drive in circles.
        """
        msg = Twist()

        # Set linear velocity (forward speed)
        msg.linear.x = 0.5  # meters per second
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        # Set angular velocity (turning speed)
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.3  # radians per second

        # Publish the message
        self.publisher.publish(msg)

        # Log for debugging
        self.get_logger().info(
            f'Publishing velocity #{self.count}: '
            f'linear={msg.linear.x}, angular={msg.angular.z}'
        )
        self.count += 1

def main(args=None):
    # Initialize ROS 2 Python client library
    rclpy.init(args=args)

    # Create the node
    node = VelocityPublisher()

    try:
        # Keep node running and processing callbacks
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Code Explanation

**Line-by-line breakdown:**

- **Lines 1-3**: Import necessary ROS 2 libraries
- **Line 11**: Call parent class constructor with node name
- **Lines 14-18**: Create publisher with message type, topic name, and queue size
- **Line 21**: Create timer for periodic publishing
- **Lines 30-43**: Timer callback creates and publishes Twist messages
- **Lines 48-50**: Initialize ROS, create node, and spin
- **Lines 51-56**: Handle shutdown gracefully

## Creating a Subscriber Node

Now let's create a subscriber that receives and processes these velocity commands:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class VelocitySubscriber(Node):
    """
    A subscriber node that receives velocity commands.
    Demonstrates callback handling and message processing.
    """

    def __init__(self):
        super().__init__('velocity_subscriber')

        # Create subscription to /cmd_vel topic
        self.subscription = self.create_subscription(
            Twist,              # Message type
            '/cmd_vel',         # Topic name
            self.callback,      # Callback function
            10                  # Queue size
        )

        # Prevent unused variable warning
        self.subscription

        self.get_logger().info('Velocity Subscriber has been started')

    def callback(self, msg):
        """
        Called automatically when a message is received.

        Args:
            msg: Twist message containing velocity commands
        """
        # Extract linear and angular velocities
        linear_vel = msg.linear.x
        angular_vel = msg.angular.z

        # Process the data
        self.get_logger().info(
            f'Received velocity command: '
            f'linear={linear_vel:.2f} m/s, '
            f'angular={angular_vel:.2f} rad/s'
        )

        # You could add more processing here:
        # - Validate velocities are within safe limits
        # - Convert to motor commands
        # - Log to file for analysis
        # - Trigger safety checks

def main(args=None):
    rclpy.init(args=args)
    node = VelocitySubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Message Types

ROS 2 provides many standard message types. Here are the most common:

### Standard Messages (std_msgs)

```python
from std_msgs.msg import String, Int32, Float64, Bool

# String message
str_msg = String()
str_msg.data = "Hello, ROS 2!"

# Numeric messages
int_msg = Int32()
int_msg.data = 42

float_msg = Float64()
float_msg.data = 3.14159

# Boolean message
bool_msg = Bool()
bool_msg.data = True
```

### Geometry Messages (geometry_msgs)

```python
from geometry_msgs.msg import Point, Pose, Twist, Vector3

# 3D point
point = Point()
point.x = 1.0
point.y = 2.0
point.z = 3.0

# Velocity command
twist = Twist()
twist.linear = Vector3(x=0.5, y=0.0, z=0.0)
twist.angular = Vector3(x=0.0, y=0.0, z=0.3)
```

### Sensor Messages (sensor_msgs)

```python
from sensor_msgs.msg import Image, LaserScan, Imu

# These are more complex and typically published by drivers
```

## Quality of Service (QoS)

QoS settings control message delivery behavior:

```python
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

# Reliable delivery (important messages)
reliable_qos = QoSProfile(
    reliability=QoSReliabilityPolicy.RELIABLE,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=10
)

# Best effort (sensor data, can lose some)
sensor_qos = QoSProfile(
    reliability=QoSReliabilityPolicy.BEST_EFFORT,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=5
)

# Use with publisher
self.publisher = self.create_publisher(
    Twist,
    '/cmd_vel',
    reliable_qos
)
```

### When to Use Each QoS

- **RELIABLE**: Commands, state updates, critical data
- **BEST_EFFORT**: High-frequency sensor data (camera, lidar)

## Practical Exercise: Temperature Monitor

Create a system with two nodes:

1. **Temperature Publisher**: Simulates temperature sensor
2. **Temperature Monitor**: Watches for unsafe temperatures

### Temperature Publisher

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class TemperatureSensor(Node):
    def __init__(self):
        super().__init__('temperature_sensor')
        self.publisher = self.create_publisher(Float32, '/temperature', 10)
        self.timer = self.create_timer(1.0, self.publish_temperature)

    def publish_temperature(self):
        temp = Float32()
        # Simulate temperature reading (15-35 degrees C)
        temp.data = 20.0 + random.uniform(-5.0, 15.0)
        self.publisher.publish(temp)
        self.get_logger().info(f'Temperature: {temp.data:.1f}°C')

def main():
    rclpy.init()
    node = TemperatureSensor()
    rclpy.spin(node)
```

### Temperature Monitor

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TemperatureMonitor(Node):
    def __init__(self):
        super().__init__('temperature_monitor')
        self.subscription = self.create_subscription(
            Float32,
            '/temperature',
            self.temperature_callback,
            10
        )
        self.max_safe_temp = 30.0

    def temperature_callback(self, msg):
        temp = msg.data
        if temp > self.max_safe_temp:
            self.get_logger().warn(
                f'HIGH TEMPERATURE WARNING: {temp:.1f}°C '
                f'(max safe: {self.max_safe_temp}°C)'
            )
        else:
            self.get_logger().info(f'Temperature OK: {temp:.1f}°C')

def main():
    rclpy.init()
    node = TemperatureMonitor()
    rclpy.spin(node)
```

## Running Your Nodes

### Terminal 1: Run Publisher
```bash
python3 temperature_sensor.py
```

### Terminal 2: Run Subscriber
```bash
python3 temperature_monitor.py
```

### Inspecting Topics

```bash
# List all topics
ros2 topic list

# Show topic info
ros2 topic info /temperature

# Echo messages in real-time
ros2 topic echo /temperature

# Check message frequency
ros2 topic hz /temperature

# View topic type
ros2 topic type /temperature
```

## Debugging Common Issues

### Issue 1: No Messages Received

**Symptoms**: Subscriber runs but receives no messages

**Causes and Solutions**:
1. **Topic name mismatch**: Check spelling with `ros2 topic list`
2. **Different DDS domains**: Ensure `ROS_DOMAIN_ID` matches
3. **QoS incompatibility**: Use compatible QoS profiles

### Issue 2: High Latency

**Symptoms**: Messages arrive with delay

**Solutions**:
1. Reduce queue size if processing is slow
2. Check CPU usage with `top`
3. Use BEST_EFFORT QoS for sensor data

### Issue 3: Message Loss

**Symptoms**: Some messages don't arrive

**Solutions**:
1. Increase queue size
2. Use RELIABLE QoS
3. Check network bandwidth

## Best Practices

1. **Always cleanup**: Call `destroy_node()` and `rclpy.shutdown()`
2. **Use descriptive names**: Node and topic names should be clear
3. **Log appropriately**: Use `info()`, `warn()`, `error()` correctly
4. **Handle errors**: Wrap `spin()` in try-except
5. **Document your code**: Explain what messages mean

## Summary

In this chapter, you learned:

- ✅ What nodes and topics are and why they're important
- ✅ How to create publishers and subscribers
- ✅ Message types and when to use them
- ✅ Quality of Service (QoS) profiles
- ✅ How to debug topic communication
- ✅ Best practices for ROS 2 development

## Review Questions

1. What is the difference between a node and a topic?
2. Why use the publish-subscribe pattern instead of direct function calls?
3. When would you use RELIABLE vs BEST_EFFORT QoS?
4. What happens if a publisher's queue fills up?
5. How can you check if messages are being published on a topic?

## Next Steps

In the next chapter, we'll explore **Services and Actions** for request-response and long-running task patterns.

## Further Reading

- [ROS 2 Topics Tutorial](https://docs.ros.org/en/humble/Tutorials/Topics.html)
- [rclpy API Documentation](https://docs.ros2.org/latest/api/rclpy/)
- [ROS 2 QoS Policies](https://docs.ros.org/en/humble/Concepts/About-Quality-of-Service-Settings.html)
