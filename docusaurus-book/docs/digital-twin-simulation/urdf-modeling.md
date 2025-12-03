---
title: URDF Robot Modeling
sidebar_label: URDF Robot Modeling
sidebar_position: 4
description: Comprehensive guide to creating robot descriptions with URDF/Xacro
keywords: [URDF, robot modeling, Xacro, kinematics, dynamics]
---

# URDF Robot Modeling

URDF (Unified Robot Description Format) is the standard for describing robot models in ROS and robotics applications. It defines the physical and kinematic properties of robots, enabling accurate simulation, visualization, and control. Xacro, an XML macro language, extends URDF with parameterization, reusability, and cleaner organization.

## Learning Objectives

After completing this section, you will be able to:

- **Create** complete robot models with proper kinematic chains and joint definitions
- **Define** visual, collision, and inertial properties for accurate simulation
- **Use** Xacro macros and properties for reusable and parameterized robot models
- **Integrate** sensors and actuators into robot descriptions
- **Validate** robot models for simulation and real-world applications
- **Optimize** URDF models for performance in Gazebo and other simulators

## URDF Fundamentals

### What is URDF?

URDF (Unified Robot Description Format) is an XML-based format that describes robots in terms of:
- **Links**: Rigid bodies with visual and collision properties
- **Joints**: Constraints between links with kinematic parameters
- **Materials**: Visual appearance properties
- **Transmissions**: Hardware interface mappings
- **Gazebo plugins**: Simulator-specific configurations

### Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Links define rigid bodies -->
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
      <inertia ixx="0.4" ixy="0" ixz="0" iyy="0.4" iyz="0" izz="0.2"/>
    </inertial>
  </link>

  <!-- Joints define connections between links -->
  <joint name="wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0.1 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.04"/>
      </geometry>
    </visual>
  </link>
</robot>
```

## Link Elements

Links represent rigid bodies in the robot and contain three main components:

### Visual Elements

Describe how the link appears in visualization and simulation:

```xml
<link name="visual_example">
  <visual>
    <!-- Origin: position and orientation relative to joint -->
    <origin xyz="0 0 0" rpy="0 0 0"/>

    <!-- Geometry: shape of the visual element -->
    <geometry>
      <!-- Box geometry -->
      <box size="0.1 0.2 0.3"/>

      <!-- Cylinder geometry -->
      <!-- <cylinder radius="0.1" length="0.2"/> -->

      <!-- Sphere geometry -->
      <!-- <sphere radius="0.1"/> -->

      <!-- Mesh geometry -->
      <!-- <mesh filename="package://my_robot/meshes/visual.dae" scale="1 1 1"/> -->
    </geometry>

    <!-- Material: appearance properties -->
    <material name="red">
      <color rgba="1 0 0 1"/>
      <!-- Optional: texture -->
      <!-- <texture filename="package://my_robot/materials/texture.png"/> -->
    </material>
  </visual>
</link>
```

### Collision Elements

Define collision properties for physics simulation:

```xml
<link name="collision_example">
  <collision>
    <!-- Origin (same as visual) -->
    <origin xyz="0 0 0" rpy="0 0 0"/>

    <!-- Geometry (usually simpler than visual) -->
    <geometry>
      <cylinder radius="0.1" length="0.1"/>
    </geometry>
  </collision>
</link>
```

Key considerations for collision geometry:
- Use simpler shapes than visual geometry for better performance
- Consider convex decomposition for complex shapes
- Align collision and visual origins carefully

### Inertial Elements

Define mass properties for physics simulation:

```xml
<link name="inertial_example">
  <inertial>
    <!-- Mass in kilograms -->
    <mass value="1.0"/>

    <!-- Inertia matrix -->
    <inertia
      ixx="0.1" ixy="0" ixz="0"
      iyy="0.1" iyz="0"
      izz="0.1"/>
  </inertial>
