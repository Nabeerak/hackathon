<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- Modified principles:
  - Added: AI/Spec-Driven Book Creation
  - Added: Integrated RAG Chatbot Development
  - Added: Reusable Intelligence (Subagents & Skills)
  - Added: Personalized Content & Authentication
  - Added: Multilingual Support
  - Added: Embodied Intelligence Focus
- Added sections:
  - Course Structure & Learning Outcomes
  - Hardware & Lab Infrastructure
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/templates/commands/*.md: ⚠ pending
- Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. AI/Spec-Driven Book Creation
Every feature in the book project must be created using Docusaurus and deployed to GitHub Pages. Spec-Kit Plus and Claude Code are the mandatory tools for the entire book creation process.

### II. Integrated RAG Chatbot Development
A Retrieval-Augmented Generation (RAG) chatbot must be built and embedded within the published book. This chatbot will utilize OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres database, and Qdrant Cloud Free Tier. It must be capable of answering user questions about the book's content, including questions based solely on text selected by the user.

### III. Reusable Intelligence (Subagents & Skills)
The project must actively create and utilize reusable intelligence via Claude Code Subagents and Agent Skills. This is a core mechanism for enhancing the book project and is crucial for achieving bonus points.

### IV. Personalized Content & Authentication
Signup and Signin functionality must be implemented using better-auth.com. During signup, the system must collect user software and hardware background information to enable personalized content delivery. Logged-in users must be able to personalize content within chapters by pressing a button at the start of each chapter.

### V. Multilingual Support
Logged-in users must be able to translate the content of chapters into Urdu by pressing a button at the start of each chapter.

### VI. Embodied Intelligence Focus
The textbook and accompanying course are fundamentally centered on AI systems operating in the physical world and the concept of embodied intelligence. The core goal is to bridge the gap between digital AI (the brain) and physical robotics (the body), enabling students to apply their AI knowledge to control Humanoid Robots in both simulated and real-world environments.

## Course Structure & Learning Outcomes

The course is structured around modules covering the Robotic Nervous System (ROS 2), Digital Twin (Gazebo & Unity), AI-Robot Brain (NVIDIA Isaac™), and Vision-Language-Action (VLA). Key learning outcomes include understanding Physical AI principles, mastering ROS 2, simulating robots with Gazebo and Unity, developing with NVIDIA Isaac, designing humanoid robots, and integrating GPT models for conversational robotics. The course also features a weekly breakdown covering introduction to Physical AI, ROS 2 fundamentals, robot simulation, NVIDIA Isaac platform, humanoid robot development, and conversational robotics.

## Hardware & Lab Infrastructure

This course is technically demanding, intersecting Physics Simulation (Isaac Sim/Gazebo), Visual Perception (SLAM/Computer Vision), and Generative AI (LLMs/VLA). Required hardware includes a "Digital Twin" Workstation (NVIDIA RTX 4070 Ti or higher GPU, Intel Core i7 13th Gen+ or AMD Ryzen 9 CPU, 64 GB DDR5 RAM, Ubuntu 22.04 LTS). Optional "Physical AI" Edge Kits (NVIDIA Jetson Orin Nano/NX, Intel RealSense D435i/D455, USB IMU, USB Microphone/Speaker array) and Robot Lab options (Unitree Go2 Edu, Unitree G1, Robotis OP3, Hiwonder TonyPi Pro) are also detailed. Cloud-Native Lab infrastructure using AWS/Azure instances with NVIDIA Isaac Sim on Omniverse Cloud is presented as an alternative for students without RTX-enabled workstations, though it introduces latency and cost complexities.

## Governance

This Constitution supersedes all other project practices. Amendments require documentation, approval, and a migration plan. All Pull Requests and reviews must verify compliance with these principles. Complexity must always be justified. The CLAUDE.md file provides runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-11-29 | **Last Amended**: 2025-11-29
