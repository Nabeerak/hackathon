---
title: Unity Simulation
sidebar_label: Unity Simulation
sidebar_position: 3
description: Comprehensive guide to real-time physics with Unity-ROS 2 integration
keywords: [Unity, simulation, ROS 2, real-time, photorealistic]
---

# Unity Simulation

Unity is a powerful game engine that provides high-fidelity, real-time robotics simulation with photorealistic graphics capabilities. As part of the Digital Twin ecosystem, Unity offers real-time rendering, advanced physics simulation, and seamless integration with ROS 2 through the Unity Robotics Hub. This approach is particularly valuable for visual perception training, human-robot interaction studies, and VR applications.

## Learning Objectives

After completing this section, you will be able to:

- **Install** and configure Unity with the Robotics Hub and ROS 2 integration
- **Create** photorealistic simulation environments with Unity's rendering pipeline
- **Integrate** robots using URDF Importer and ROS 2 TCP connector
- **Implement** realistic sensor models including cameras, LIDAR, and IMU
- **Optimize** Unity scenes for real-time performance
- **Generate** synthetic data for computer vision and perception training
- **Deploy** Unity simulations to various platforms

## Unity Robotics Ecosystem

Unity provides a comprehensive set of tools specifically designed for robotics applications:

### Unity Robotics Hub
- **URDF Importer**: Convert ROS 2 URDF files to Unity-compatible models
- **ROS-TCP-Connector**: Communication between Unity and ROS 2 nodes
- **Robotics Simulation Framework**: Physics, sensors, and control systems
- **Synthetic Data Generation**: Photorealistic data for AI training

### Key Features
- **Real-time Rendering**: Physically-based rendering for photorealistic simulation
- **Advanced Physics**: NVIDIA PhysX integration for accurate physics simulation
- **Flexible Asset Pipeline**: Import from CAD software and 3D modeling tools
- **Cross-platform Deployment**: Build for various hardware platforms
- **VR/AR Support**: Immersive simulation environments

## Installation and Setup

### Prerequisites

Before installing Unity robotics tools, ensure you have:

- **Unity Hub**: Latest version (Unity 2022.3 LTS or newer recommended)
- **Graphics Hardware**: Modern GPU with DirectX 11/12 or OpenGL 4.3+ support
- **System Requirements**:
  - Operating System: Windows 10/11, macOS 10.14+, or Ubuntu 20.04+
  - Memory: 8GB+ RAM (16GB+ recommended for complex scenes)
  - Storage: 20GB+ available space
  - CPU: Intel/AMD multi-core processor

### Installing Unity Editor

```bash
# 1. Download Unity Hub from Unity's official website
# 2. Install Unity Hub and sign in to Unity account (free)
# 3. Install Unity Editor 2022.3 LTS with the following modules:
#    - Universal Render Pipeline
#    - High Definition Render Pipeline (HDRP)
#    - Graphics Tools
#    - Built-in Renderer
```

### Installing Unity Robotics Packages

1. **Open Unity Hub**
2. **Create new project** with "3D Core" template
3. **Open Package Manager** (Window > Package Manager)
4. **Add Unity Robotics packages**:

```csharp
// In Package Manager, click "+" button and select "Add package from git URL"
// Add the following packages:

// 1. com.unity.robotics.ros-tcp-connector
https://github.com/Unity-Technologies/ROS-TCP-Connector.git

// 2. com.unity.robotics.urdf-importer
https://github.com/Unity-Technologies/URDF-Importer.git

// 3. com.unity.robotics.robotics-visualization-tools
https://github.com/Unity-Technologies/Robotics-Visualization-Tools.git

// 4. com.unity.render-pipelines.high-definition (for HDRP)
com.unity.render-pipelines.high-definition

// 5. com.unity.mathematics (for robotics math)
com.unity.mathematics
```

### Alternative Installation via manifest.json

Edit `Packages/manifest.json` in your Unity project:

