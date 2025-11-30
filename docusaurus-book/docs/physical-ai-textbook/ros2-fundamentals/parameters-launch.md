---
title: Parameters and Launch Files
sidebar_label: Parameters and Launch Files
sidebar_position: 5
description: Configuration and multi-node startup in ROS 2
keywords: [ROS 2, parameters, launch files, configuration]
---

# Parameters and Launch Files

## Introduction

Real robot systems have many configurable settings and multiple nodes that need to start together. ROS 2 provides:

- **Parameters**: Runtime configuration for nodes
- **Launch files**: Automated multi-node startup and configuration

This chapter shows how to build flexible, configurable robot systems.

## Understanding Parameters

Parameters allow you to change node behavior without modifying code. Common uses:

- Robot dimensions and physical properties
- Sensor configurations (camera resolution, update rates)
- Algorithm tuning (PID gains, thresholds)
- Feature toggles (enable/disable debugging)

### Declaring Parameters

```python
import rclpy
from rclpy.node import Node

class ConfigurableRobot(Node):
    """
    Robot node with configurable parameters.
    Demonstrates parameter declaration and usage.
    """

    def __init__(self):
        super().__init__('configurable_robot')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'MyRobot')
        self.declare_parameter('max_speed', 1.0)
        self.declare_parameter('wheel_radius', 0.05)
        self.declare_parameter('enable_safety', True)
        self.declare_parameter('update_rate', 10.0)

        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.max_speed = self.get_parameter('max_speed').value
        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.safety_enabled = self.get_parameter('enable_safety').value
        update_rate = self.get_parameter('update_rate').value

        # Use parameters
        self.get_logger().info(f'Robot Name: {self.robot_name}')
        self.get_logger().info(f'Max Speed: {self.max_speed} m/s')
        self.get_logger().info(f'Wheel Radius: {self.wheel_radius} m')
        self.get_logger().info(f'Safety: {"ON" if self.safety_enabled else "OFF"}')

        # Create timer based on parameter
        timer_period = 1.0 / update_rate
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        """Use parameters in control logic."""
        # Compute wheel velocity from max speed
        linear_vel = self.max_speed if not self.safety_enabled else self.max_speed * 0.5
        wheel_angular_vel = linear_vel / self.wheel_radius

        self.get_logger().info(
            f'{self.robot_name}: wheel_vel={wheel_angular_vel:.2f} rad/s'
        )

def main(args=None):
    rclpy.init(args=args)
    node = ConfigurableRobot()
    rclpy.spin(node)
```

### Setting Parameters from Command Line

```bash
# Set parameters when launching node
ros2 run my_package configurable_robot --ros-args   -p robot_name:=TestBot   -p max_speed:=2.0   -p enable_safety:=false
```

### Setting Parameters at Runtime

```bash
# Get parameter value
ros2 param get /configurable_robot max_speed

# Set parameter value
ros2 param set /configurable_robot max_speed 1.5

# List all parameters
ros2 param list

# Dump all parameters
ros2 param dump /configurable_robot
```

### Parameter Callbacks

Respond to parameter changes at runtime:

```python
from rcl_interfaces.msg import ParameterDescriptor, SetParametersResult

class DynamicRobot(Node):
    def __init__(self):
        super().__init__('dynamic_robot')

        # Declare parameter with descriptor
        descriptor = ParameterDescriptor(
            description='Maximum robot velocity in m/s',
            read_only=False
        )

        self.declare_parameter('max_speed', 1.0, descriptor)

        # Add callback for parameter changes
        self.add_on_set_parameters_callback(self.parameters_callback)

    def parameters_callback(self, params):
        """
        Called when parameters are changed.

        Args:
            params: List of changed parameters

        Returns:
            SetParametersResult indicating success/failure
        """
        result = SetParametersResult(successful=True)

        for param in params:
            if param.name == 'max_speed':
                if param.value < 0 or param.value > 5.0:
                    result.successful = False
                    result.reason = 'max_speed must be between 0 and 5.0 m/s'
                else:
                    self.get_logger().info(
                        f'max_speed updated to {param.value} m/s'
                    )

        return result
```

