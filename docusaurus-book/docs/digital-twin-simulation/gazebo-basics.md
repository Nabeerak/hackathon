---
title: Gazebo Basics
sidebar_label: Gazebo Basics
sidebar_position: 2
description: Comprehensive guide to world building and robot simulation in Gazebo
keywords: [Gazebo, simulation, ROS 2, physics, world building]
---

# Gazebo Basics

Gazebo is the standard open-source robot simulator used extensively in the robotics community. As part of the Digital Twin approach, Gazebo provides accurate physics simulation, realistic sensor models, and seamless ROS 2 integration. This chapter covers setting up Gazebo, creating simulation environments, and integrating your robots with realistic sensors.

## Learning Objectives

After completing this section, you will be able to:

- **Install** and configure Gazebo with ROS 2 Humble
- **Launch** Gazebo with custom world files and robot models
- **Create** basic world files with obstacles and environments
- **Spawn** robot models in simulation with proper URDF integration
- **Configure** physics parameters for realistic simulation
- **Debug** common Gazebo issues and performance problems

## Gazebo Overview

Gazebo is a physics-based simulation environment that provides:
- **Accurate physics simulation**: ODE, Bullet, and DART physics engines
- **Realistic sensors**: Cameras, LIDAR, IMU, GPS, force/torque sensors
- **High-quality graphics**: OGRE rendering engine for visualization
- **ROS integration**: Native support for ROS 2 communication patterns
- **Realistic environments**: Complex world files with terrain and obstacles

### Key Components of Gazebo

**Gazebo Server** (`gzserver`):
- Runs simulation core
- Handles physics, rendering, and updates
- Communicates via Gazebo Transport

**Gazebo Client** (`gzclient`):
- Provides graphical user interface
- Shows simulation visualization
- Allows user interaction with simulation

## Installation and Setup

### Installing Gazebo and ROS 2 Integration

```bash
# Update package list
sudo apt update

# Install Gazebo Fortress (recommended for ROS 2 Humble)
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-gazebo-plugins
sudo apt install ros-humble-gazebo-dev

# Install Gazebo Classic (if needed)
sudo apt install ros-humble-gazebo-classic-ros-pkgs

# Install additional dependencies
sudo apt install libgazebo11-dev
sudo apt install gazebo11
```

### Verify Installation

```bash
# Check if Gazebo is installed
gazebo --version

# Launch basic Gazebo GUI
gazebo
```

## Launching Gazebo with ROS 2

### Basic Gazebo Launch

```bash
# Launch Gazebo with empty world
ros2 launch gazebo_ros gazebo.launch.py

# Launch with specific world
ros2 launch gazebo_ros gazebo.launch.py world:=/path/to/world.world

# Launch with GUI disabled (headless)
ros2 launch gazebo_ros gazebo.launch.py gui:=false
```

### Custom Launch Configuration

