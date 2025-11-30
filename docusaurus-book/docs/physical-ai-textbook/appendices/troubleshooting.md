---
title: Troubleshooting Guide
sidebar_label: Troubleshooting Guide
sidebar_position: 3
description: Common issues and solutions
keywords: [troubleshooting, debugging, FAQ]
---

# Troubleshooting Guide

## ROS 2 Issues

**Problem**: Nodes can't see each other

**Solution**: Check DDS discovery, firewall settings

**Problem**: Package not found

**Solution**: Source workspace: `source install/setup.bash`

## Gazebo Issues

**Problem**: Low FPS

**Solution**: Reduce sensor update rates, simplify models

**Problem**: Robot falls through ground

**Solution**: Check collision meshes, increase solver iterations

## Isaac Sim Issues

**Problem**: Out of VRAM

**Solution**: Reduce scene complexity, close other GPU apps

**Problem**: Crash on startup

**Solution**: Update NVIDIA drivers, check GPU compatibility

## General Tips

- Always check logs first
- Use `ros2 doctor` for health checks
- Update software regularly
- Check GitHub issues for known bugs
