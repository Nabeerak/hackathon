/**
 * Sidebar Navigation Contract for Physical AI & Humanoid Robotics Textbook
 *
 * This file defines the complete sidebar structure to be added to sidebars.ts
 * in the Docusaurus configuration.
 *
 * Feature: 002-constitution-book
 * Created: 2025-11-30
 * Phase: Phase 1 - Design
 */

export type SidebarConfig = {
  physicalAiTextbook: SidebarItem[];
};

export type SidebarItem = CategoryItem | DocItem | LinkItem;

export interface CategoryItem {
  type: 'category';
  label: string;
  items: SidebarItem[];
  collapsed?: boolean;
  collapsible?: boolean;
}

export interface DocItem {
  type: 'doc';
  id: string;
  label?: string;
}

export interface LinkItem {
  type: 'link';
  label: string;
  href: string;
}

/**
 * Complete sidebar structure for the Physical AI textbook
 *
 * This should be added to the sidebars object in docusaurus-book/sidebars.ts:
 *
 * const sidebars = {
 *   tutorialSidebar: [...], // existing sidebar
 *   physicalAiTextbook: physicalAiTextbookSidebar, // add this
 * };
 */
export const physicalAiTextbookSidebar: SidebarItem[] = [
  // Book Introduction
  {
    type: 'doc',
    id: 'physical-ai-textbook/index',
    label: 'Introduction'
  },

  // Course Overview Section
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

  // Hardware & Infrastructure Chapter
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

  // ROS 2 Fundamentals Chapter
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

  // Digital Twin Simulation Chapter
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

  // NVIDIA Isaac Chapter
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

  // Vision-Language-Action Chapter
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

  // Humanoid Robotics Chapter
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

  // Appendices
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
];

/**
 * Navigation Statistics
 *
 * Total Chapters: 7 main chapters + 1 course overview + 1 appendix = 9 sections
 * Total Pages: ~50-60 pages
 * Estimated Content: 100-150 pages of material
 *
 * Navigation Depth:
 * - Level 1: Book sections (9 items)
 * - Level 2: Chapter pages (average 5-7 per chapter)
 * - Level 3: Not used (keeps navigation simple)
 *
 * Compliance with Success Criteria:
 * - SC-003: Students can navigate within 3 clicks ✓
 *   (Book → Chapter → Section = max 2 clicks)
 * - SC-002: Minimum 5 sections per major topic ✓
 *   (All chapters have 5-7 sections)
 */