</link>
```

**Calculating Inertia Values**:

For common shapes:
- **Box**: `ixx = 1/12 * m * (h² + d²)`, `iyy = 1/12 * m * (w² + d²)`, `izz = 1/12 * m * (w² + h²)`
- **Cylinder**: `ixx = 1/12 * m * (3*r² + h²)`, `izz = 1/2 * m * r²`
- **Sphere**: `ixx = iyy = izz = 2/5 * m * r²`

Where:
- `m`: mass
- `w`: width, `h`: height, `d`: depth
- `r`: radius, `h`: height

## Joint Elements

Joints define the relationship between links and can be of several types:

### Joint Types

1. **Fixed**: No degrees of freedom (0 DOF)
2. **Continuous**: Revolute joint without limits (1 DOF)
3. **Revolute**: Limited revolute joint (1 DOF)
4. **Prismatic**: Linear sliding joint (1 DOF)
5. **Floating**: 6 DOF (rarely used)
6. **Planar**: 3 DOF (2 translational, 1 rotational)

### Joint Definition Example

```xml
<joint name="example_joint" type="revolute">
  <!-- Parent link: the link closer to the base -->
  <parent link="base_link"/>

  <!-- Child link: the link further from the base -->
  <child link="arm_link"/>

  <!-- Joint origin: position of joint relative to parent -->
  <origin xyz="0.1 0 0.05" rpy="0 0 0"/>

  <!-- Joint axis: rotation axis in child link frame -->
  <axis xyz="0 0 1"/>

  <!-- Joint limits (for revolute joints) -->
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>

  <!-- Joint safety limits -->
  <safety_controller k_position="20" k_velocity="400" soft_lower_limit="-1.5" soft_upper_limit="1.5"/>
</joint>
```

## Material Definitions

Define reusable materials for visual elements:

```xml
<!-- Define materials at the robot level -->
<material name="blue">
  <color rgba="0 0 1 1"/>
</material>

<material name="red">
  <color rgba="1 0 0 1"/>
</material>

<material name="black">
  <color rgba="0 0 0 1"/>
</material>

<material name="white">
  <color rgba="1 1 1 1"/>
</material>
```

## Complete Robot Example

Here's a complete differential drive robot model:

```xml
<?xml version="1.0"?>
<robot name="diff_drive_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Robot properties -->
  <xacro:property name="base_width" value="0.3"/>
  <xacro:property name="base_length" value="0.4"/>
  <xacro:property name="base_height" value="0.1"/>
  <xacro:property name="wheel_radius" value="0.05"/>
  <xacro:property name="wheel_width" value="0.04"/>
  <xacro:property name="wheel_offset_x" value="0.15"/>
  <xacro:property name="wheel_offset_y" value="0.15"/>
  <xacro:property name="mass_base" value="10"/>
  <xacro:property name="mass_wheel" value="0.5"/>

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 ${base_height/2}" rpy="0 0 0"/>
      <geometry>
        <box size="${base_length} ${base_width} ${base_height}"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 0.8"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 ${base_height/2}" rpy="0 0 0"/>
      <geometry>
        <box size="${base_length} ${base_width} ${base_height}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="${mass_base}"/>
      <origin xyz="0 0 ${base_height/2}" rpy="0 0 0"/>
      <inertia
        ixx="${mass_base/12 * (base_width*base_width + base_height*base_height)}"
        ixy="0" ixz="0"
        iyy="${mass_base/12 * (base_length*base_length + base_height*base_height)}"
        iyz="0"
        izz="${mass_base/12 * (base_length*base_length + base_width*base_width)}"/>
    </inertial>
  </link>

  <!-- Wheel macro -->
  <xacro:macro name="wheel" params="prefix reflect_x reflect_y">
    <link name="${prefix}_wheel">
      <visual>
        <origin xyz="0 0 0" rpy="${pi/2} 0 0"/>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
        <material name="black">
          <color rgba="0 0 0 1"/>
        </material>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="${pi/2} 0 0"/>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="${mass_wheel}"/>
        <inertia
          ixx="${mass_wheel/12 * (3*wheel_radius*wheel_radius + wheel_width*wheel_width)}"
          ixy="0" ixz="0"
          iyy="${mass_wheel/12 * (3*wheel_radius*wheel_radius + wheel_width*wheel_width)}"
          iyz="0"
          izz="${mass_wheel/2 * wheel_radius*wheel_radius}"/>
      </inertial>
    </link>

    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="base_link"/>
      <child link="${prefix}_wheel"/>
      <origin xyz="${reflect_x*wheel_offset_x} ${reflect_y*wheel_offset_y} 0" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
    </joint>
  </xacro:macro>

  <!-- Create wheels -->
  <xacro:wheel prefix="front_left" reflect_x="1" reflect_y="1"/>
  <xacro:wheel prefix="front_right" reflect_x="1" reflect_y="-1"/>
  <xacro:wheel prefix="rear_left" reflect_x="-1" reflect_y="1"/>
  <xacro:wheel prefix="rear_right" reflect_x="-1" reflect_y="-1"/>

  <!-- IMU sensor -->
  <link name="imu_link">
    <visual>
      <geometry>
        <box size="0.02 0.02 0.02"/>
      </geometry>
      <material name="red">
        <color rgba="1 0 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="imu_joint" type="fixed">
    <parent link="base_link"/>
    <child link="imu_link"/>
    <origin xyz="0 0 ${base_height*0.75}" rpy="0 0 0"/>
  </joint>
