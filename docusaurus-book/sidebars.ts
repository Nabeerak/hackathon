import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
    physicalAiTextbook: [
      {
        type: 'doc',
        id: 'physical-ai-textbook/index',
        label: 'Introduction'
      },
      {
        type: 'category',
        label: 'Course Overview',
        collapsed: false,
        items: [
          {
            type: 'doc',
            id: 'physical-ai-textbook/course-overview/learning-outcomes',
            label: 'Learning Outcomes'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/course-overview/weekly-breakdown',
            label: 'Weekly Breakdown'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/course-overview/prerequisites',
            label: 'Prerequisites'
          }
        ]
      },
      {
        type: 'category',
        label: 'Hardware & Infrastructure',
        collapsed: true,
        items: [
          {
            type: 'doc',
            id: 'physical-ai-textbook/hardware-infrastructure/index',
            label: 'Overview'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/hardware-infrastructure/digital-twin-workstation',
            label: 'Digital Twin Workstation'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/hardware-infrastructure/physical-ai-edge-kits',
            label: 'Physical AI Edge Kits'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/hardware-infrastructure/robot-lab-options',
            label: 'Robot Lab Options'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/hardware-infrastructure/cloud-native-alternatives',
            label: 'Cloud-Native Alternatives'
          }
        ]
      },
      {
        type: 'category',
        label: 'ROS 2 Fundamentals',
        collapsed: true,
        items: [
          {
            type: 'doc',
            id: 'physical-ai-textbook/ros2-fundamentals/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/ros2-fundamentals/installation',
            label: 'Installation & Setup'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/ros2-fundamentals/nodes-topics',
            label: 'Nodes and Topics'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/ros2-fundamentals/services-actions',
            label: 'Services and Actions'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/ros2-fundamentals/parameters-launch',
            label: 'Parameters and Launch Files'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/ros2-fundamentals/navigation-stack',
            label: 'Navigation Stack'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/ros2-fundamentals/debugging-tools',
            label: 'Debugging Tools'
          }
        ]
      },
      {
        type: 'category',
        label: 'Digital Twin Simulation',
        collapsed: true,
        items: [
          {
            type: 'doc',
            id: 'physical-ai-textbook/digital-twin-simulation/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/digital-twin-simulation/gazebo-basics',
            label: 'Gazebo Basics'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/digital-twin-simulation/unity-simulation',
            label: 'Unity Simulation'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/digital-twin-simulation/urdf-modeling',
            label: 'URDF Robot Modeling'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/digital-twin-simulation/sensor-integration',
            label: 'Sensor Integration'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/digital-twin-simulation/physics-simulation',
            label: 'Physics Simulation'
          }
        ]
      },
      {
        type: 'category',
        label: 'NVIDIA Isaac Platform',
        collapsed: true,
        items: [
          {
            type: 'doc',
            id: 'physical-ai-textbook/nvidia-isaac/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/nvidia-isaac/isaac-sim-intro',
            label: 'Isaac Sim Overview'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/nvidia-isaac/omniverse-setup',
            label: 'Omniverse Setup'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/nvidia-isaac/robot-brain-ai',
            label: 'Robot Brain AI'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/nvidia-isaac/perception-systems',
            label: 'Perception Systems'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/nvidia-isaac/slam-navigation',
            label: 'SLAM and Navigation'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/nvidia-isaac/sim-to-real-transfer',
            label: 'Sim-to-Real Transfer'
          }
        ]
      },
      {
        type: 'category',
        label: 'Vision-Language-Action (VLA)',
        collapsed: true,
        items: [
          {
            type: 'doc',
            id: 'physical-ai-textbook/vision-language-action/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/vision-language-action/vla-overview',
            label: 'VLA Model Architecture'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/vision-language-action/multimodal-models',
            label: 'Multimodal Foundation Models'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/vision-language-action/action-primitives',
            label: 'Action Primitives'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/vision-language-action/integration-patterns',
            label: 'Integration with Robots'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/vision-language-action/training-fine-tuning',
            label: 'Training and Fine-Tuning'
          }
        ]
      },
      {
        type: 'category',
        label: 'Humanoid Robotics',
        collapsed: true,
        items: [
          {
            type: 'doc',
            id: 'physical-ai-textbook/humanoid-robotics/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/humanoid-robotics/bipedal-locomotion',
            label: 'Bipedal Locomotion'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/humanoid-robotics/manipulation-control',
            label: 'Manipulation and Control'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/humanoid-robotics/balance-stability',
            label: 'Balance and Stability'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/humanoid-robotics/conversational-robotics',
            label: 'Conversational Robotics'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/humanoid-robotics/gpt-integration',
            label: 'GPT Integration'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/humanoid-robotics/hri-design',
            label: 'Human-Robot Interaction Design'
          }
        ]
      },
      {
        type: 'category',
        label: 'Appendices',
        collapsed: true,
        items: [
          {
            type: 'doc',
            id: 'physical-ai-textbook/appendices/glossary',
            label: 'Glossary'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/appendices/resources',
            label: 'Additional Resources'
          },
          {
            type: 'doc',
            id: 'physical-ai-textbook/appendices/troubleshooting',
            label: 'Troubleshooting Guide'
          }
        ]
      }
    ],
};

export default sidebars;
