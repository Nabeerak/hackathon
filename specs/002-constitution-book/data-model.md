# Data Model: Physical AI & Humanoid Robotics Textbook

**Feature**: 002-constitution-book
**Created**: 2025-11-30
**Phase**: Phase 1 - Design

## Overview

This document defines the content structure and organization for the Physical AI & Humanoid Robotics textbook. Since this is a static documentation site, the "data model" represents the content hierarchy and metadata structure.

## Content Entities

### 1. Book

Represents the entire textbook as a cohesive unit.

**Attributes**:
- `title`: "Physical AI & Humanoid Robotics"
- `version`: "1.0.0"
- `baseUrl`: "/physical-ai-textbook"
- `lastUpdated`: ISO date string
- `authors`: List of contributors
- `chapters`: List of Chapter entities

**Relationships**:
- Has many Chapters
- Has one CourseStructure

**File Location**: `docs/physical-ai-textbook/index.md`

**Metadata (Frontmatter)**:
```yaml
---
title: Physical AI & Humanoid Robotics
sidebar_label: Introduction
sidebar_position: 1
---
```

### 2. Chapter

Represents a major topic area in the textbook.

**Attributes**:
- `id`: Unique identifier (slug)
- `title`: Chapter name
- `description`: Brief overview (2-3 sentences)
- `learningObjectives`: List of 3-5 objectives
- `sidebarPosition`: Order in navigation
- `sections`: List of Section entities
- `estimatedReadTime`: Minutes
- `prerequisites`: List of prerequisite chapter IDs
- `lastUpdated`: ISO date string

**Relationships**:
- Belongs to Book
- Has many Sections
- May reference other Chapters (prerequisites)

**File Location**: `docs/physical-ai-textbook/{chapter-slug}/index.md`

**Example**:
```yaml
---
title: ROS 2 Fundamentals
sidebar_label: ROS 2 Fundamentals
sidebar_position: 4
description: Learn the Robot Operating System 2 framework
---

# ROS 2 Fundamentals

## Learning Objectives

- Understand ROS 2 architecture and design principles
- Create and manage ROS 2 nodes, topics, and services
- Implement navigation stack for mobile robots
- Debug ROS 2 applications using command-line tools
- Build multi-robot communication systems

## Prerequisites

- Basic Linux command-line knowledge
- Python 3.8+ or C++17 programming experience
- Understanding of process communication concepts
```

**Validation Rules**:
- Must have 3-5 learning objectives
- Must have description < 500 characters
- sidebarPosition must be unique
- Must have at least 1 section

### 3. Section

Represents a subtopic within a chapter.

**Attributes**:
- `id`: Unique identifier (slug)
- `title`: Section name
- `chapterId`: Parent chapter ID
- `sidebarPosition`: Order within chapter
- `content`: Markdown content
- `codeExamples`: List of CodeExample entities
- `hardwareSpecs`: List of HardwareSpecification entities (if applicable)
- `lastUpdated`: ISO date string

**Relationships**:
- Belongs to Chapter
- Has many CodeExamples (optional)
- Has many HardwareSpecifications (optional)

**File Location**: `docs/physical-ai-textbook/{chapter-slug}/{section-slug}.md`

**Example**:
```yaml
---
title: Nodes and Topics
sidebar_label: Nodes and Topics
sidebar_position: 3
---

# Nodes and Topics

[Content here with explanations, diagrams, and examples]
```

**Validation Rules**:
- Must have unique slug within chapter
- Content must be at least 500 words
- sidebarPosition must be unique within chapter

### 4. CodeExample

Represents an executable code snippet with context.

**Attributes**:
- `id`: Unique identifier
- `title`: Brief description
- `language`: Programming language ("python", "cpp", "bash", "yaml")
- `prerequisites`: List of setup requirements
- `code`: Source code
- `expectedOutput`: Expected execution result
- `notes`: Additional context or warnings
- `sectionId`: Parent section ID

**Relationships**:
- Belongs to Section

