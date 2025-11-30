#!/usr/bin/env python3
"""
Expand Physical AI textbook with comprehensive educational content.
This creates REAL textbook material with depth, examples, and exercises.
"""

import os

BASE_DIR = "docusaurus-book/docs/physical-ai-textbook"

# Comprehensive educational content for all pages
COMPREHENSIVE_CONTENT = {
    # ===== ROS 2 FUNDAMENTALS - Full expansion =====
    "ros2-fundamentals/nodes-topics.md": """---
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
    \"\"\"
    A publisher node that sends velocity commands to a robot.
    Demonstrates timer-based publishing and proper node structure.
    \"\"\"

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
        \"\"\"
        Called every 0.5 seconds by the timer.
        Publishes velocity commands to make robot drive in circles.
        \"\"\"
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
    \"\"\"
    A subscriber node that receives velocity commands.
    Demonstrates callback handling and message processing.
    \"\"\"

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
        \"\"\"
        Called automatically when a message is received.

        Args:
            msg: Twist message containing velocity commands
        \"\"\"
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
""",

    # More ROS 2 content...
    "ros2-fundamentals/services-actions.md": """---
title: Services and Actions
sidebar_label: Services and Actions
sidebar_position: 4
description: Request-response and goal-based communication in ROS 2
keywords: [ROS 2, services, actions, request, response, goals]
---

# Services and Actions

## Introduction

While topics are great for continuous data streams, many robotic tasks require different communication patterns:

- **Services**: Request-response pattern (like asking "What's the battery level?" and getting an answer)
- **Actions**: Long-running tasks with feedback (like "Navigate to location X" with progress updates)

This chapter covers both patterns with practical examples.

## Services: Request-Response Communication

### When to Use Services

Use services when you need:
- ✅ A response to a request
- ✅ Synchronous communication
- ✅ One-to-one interactions
- ❌ NOT for high-frequency data (use topics)
- ❌ NOT for long-running tasks (use actions)

### Creating a Service Server

Let's create a service that adds two integers:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntsServer(Node):
    \"\"\"
    Service server that adds two integers.
    Demonstrates request handling and response generation.
    \"\"\"

    def __init__(self):
        super().__init__('add_two_ints_server')

        # Create service
        self.srv = self.create_service(
            AddTwoInts,              # Service type
            'add_two_ints',          # Service name
            self.handle_add_request  # Callback function
        )

        self.get_logger().info('Add Two Ints service is ready')

    def handle_add_request(self, request, response):
        \"\"\"
        Called when client sends request.

        Args:
            request: Contains request.a and request.b
            response: Object to fill with result

        Returns:
            response: Filled response object
        \"\"\"
        # Perform the addition
        response.sum = request.a + request.b

        # Log the operation
        self.get_logger().info(
            f'Incoming request: {request.a} + {request.b} = {response.sum}'
        )

        return response

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServer()

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

### Creating a Service Client

Now let's create a client to use this service:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import sys

class AddTwoIntsClient(Node):
    \"\"\"
    Service client that requests addition of two integers.
    \"\"\"

    def __init__(self):
        super().__init__('add_two_ints_client')

        # Create client
        self.client = self.create_client(
            AddTwoInts,
            'add_two_ints'
        )

        # Wait for service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

    def send_request(self, a, b):
        \"\"\"
        Send request to add two numbers.

        Args:
            a: First integer
            b: Second integer

        Returns:
            Future object that will contain response
        \"\"\"
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        # Call service asynchronously
        future = self.client.call_async(request)
        return future

def main(args=None):
    rclpy.init(args=args)

    # Get numbers from command line
    if len(sys.argv) != 3:
        print('Usage: python3 client.py <int> <int>')
        return

    a = int(sys.argv[1])
    b = int(sys.argv[2])

    # Create client and send request
    client_node = AddTwoIntsClient()
    future = client_node.send_request(a, b)

    # Wait for response
    rclpy.spin_until_future_complete(client_node, future)

    if future.result() is not None:
        response = future.result()
        client_node.get_logger().info(
            f'Result: {a} + {b} = {response.sum}'
        )
    else:
        client_node.get_logger().error('Service call failed')

    client_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Running the Service

**Terminal 1: Start Server**
```bash
python3 add_server.py
```

**Terminal 2: Call Service**
```bash
python3 add_client.py 5 7
# Output: Result: 5 + 7 = 12

# Using CLI
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 7}"
```

## Actions: Long-Running Tasks with Feedback

### When to Use Actions

Use actions for:
- ✅ Tasks that take time (navigation, manipulation)
- ✅ Need progress feedback
- ✅ Can be preempted/cancelled
- ✅ May succeed or fail

### Action Architecture

An action has three components:

1. **Goal**: What you want to achieve
2. **Feedback**: Progress updates
3. **Result**: Final outcome

### Example: Fibonacci Action Server

```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci
import time

class FibonacciActionServer(Node):
    \"\"\"
    Action server that computes Fibonacci sequence.
    Demonstrates goal handling, feedback, and results.
    \"\"\"

    def __init__(self):
        super().__init__('fibonacci_action_server')

        # Create action server
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

        self.get_logger().info('Fibonacci action server started')

    def execute_callback(self, goal_handle):
        \"\"\"
        Execute the Fibonacci goal.

        Args:
            goal_handle: Handle to goal execution

        Returns:
            result: Final Fibonacci sequence
        \"\"\"
        self.get_logger().info('Executing Fibonacci goal...')

        # Get requested order from goal
        order = goal_handle.request.order

        # Initialize sequence
        sequence = [0, 1]

        # Compute Fibonacci with feedback
        for i in range(1, order):
            # Check if goal was cancelled
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal cancelled')
                return Fibonacci.Result()

            # Compute next number
            sequence.append(sequence[i] + sequence[i-1])

            # Publish feedback
            feedback = Fibonacci.Feedback()
            feedback.partial_sequence = sequence
            goal_handle.publish_feedback(feedback)

            self.get_logger().info(f'Progress: {sequence}')

            # Simulate computation time
            time.sleep(0.5)

        # Mark goal as succeeded
        goal_handle.succeed()

        # Create result
        result = Fibonacci.Result()
        result.sequence = sequence

        return result

def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()

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

### Fibonacci Action Client

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionClient(Node):
    \"\"\"
    Action client that requests Fibonacci computation.
    \"\"\"

    def __init__(self):
        super().__init__('fibonacci_action_client')

        # Create action client
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )

    def send_goal(self, order):
        \"\"\"
        Send Fibonacci goal.

        Args:
            order: Number of Fibonacci numbers to compute
        \"\"\"
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        # Create goal
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info(f'Sending goal: order={order}')

        # Send goal and register callbacks
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        \"\"\"
        Called when feedback is received.
        \"\"\"
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Feedback: {feedback.partial_sequence}'
        )

    def goal_response_callback(self, future):
        \"\"\"
        Called when goal is accepted or rejected.
        \"\"\"
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        # Get result
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        \"\"\"
        Called when final result is received.
        \"\"\"
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')

        # Shutdown after getting result
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)

    client_node = FibonacciActionClient()
    client_node.send_goal(10)  # Compute first 10 Fibonacci numbers

    rclpy.spin(client_node)

if __name__ == '__main__':
    main()
```

### Running the Action

**Terminal 1: Start Server**
```bash
python3 fibonacci_server.py
```

**Terminal 2: Send Goal**
```bash
python3 fibonacci_client.py
# Output shows feedback and final result

# Using CLI
ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 10}" --feedback
```

## Practical Example: Robot Battery Service

Let's create a realistic service for checking robot battery:

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from std_msgs.msg import Float32

class BatteryService(Node):
    \"\"\"
    Service that reports robot battery status.
    Realistic example for robot systems.
    \"\"\"

    def __init__(self):
        super().__init__('battery_service')

        # Service to check battery
        self.srv = self.create_service(
            Trigger,
            'check_battery',
            self.check_battery_callback
        )

        # Subscribe to battery level topic
        self.battery_sub = self.create_subscription(
            Float32,
            '/battery_level',
            self.battery_callback,
            10
        )

        self.current_battery = 100.0  # Start at 100%
        self.low_battery_threshold = 20.0

        self.get_logger().info('Battery service ready')

    def battery_callback(self, msg):
        \"\"\"Update current battery level.\"\"\"
        self.current_battery = msg.data

    def check_battery_callback(self, request, response):
        \"\"\"
        Handle battery check request.

        Returns:
            response: success=True if battery OK, message with details
        \"\"\"
        if self.current_battery > self.low_battery_threshold:
            response.success = True
            response.message = (
                f'Battery OK: {self.current_battery:.1f}% remaining'
            )
        else:
            response.success = False
            response.message = (
                f'LOW BATTERY: {self.current_battery:.1f}% remaining. '
                f'Please charge soon!'
            )

        self.get_logger().info(f'Battery check: {response.message}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = BatteryService()
    rclpy.spin(node)
```

## Debugging Services and Actions

### Inspect Services

```bash
# List all services
ros2 service list

# Show service type
ros2 service type /add_two_ints

# Call service from CLI
ros2 service call /check_battery std_srvs/srv/Trigger
```

### Inspect Actions

```bash
# List all actions
ros2 action list

# Show action info
ros2 action info /fibonacci

# Send action goal
ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 5}" --feedback
```

## Common Patterns

### Pattern 1: Service with Validation

```python
def handle_request(self, request, response):
    # Validate input
    if request.value < 0:
        response.success = False
        response.message = "Value must be non-negative"
        return response

    # Process valid request
    response.success = True
    response.result = process(request.value)
    return response
```

### Pattern 2: Action with Cancellation

```python
def execute_callback(self, goal_handle):
    for i in range(100):
        # Check for cancellation
        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            return Result()

        # Do work...
        time.sleep(0.1)

    goal_handle.succeed()
    return Result()
```

## Summary

Key takeaways:

- ✅ **Services**: Use for request-response (battery check, calculations)
- ✅ **Actions**: Use for long tasks with feedback (navigation, manipulation)
- ✅ Services are synchronous, actions are asynchronous
- ✅ Actions can be cancelled, services cannot
- ✅ Use CLI tools for debugging

## Review Questions

1. When would you use a service instead of a topic?
2. What are the three components of an action?
3. How do you cancel an action goal?
4. What's the difference between synchronous and asynchronous calls?
5. Why would feedback be important for a navigation action?

## Next Steps

Next chapter: **Parameters and Launch Files** for configuring complex robot systems.
""",
}

# Write expanded content
total = 0
for filepath, content in COMPREHENSIVE_CONTENT.items():
    full_path = os.path.join(BASE_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    total += 1
    print(f"[{total}] Expanded {filepath}")

print(f"\n==> Expanded {total} pages with comprehensive content!")
print("Next: Continue expanding remaining chapters...")