</robot>
```

## Xacro: XML Macros for URDF

Xacro (XML Macros) extends URDF with features like:
- Property definitions
- Macros
- Mathematical expressions
- File inclusion

### Xacro Properties and Math

```xml
<!-- Define properties -->
<xacro:property name="pi" value="3.1415926535897931"/>
<xacro:property name="wheel_separation" value="0.3"/>
<xacro:property name="wheel_radius" value="0.05"/>

<!-- Use mathematical expressions -->
<origin xyz="${wheel_separation/2} 0 ${wheel_radius}" rpy="0 0 0"/>
```

### Xacro Macros

```xml
<!-- Define a macro for repeated elements -->
<xacro:macro name="caster_wheel" params="prefix *origin">
  <link name="${prefix}_caster_wheel">
    <visual>
      <geometry>
        <sphere radius="0.02"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.02"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" iyy="0.001" izz="0.001" ixy="0" ixz="0" iyz="0"/>
    </inertial>
  </link>

  <joint name="${prefix}_caster_joint" type="fixed">
    <parent link="base_link"/>
    <child link="${prefix}_caster_wheel"/>
    <xacro:insert_block name="origin"/>
  </joint>
</xacro:macro>

<!-- Use the macro -->
<xacro:caster_wheel prefix="front">
  <origin xyz="0.15 0 -0.03" rpy="0 0 0"/>
</xacro:caster_wheel>

<xacro:caster_wheel prefix="rear">
  <origin xyz="-0.15 0 -0.03" rpy="0 0 0"/>
</xacro:caster_wheel>
```

### File Inclusion

```xml
<!-- Include other xacro files -->
<xacro:include filename="$(find my_robot_description)/urdf/materials.xacro"/>
<xacro:include filename="$(find my_robot_description)/urdf/transmissions.xacro"/>
<xacro:include filename="$(find my_robot_description)/urdf/gazebo.xacro"/>
```

## Advanced URDF Features

### Transmissions

Define how ROS controllers interface with robot hardware:

```xml
<transmission name="front_left_wheel_trans">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="front_left_wheel_joint">
    <hardwareInterface>hardware_interface/VelocityJointInterface</hardwareInterface>
  </joint>
  <actuator name="front_left_wheel_motor">
    <hardwareInterface>hardware_interface/VelocityJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### Gazebo Integration

Add Gazebo-specific plugins and visual properties:

```xml
<!-- Gazebo material -->
<gazebo reference="base_link">
  <material>Gazebo/Blue</material>
</gazebo>

<!-- Gazebo plugins -->
<gazebo>
  <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
    <leftJoint>front_left_wheel_joint</leftJoint>
    <rightJoint>front_right_wheel_joint</rightJoint>
    <wheelSeparation>0.3</wheelSeparation>
    <wheelDiameter>0.1</wheelDiameter>
    <commandTopic>cmd_vel</commandTopic>
    <odometryTopic>odom</odometryTopic>
    <odometryFrame>odom</odometryFrame>
    <robotBaseFrame>base_link</robotBaseFrame>
  </plugin>
</gazebo>
```

### Sensors

Define sensors with Gazebo plugins:

```xml
<link name="camera_link">
  <visual>
    <geometry>
      <box size="0.05 0.05 0.05"/>
    </geometry>
  </visual>
</link>

<joint name="camera_joint" type="fixed">
  <parent link="base_link"/>
  <child link="camera_link"/>
  <origin xyz="0.2 0 0.1" rpy="0 0 0"/>
</joint>

<gazebo reference="camera_link">
  <sensor type="camera" name="camera1">
    <update_rate>30.0</update_rate>
    <camera name="head_camera">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>800</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_link</frame_name>
      <topic_name>camera/image_raw</topic_name>
    </plugin>
  </sensor>
</gazebo>
```

## Kinematic Chain Verification

### Checking for Errors

Use these tools to verify your URDF:

```bash
# Check URDF syntax
check_urdf my_robot.urdf

# Check joint limits and kinematics
ros2 run joint_state_publisher joint_state_publisher --ros-args --remap robot_description:=/path/to/robot.urdf

# Visualize in RViz
ros2 run rviz2 rviz2
```

### Common Errors