**Markdown Structure**:
```markdown
## Example: Creating a ROS 2 Publisher Node

**Prerequisites**:
- ROS 2 Humble installed
- Workspace sourced: `source /opt/ros/humble/setup.bash`
- Package created: `ros2 pkg create --build-type ament_python my_robot_package`

**Code** (`talker.py`):
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Expected Output**:
```
[INFO] [minimal_publisher]: Publishing: "Hello World: 0"
[INFO] [minimal_publisher]: Publishing: "Hello World: 1"
[INFO] [minimal_publisher]: Publishing: "Hello World: 2"
...
```

**Validation Rules**:
- Must specify language
- Must include prerequisites if code requires setup
- Code must be syntactically valid (manual review)
- Should include expected output for clarity

### 5. HardwareSpecification

Represents equipment requirements or options.

**Attributes**:
- `id`: Unique identifier
- `category`: "workstation" | "edge-kit" | "robot-lab" | "cloud-native"
- `name`: Component or system name
- `components`: List of ComponentSpec entities
- `estimatedCost`: Price range
- `purpose`: What this hardware enables
- `alternatives`: List of alternative options
- `vendors`: List of vendor links

**Relationships**:
- Belongs to Section
- Has many ComponentSpecs

**Markdown Structure**:
```markdown
## Digital Twin Workstation Specifications

### Recommended Configuration

| Component | Specification | Purpose | Est. Cost |
|-----------|--------------|---------|-----------|
| GPU | NVIDIA RTX 4070 Ti (12GB VRAM) | Isaac Sim rendering, AI inference | $800 |
| CPU | Intel Core i7 13700K (16 cores) | Parallel simulation processing | $400 |
| RAM | 64GB DDR5-5600 | Large scene loading, multi-robot sim | $200 |
| Storage | 1TB NVMe SSD | Fast asset loading | $100 |
| OS | Ubuntu 22.04 LTS | ROS 2 compatibility | Free |

**Total Estimated Cost**: $1,500

**Minimum Configuration** (budget option):

| Component | Specification | Purpose | Est. Cost |
|-----------|--------------|---------|-----------|
| GPU | NVIDIA RTX 4060 Ti (8GB VRAM) | Basic Isaac Sim rendering | $450 |
| CPU | Intel Core i5 13400F (10 cores) | Simulation processing | $200 |
| RAM | 32GB DDR5-4800 | Essential simulation needs | $100 |
| Storage | 512GB NVMe SSD | Basic storage | $50 |
| OS | Ubuntu 22.04 LTS | ROS 2 compatibility | Free |

**Total Estimated Cost**: $800

### Alternative: Cloud-Native Setup

See [Cloud-Native Lab Infrastructure](./cloud-native-alternatives.md) for AWS/Azure options.
```

**Validation Rules**:
- Must include estimated cost
- Must explain purpose of each component
- Must provide at least 2 options (minimum + recommended, or alternatives)

### 6. LearningOutcome

Represents measurable skills or knowledge.

**Attributes**:
- `id`: Unique identifier
- `description`: What student will be able to do
- `bloomLevel`: Cognitive level ("remember", "understand", "apply", "analyze", "evaluate", "create")
- `assessmentCriteria`: How to verify achievement
- `chapterId`: Parent chapter ID
- `weekNumber`: Corresponding week in course (1-12)

**Relationships**:
- Belongs to Chapter
- Maps to WeeklyModule

**Markdown Structure**:
```markdown
## Learning Outcomes

By the end of this chapter, you will be able to:

1. **Create** ROS 2 nodes using Python and C++ (Apply)
   - *Assessment*: Build a publisher-subscriber system for sensor data

2. **Analyze** ROS 2 graph topology using command-line tools (Analyze)
   - *Assessment*: Debug communication issues in multi-node systems

3. **Implement** navigation stack for mobile robot simulation (Apply)
   - *Assessment*: Navigate robot through simulated environment autonomously
