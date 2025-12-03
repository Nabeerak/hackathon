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
        id: 'index',
        label: 'Introduction'
      },
      {
        type: 'category',
        label: 'Course Overview',
        collapsed: false,
        items: [
          {
            type: 'doc',
            id: 'course-overview/learning-outcomes',
            label: 'Learning Outcomes'
          },
          {
            type: 'doc',
            id: 'course-overview/weekly-breakdown',
            label: 'Weekly Breakdown'
          },
          {
            type: 'doc',
            id: 'course-overview/prerequisites',
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
            id: 'hardware-infrastructure/index',
            label: 'Overview'
          },
          {
            type: 'doc',
            id: 'hardware-infrastructure/digital-twin-workstation',
            label: 'Digital Twin Workstation'
          },
          {
            type: 'doc',
            id: 'hardware-infrastructure/physical-ai-edge-kits',
            label: 'Physical AI Edge Kits'
          },
          {
            type: 'doc',
            id: 'hardware-infrastructure/robot-lab-options',
            label: 'Robot Lab Options'
          },
          {
            type: 'doc',
            id: 'hardware-infrastructure/cloud-native-alternatives',
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
            id: 'ros2-fundamentals/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'ros2-fundamentals/installation',
            label: 'Installation & Setup'
          },
          {
            type: 'doc',
            id: 'ros2-fundamentals/nodes-topics',
            label: 'Nodes and Topics'
          },
          {
            type: 'doc',
            id: 'ros2-fundamentals/services-actions',
            label: 'Services and Actions'
          },
          {
            type: 'doc',
            id: 'ros2-fundamentals/parameters-launch',
            label: 'Parameters and Launch Files'
          },
          {
            type: 'doc',
            id: 'ros2-fundamentals/navigation-stack',
            label: 'Navigation Stack'
          },
          {
            type: 'doc',
            id: 'ros2-fundamentals/debugging-tools',
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
            id: 'digital-twin-simulation/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'digital-twin-simulation/gazebo-basics',
            label: 'Gazebo Basics'
          },
          {
            type: 'doc',
            id: 'digital-twin-simulation/unity-simulation',
            label: 'Unity Simulation'
          },
          {
            type: 'doc',
            id: 'digital-twin-simulation/urdf-modeling',
            label: 'URDF Robot Modeling'
          },
          {
            type: 'doc',
            id: 'digital-twin-simulation/sensor-integration',
            label: 'Sensor Integration'
          },
          {
            type: 'doc',
            id: 'digital-twin-simulation/physics-simulation',
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
            id: 'nvidia-isaac/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'nvidia-isaac/isaac-sim-intro',
            label: 'Isaac Sim Overview'
          },
          {
            type: 'doc',
            id: 'nvidia-isaac/omniverse-setup',
            label: 'Omniverse Setup'
          },
          {
            type: 'doc',
            id: 'nvidia-isaac/robot-brain-ai',
            label: 'Robot Brain AI'
          },
          {
            type: 'doc',
            id: 'nvidia-isaac/perception-systems',
            label: 'Perception Systems'
          },
          {
            type: 'doc',
            id: 'nvidia-isaac/slam-navigation',
            label: 'SLAM and Navigation'
          },
          {
            type: 'doc',
            id: 'nvidia-isaac/sim-to-real-transfer',
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
            id: 'vision-language-action/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'vision-language-action/vla-overview',
            label: 'VLA Model Architecture'
          },
          {
            type: 'doc',
            id: 'vision-language-action/multimodal-models',
            label: 'Multimodal Foundation Models'
          },
          {
            type: 'doc',
            id: 'vision-language-action/action-primitives',
            label: 'Action Primitives'
          },
          {
            type: 'doc',
            id: 'vision-language-action/integration-patterns',
            label: 'Integration with Robots'
          },
          {
            type: 'doc',
            id: 'vision-language-action/training-fine-tuning',
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
            id: 'humanoid-robotics/index',
            label: 'Introduction'
          },
          {
            type: 'doc',
            id: 'humanoid-robotics/bipedal-locomotion',
            label: 'Bipedal Locomotion'
          },
          {
            type: 'doc',
            id: 'humanoid-robotics/manipulation-control',
            label: 'Manipulation and Control'
          },
          {
            type: 'doc',
            id: 'humanoid-robotics/balance-stability',
            label: 'Balance and Stability'
          },
          {
            type: 'doc',
            id: 'humanoid-robotics/conversational-robotics',
            label: 'Conversational Robotics'
          },
          {
            type: 'doc',
            id: 'humanoid-robotics/gpt-integration',
            label: 'GPT Integration'
          },
          {
            type: 'doc',
            id: 'humanoid-robotics/hri-design',
            label: 'Human-Robot Interaction Design'
          }
        ]
      },
      {
        type: 'category',
        label: 'AI Integration',
        collapsed: true,
        items: [
          {
            type: 'doc',
            id: 'ai-integration/reusable-intelligence',
            label: 'Reusable Intelligence'
          },
          {
            type: 'doc',
            id: 'ai-integration/rag-chatbot-integration',
            label: 'RAG Chatbot Integration'
          },
          {
            type: 'doc',
            id: 'ai-integration/multilingual-support',
            label: 'Multilingual Support'
          },
          {
            type: 'doc',
            id: 'ai-integration/authentication-personalization',
            label: 'Authentication & Personalization'
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
            id: 'appendices/glossary',
            label: 'Glossary'
          },
          {
            type: 'doc',
            id: 'appendices/resources',
            label: 'Additional Resources'
          },
          {
            type: 'doc',
            id: 'appendices/troubleshooting',
            label: 'Troubleshooting Guide'
          }
        ]
      }
    ],
};

export default sidebars;