```json
{
  "dependencies": {
    "com.unity.robotics.ros-tcp-connector": "https://github.com/Unity-Technologies/ROS-TCP-Connector.git",
    "com.unity.robotics.urdf-importer": "https://github.com/Unity-Technologies/URDF-Importer.git",
    "com.unity.robotics.robotics-visualization-tools": "https://github.com/Unity-Technologies/Robotics-Visualization-Tools.git",
    "com.unity.render-pipelines.high-definition": "14.0.8",
    "com.unity.mathematics": "1.2.6",
    "com.unity.ide.rider": "3.0.21",
    "com.unity.ide.visualstudio": "2.0.18",
    "com.unity.test-framework": "1.1.33"
  }
}
```

## URDF Robot Import

Unity's URDF Importer allows you to import existing ROS 2 robot models directly into Unity:

### Import Process

1. **Prepare URDF files**: Ensure all mesh files and dependencies are accessible
2. **Import URDF**: Assets > Import Robot from URDF
3. **Configure import settings**:
   - Robot name and package path
   - Scale factor (if needed)
   - Joint configurations
   - Collision mesh settings

### Example URDF Import Configuration

```xml
<!-- Sample URDF for import -->
<robot name="unity_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <mesh filename="package://robot_description/meshes/base.dae"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
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

### Post-Import Processing

After importing, Unity creates a robot prefab with appropriate components:

```csharp
using UnityEngine;
using Unity.Robotics.Core;
using Unity.Robotics.ROSTCPConnector;

public class RobotController : MonoBehaviour
{
    [SerializeField] private string rosIpAddress = "127.0.0.1";
    [SerializeField] private int rosPort = 10000;

    private ROSConnection ros;
    private ArticulationBody[] joints;

    void Start()
    {
        // Initialize ROS connection
        ros = ROSConnection.GetOrCreateInstance();
        ros.Initialize(rosIpAddress, rosPort);

        // Find all articulation bodies (joints)
        joints = GetComponentsInChildren<ArticulationBody>();

        // Subscribe to ROS topics
        ros.Subscribe<geometry_msgs.Twist>("/cmd_vel", OnTwistReceived);
    }

    void OnTwistReceived(geometry_msgs.Twist twist)
    {
        // Apply velocity commands to robot joints
        // Implementation depends on robot configuration
        ApplyVelocityCommands(twist);
    }

    void ApplyVelocityCommands(geometry_msgs.Twist twist)
    {
        // Convert ROS velocity commands to Unity joint movements
        // This is robot-specific implementation
    }
}
```

## Unity-ROS 2 Communication

### TCP Connector Setup

The ROS-TCP-Connector enables communication between Unity and ROS 2 nodes:

#### Unity Side

```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;
using UnityEngine;

public class UnityROSConnection : MonoBehaviour
{
    [SerializeField] private RosConnection connection;
    [SerializeField] private string rosIp = "127.0.0.1";
    [SerializeField] private int rosPort = 10000;

    void Start()
    {
        // Initialize connection
        connection = ROSConnection.GetOrCreateInstance();
        connection.Initialize(rosIp, rosPort);
    }

    // Publish sensor data
    public void PublishLaserScan(float[] ranges)
    {
        sensor_msgs.LaserScanMsg msg = new sensor_msgs.LaserScanMsg();
        msg.ranges = ranges;
        msg.angle_min = -Mathf.PI / 2;
        msg.angle_max = Mathf.PI / 2;
        msg.angle_increment = Mathf.PI / 180;
        msg.range_min = 0.1f;
        msg.range_max = 10.0f;
        msg.header = new std_msgs.HeaderMsg();
        msg.header.stamp = new builtin_interfaces.TimeMsg(ROSConnection.GetNodeTime());
        msg.header.frame_id = "laser_frame";

        connection.Publish("/scan", msg);
    }

    // Subscribe to control commands
    public void SubscribeToCmdVel()
    {
        connection.Subscribe<geometry_msgs.Twist>("/cmd_vel", OnCmdVelReceived);
    }