```

**Validation Rules**:
- Must use action verbs (Bloom's taxonomy)
- Must include assessment criteria
- Must be measurable

### 7. WeeklyModule

Represents one week of course instruction.

**Attributes**:
- `weekNumber`: 1-12
- `title`: Week theme
- `topics`: List of topics covered
- `chapters`: List of chapter IDs to read
- `labActivities`: List of hands-on exercises
- `deliverables`: What students submit
- `estimatedHours`: Study time required

**Relationships**:
- References multiple Chapters
- Has many LearningOutcomes

**File Location**: `docs/physical-ai-textbook/course-overview/weekly-breakdown.md`

**Markdown Structure**:
```markdown
## Week 1: Introduction to Physical AI

**Topics**:
- What is Physical AI and Embodied Intelligence?
- Overview of robotics stack: perception, planning, control
- Introduction to ROS 2 ecosystem

**Reading**:
- [Introduction to Physical AI](../introduction/what-is-physical-ai.md)
- [Embodied Intelligence Concepts](../introduction/embodied-intelligence.md)
- [ROS 2 Fundamentals - Introduction](../ros2-fundamentals/introduction.md)

**Lab Activities**:
1. Install Ubuntu 22.04 LTS (dual boot or VM)
2. Install ROS 2 Humble
3. Run turtlesim demo
4. Create first publisher/subscriber

**Deliverables**:
- Screenshot of turtlesim running
- Git repository with first ROS 2 nodes

**Estimated Hours**: 8-10 hours
```

**Validation Rules**:
- Must reference at least 1 chapter
- Must include lab activities
- estimatedHours must be 6-12 per week

### 8. CourseStructure

Represents overall course organization.

**Attributes**:
- `totalWeeks`: 12
- `modules`: List of WeeklyModule entities
- `prerequisites`: Course prerequisites
- `learningOutcomes`: Overall course outcomes
- `assessmentStrategy`: How students are evaluated

**Relationships**:
- Has many WeeklyModules
- References all Chapters

**File Location**: `docs/physical-ai-textbook/course-overview/index.md`

## Content Hierarchy

```
Book (index.md)
├── CourseStructure
│   ├── Learning Outcomes (learning-outcomes.md)
│   ├── Weekly Breakdown (weekly-breakdown.md)
│   └── Prerequisites (prerequisites.md)
├── Chapter: Hardware Infrastructure
│   ├── Section: Digital Twin Workstation
│   │   └── HardwareSpecification: Workstation configs
│   ├── Section: Physical AI Edge Kits
│   │   └── HardwareSpecification: Edge device options
│   ├── Section: Robot Lab Options
│   │   └── HardwareSpecification: Robot platforms
│   └── Section: Cloud-Native Alternatives
│       └── HardwareSpecification: AWS/Azure configs
├── Chapter: ROS 2 Fundamentals
│   ├── Section: Introduction
│   ├── Section: Installation
│   │   └── CodeExample: Install commands
│   ├── Section: Nodes and Topics
│   │   ├── CodeExample: Publisher node
│   │   └── CodeExample: Subscriber node
│   ├── Section: Services and Actions
│   │   └── CodeExample: Service client/server
│   └── Section: Navigation Stack
│       └── CodeExample: Nav2 configuration
├── Chapter: Digital Twin Simulation
│   ├── Section: Gazebo Basics
│   ├── Section: Unity Simulation
│   ├── Section: URDF Modeling
│   └── Section: Sensor Integration
├── Chapter: NVIDIA Isaac
│   ├── Section: Isaac Sim Introduction
│   ├── Section: Omniverse Setup
│   ├── Section: Robot Brain AI
│   └── Section: Perception Systems
├── Chapter: Vision-Language-Action
│   ├── Section: VLA Overview
│   ├── Section: Multimodal Models
│   ├── Section: Action Primitives
│   └── Section: Integration Patterns
└── Chapter: Humanoid Robotics
    ├── Section: Bipedal Locomotion
    ├── Section: Manipulation Control
    ├── Section: Conversational Robotics
    └── Section: GPT Integration