## Parameter Files (YAML)

Store parameters in YAML files for easy configuration:

### robot_config.yaml

```yaml
# Robot configuration parameters
/configurable_robot:
  ros__parameters:
    robot_name: "ProductionBot"
    max_speed: 1.5
    wheel_radius: 0.06
    enable_safety: true
    update_rate: 20.0

    # Sensor configuration
    camera:
      resolution_width: 640
      resolution_height: 480
      fps: 30

    # PID gains
    pid:
      kp: 1.0
      ki: 0.1
      kd: 0.05
```

### Loading Parameter Files

```bash
# Load from YAML file
ros2 run my_package configurable_robot --ros-args   --params-file ./robot_config.yaml
```

### Nested Parameters in Code

```python
class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')

        # Declare nested camera parameters
        self.declare_parameter('camera.resolution_width', 640)
        self.declare_parameter('camera.resolution_height', 480)
        self.declare_parameter('camera.fps', 30)

        # Access nested parameters
        width = self.get_parameter('camera.resolution_width').value
        height = self.get_parameter('camera.resolution_height').value
        fps = self.get_parameter('camera.fps').value

        self.get_logger().info(f'Camera: {width}x{height} @ {fps} fps')
```

## Launch Files

Launch files automate starting multiple nodes with proper configuration.

### Python Launch Files

Create `robot_launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """
    Launch multiple robot nodes with configuration.
    """
    return LaunchDescription([
        # Camera node
        Node(
            package='camera_driver',
            executable='camera_node',
            name='front_camera',
            parameters=[{
                'resolution_width': 1280,
                'resolution_height': 720,
                'fps': 30,
                'device_id': 0
            }],
            remappings=[
                ('/image', '/camera/image_raw')
            ]
        ),

        # Robot controller
        Node(
            package='robot_control',
            executable='controller_node',
            name='robot_controller',
            parameters=[{
                'max_speed': 1.5,
                'wheel_radius': 0.06
            }],
            output='screen'  # Show logs in terminal
        ),

        # Navigation node
        Node(
            package='navigation',
            executable='nav_node',
            name='navigator',
            parameters=['config/nav_params.yaml']
        )
    ])
```

### Running Launch Files

```bash
# Run launch file
ros2 launch my_package robot_launch.py

# With arguments
ros2 launch my_package robot_launch.py robot_name:=TestBot
```

### Launch File with Arguments

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='DefaultBot',
        description='Name of the robot'
    )

    max_speed_arg = DeclareLaunchArgument(
        'max_speed',
        default_value='1.0',
        description='Maximum robot speed in m/s'
    )

    # Use launch arguments in nodes
    robot_node = Node(
        package='robot_control',
        executable='controller_node',
        name=LaunchConfiguration('robot_name'),
        parameters=[{
            'max_speed': LaunchConfiguration('max_speed')
        }]
    )

    return LaunchDescription([
        robot_name_arg,
        max_speed_arg,
        robot_node
    ])
```

### Including Other Launch Files

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get path to other launch file
    sensors_launch = os.path.join(
        get_package_share_directory('sensor_package'),
        'launch',
        'sensors_launch.py'
    )

    return LaunchDescription([
        # Include sensor launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sensors_launch),
            launch_arguments={
                'camera_enabled': 'true',
                'lidar_enabled': 'true'
            }.items()
        ),

        # Add more nodes
        Node(
            package='my_package',
            executable='my_node'
        )
    ])
```

## Practical Example: Multi-Robot System

Complete launch system for a mobile robot:

### multi_robot_launch.py

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace

def generate_launch_description():
    # Arguments
    robot_name_arg = DeclareLaunchArgument('robot_name', default_value='robot1')
    use_sim_arg = DeclareLaunchArgument('use_sim', default_value='false')

    robot_name = LaunchConfiguration('robot_name')
    use_sim = LaunchConfiguration('use_sim')

    # Group nodes under namespace
    robot_group = GroupAction([
        PushRosNamespace(robot_name),

        # Sensors
        Node(
            package='sensor_drivers',
            executable='lidar_node',
            name='lidar',
            parameters=[{'frame_id': 'lidar_link'}]
        ),

        Node(
            package='sensor_drivers',
            executable='imu_node',
            name='imu',
            parameters=[{'update_rate': 100.0}]
        ),

        # Controllers
        Node(
            package='robot_control',
            executable='base_controller',
            name='base_controller',
            parameters=['config/robot_params.yaml']
        ),

        # Localization
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_localization',
            parameters=['config/ekf_params.yaml']
        )
    ])

    return LaunchDescription([
        robot_name_arg,
        use_sim_arg,
        robot_group
    ])
```

### Running Multiple Robots

```bash
# Start robot 1
ros2 launch my_package multi_robot_launch.py robot_name:=robot1

# Start robot 2 (different terminal)
ros2 launch my_package multi_robot_launch.py robot_name:=robot2
```

## Conditional Launch

Launch nodes based on conditions:

```python
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_camera_arg = DeclareLaunchArgument('use_camera', default_value='true')

    # Only launch if use_camera is true
    camera_node = Node(
        package='camera_driver',
        executable='camera_node',
        condition=IfCondition(LaunchConfiguration('use_camera'))
    )

    # Launch if use_camera is false
    virtual_camera = Node(
        package='sim_camera',
        executable='virtual_camera_node',
        condition=UnlessCondition(LaunchConfiguration('use_camera'))
    )

    return LaunchDescription([
        use_camera_arg,
        camera_node,
        virtual_camera
    ])
```

## Event Handlers

React to node lifecycle events:

```python
from launch.actions import RegisterEventHandler, LogInfo
from launch.event_handlers import OnProcessStart, OnProcessExit

def generate_launch_description():
    talker_node = Node(
        package='demo_nodes_py',
        executable='talker'
    )

    # Handler for when node starts
    start_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=talker_node,
            on_start=[
                LogInfo(msg='Talker node has started!')
            ]
        )
    )

    # Handler for when node exits
    exit_handler = RegisterEventHandler(
        OnProcessExit(
            target_action=talker_node,
            on_exit=[
                LogInfo(msg='Talker node has exited!')
            ]
        )
    )

    return LaunchDescription([
        talker_node,
        start_handler,
        exit_handler
    ])
```

## Best Practices

### Parameters

1. ✅ Provide sensible defaults
2. ✅ Validate parameter values
3. ✅ Document parameters in YAML files
4. ✅ Use descriptive parameter names
5. ❌ Don't hardcode values that might change

### Launch Files

1. ✅ Use launch arguments for flexibility
2. ✅ Group related nodes
3. ✅ Use parameter files for complex config
4. ✅ Include proper namespacing
5. ✅ Handle both simulation and real robot

## Debugging

### Check Parameters

```bash
# List all nodes
ros2 node list

# Get all parameters for a node
ros2 param list /robot_controller

# Get parameter value
ros2 param get /robot_controller max_speed

# Set parameter
ros2 param set /robot_controller max_speed 2.0
```

### Debug Launch Files

```bash
# See what launch file will do (dry run)
ros2 launch --show-args my_package robot_launch.py

# Launch with debug output
ros2 launch --debug my_package robot_launch.py
```

## Summary

You learned:

- ✅ How to declare and use parameters
- ✅ Parameter validation with callbacks
- ✅ YAML configuration files
- ✅ Python launch files
- ✅ Launch arguments and conditions
- ✅ Multi-robot systems
- ✅ Event handlers

## Review Questions

1. What's the difference between declaring a parameter with a default vs without?
2. When should you use a parameter callback?
3. How do you launch multiple nodes with one command?
4. What's the purpose of namespacing in multi-robot systems?
5. How can you make a launch file work for both simulation and real robots?

## Next Steps

Next chapter: **Navigation Stack** - putting it all together for autonomous robot navigation.
