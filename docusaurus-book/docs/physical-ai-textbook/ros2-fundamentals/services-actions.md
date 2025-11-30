---
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
    """
    Service server that adds two integers.
    Demonstrates request handling and response generation.
    """

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
        """
        Called when client sends request.

        Args:
            request: Contains request.a and request.b
            response: Object to fill with result

        Returns:
            response: Filled response object
        """
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
    """
    Service client that requests addition of two integers.
    """

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
        """
        Send request to add two numbers.

        Args:
            a: First integer
            b: Second integer

        Returns:
            Future object that will contain response
        """
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
    """
    Action server that computes Fibonacci sequence.
    Demonstrates goal handling, feedback, and results.
    """

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
        """
        Execute the Fibonacci goal.

        Args:
            goal_handle: Handle to goal execution

        Returns:
            result: Final Fibonacci sequence
        """
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
    """
    Action client that requests Fibonacci computation.
    """

    def __init__(self):
        super().__init__('fibonacci_action_client')

        # Create action client
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )

    def send_goal(self, order):
        """
        Send Fibonacci goal.

        Args:
            order: Number of Fibonacci numbers to compute
        """
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
        """
        Called when feedback is received.
        """
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Feedback: {feedback.partial_sequence}'
        )

    def goal_response_callback(self, future):
        """
        Called when goal is accepted or rejected.
        """
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        # Get result
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """
        Called when final result is received.
        """
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
    """
    Service that reports robot battery status.
    Realistic example for robot systems.
    """

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
        """Update current battery level."""
        self.current_battery = msg.data

    def check_battery_callback(self, request, response):
        """
        Handle battery check request.

        Returns:
            response: success=True if battery OK, message with details
        """
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