    void OnCmdVelReceived(geometry_msgs.Twist msg)
    {
        // Process velocity commands
        Debug.Log($"Received cmd_vel: linear={msg.linear.x}, angular={msg.angular.z}");
    }
}
```

#### ROS 2 Side

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class UnityControlBridge(Node):
    def __init__(self):
        super().__init__('unity_control_bridge')

        # Subscriber for commands to send to Unity
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Publisher for sensor data from Unity
        self.laser_pub = self.create_publisher(
            LaserScan,
            '/scan',
            10
        )

        # Timer for publishing simulated sensor data
        self.timer = self.create_timer(0.05, self.publish_sensor_data)  # 20 Hz

        self.get_logger().info('Unity-ROS bridge initialized')

    def cmd_vel_callback(self, msg):
        # Forward commands to Unity (through TCP connection)
        self.get_logger().info(f'Forwarding cmd_vel to Unity: {msg}')

    def publish_sensor_data(self):
        # Publish simulated sensor data
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_frame'
        msg.angle_min = -1.57
        msg.angle_max = 1.57
        msg.angle_increment = 0.0174533  # 1 degree
        msg.range_min = 0.1
        msg.range_max = 10.0
        msg.ranges = [2.0] * 181  # 181 readings for full range

        self.laser_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = UnityControlBridge()

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

## Sensor Integration in Unity

### Camera Sensors

Unity's rendering pipeline allows for high-quality camera simulation:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using Unity.Robotics.UrdfImporter;

public class UnityCameraSensor : MonoBehaviour
{
    [SerializeField] private Camera cameraComponent;
    [SerializeField] private int imageWidth = 640;
    [SerializeField] private int imageHeight = 480;
    [SerializeField] private string topicName = "/camera/image_raw";

    private RenderTexture renderTexture;
    private Texture2D texture2D;
    private ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        // Create render texture for camera
        renderTexture = new RenderTexture(imageWidth, imageHeight, 24);
        cameraComponent.targetTexture = renderTexture;

        // Create texture for image conversion
        texture2D = new Texture2D(imageWidth, imageHeight, TextureFormat.RGB24, false);

        // Start publishing loop
        InvokeRepeating("PublishCameraImage", 0.0, 1.0f / 30.0f); // 30 FPS
    }

    void PublishCameraImage()
    {
        // Set active render texture
        RenderTexture.active = renderTexture;

        // Copy render texture to texture2D
        texture2D.ReadPixels(new Rect(0, 0, imageWidth, imageHeight), 0, 0);
        texture2D.Apply();

        // Convert to ROS message and publish
        byte[] imageData = texture2D.EncodeToJPG();

        sensor_msgs.ImageMsg msg = new sensor_msgs.ImageMsg();
        msg.header = new std_msgs.HeaderMsg();
        msg.header.stamp = new builtin_interfaces.TimeMsg(ROSConnection.GetNodeTime());
        msg.header.frame_id = transform.name;
        msg.height = (uint)imageHeight;
        msg.width = (uint)imageWidth;
        msg.encoding = "rgb8";
        msg.is_bigendian = 0;
        msg.step = (uint)(imageWidth * 3); // 3 bytes per pixel
        msg.data = imageData;

        ros.Publish(topicName, msg);
    }
}
```

### LIDAR Sensor Simulation

