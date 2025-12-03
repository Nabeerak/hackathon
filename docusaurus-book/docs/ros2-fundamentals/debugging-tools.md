---
title: Debugging Tools
sidebar_label: Debugging Tools
sidebar_position: 7
description: Comprehensive guide to ros2 CLI, rqt, and rviz2 for troubleshooting
keywords: [ROS 2, debugging, tools, CLI, rqt, rviz2, visualization]
---

# Debugging Tools

Debugging is an essential skill for ROS 2 development. This chapter covers the comprehensive set of tools available for troubleshooting, visualizing, and analyzing your ROS 2 systems. Effective debugging will save you countless hours and help you identify issues quickly.

## Learning Objectives

After completing this section, you will be able to:

- **Use** ROS 2 command-line tools for system analysis and debugging
- **Visualize** robot data using RViz2 with various display types
- **Monitor** system performance and message flows with RQt tools
- **Diagnose** common ROS 2 system issues using appropriate tools
- **Debug** complex multi-node systems effectively

## Command Line Interface (CLI) Tools

The ROS 2 command-line interface provides powerful tools for system inspection and debugging. These tools are essential for understanding your robot's state without additional GUI dependencies.

### Node Inspection

**List All Nodes**
```bash
# List all active nodes
ros2 node list

# Show nodes with namespaces
ros2 node list --include-hidden-nodes

# Get detailed information about a specific node
ros2 node info /robot_controller
```

**Example Output**:
```
/robot_controller
  Subscribers:
    /cmd_vel: geometry_msgs/msg/Twist
    /tf: tf2_msgs/msg/TFMessage
  Publishers:
    /odom: nav_msgs/msg/Odometry
    /robot_description: std_msgs/msg/String
  Services:
    /robot_controller/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
```

### Topic Inspection and Monitoring

**List All Topics**
```bash
# List all topics with message types
ros2 topic list -t

# List topics for specific node
ros2 topic list --node /robot_controller
```

**Monitor Topic Data**
```bash
# Echo messages on a topic
ros2 topic echo /cmd_vel geometry_msgs/msg/Twist

# Echo with specific frequency
ros2 topic echo /camera/image_raw --field data --times 10

# Echo with rate limiting (0.5 Hz)
ros2 topic echo /imu/data --rate 0.5

# Show only headers
ros2 topic echo /laser_scan --field header
```

**Topic Performance**
```bash
# Check message frequency
ros2 topic hz /camera/image_raw

# Check message delay
ros2 topic delay /imu/data

# Check topic bandwidth
ros2 topic bw /pointcloud
```

### Service Debugging

**List Services**
```bash
# List all services
ros2 service list

# List services with types
ros2 service list -t

# List services for specific node
ros2 service list --node /robot_controller
```

**Call Services**
```bash
# Call a service with arguments
ros2 service call /set_mode std_srvs/srv/SetBool "{data: true}"

# Call with complex message
ros2 service call /navigate_to_pose nav2_msgs/srv/NavigateToPose "{pose: {pose: {position: {x: 1.0, y: 2.0, z: 0.0}, orientation: {w: 1.0}}, header: {frame_id: 'map'}}}"
```

### Action Inspection

**List Actions**
```bash
# List all actions
ros2 action list

# List actions with types
ros2 action list -t
```

**Send Action Goals**
```bash
# Send goal with feedback
ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 10}" --feedback

# Send goal and wait for result
ros2 action send_goal /navigate_fibonacci example_interfaces/action/Fibonacci "{order: 5}"
```

### Parameter Debugging

**List Parameters**
```bash
# List all parameters for a node
ros2 param list /robot_controller

# Get specific parameter value
ros2 param get /robot_controller max_speed

# Set parameter at runtime
ros2 param set /robot_controller max_speed 2.0

# Dump all parameters to file
ros2 param dump /robot_controller
```

### Lifecycle Node Management