Create `launch/gazebo.launch.py`:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Declare arguments
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='empty.world',
        description='Choose one of the world files from `/my_package/worlds`'
    )

    # Gazebo launch configuration
    world_path = PathJoinSubstitution([
        get_package_share_directory('my_package'),
        'worlds',
        LaunchConfiguration('world')
    ])

    # Start Gazebo server
    gzserver = Node(
        package='gazebo_ros',
        executable='gzserver',
        arguments=[world_path, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
        parameters=[
            {'use_sim_time': True}
        ]
    )

    # Start Gazebo client
    gzclient = Node(
        package='gazebo_ros',
        executable='gzclient',
        parameters=[
            {'use_sim_time': True}
        ]
    )

    return LaunchDescription([
        world_arg,
        gzserver,
        gzclient
    ])
```

## World File Creation

World files define the simulation environment including terrain, obstacles, and lighting.

### Basic World Structure

Create `worlds/simple_room.world`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="simple_room">
    <!-- Include outdoor environment -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Room walls -->
    <model name="wall_1">
      <pose>0 5 0 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>10 0.1 3</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>10 0.1 3</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Add objects to the room -->
    <model name="table">
      <pose>-2 0 0 0 0 0</pose>
      <static>true</static>
      <link name="table_link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1.5 0.8 0.8</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1.5 0.8 0.8</size>
            </box>
          </geometry>
          <material>
            <ambient>0.6 0.4 0.2 1</ambient>
            <diffuse>0.6 0.4 0.2 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Physics configuration -->
    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>
  </world>
</sdf>
```

### Lighting and Environment

```xml
<!-- Add lighting configuration -->
<world name="lit_room">
  <!-- Ambient light -->
  <ambient>0.3 0.3 0.3 1</ambient>

  <!-- Background color -->
  <background>0.6 0.7 0.8 1</background>

  <!-- Custom sun light -->
  <light name="sun" type="directional">
    <pose>0 0 10 0 0 0</pose>
    <diffuse>1 1 1 1</diffuse>
    <specular>0.5 0.5 0.5 1</specular>
    <attenuation>
      <range>1000</range>
      <constant>0.9</constant>
      <linear>0.01</linear>
      <quadratic>0.001</quadratic>
    </attenuation>
    <direction>-0.4 0.2 -1</direction>
  </light>

  <!-- Additional point light -->
  <light name="room_light" type="point">
    <pose>-2 0 2 0 0 0</pose>
    <diffuse>1 0.9 0.8 1</diffuse>
    <attenuation>
      <range>10</range>
      <constant>0.2</constant>
      <linear>0.5</linear>
      <quadratic>0.01</quadratic>
    </attenuation>
  </light>
</world>
```

## Robot URDF Integration

### Complete Robot Model with Gazebo Plugins

Create `urdf/robot.urdf.xacro`:

```xml
<?xml version="1.0"?>
<robot name="simulated_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.2" length="0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.2" length="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Wheels -->
  <xacro:macro name="wheel" params="suffix parent x_reflect y_reflect">
    <joint name="${suffix}_wheel_joint" type="continuous">
      <parent link="${parent}"/>
      <child link="${suffix}_wheel"/>
      <origin xyz="${x_reflect*0.15} ${y_reflect*0.15} -0.05" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
    </joint>

    <link name="${suffix}_wheel">
      <visual>
        <geometry>
          <cylinder radius="0.05" length="0.04"/>
        </geometry>
        <material name="black">
          <color rgba="0 0 0 1"/>
        </material>
      </visual>
      <collision>
        <geometry>
          <cylinder radius="0.05" length="0.04"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="0.5"/>
        <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
      </inertial>
    </link>

    <!-- Gazebo plugin for differential drive -->
    <gazebo reference="${suffix}_wheel">
      <material>Gazebo/Black</material>
    </gazebo>
  </xacro:macro>

  <!-- Create wheels -->
  <xacro:wheel suffix="front_left" parent="base_link" x_reflect="1" y_reflect="1"/>
  <xacro:wheel suffix="front_right" parent="base_link" x_reflect="1" y_reflect="-1"/>
  <xacro:wheel suffix="rear_left" parent="base_link" x_reflect="-1" y_reflect="1"/>
  <xacro:wheel suffix="rear_right" parent="base_link" x_reflect="-1" y_reflect="-1"/>

  <!-- Gazebo plugins for ROS 2 integration -->
  <gazebo>
    <!-- Differential drive plugin -->
    <plugin filename="libgazebo_ros_diff_drive.so" name="differential_drive">
      <commandTopic>cmd_vel</commandTopic>
      <odometryTopic>odom</odometryTopic>
      <odometryFrame>odom</odometryFrame>
      <robotBaseFrame>base_link</robotBaseFrame>
      <publishOdomTF>true</publishOdomTF>
      <wheelSeparation>0.3</wheelSeparation>
      <wheelDiameter>0.1</wheelDiameter>
      <maxWheelTorque>20</maxWheelTorque>
      <maxWheelAcceleration>1.0</maxWheelAcceleration>
      <odometrySource>world</odometrySource>
    </plugin>

    <!-- Joint state publisher -->
    <plugin filename="libgazebo_ros_joint_state_publisher.so" name="joint_state">
      <jointName>front_left_wheel_joint, front_right_wheel_joint, rear_left_wheel_joint, rear_right_wheel_joint</jointName>
    </plugin>
  </gazebo>
</robot>
```

## Spawning Robots in Gazebo

### Spawn Launch File

Create `launch/spawn_robot.launch.py`:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Arguments
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='simulated_robot',
        description='Name of the robot to spawn'
    )

    x_arg = DeclareLaunchArgument(
        'x',
        default_value='0.0',
        description='Initial x position'
    )

    y_arg = DeclareLaunchArgument(
        'y',
        default_value='0.0',
        description='Initial y position'
    )

    z_arg = DeclareLaunchArgument(
        'z',
        default_value='0.1',
        description='Initial z position'
    )

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('gazebo_ros'),
            '/launch',
            '/gazebo.launch.py'
        ])
    )

    # Robot description
    robot_description = PathJoinSubstitution([
        get_package_share_directory('my_package'),
        'urdf',
        'robot.urdf.xacro'
    ])

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_description
        }]
    )

    # Spawn entity node
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', LaunchConfiguration('robot_name'),
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', LaunchConfiguration('z')
        ],
        output='screen'
    )

    return LaunchDescription([
        robot_name_arg,
        x_arg,
        y_arg,
        z_arg,
        gazebo,
        robot_state_publisher,
        spawn_entity
    ])