Unity can simulate LIDAR sensors using raycasting:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class UnityLidarSensor : MonoBehaviour
{
    [SerializeField] private int numRays = 360;
    [SerializeField] private float fieldOfView = 360.0f;
    [SerializeField] private float maxDistance = 10.0f;
    [SerializeField] private string topicName = "/scan";
    [SerializeField] private LayerMask raycastLayerMask = -1;

    private ROSConnection ros;
    private float[] ranges;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ranges = new float[numRays];

        // Start publishing loop
        InvokeRepeating("PublishLaserScan", 0.0, 0.1f); // 10 Hz
    }

    void PublishLaserScan()
    {
        // Perform raycasting for each ray
        for (int i = 0; i < numRays; i++)
        {
            float angle = fieldOfView * i / numRays - fieldOfView / 2;
            Vector3 direction = Quaternion.Euler(0, angle, 0) * transform.forward;

            if (Physics.Raycast(transform.position, direction, out RaycastHit hit, maxDistance, raycastLayerMask))
            {
                ranges[i] = hit.distance;
            }
            else
            {
                ranges[i] = maxDistance;
            }
        }

        // Create and publish ROS message
        sensor_msgs.LaserScanMsg msg = new sensor_msgs.LaserScanMsg();
        msg.header = new std_msgs.HeaderMsg();
        msg.header.stamp = new builtin_interfaces.TimeMsg(ROSConnection.GetNodeTime());
        msg.header.frame_id = transform.name;
        msg.angle_min = -fieldOfView * Mathf.Deg2Rad / 2;
        msg.angle_max = fieldOfView * Mathf.Deg2Rad / 2;
        msg.angle_increment = (fieldOfView * Mathf.Deg2Rad) / numRays;
        msg.range_min = 0.1f;
        msg.range_max = maxDistance;
        msg.ranges = ranges;

        ros.Publish(topicName, msg);
    }
}
```

### IMU Sensor Simulation

Simulate IMU sensor data with Unity's physics engine:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using Unity.Robotics.Core;

public class UnityImuSensor : MonoBehaviour
{
    [SerializeField] private ArticulationBody robotBody;
    [SerializeField] private string topicName = "/imu/data";

    private ROSConnection ros;
    private Rigidbody rb;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        if (robotBody != null)
        {
            rb = robotBody.GetComponent<Rigidbody>();
        }

        // Start publishing loop
        InvokeRepeating("PublishImuData", 0.0, 0.01f); // 100 Hz
    }

    void PublishImuData()
    {
        sensor_msgs.ImuMsg msg = new sensor_msgs.ImuMsg();
        msg.header = new std_msgs.HeaderMsg();
        msg.header.stamp = new builtin_interfaces.TimeMsg(ROSConnection.GetNodeTime());
        msg.header.frame_id = transform.name;

        // Angular velocity (from Unity's angular velocity)
        if (rb != null)
        {
            msg.angular_velocity.x = rb.angularVelocity.x;
            msg.angular_velocity.y = rb.angularVelocity.y;
            msg.angular_velocity.z = rb.angularVelocity.z;
        }

        // Linear acceleration (from Unity's acceleration)
        msg.linear_acceleration.x = Physics.gravity.x;
        msg.linear_acceleration.y = Physics.gravity.y;
        msg.linear_acceleration.z = Physics.gravity.z;

        // Orientation (from Unity's rotation)
        Quaternion unityRot = transform.rotation;

        // Convert Unity coordinates to ROS coordinates if needed
        msg.orientation.w = unityRot.w;
        msg.orientation.x = unityRot.x;
        msg.orientation.y = unityRot.y;
        msg.orientation.z = unityRot.z;

        ros.Publish(topicName, msg);
    }
}
```

## Physics Configuration

### Unity Physics vs ROS 2 Integration

Unity's physics engine (NVIDIA PhysX) provides accurate simulation:

```csharp
using UnityEngine;

public class UnityPhysicsConfig : MonoBehaviour
{
    void Start()
    {
        // Configure global physics settings
        Physics.defaultSolverIterations = 8;      // Solver iterations
        Physics.defaultSolverVelocityIterations = 1;  // Velocity iterations
        Physics.sleepThreshold = 0.005f;         // Sleep threshold
        Physics.defaultContactOffset = 0.01f;    // Contact offset
        Physics.bounceThreshold = 2.0f;          // Bounce threshold

        // For robotics applications, you might want to adjust:
        Time.fixedDeltaTime = 0.01f;             // Physics update rate (100 Hz)
        Time.maximumDeltaTime = 0.02f;           // Max allowed delta time
    }
}
```

