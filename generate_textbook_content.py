#!/usr/bin/env python3
"""
Generate comprehensive content for Physical AI & Humanoid Robotics textbook
"""

import os

# Base directory
base_dir = "docusaurus-book/docs/physical-ai-textbook"

# Content templates for each page
content_map = {
    # Hardware & Infrastructure Chapter
    "hardware-infrastructure/index.md": """---
title: Hardware & Infrastructure Overview
sidebar_label: Overview
sidebar_position: 1
description: Overview of hardware options for Physical AI development
keywords: [Physical AI, robotics, hardware, infrastructure, workstation]
---

# Hardware & Infrastructure Overview

Developing Physical AI systems requires carefully selected hardware that can handle the computational demands of robot simulation, AI training, and real-time control. This chapter explores the hardware ecosystem for Physical AI development.

## Why Hardware Matters

Physical AI systems must:
- **Simulate physics in real-time**: Digital twins require GPU acceleration
- **Process sensor data**: Cameras, LIDAR, IMU generate massive data streams
- **Run AI models**: VLA models need significant compute power
- **Deploy to robots**: Edge devices must be power-efficient yet capable

## Hardware Categories

1. **Digital Twin Workstation**: Development machine for Isaac Sim and ROS 2
2. **Physical AI Edge Kits**: Compact computers for robot deployment
3. **Robot Lab Options**: Physical platforms for real-world testing
4. **Cloud-Native Alternatives**: Scalable cloud compute

## Decision Matrix

| Use Case | Hardware | Cost |
|----------|----------|------|
| Learning | Cloud + Jetson Nano | $500-1,500 |
| Professional | Workstation + Robot | $5K-15K |
| Research | Multiple workstations + fleet | $25K+ |

## Summary

Hardware selection is crucial for Physical AI success. The right combination of workstation, edge compute, and physical robots depends on budget and requirements.

## Further Reading

- [NVIDIA Isaac Hardware Requirements](https://docs.nvidia.com/isaac/)
- [ROS 2 Hardware Guide](https://docs.ros.org/)
""",

    "hardware-infrastructure/digital-twin-workstation.md": """---
title: Digital Twin Workstation
sidebar_label: Digital Twin Workstation
sidebar_position: 2
description: Workstation specifications for running Isaac Sim and ROS 2
keywords: [workstation, NVIDIA RTX, Isaac Sim, ROS 2]
---

# Digital Twin Workstation

A digital twin workstation runs physics simulations, trains AI models, and tests robot behaviors virtually before deployment.

## Recommended Specifications

### Professional Setup ($3K-4.5K)

- **GPU**: NVIDIA RTX 4070 Ti (12GB) or RTX 4080 (16GB)
- **CPU**: Intel i7-13700K / AMD Ryzen 9 7900X
- **RAM**: 64GB DDR5
- **Storage**: 1TB NVMe SSD + 2TB data drive
- **OS**: Ubuntu 22.04 LTS

### Why These Specs?

**GPU**: Most critical component
- CUDA required for Isaac Sim, PyTorch
- RTX cores for ray tracing
- 12GB+ VRAM for complex scenes

**RAM**: 64GB recommended
- Ubuntu: 4-6GB
- Isaac Sim: 8-16GB
- ROS 2: 2-8GB
- AI training: 8-32GB

## Software Installation

### 1. NVIDIA Drivers

```bash
ubuntu-drivers devices
sudo ubuntu-drivers autoinstall
sudo reboot
```

### 2. CUDA Toolkit

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update && sudo apt install cuda-toolkit-12-4
```

### 3. ROS 2 Humble

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install ros-humble-desktop
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

## Performance Tips

```bash
# Monitor GPU
watch -n 1 nvidia-smi

# Enable performance mode
sudo nvidia-settings
```

## Summary

Prioritize GPU (RTX 4070 Ti+), 64GB RAM, and NVMe SSD. Ubuntu 22.04 with ROS 2 Humble provides the complete environment.

## Further Reading

- [Isaac Sim Requirements](https://docs.omniverse.nvidia.com/)
- [GPU Buying Guide](https://timdettmers.com/2023/01/30/which-gpu-for-deep-learning/)
""",

    "hardware-infrastructure/physical-ai-edge-kits.md": """---
title: Physical AI Edge Kits
sidebar_label: Physical AI Edge Kits
sidebar_position: 3
description: Edge devices for on-robot AI processing
keywords: [edge computing, NVIDIA Jetson, embedded systems]
---

# Physical AI Edge Kits

Edge kits are compact computers that run on robots for real-time AI inference and control.

## NVIDIA Jetson Platform

### Jetson Orin Nano ($499)

**Specs**:
- 6-core ARM CPU
- 1024-core NVIDIA GPU
- 8GB RAM
- 15-25W power

**Use Cases**:
- Mobile robots
- Drones
- Basic AI inference

### Jetson Orin NX ($699)

**Specs**:
- 8-core ARM CPU
- 1024-core GPU
- 16GB RAM
- 25W power

**Use Cases**:
- Quadruped robots
- Advanced perception
- Multi-sensor fusion

### Jetson AGX Orin ($1,999)

**Specs**:
- 12-core ARM CPU
- 2048-core GPU
- 64GB RAM
- 60W power

**Use Cases**:
- Humanoid robots
- Real-time VLA inference
- Complex planning

## Setup Guide

### 1. Flash JetPack

```bash
# Download SDK Manager
# Flash JetPack 6.0 with Ubuntu 22.04
```

### 2. Install ROS 2

```bash
sudo apt install ros-humble-ros-base
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

### 3. Optimize for Inference

```bash
# Enable max performance
sudo nvpmodel -m 0
sudo jetson_clocks
```

## AI Model Deployment

### TensorRT Optimization

```python
import tensorrt as trt

# Convert PyTorch to ONNX
torch.onnx.export(model, dummy_input, "model.onnx")

# Build TensorRT engine
# 5-10x faster inference
```

## Comparison Table

| Model | CPU | GPU | RAM | Power | Price |
|-------|-----|-----|-----|-------|-------|
| Orin Nano | 6-core | 1024 CUDA | 8GB | 15W | $499 |
| Orin NX | 8-core | 1024 CUDA | 16GB | 25W | $699 |
| AGX Orin | 12-core | 2048 CUDA | 64GB | 60W | $1999 |

## Summary

Jetson Orin series provides scalable edge AI from $499 to $1999. Choose based on robot power budget and AI workload complexity.

## Further Reading

- [Jetson Developer Zone](https://developer.nvidia.com/embedded/jetson)
- [TensorRT Documentation](https://docs.nvidia.com/deeplearning/tensorrt/)
""",
}

def write_content_file(filepath, content):
    """Write content to file"""
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Written: {filepath}")

# Write all content
for filepath, content in content_map.items():
    write_content_file(filepath, content)

print(f"\n✅ Generated {len(content_map)} content files!")