```

### Running the Robot Spawn

```bash
# Spawn robot at default position
ros2 launch my_package spawn_robot.launch.py

# Spawn robot at specific position
ros2 launch my_package spawn_robot.launch.py x:=2.0 y:=1.0 z:=0.1

# Spawn multiple robots
# Terminal 1
ros2 launch my_package spawn_robot.launch.py robot_name:=robot1 x:=0.0 y:=0.0
# Terminal 2
ros2 launch my_package spawn_robot.launch.py robot_name:=robot2 x:=2.0 y:=2.0
```

## Basic Robot Control in Simulation

### Simple Velocity Control Node

Create `robot_control.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class SimpleController(Node):
    """
    Simple controller to test robot in Gazebo.
    """

    def __init__(self):
        super().__init__('simple_controller')

        # Create publisher for velocity commands
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

        # Create subscriber for odometry
        self.odom_sub = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            10
        )

        # Timer for control loop
        self.timer = self.create_timer(0.1, self.control_loop)  # 10 Hz

        # Control state
        self.current_pose = None
        self.goal_x = 1.0
        self.goal_y = 1.0

        self.get_logger().info('Simple controller started')

    def odom_callback(self, msg):
        """Update current position from odometry."""
        self.current_pose = msg.pose.pose

    def control_loop(self):
        """Basic control logic to move to goal."""
        if self.current_pose is None:
            return

        # Calculate current position
        current_x = self.current_pose.position.x
        current_y = self.current_pose.position.y

        # Calculate distance to goal
        dx = self.goal_x - current_x
        dy = self.goal_y - current_y
        distance = math.sqrt(dx*dx + dy*dy)

        # Create velocity command
        cmd = Twist()

        if distance > 0.1:  # If not at goal
            # Move toward goal
            cmd.linear.x = min(0.5, distance)  # Max 0.5 m/s
            cmd.angular.z = math.atan2(dy, dx)  # Turn toward goal
        else:
            # Reached goal, stop
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        # Publish command
        self.cmd_vel_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    controller = SimpleController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Physics Configuration

### Tuning Physics Parameters

Physics parameters significantly affect simulation stability and realism:

```xml
<physics name="realistic_physics" type="ode">
  <!-- Time step - smaller = more accurate but slower -->
  <max_step_size>0.001</max_step_size>

  <!-- Real-time factor - 1.0 means real-time -->
  <real_time_factor>1.0</real_time_factor>

  <!-- Update rate - 1000 = 1000 Hz updates -->
  <real_time_update_rate>1000</real_time_update_rate>

  <ode>
    <!-- Solver iterations - more = more stable but slower -->
    <solver>
      <type>quick</type>
      <iters>100</iters>
      <sor>1.3</sor>
    </solver>

    <!-- Constraint parameters -->
    <constraints>
      <cfm>0.0</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

### Material Properties and Friction

```xml
<model name="physical_object">
  <link name="link">
    <!-- Collision properties -->
    <collision name="collision">
      <surface>
        <friction>
          <ode>
            <mu>1.0</mu>  <!-- Coefficient of friction -->
            <mu2>1.0</mu2>
          </ode>
        </friction>
        <bounce>  <!-- Bounce properties -->
          <restitution_coefficient>0.1</restitution_coefficient>
          <threshold>100000</threshold>
        </bounce>
        <contact>  <!-- Contact properties -->
          <ode>
            <soft_cfm>0.01</soft_cfm>
            <soft_erp>0.2</soft_erp>
            <max_vel>100.0</max_vel>
            <min_depth>0.001</min_depth>
          </ode>
        </contact>
      </surface>
    </collision>
  </link>
