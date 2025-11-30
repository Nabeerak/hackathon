---
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
ros2 launch turtlebot3_navigation2 navigation2.launch.py   use_sim_time:=True   map:=$HOME/my_map.yaml
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
    """
    Client for sending navigation goals programmatically.
    """

    def __init__(self):
        super().__init__('navigation_client')

        # Create navigator
        self.navigator = BasicNavigator()

        # Wait for Nav2 to be ready
        self.navigator.waitUntilNav2Active()

        self.get_logger().info('Navigation system ready!')

    def create_pose(self, x, y, yaw):
        """
        Create a PoseStamped message.

        Args:
            x: X position in meters
            y: Y position in meters
            yaw: Orientation in radians

        Returns:
            PoseStamped message
        """
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
        """
        Navigate to a goal pose.

        Args:
            x, y, yaw: Goal position and orientation
        """
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
        """
        Navigate through multiple waypoints.

        Args:
            waypoints: List of (x, y, yaw) tuples
        """
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
        """Continuously patrol waypoints."""
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
