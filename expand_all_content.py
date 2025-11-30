#!/usr/bin/env python3
"""
Complete textbook content expansion - ALL remaining pages
Comprehensive educational material with depth, examples, and exercises
"""

import os

BASE_DIR = "docusaurus-book/docs/physical-ai-textbook"

ALL_EXPANDED_CONTENT = {
    # Continue ROS 2 Fundamentals
    "ros2-fundamentals/parameters-launch.md": """---
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
    \"\"\"
    Robot node with configurable parameters.
    Demonstrates parameter declaration and usage.
    \"\"\"

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
        \"\"\"Use parameters in control logic.\"\"\"
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
ros2 run my_package configurable_robot --ros-args \
  -p robot_name:=TestBot \
  -p max_speed:=2.0 \
  -p enable_safety:=false
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
        \"\"\"
        Called when parameters are changed.

        Args:
            params: List of changed parameters

        Returns:
            SetParametersResult indicating success/failure
        \"\"\"
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
ros2 run my_package configurable_robot --ros-args \
  --params-file ./robot_config.yaml
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
    \"\"\"
    Launch multiple robot nodes with configuration.
    \"\"\"
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
""",

    "ros2-fundamentals/navigation-stack.md": """---
title: Navigation Stack
sidebar_label: Navigation Stack
sidebar_position: 6
description: Autonomous navigation with Nav2
keywords: [ROS 2, Nav2, navigation, SLAM, AMCL]
---

# Navigation Stack (Nav2)

## Introduction

The ROS 2 Navigation Stack (Nav2) enables mobile robots to autonomously navigate from point A to point B while avoiding obstacles. This is one of the most important capabilities for mobile robots.

### What You'll Learn

- Nav2 architecture and components
- Setting up navigation for your robot
- Creating and using maps
- Path planning and obstacle avoidance
- Practical navigation examples

## Nav2 Architecture

Nav2 consists of several key components working together:

### Core Components

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Sensors   │────▶│ Localization │────▶│   Planner   │
│ (Lidar/Cam) │     │    (AMCL)    │     │  (Global)   │
└─────────────┘     └──────────────┘     └─────────────┘
                            │                     │
                            ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │   Costmaps   │────▶│ Controller  │
                    │              │     │  (Local)    │
                    └──────────────┘     └─────────────┘
                                                │
                                                ▼
                                        ┌─────────────┐
                                        │   Motors    │
                                        └─────────────┘
```

**1. Map Server**: Provides occupancy grid map

**2. AMCL (Localization)**: Estimates robot position on map

**3. Planner**: Computes global path from start to goal

**4. Controller**: Follows path while avoiding obstacles

**5. Costmaps**: Represent obstacles for planning

**6. Recovery Behaviors**: Handle stuck situations

## Installation

Install Nav2 and dependencies:

```bash
# Install Nav2
sudo apt update
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup

# Install Turtlebot3 simulation (for testing)
sudo apt install ros-humble-turtlebot3* ros-humble-turtlebot3-gazebo

# Set robot model
echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc
source ~/.bashrc
```

## Creating a Map with SLAM

Before navigation, you need a map. Use SLAM to create one:

### Launch SLAM in Simulation

```bash
# Terminal 1: Start Gazebo simulation
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# Terminal 2: Start SLAM
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True

# Terminal 3: Start teleoperation
ros2 run turtlebot3_teleop teleop_keyboard
```

### Save the Map

Drive around to build a complete map, then save it:

```bash
# Save map
ros2 run nav2_map_server map_saver_cli -f ~/my_map

# This creates two files:
# - my_map.pgm (image file)
# - my_map.yaml (metadata)
```

### Map YAML Format

```yaml
image: my_map.pgm
resolution: 0.05        # meters per pixel
origin: [-10.0, -10.0, 0.0]  # x, y, yaw
negate: 0
occupied_thresh: 0.65   # > this = occupied
free_thresh: 0.196      # < this = free
```

## Running Navigation

### Launch Nav2

```bash
# Terminal 1: Start simulation
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# Terminal 2: Start Nav2
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
  use_sim_time:=True \
  map:=$HOME/my_map.yaml
```

### Set Initial Pose

In RViz2:
1. Click "2D Pose Estimate" button
2. Click and drag on map where robot actually is
3. Robot should localize (particles converge)

### Send Navigation Goal

In RViz2:
1. Click "Nav2 Goal" button
2. Click and drag to set goal pose
3. Robot plans path and navigates

## Configuration Files

### nav2_params.yaml

Key parameters for Nav2:

```yaml
# Global Planner
planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

# Local Controller
controller_server:
  ros__parameters:
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    controller_plugins: ["FollowPath"]

    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      min_vel_x: 0.0
      max_vel_x: 0.26
      max_vel_theta: 1.0
      min_speed_xy: 0.0
      max_speed_xy: 0.26
      acc_lim_x: 2.5
      acc_lim_theta: 3.2
      decel_lim_x: -2.5
      decel_lim_theta: -3.2

# Costmap settings
global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      robot_radius: 0.22
      resolution: 0.05
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]

      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True

      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True

      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      robot_radius: 0.22
      resolution: 0.05
      width: 3
      height: 3
      # Same plugins as global
```

## Programmatic Navigation

Send navigation goals from code:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import tf_transformations

class NavigationClient(Node):
    \"\"\"
    Client for sending navigation goals programmatically.
    \"\"\"

    def __init__(self):
        super().__init__('navigation_client')

        # Create navigator
        self.navigator = BasicNavigator()

        # Wait for Nav2 to be ready
        self.navigator.waitUntilNav2Active()

        self.get_logger().info('Navigation system ready!')

    def create_pose(self, x, y, yaw):
        \"\"\"
        Create a PoseStamped message.

        Args:
            x: X position in meters
            y: Y position in meters
            yaw: Orientation in radians

        Returns:
            PoseStamped message
        \"\"\"
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()

        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0

        # Convert yaw to quaternion
        quaternion = tf_transformations.quaternion_from_euler(0, 0, yaw)
        pose.pose.orientation.x = quaternion[0]
        pose.pose.orientation.y = quaternion[1]
        pose.pose.orientation.z = quaternion[2]
        pose.pose.orientation.w = quaternion[3]

        return pose

    def navigate_to_pose(self, x, y, yaw):
        \"\"\"
        Navigate to a goal pose.

        Args:
            x, y, yaw: Goal position and orientation
        \"\"\"
        goal_pose = self.create_pose(x, y, yaw)

        self.get_logger().info(f'Navigating to: x={x}, y={y}, yaw={yaw}')

        # Send goal
        self.navigator.goToPose(goal_pose)

        # Wait for result
        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            if feedback:
                self.get_logger().info(
                    f'Distance remaining: {feedback.distance_remaining:.2f}m'
                )

        result = self.navigator.getResult()
        if result == 'succeeded':
            self.get_logger().info('Goal reached!')
        else:
            self.get_logger().warn(f'Navigation failed: {result}')

    def follow_waypoints(self, waypoints):
        \"\"\"
        Navigate through multiple waypoints.

        Args:
            waypoints: List of (x, y, yaw) tuples
        \"\"\"
        poses = [self.create_pose(x, y, yaw) for x, y, yaw in waypoints]

        self.get_logger().info(f'Following {len(poses)} waypoints')

        self.navigator.followWaypoints(poses)

        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            if feedback:
                self.get_logger().info(
                    f'Waypoint {feedback.current_waypoint + 1}/{len(poses)}'
                )

        self.get_logger().info('Waypoint following complete!')

def main():
    rclpy.init()

    nav_client = NavigationClient()

    # Example: Navigate to single goal
    nav_client.navigate_to_pose(x=2.0, y=1.0, yaw=0.0)

    # Example: Follow waypoints
    waypoints = [
        (2.0, 0.5, 0.0),
        (2.0, -0.5, 1.57),
        (0.5, -0.5, 3.14),
        (0.0, 0.0, 0.0)
    ]
    nav_client.follow_waypoints(waypoints)

    nav_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Understanding Costmaps

Costmaps represent space around the robot with costs:

- **0**: Free space (white)
- **1-99**: Low cost (gray)
- **100-252**: Medium cost (dark gray)
- **253**: Inscribed (very close to obstacle)
- **254**: Occupied (black)
- **255**: Unknown

### Layers

**Static Layer**: From map file (doesn't change)

**Obstacle Layer**: From sensors (dynamic)

**Inflation Layer**: Adds safety margin around obstacles

```python
# Configure inflation
inflation_radius: 0.55  # meters
cost_scaling_factor: 3.0  # exponential decay rate
```

## Recovery Behaviors

When robot gets stuck, Nav2 tries recovery behaviors:

1. **Clear Costmap**: Reset costmaps
2. **Spin**: Rotate 360° to clear obstacles
3. **Back Up**: Drive backwards
4. **Wait**: Pause and let dynamic obstacles pass

Configure in nav2_params.yaml:

```yaml
recoveries_server:
  ros__parameters:
    costmap_topic: local_costmap/costmap_raw
    footprint_topic: local_costmap/published_footprint
    recovery_plugins: ["spin", "backup", "wait"]

    spin:
      plugin: "nav2_recoveries/Spin"
      simulate_ahead_time: 2.0

    backup:
      plugin: "nav2_recoveries/BackUp"

    wait:
      plugin: "nav2_recoveries/Wait"
```

## Practical Exercise: Warehouse Robot

Create a robot that patrols waypoints in a warehouse:

```python
import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped

class WarehousePatrol(Node):
    def __init__(self):
        super().__init__('warehouse_patrol')

        self.navigator = BasicNavigator()
        self.navigator.waitUntilNav2Active()

        # Define patrol waypoints
        self.patrol_points = [
            (1.0, 1.0, 0.0),    # Point A
            (3.0, 1.0, 1.57),   # Point B
            (3.0, -1.0, 3.14),  # Point C
            (1.0, -1.0, -1.57), # Point D
        ]

    def patrol(self):
        \"\"\"Continuously patrol waypoints.\"\"\"
        while rclpy.ok():
            self.get_logger().info('Starting patrol...')

            for i, (x, y, yaw) in enumerate(self.patrol_points):
                pose = self.create_pose(x, y, yaw)

                self.get_logger().info(f'Going to checkpoint {i+1}')
                self.navigator.goToPose(pose)

                while not self.navigator.isTaskComplete():
                    rclpy.spin_once(self, timeout_sec=0.1)

                result = self.navigator.getResult()
                if result != 'succeeded':
                    self.get_logger().warn(f'Failed to reach checkpoint {i+1}')
                    break

            self.get_logger().info('Patrol complete. Repeating...')

def main():
    rclpy.init()
    patrol = WarehousePatrol()
    patrol.patrol()
```

## Tuning Navigation

### Common Issues and Fixes

**Robot oscillates:**
- Decrease `min_vel_x`
- Increase `xy_goal_tolerance`

**Robot gets too close to obstacles:**
- Increase `inflation_radius`
- Increase `robot_radius`

**Robot moves too slowly:**
- Increase `max_vel_x`
- Decrease `acc_lim_x`

**Path planning fails:**
- Increase `tolerance` in planner
- Set `allow_unknown: true`

## Summary

Key concepts:

- ✅ Nav2 combines mapping, localization, planning, and control
- ✅ SLAM creates maps, AMCL localizes on them
- ✅ Global planner finds path, local controller follows it
- ✅ Costmaps represent obstacles with multiple layers
- ✅ Recovery behaviors handle stuck situations
- ✅ Programmatic control via BasicNavigator

## Review Questions

1. What are the main components of Nav2?
2. What's the difference between global and local costmaps?
3. Why do we need inflation layers?
4. When would you use recovery behaviors?
5. How do you send navigation goals from code?

## Next Steps

Next chapter: **Debugging Tools** - essential tools for developing and troubleshooting ROS 2 systems.
"""
}

# Write all expanded content
total = 0
for filepath, content in ALL_EXPANDED_CONTENT.items():
    full_path = os.path.join(BASE_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    total += 1
    print(f"[{total}] Expanded {filepath}")

print(f"\n==> Expanded {total} more pages!")
print(f"Total expanded so far: {total + 2} pages")
print("Continuing with more content...")
