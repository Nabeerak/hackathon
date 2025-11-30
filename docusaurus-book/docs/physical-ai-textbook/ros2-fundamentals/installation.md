---
title: Installation & Setup
sidebar_label: Installation & Setup
sidebar_position: 2
description: Installing ROS 2 Humble on Ubuntu 22.04
keywords: [ROS 2, installation, Ubuntu]
---

# Installation & Setup

Install ROS 2 Humble on Ubuntu 22.04.

## Prerequisites

```bash
sudo apt update && sudo apt upgrade -y
```

## Add ROS 2 Repository

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
```

## Install ROS 2 Humble

```bash
sudo apt update
sudo apt install ros-humble-desktop
```

## Setup Environment

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Verify Installation

```bash
ros2 run demo_nodes_cpp talker
# Open new terminal
ros2 run demo_nodes_cpp listener
```

## Summary

ROS 2 Humble is now installed and ready for development.