### Joint Control and Actuator Simulation

Simulate robot actuators with Unity's ArticulationBody:

```csharp
using UnityEngine;

public class UnityActuatorControl : MonoBehaviour
{
    [SerializeField] private ArticulationBody[] joints;
    [SerializeField] private float maxForce = 100f;
    [SerializeField] private float maxVelocity = 10f;

    void Start()
    {
        ConfigureJoints();
    }

    void ConfigureJoints()
    {
        foreach (var joint in joints)
        {
            // Configure joint drive for realistic actuator behavior
            ArticulationDrive drive = joint.xDrive;
            drive.forceLimit = maxForce;
            drive.velocity = maxVelocity;
            drive.damping = 10f;
            drive.stiffness = 100f;

            joint.xDrive = drive;
        }
    }

    public void SetJointTargetVelocities(float[] velocities)
    {
        for (int i = 0; i < joints.Length && i < velocities.Length; i++)
        {
            ArticulationDrive drive = joints[i].xDrive;
            drive.targetVelocity = velocities[i];
            joints[i].xDrive = drive;
        }
    }

    public void SetJointTargetPositions(float[] positions)
    {
        for (int i = 0; i < joints.Length && i < positions.Length; i++)
        {
            ArticulationDrive drive = joints[i].xDrive;
            drive.target = positions[i];
            joints[i].xDrive = drive;
        }
    }
}
```

## Real-time Performance Optimization

### Rendering Optimization

For real-time robotics simulation, optimize rendering performance:

```csharp
using UnityEngine;

public class UnityRenderingOptimization : MonoBehaviour
{
    [Header("Performance Settings")]
    [SerializeField] private int targetFrameRate = 60;
    [SerializeField] private bool useFixedTimeStep = true;
    [SerializeField] private float fixedTimeStep = 0.016f;  // ~60 FPS

    [Header("Quality Settings")]
    [SerializeField] private int qualityLevel = 2;  // Medium quality
    [SerializeField] private bool vSync = false;

    void Start()
    {
        ConfigurePerformance();
    }

    void ConfigurePerformance()
    {
        // Set target frame rate
        Application.targetFrameRate = targetFrameRate;

        // VSync settings
        QualitySettings.vSyncCount = vSync ? 1 : 0;

        // Quality level (0=Fastest, 5=Fantastic)
        QualitySettings.SetQualityLevel(qualityLevel);

        // Fixed timestep for consistent physics
        if (useFixedTimeStep)
        {
            Time.fixedDeltaTime = fixedTimeStep;
        }

        // Optimize for real-time performance
        QualitySettings.shadowDistance = 10f;  // Reduce shadow distance
        QualitySettings.lodBias = 0.7f;       // Reduce LOD distance
        QualitySettings.maxQueuedFrames = 1;  // Reduce input lag
    }

    [Header("LOD Settings")]
    [SerializeField] private float lodDistance = 20f;

    void ConfigureLOD()
    {
        // Unity has built-in LOD system for complex models
        // For robotics applications, use simpler models at distance
    }
}
```

### Sensor Data Optimization

Optimize sensor data processing for real-time performance:

```csharp
using UnityEngine;
using System.Collections.Generic;

public class OptimizedSensorProcessing : MonoBehaviour
{
    [SerializeField] private float sensorUpdateRate = 30f;  // Hz
    [SerializeField] private int cameraResolutionReduction = 1;  // 1=full, 2=half, 4=quarter

    private float lastSensorUpdate;
    private RenderTexture reducedTexture;

    void Start()
    {
        lastSensorUpdate = Time.time;

        if (cameraResolutionReduction > 1)
        {
            // Create reduced resolution texture for faster processing
            int reducedWidth = 640 / cameraResolutionReduction;
            int reducedHeight = 480 / cameraResolutionReduction;
            reducedTexture = new RenderTexture(reducedWidth, reducedHeight, 24);
        }
    }

    void Update()
    {
        if (Time.time - lastSensorUpdate >= 1.0f / sensorUpdateRate)
        {
            ProcessSensors();
            lastSensorUpdate = Time.time;
        }
    }

    void ProcessSensors()
    {
        // Process all sensors at reduced frequency
        // This reduces CPU/GPU load for real-time simulation
    }

    Texture2D ReduceResolution(Texture2D originalTexture)
    {
        if (reducedTexture == null) return originalTexture;

        // Blit to reduced texture
        Graphics.Blit(originalTexture, reducedTexture);

        // Read back to Texture2D
        RenderTexture.active = reducedTexture;
        Texture2D reduced = new Texture2D(reducedTexture.width, reducedTexture.height, TextureFormat.RGB24, false);
        reduced.ReadPixels(new Rect(0, 0, reducedTexture.width, reducedTexture.height), 0, 0);
        reduced.Apply();

        return reduced;
    }
}
```

## Advanced Features

### Synthetic Data Generation

Unity excels at generating synthetic training data for AI models:

```csharp
using UnityEngine;
using System.IO;

public class SyntheticDataGenerator : MonoBehaviour
{
    [Header("Data Generation Settings")]
    [SerializeField] private string dataOutputPath = "Assets/SyntheticData/";
    [SerializeField] private int samplesPerScene = 100;
    [SerializeField] private bool generateDepthMaps = true;
    [SerializeField] private bool generateSegmentation = true;

    [Header("Domain Randomization")]
    [SerializeField] private Color[] randomColors = { Color.red, Color.blue, Color.green };
    [SerializeField] private float positionVariation = 1.0f;
    [SerializeField] private float lightIntensityVariation = 0.5f;

    private int sampleCount = 0;

    public void GenerateTrainingData()
    {
        // Randomize environment
        RandomizeEnvironment();

        // Capture data
        CaptureDataSample();

        sampleCount++;
        if (sampleCount < samplesPerScene)
        {
            Invoke("GenerateTrainingData", 0.1f);
        }
    }

    void RandomizeEnvironment()
    {
        // Randomize object positions
        Transform[] environmentObjects = FindObjectsOfType<Transform>();
        foreach (Transform obj in environmentObjects)
        {
            if (obj.CompareTag("Randomizable"))
            {
                Vector3 randomPos = obj.position + Random.insideUnitSphere * positionVariation;
                obj.position = randomPos;
            }
        }

        // Randomize lighting
        Light[] lights = FindObjectsOfType<Light>();
        foreach (Light light in lights)
        {
            light.intensity = Random.Range(
                light.intensity - lightIntensityVariation,
                light.intensity + lightIntensityVariation
            );
        }
    }

    void CaptureDataSample()
    {
        // Capture RGB image
        string rgbPath = Path.Combine(dataOutputPath, $"rgb_{sampleCount:D6}.png");
        // Save image to path

        // Capture depth map if enabled
        if (generateDepthMaps)
        {
            string depthPath = Path.Combine(dataOutputPath, $"depth_{sampleCount:D6}.png");
            // Generate and save depth map
        }

        // Capture segmentation if enabled
        if (generateSegmentation)
        {
            string segPath = Path.Combine(dataOutputPath, $"seg_{sampleCount:D6}.png");
            // Generate and save segmentation map
        }

        // Save annotations
        string annotationPath = Path.Combine(dataOutputPath, $"annotations_{sampleCount:D6}.json");
        // Save annotation data
    }
}
```

### VR/AR Integration

Unity supports VR/AR for immersive robotics applications:

```csharp
using UnityEngine;
using UnityEngine.XR;

public class VRRoboticsInterface : MonoBehaviour
{
    [SerializeField] private Transform robotModel;
    [SerializeField] private SteamVR_Behaviour_Pose controllerPose;
    [SerializeField] private OVRGrabbable[] grabbableParts;

    void Update()
    {
        // Handle VR controller input for robot manipulation
        HandleVRControllers();

        // Update robot model based on VR interaction
        UpdateRobotFromVR();
    }

    void HandleVRControllers()
    {
        if (controllerPose != null)
        {
            // Get controller pose and apply to robot
            robotModel.position = controllerPose.transform.position;
            robotModel.rotation = controllerPose.transform.rotation;

            // Forward controller inputs to ROS 2
            ForwardVRInputToROS2();
        }
    }

    void ForwardVRInputToROS2()
    {
        // Convert VR controller input to ROS 2 messages
        // This enables remote robot control through VR
    }
}
```

## Troubleshooting Common Issues

### Performance Issues

**Symptoms**: Low frame rate, stuttering, high CPU/GPU usage
**Solutions**:
- Reduce rendering quality settings
- Use lower polygon models for collision detection
- Limit simultaneous active robots
- Reduce sensor update rates
- Use occlusion culling

### Physics Instability

**Symptoms**: Robot shaking, unrealistic movement, interpenetration
**Solutions**:
- Adjust Unity physics solver settings
- Use appropriate collider shapes
- Verify mass properties are realistic
- Increase solver iterations

### ROS Connection Issues

**Symptoms**: No communication between Unity and ROS 2
**Solutions**:
- Verify IP address and port configuration
- Check firewall settings
- Ensure ROS TCP connector is properly configured
- Use network debugging tools

### Sensor Data Discrepancies

**Symptoms**: Simulated sensor data doesn't match real robot
**Solutions**:
- Calibrate sensor parameters
- Verify coordinate frame transformations
- Check sensor mounting positions
- Validate noise models

## Best Practices

### Scene Organization
1. **Use layers**: Organize objects into layers for physics and rendering
2. **Prefab-based approach**: Create reusable robot and environment prefabs
3. **Lighting considerations**: Use appropriate lighting for computer vision
4. **Physics optimization**: Balance visual fidelity with physics performance

### Real-time Performance
1. **Frame rate consistency**: Maintain consistent frame rate for sensor data
2. **Asynchronous processing**: Use coroutines for non-critical tasks
3. **Resource management**: Monitor and optimize asset loading
4. **Testing procedures**: Validate simulation behavior on target hardware

### Data Generation
1. **Domain randomization**: Vary parameters for robust training
2. **Quality validation**: Verify generated data quality
3. **Annotation accuracy**: Ensure precise ground truth data
4. **Storage efficiency**: Compress and optimize data storage

## Integration with Course Curriculum

### Week 5: Unity Simulation
- Real-time rendering and visual quality
- Complex sensor modeling
- Human-robot interaction scenarios
- VR integration possibilities

### Applications in Physical AI
- Computer vision training with photorealistic data
- Perception algorithm validation
- Human-robot interaction studies
- VR-based robot teleoperation

## Summary

Unity provides powerful capabilities for real-time, photorealistic robotics simulation. The integration with ROS 2 through the Unity Robotics Hub enables seamless development of complex simulation scenarios. With proper configuration and optimization, Unity can serve as an essential component of the Digital Twin approach, bridging the gap between digital AI and physical robotics.

The combination of real-time physics, photorealistic rendering, and comprehensive sensor simulation makes Unity particularly valuable for computer vision training, perception validation, and human-robot interaction studies.

## Further Reading

- [Unity Robotics Hub Documentation](https://github.com/Unity-Technologies/Unity-Robotics-Hub)
- [ROS-TCP-Connector Guide](https://github.com/Unity-Technologies/ROS-TCP-Connector)
- [URDF-Importer Documentation](https://github.com/Unity-Technologies/URDF-Importer)
- [Unity Physics Manual](https://docs.unity3d.com/Manual/PhysicsSection.html)
- [Synthetic Data Generation Best Practices](https://arxiv.org/abs/1804.06516)