1. **Missing parent links**: Ensure all joint parent links exist
2. **Non-physical inertias**: Verify inertia values are positive and realistic
3. **Kinematic loops**: Avoid closed kinematic chains without proper handling
4. **Unreasonable joint limits**: Set realistic position and velocity limits

## URDF Best Practices

### Organization

1. **Use Xacro**: Makes complex robots manageable
2. **Separate files**: Split large robots into functional components
3. **Standard directories**: Use `urdf/`, `meshes/`, `materials/` organization
4. **Naming conventions**: Use consistent, descriptive names

### Performance

1. **Simple collision geometry**: Use boxes and cylinders for collision
2. **Efficient meshes**: Optimize mesh complexity for visual elements
3. **Appropriate mass properties**: Use realistic values for physics simulation
4. **Minimal joints**: Only include necessary joints for function

### Simulation Accuracy

1. **Realistic inertias**: Calculate or measure actual inertia values
2. **Proper scaling**: Ensure all dimensions are correct
3. **Material properties**: Include friction and damping where relevant
4. **Sensor placement**: Position sensors accurately for simulation

## Troubleshooting Common Issues

### Visualization Issues

**Problem**: Robot appears broken or floating parts
**Solution**:
- Check joint origins and child/parent relationships
- Verify that links are properly connected in kinematic chain
- Use `robot_state_publisher` with fake joint values to visualize

**Check with:**
```bash
# Publish static TF for visualization
ros2 run robot_state_publisher robot_state_publisher --ros-args -p use_sim_time:=false
```

### Physics Simulation Issues

**Problem**: Robot falls apart or behaves unrealistically
**Solution**:
- Verify mass and inertia values are realistic
- Check that all connections are properly defined
- Ensure joint limits and effort values are appropriate
- Verify collision geometry is properly defined

### Kinematic Issues

**Problem**: Inverse kinematics fails or robot has unexpected behavior
**Solution**:
- Verify degrees of freedom match intended motion
- Check that joint types align with intended function
- Ensure joint limits allow for intended range of motion

## Integration with Simulators

### Gazebo Specific Considerations

```xml
<!-- Gazebo physics parameters -->
<gazebo reference="base_link">
  <mu1>0.2</mu1>           <!-- Friction coefficient -->
  <mu2>0.2</mu2>           <!-- Secondary friction coefficient -->
  <kp>1000000.0</kp>       <!-- Contact stiffness -->
  <kd>100.0</kd>           <!-- Contact damping -->
  <max_vel>10.0</max_vel>  <!-- Maximum contact penetration velocity -->
  <min_depth>0.001</min_depth>  <!-- Minimum contact penetration depth -->
</gazebo>
```

### ROS 2 Integration

Ensure proper integration with ROS 2 control and navigation:

```xml
<!-- Proper frame naming for TF -->
<link name="base_link"/>  <!-- Robot base coordinate frame -->

<!-- Include joint state publisher -->
<gazebo>
  <plugin name="joint_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
    <update_rate>30</update_rate>
    <joint_name>joint1, joint2, joint3</joint_name>
  </plugin>
</gazebo>
```

## Validation and Testing

### URDF Validation Tools

```bash
# Basic URDF check
check_urdf robot.urdf

# Visualize kinematic structure
urdf_to_graphviz robot.urdf
# This creates urdf_file.dot which can be viewed with graphviz tools

# Check with robot state publisher
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:=$(cat robot.urdf)
```

### Simulation Testing

```bash
# Launch in Gazebo
ros2 launch gazebo_ros gazebo.launch.py
ros2 run gazebo_ros spawn_entity.py -file robot.urdf -entity robot_name

# Test joint limits and control
ros2 topic pub /joint_states sensor_msgs/msg/JointState "..."
```

## Summary

URDF modeling is fundamental to robotics development, providing the foundation for simulation, visualization, and real robot control. Using Xacro extensions, you can create reusable, parameterized robot descriptions that scale from simple mobile robots to complex manipulator systems.

Proper URDF modeling involves attention to physical accuracy, simulation performance, and maintainability. Well-crafted robot models enable effective testing of algorithms in simulation before deployment to real hardware, supporting the Digital Twin approach essential to Physical AI development.

## Further Reading

- [URDF/XML Format Documentation](http://wiki.ros.org/urdf/XML)
- [Xacro Tutorial](http://wiki.ros.org/xacro)
- [Robot State Publisher](http://wiki.ros.org/robot_state_publisher)
- [Gazebo Robot Simulation](http://gazebosim.org/tutorials?tut=ros2_overview)
- [ROS 2 Robot Modeling Tutorials](https://docs.ros.org/en/humble/Tutorials/Advanced/URDF/)