```

## File Naming Conventions

**Chapters**:
- Directory: `docs/physical-ai-textbook/{chapter-slug}/`
- Index: `index.md`
- Slug format: lowercase, hyphenated (e.g., `ros2-fundamentals`)

**Sections**:
- File: `docs/physical-ai-textbook/{chapter-slug}/{section-slug}.md`
- Slug format: lowercase, hyphenated (e.g., `nodes-and-topics`)

**Images**:
- Location: `static/img/physical-ai-textbook/{chapter-slug}/{image-name}.{ext}`
- Format: SVG (preferred), PNG, JPG
- Naming: descriptive, hyphenated (e.g., `ros2-architecture-diagram.svg`)

## Metadata Standards

All content files MUST include frontmatter:

```yaml
---
title: Display Title
sidebar_label: Short Label
sidebar_position: Number
description: Brief description for SEO
keywords: [keyword1, keyword2, keyword3]
last_updated: YYYY-MM-DD
---
```

**Required Fields**:
- `title`: Page title
- `sidebar_label`: Navigation label
- `sidebar_position`: Order in sidebar

**Optional Fields**:
- `description`: Meta description
- `keywords`: Search keywords
- `last_updated`: Maintenance tracking

## State Transitions

Content lifecycle states:

1. **Draft**: Initial content creation
2. **Review**: Technical accuracy review
3. **Published**: Merged to main branch
4. **Updated**: Content revised for accuracy
5. **Deprecated**: Marked as outdated (if needed)

**State Management**:
- Use Git branches for Draft state
- Use pull requests for Review state
- Main branch represents Published state
- Add update notices for Updated content

## Validation Rules Summary

### Chapter Validation
- ✅ Must have 3-5 learning objectives
- ✅ Must have 1+ sections
- ✅ Must have unique sidebar position
- ✅ Must have description < 500 chars

### Section Validation
- ✅ Must have minimum 500 words content
- ✅ Must have unique slug within chapter
- ✅ May include 0+ code examples

### Code Example Validation
- ✅ Must specify language
- ✅ Must include prerequisites if needed
- ✅ Should include expected output
- ✅ Must be syntactically valid

### Hardware Spec Validation
- ✅ Must include cost estimates
- ✅ Must explain component purpose
- ✅ Must provide 2+ configuration options

### Weekly Module Validation
- ✅ Must reference 1+ chapters
- ✅ Must include lab activities
- ✅ Must estimate 6-12 hours per week

## Integration Points

### Docusaurus Configuration

**Sidebar Definition** (`sidebars.ts`):
```typescript
const sidebars = {
  // Existing sidebars...

  physicalAiTextbook: [
    {
      type: 'doc',
      id: 'physical-ai-textbook/index',
      label: 'Introduction'
    },
    {
      type: 'category',
      label: 'Course Overview',
      items: [
        'physical-ai-textbook/course-overview/index',
        'physical-ai-textbook/course-overview/learning-outcomes',
        'physical-ai-textbook/course-overview/weekly-breakdown',
        'physical-ai-textbook/course-overview/prerequisites'
      ]
    },
    {
      type: 'category',
      label: 'Hardware & Infrastructure',
      items: [
        'physical-ai-textbook/hardware-infrastructure/index',
        'physical-ai-textbook/hardware-infrastructure/digital-twin-workstation',
        'physical-ai-textbook/hardware-infrastructure/physical-ai-edge-kits',
        'physical-ai-textbook/hardware-infrastructure/robot-lab-options',
        'physical-ai-textbook/hardware-infrastructure/cloud-native-alternatives'
      ]
    },
    // Additional chapters...
  ]
};
```

### Search Integration

Search plugin configuration (verify in `docusaurus.config.ts`):
```typescript
[
  '@easyops-cn/docusaurus-search-local',
  {
    hashed: true,
    indexDocs: true,
    indexBlog: false,
    docsRouteBasePath: '/',
    highlightSearchTermsOnTargetPage: true,
    searchResultLimits: 8,
    searchResultContextMaxLength: 50
  }
]
```

## Summary

This data model defines the complete content structure for the Physical AI & Humanoid Robotics textbook. All entities map to Markdown files with YAML frontmatter, organized hierarchically for Docusaurus rendering. Validation rules ensure content quality and consistency.