**Check Lifecycle States**
```bash
# Get lifecycle state
ros2 lifecycle list /lifecycle_node

# Change lifecycle state
ros2 lifecycle set /lifecycle_node configure
ros2 lifecycle set /lifecycle_node activate
```

## RQt: Qt-based Debugging Suite

RQt provides a comprehensive set of GUI tools for ROS 2 debugging and analysis. These tools offer visual interfaces for complex debugging tasks.

### RQt Graph

Visualize the ROS 2 communication graph showing nodes, topics, and connections.

```bash
# Launch RQt graph
ros2 run rqt_graph rqt_graph

# Launch with specific settings
ros2 run rqt_graph rqt_graph --on-top --fixed-size 800 600
```

**Features**:
- Visual representation of nodes and topics
- Color-coded connections (publishers/subscribers)
- Node grouping and filtering
- Topic type visualization

### RQt Console

Monitor ROS 2 log messages in real-time with filtering capabilities.

```bash
# Launch console
ros2 run rqt_console rqt_console

# Launch with log level filtering
ros2 run rqt_console rqt_console --default-level INFO
```

**Features**:
- Real-time log message display
- Log level filtering (DEBUG, INFO, WARN, ERROR, FATAL)
- Message search and filtering
- Message saving and replay
- Custom message formatting

### RQt Plot

Plot numeric data from ROS 2 topics in real-time graphs.

```bash
# Launch plotter
ros2 run rqt_plot rqt_plot

# Plot specific topics
# In the GUI: add topics like /odom/twist/twist/linear/x
```

**Features**:
- Real-time plotting of numeric data
- Multiple series on same graph
- Customizable display styles
- Data export capabilities
- Overlay multiple datasets

### RQt Topic Monitor

Monitor all topics and their message rates simultaneously.

```bash
# Launch topic monitor
ros2 run rqt_topic rqt_topic
```

**Features**:
- Real-time topic statistics
- Message rate monitoring
- Topic type inspection
- Quick access to echo commands

### Custom RQt Plugins

RQt supports custom plugins for specialized debugging needs:

```python
# Example custom RQt plugin structure
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from python_qt_binding.QtWidgets import QWidget
import rclpy
from rqt_gui_py.plugin import Plugin

class CustomDebugWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.button = QPushButton("Debug Action")
        self.button.clicked.connect(self.on_button_click)

        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def on_button_click(self):
        print("Debug button clicked!")

class CustomDebugPlugin(Plugin):
    def __init__(self, context):
        super().__init__(context)
        self.setObjectName('CustomDebugPlugin')

        self.widget = CustomDebugWidget()
        context.add_widget(self.widget)

    def shutdown_plugin(self):
        pass
```

## RViz2: 3D Visualization Tool

RViz2 is the primary visualization tool for ROS 2, allowing you to visualize robot models, sensor data, and planning results in 3D.

### Launching RViz2

```bash
# Basic launch
ros2 run rviz2 rviz2

# Launch with configuration file
ros2 run rviz2 rviz2 -d /path/to/config.rviz

# Launch with specific display options
ros2 run rviz2 rviz2 --force-discover
```

### Essential RViz2 Displays

#### Robot Model Display

Visualize your robot's URDF model:

1. **Add Display**: `RobotModel`
2. **Topic**: `/robot_description`
3. **Visual Enabled**: Check for visual elements
4. **Collision Enabled**: Check for collision elements

#### Laser Scan Display

Visualize LIDAR data:

1. **Add Display**: `LaserScan`
2. **Topic**: `/scan` or `/laser_scan`
3. **Style**: Points, Flat Squares, or Spheres
4. **Size**: Point size in meters

#### Point Cloud Display

Visualize 3D sensor data:

1. **Add Display**: `PointCloud2`
2. **Topic**: `/pointcloud`, `/camera/depth/points`
3. **Color Transformer**: RGB, Intensity, Axis-based
4. **Style**: Points, Spheres, Boxes

#### Map Display

Visualize occupancy grids:

1. **Add Display**: `Map`
2. **Topic**: `/map`, `/local_costmap/costmap`, `/global_costmap/costmap`
3. **Resolution**: Auto or manual
4. **Color Scheme**: map, costmap, raw

#### Odometry Display

Visualize robot pose and trajectory:

1. **Add Display**: `Odometry`
2. **Topic**: `/odom`, `/ground_truth`
3. **Shape**: Arrow, Axes, or None
4. **Trail**: Enable for path following

#### TF Display

Visualize coordinate frame relationships:

1. **Add Display**: `TF`
2. **Show Arrows**: Visualize frame orientation
3. **Show Axes**: Show coordinate system
4. **Show Names**: Display frame names

### RViz2 Configuration

Save and load configurations to reproduce visualization setups:

```bash
# Save current configuration
# File -> Save Config As -> my_config.rviz

# Load configuration
ros2 run rviz2 rviz2 -d my_config.rviz
```

### Advanced RViz2 Usage

**Custom Displays**:
```yaml
# Example RViz configuration snippet
Visualization Manager:
  Class: ""
  Displays:
    - Class: rviz_default_plugins/RobotModel
      Name: Robot Model
      Enabled: true
      Topic: /robot_description
    - Class: rviz_default_plugins/LaserScan
      Name: Laser Scan
      Enabled: true
      Topic: /scan
      Size (m): 0.05
```

**Coordinate Frame Setup**:
- **Fixed Frame**: Usually `map` or `odom` for navigation
- **Target Frame**: Usually `base_link` for the robot
- **Transforms**: Ensure TF tree is complete and connected

## Performance Analysis Tools

### ROS 2 Doctor

Diagnose system issues and configuration problems:

```bash
# Basic system check
ros2 doctor

# Verbose output
ros2 doctor --report

# Check specific checks
ros2 doctor --include list,topic
```

### Process Monitor

Monitor resource usage of ROS 2 nodes:

```bash
# Monitor system resources
htop

# Monitor specific ROS 2 processes
pidstat -u -p $(pgrep -f ros2)

# Monitor network usage
iftop -i lo  # for localhost communication
```

### Memory Profiling

Track memory usage of your ROS 2 applications:

```bash
# Track memory usage over time
watch -n 1 'ps aux | grep ros'

# Use Valgrind for detailed memory debugging
valgrind --tool=memcheck --leak-check=full ros2 run my_package my_node
```

## Debugging Strategies

### Top-Down Approach

1. **System Level**: Use CLI tools to identify which nodes are running
2. **Communication Level**: Check topic connections and message flows
3. **Component Level**: Use RQt to inspect individual node behavior
4. **Code Level**: Use GDB/IDE debugging for specific issues

### Common Debugging Scenarios

#### No Communication Between Nodes

**Symptoms**: Publishers not reaching subscribers, empty topic messages

**Debugging Steps**:
```bash
# 1. Check if nodes are running
ros2 node list

# 2. Check topic connections
ros2 topic info /topic_name

# 3. Verify message type compatibility
ros2 topic type /topic_name

# 4. Check QoS compatibility
ros2 topic info /topic_name
```

#### Robot Not Moving

**Symptoms**: Robot stays still despite velocity commands

**Debugging Steps**:
```bash
# 1. Check if velocity commands are being published
ros2 topic echo /cmd_vel

# 2. Check if the driver node is running
ros2 node list | grep driver

# 3. Check if the robot is enabled
ros2 param get /robot_driver enabled

# 4. Check for safety stops
ros2 service call /robot_driver/emergency_stop std_srvs/srv/Trigger
```

#### Navigation Fails

**Symptoms**: Robot doesn't reach goal or gets stuck

**Debugging Steps**:
```bash
# 1. Check if localization is working (AMCL)
ros2 topic echo /amcl_pose

# 2. Check costmaps
ros2 topic echo /global_costmap/costmap
ros2 topic echo /local_costmap/costmap

# 3. Check path planning
ros2 topic echo /plan

# 4. Check local controller
ros2 topic echo /cmd_vel
```

