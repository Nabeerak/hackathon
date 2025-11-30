#!/usr/bin/env python3
"""
Generate skeleton pages for Physical AI textbook
This creates all chapter index and section pages with basic frontmatter
"""

import os

# Base directory
base_dir = "docusaurus-book/docs/physical-ai-textbook"

# Chapter definitions
chapters = {
    "hardware-infrastructure": {
        "title": "Hardware & Infrastructure",
        "position": 2,
        "sections": [
            ("index", "Overview", "Overview of hardware options for Physical AI development"),
            ("digital-twin-workstation", "Digital Twin Workstation", "Workstation specifications for running Isaac Sim and ROS 2"),
            ("physical-ai-edge-kits", "Physical AI Edge Kits", "Edge devices for on-robot AI processing"),
            ("robot-lab-options", "Robot Lab Options", "Physical robot platforms for hands-on labs"),
            ("cloud-native-alternatives", "Cloud-Native Alternatives", "AWS/Azure options for cloud-based development")
        ]
    },
    "ros2-fundamentals": {
        "title": "ROS 2 Fundamentals",
        "position": 3,
        "sections": [
            ("index", "Introduction to ROS 2", "Overview of ROS 2 architecture and ecosystem"),
            ("installation", "Installation & Setup", "Installing ROS 2 Humble on Ubuntu 22.04"),
            ("nodes-topics", "Nodes and Topics", "Creating publishers and subscribers"),
            ("services-actions", "Services and Actions", "Request-response and goal-based communication"),
            ("parameters-launch", "Parameters and Launch Files", "Configuration and multi-node startup"),
            ("navigation-stack", "Navigation Stack", "Nav2 for autonomous robot navigation"),
            ("debugging-tools", "Debugging Tools", "ros2 CLI, rqt, and rviz2 for troubleshooting")
        ]
    },
    "digital-twin-simulation": {
        "title": "Digital Twin Simulation",
        "position": 4,
        "sections": [
            ("index", "Introduction to Digital Twins", "Physics simulation for robot development"),
            ("gazebo-basics", "Gazebo Basics", "World building and robot simulation in Gazebo"),
            ("unity-simulation", "Unity Simulation", "Real-time physics with Unity-ROS 2 integration"),
            ("urdf-modeling", "URDF Robot Modeling", "Creating robot descriptions with URDF/Xacro"),
            ("sensor-integration", "Sensor Integration", "Virtual cameras, LIDAR, and IMU sensors"),
            ("physics-simulation", "Physics Simulation", "Collision, friction, and dynamics modeling")
        ]
    },
    "nvidia-isaac": {
        "title": "NVIDIA Isaac Platform",
        "position": 5,
        "sections": [
            ("index", "Introduction to Isaac", "NVIDIA Isaac platform overview"),
            ("isaac-sim-intro", "Isaac Sim Overview", "Photorealistic robot simulation"),
            ("omniverse-setup", "Omniverse Setup", "Installing and configuring Isaac Sim"),
            ("robot-brain-ai", "Robot Brain AI", "AI modules for perception and decision-making"),
            ("perception-systems", "Perception Systems", "Computer vision and depth sensing"),
            ("slam-navigation", "SLAM and Navigation", "Simultaneous localization and mapping"),
            ("sim-to-real-transfer", "Sim-to-Real Transfer", "Domain randomization and reality gap")
        ]
    },
    "vision-language-action": {
        "title": "Vision-Language-Action (VLA)",
        "position": 6,
        "sections": [
            ("index", "Introduction to VLA", "Vision-Language-Action models for robotics"),
            ("vla-overview", "VLA Model Architecture", "Understanding multimodal transformer models"),
            ("multimodal-models", "Multimodal Foundation Models", "Vision-language pre-training for robots"),
            ("action-primitives", "Action Primitives", "Discrete and continuous action spaces"),
            ("integration-patterns", "Integration with Robots", "Connecting VLA to robot control"),
            ("training-fine-tuning", "Training and Fine-Tuning", "Adapting VLA models to custom tasks")
        ]
    },
    "humanoid-robotics": {
        "title": "Humanoid Robotics",
        "position": 7,
        "sections": [
            ("index", "Introduction to Humanoid Robots", "Bipedal robots and human-like interaction"),
            ("bipedal-locomotion", "Bipedal Locomotion", "Walking gait generation and control"),
            ("manipulation-control", "Manipulation Control", "Arm and hand control for object interaction"),
            ("balance-stability", "Balance and Stability", "ZMP and COM for maintaining balance"),
            ("conversational-robotics", "Conversational Robotics", "Speech recognition and synthesis"),
            ("gpt-integration", "GPT Integration", "Large language models for robot dialogue"),
            ("hri-design", "Human-Robot Interaction Design", "Designing effective HRI experiences")
        ]
    },
    "appendices": {
        "title": "Appendices",
        "position": 8,
        "sections": [
            ("glossary", "Glossary", "Definitions of key terms"),
            ("resources", "Additional Resources", "External learning materials and references"),
            ("troubleshooting", "Troubleshooting Guide", "Common issues and solutions")
        ]
    }
}

def create_page(chapter_dir, filename, title, description, position):
    """Create a skeleton markdown page"""
    filepath = os.path.join(base_dir, chapter_dir, f"{filename}.md")

    # Create frontmatter
    frontmatter = f"""---
title: {title}
sidebar_label: {title if len(title) < 30 else title[:27] + '...'}
sidebar_position: {position}
description: {description}
keywords: [Physical AI, robotics, {title.lower()}]
---

# {title}

*Content coming soon...*

## Overview

This section covers {description.lower()}.

## Learning Objectives

After completing this section, you will be able to:

- Objective 1
- Objective 2
- Objective 3

## Content

[To be filled with comprehensive content]

## Summary

Key takeaways from this section.

## Further Reading

- Additional resources
"""

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    print(f"Created: {filepath}")

# Generate all pages
for chapter_dir, chapter_info in chapters.items():
    for idx, (filename, title, description) in enumerate(chapter_info['sections'], 1):
        create_page(chapter_dir, filename, title, description, idx)

print("\nAll skeleton pages created successfully!")