</model>
```

## Gazebo GUI and Visualization

### Using the Gazebo Client

Gazebo offers several visualization and interaction features:

1. **World View**: 3D visualization of the simulation
2. **Model Insert**: Add pre-built models from Gazebo database
3. **Layer Controls**: Toggle visualization layers
4. **Time Control**: Play, pause, step through simulation

### Common GUI Interactions

- **Right-click and drag**: Orbit camera
- **Middle-click and drag**: Pan camera
- **Scroll wheel**: Zoom in/out
- **Ctrl+click**: Select objects
- **Shift+click**: Multi-select

## Advanced Gazebo Features

### Custom Sensors

Add custom sensors to your robot using Gazebo plugins:

```xml
<sensor name="custom_camera" type="camera">
  <camera>
    <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees in radians -->
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>10.0</far>
    </clip>
  </camera>
  <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
    <frame_name>camera_link</frame_name>
    <topic_name>camera/image_raw</topic_name>
    <camera_info_topic_name>camera/camera_info</camera_info_topic_name>
  </plugin>
</sensor>
```

### Joint Control

Control joints with Gazebo plugins:

```xml
<plugin name="joint_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
  <robot_param>robot_description</robot_param>
  <joint_name>joint1, joint2, joint3</joint_name>
  <update_rate>30</update_rate>
</plugin>

<plugin name="joint_trajectory_controller" filename="libgazebo_ros_joint_trajectory.so">
  <command_topic>joint_trajectory</command_topic>
  <state_topic>joint_states</state_topic>
</plugin>
```

## Troubleshooting Common Gazebo Issues

### Physics Instability
**Symptoms**: Robot shaking, unrealistic movements, simulation crashes
**Solutions**:
```bash
# Reduce time step in world file
<max_step_size>0.001</max_step_size>

# Increase solver iterations
<iters>1000</iters>

# Add damping to joints
<damping>0.1</damping>
```

### Robot Fall-through
**Symptoms**: Robot falls through ground plane
**Solutions**:
- Check mass and inertia values in URDF
- Verify collision geometry definition
- Adjust physics parameters (time step, solver)

### Performance Issues
**Symptoms**: Slow simulation, high CPU usage
**Solutions**:
```bash
# Increase time step for faster simulation
<max_step_size>0.01</max_step_size>

# Reduce solver iterations
<iters>50</iters>

# Use simpler collision geometry
```

## Integration with ROS 2 Ecosystem

### TF Integration
Make sure your robot publishes proper transforms:

```xml
<!-- In URDF -->
<ros2_control name="GazeboSystem" type="system">
  <hardware>
    <plugin>gazebo_ros2_control/GazeboSystem</plugin>
  </hardware>
  <joint name="joint1">
    <command_interface name="position"/>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
</ros2_control>
```

### Sensor Integration
Connect Gazebo sensors to ROS 2 topics:

```xml
<!-- Camera plugin -->
<plugin name="camera" filename="libgazebo_ros_camera.so">
  <remapping>~/image_raw:=/camera/image_raw</remapping>
  <remapping>~/camera_info:=/camera/camera_info</remapping>
</plugin>
```

## Best Practices

### Model Optimization
1. **Use simple collision meshes**: Simplify geometry for collision detection
2. **Optimize visual meshes**: Use detailed models only for visualization
3. **Use realistic inertia values**: Use realistic mass and inertia properties
4. **Test physics stability**: Verify models don't exhibit unstable behavior

### World Design
1. **Start simple**: Begin with basic environments
2. **Add complexity gradually**: Introduce elements one by one
3. **Use existing models**: Leverage Gazebo model database
4. **Validate physics**: Test that objects behave realistically

## Summary

Gazebo provides a robust foundation for Digital Twin simulation in Physical AI development. With proper setup and configuration, you can create realistic simulation environments where you can test algorithms safely and rapidly. The integration with ROS 2 enables seamless simulation and real-robot development workflows.

In the next sections, you'll learn about more advanced topics including Unity simulation, sensor integration, and physics tuning for realistic behavior.

## Further Reading

- [Gazebo Classic Documentation](http://classic.gazebosim.org/)
- [Gazebo Fortress/Edifice Documentation](https://gazebosim.org/docs)
- [ROS 2 Gazebo Tutorials](https://classic.gazebosim.org/tutorials?cat=connect_ros)
- [URDF and Gazebo Integration Guide](http://gazebosim.org/tutorials/?tut=ros2_overview)