## Integration with Development Environment

### IDE Integration

Most ROS 2 IDEs (VS Code, Eclipse, etc.) integrate debugging tools:

**VS Code Launch Configuration**:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "ROS2 Debug Node",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/install/my_package/lib/my_package/my_node",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```

### Logging Best Practices

**Log Levels**:
- **DEBUG**: Detailed information for debugging
- **INFO**: General information about normal operation
- **WARN**: Potential issues that aren't errors
- **ERROR**: Problems that prevent normal operation
- **FATAL**: Critical errors that cause node shutdown

**Example Logging Code**:
```python
def timer_callback(self):
    try:
        # Process sensor data
        sensor_data = self.get_sensor_data()

        # Log at appropriate level
        if sensor_data is None:
            self.get_logger().warn('No sensor data available')
        elif sensor_data.range < 0.5:
            self.get_logger().info(f'Obstacle detected: {sensor_data.range:.2f}m')
        else:
            self.get_logger().debug(f'Sensor data OK: {sensor_data.range:.2f}m')

    except Exception as e:
        self.get_logger().error(f'Sensor processing failed: {e}')
```

## Troubleshooting Examples

### Example 1: Debugging a Navigation System

```bash
# 1. Check overall system status
ros2 node list
ros2 topic list

# 2. Check navigation-specific topics
ros2 topic echo /goal_pose
ros2 topic echo /navigate_to_pose/_action/send_goal
ros2 topic echo /cmd_vel

# 3. Check navigation parameters
ros2 param list /controller_server
ros2 param list /planner_server

# 4. Visualize with RViz2
ros2 run rviz2 rviz2 -d nav2_default_view.rviz
```

### Example 2: Debugging Sensor Integration

```bash
# 1. Check sensor node status
ros2 node info /camera_node
ros2 node info /lidar_node

# 2. Monitor sensor data
ros2 topic echo /camera/image_raw --field header.stamp
ros2 topic hz /lidar/points

# 3. Visualize in RViz2
ros2 run rviz2 rviz2
# Add displays for camera and laser scan
```

## Best Practices for Effective Debugging

### 1. Systematic Approach
- Start with the simplest possible test
- Isolate issues by eliminating variables
- Document your debugging process
- Keep a hypothesis log

### 2. Use Appropriate Tools
- CLI for quick status checks
- RQt for detailed node analysis
- RViz2 for spatial data visualization
- Custom tools for specific use cases

### 3. Logging Strategy
- Log important events and state changes
- Use appropriate log levels
- Avoid excessive logging in production
- Include timestamps and node names

### 4. Version Control for Configurations
- Store RViz configurations in version control
- Document parameter changes
- Keep backup configurations
- Use launch files for reproducible setups

## Performance Considerations

### Tool Overhead
- RViz2 can consume significant resources
- Continuous logging impacts performance
- Monitor tool resource usage
- Disable tools during performance testing

### Network Impact
- Remote debugging adds network overhead
- Large message visualization may cause lag
- Consider message throttling for debugging
- Use compressed messages when possible

## Summary

Debugging tools are essential for effective ROS 2 development. The combination of CLI tools, RQt applications, and RViz2 provides comprehensive debugging capabilities:

- **CLI Tools**: Essential for system inspection and quick checks
- **RQt**: Powerful GUI tools for analysis and monitoring
- **RViz2**: Critical for spatial data visualization
- **Performance Tools**: Important for profiling and optimization

Mastering these tools will significantly improve your ability to develop, test, and maintain complex ROS 2 systems. Remember to use the right tool for each debugging situation and maintain good logging practices in your code.

## Further Reading

- [ROS 2 CLI Tools Documentation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
- [RQt User Guide](http://wiki.ros.org/rqt)
- [RViz2 User Documentation](http://wiki.ros.org/rviz)
- [ROS 2 Performance Analysis](https://docs.ros.org/en/humble/How-To-Guides/Performance-tuning.html)
