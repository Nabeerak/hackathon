---
title: Reusable Intelligence (Subagents & Skills)
sidebar_label: Reusable Intelligence
sidebar_position: 4
description: Creating and utilizing Claude Code Subagents and Agent Skills for textbook enhancement
keywords: [subagents, skills, Claude Code, reusable intelligence, AI agents]
---

# Reusable Intelligence (Subagents & Skills)

## Introduction

This chapter covers the creation and utilization of reusable intelligence through Claude Code Subagents and Agent Skills. This is a core mechanism for enhancing the Physical AI & Humanoid Robotics textbook project and achieving the advanced capabilities outlined in the constitution.

## What are Subagents and Skills?

### Subagents
**Subagents** are specialized AI assistants that handle specific tasks within the textbook ecosystem:
- **Content Generation Subagent**: Creates new textbook content
- **Code Review Subagent**: Validates code examples and exercises
- **Translation Subagent**: Handles multilingual content conversion
- **Debugging Subagent**: Helps troubleshoot code examples
- **Assessment Subagent**: Creates quizzes and exercises

### Skills
**Skills** are reusable functions that agents can use to perform specific actions:
- **Document Processing**: Reading, parsing, and analyzing textbook content
- **Code Generation**: Creating ROS 2, Python, and C++ examples
- **Simulation Integration**: Interfacing with Gazebo, Unity, and Isaac Sim
- **Testing Framework**: Running code examples and validating results
- **User Interaction**: Handling Q&A, feedback, and learning progression

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Main Agent    │───▶│   Subagent       │───▶│   Skill         │
│   (Textbook     │    │   (Content       │    │   (Code         │
│   Manager)      │    │   Generation)    │    │   Generation)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Knowledge     │    │   Task Specific  │    │   Reusable      │
│   Base          │    │   Logic          │    │   Functions     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Claude Code Subagent Implementation

### Content Generation Subagent

```python
# content_generation_subagent.py
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
import re

@dataclass
class ContentRequest:
    topic: str
    difficulty: str  # beginner, intermediate, advanced
    content_type: str  # explanation, code, exercise, example
    target_audience: str  # software_engineer, hardware_engineer, student, etc.
    prerequisites: List[str] = None
    learning_objectives: List[str] = None

@dataclass
class ContentResponse:
    title: str
    content: str
    metadata: Dict[str, any]
    quality_score: float
    generated_at: str

class ContentGenerationSubagent:
    def __init__(self, claude_client, textbook_knowledge_base):
        self.claude_client = claude_client
        self.knowledge_base = textbook_knowledge_base
        self.name = "ContentGenerationSubagent"
        
    async def generate_content(self, request: ContentRequest) -> ContentResponse:
        """Generate educational content based on request parameters."""
        
        # Build context from knowledge base
        context = await self._build_context(request)
        
        # Construct prompt for Claude
        prompt = self._construct_prompt(request, context)
        
        # Generate content using Claude
        response = await self.claude_client.generate(prompt)
        
        # Validate and format response
        validated_content = self._validate_content(response, request)
        
        return ContentResponse(
            title=self._extract_title(response),
            content=validated_content,
            metadata={
                "topic": request.topic,
                "difficulty": request.difficulty,
                "content_type": request.content_type,
                "target_audience": request.target_audience,
                "prerequisites": request.prerequisites or [],
                "learning_objectives": request.learning_objectives or [],
            },
            quality_score=self._calculate_quality_score(validated_content),
            generated_at=str(response.timestamp)
        )
    
    async def _build_context(self, request: ContentRequest) -> str:
        """Build context from knowledge base based on request."""
        context_parts = []
        
        # Add general topic context
        topic_context = await self.knowledge_base.search(f"topic:{request.topic}")
        context_parts.append(f"Topic Context:\n{topic_context}")
        
        # Add difficulty-specific guidelines
        difficulty_guidelines = await self.knowledge_base.get_difficulty_guidelines(request.difficulty)
        context_parts.append(f"Difficulty Guidelines:\n{difficulty_guidelines}")
        
        # Add target audience guidelines
        audience_guidelines = await self.knowledge_base.get_audience_guidelines(request.target_audience)
        context_parts.append(f"Audience Guidelines:\n{audience_guidelines}")
        
        # Add prerequisite content if specified
        if request.prerequisites:
            prereq_content = await self.knowledge_base.search_multi(request.prerequisites)
            context_parts.append(f"Prerequisite Content:\n{prereq_content}")
        
        return "\n\n".join(context_parts)
    
    def _construct_prompt(self, request: ContentRequest, context: str) -> str:
        """Construct the prompt for Claude based on request and context."""
        prompt = f"""
        {context}
        
        Generate educational content for the Physical AI & Humanoid Robotics textbook.
        
        Requirements:
        - Topic: {request.topic}
        - Difficulty Level: {request.difficulty}
        - Content Type: {request.content_type}
        - Target Audience: {request.target_audience}
        - Learning Objectives: {', '.join(request.learning_objectives or [])}
        - Prerequisites: {', '.join(request.prerequisites or [])}
        
        Content should be:
        - Technically accurate
        - Educationally appropriate for the difficulty level
        - Relevant to Physical AI and robotics
        - Include practical examples where applicable
        - Follow textbook format and style
        
        Generate the content now:
        """
        return prompt
    
    def _validate_content(self, response: str, request: ContentRequest) -> str:
        """Validate generated content meets requirements."""
        content = response.strip()
        
        # Check for basic requirements
        if request.content_type == "code":
            if "```" not in content:
                # Add code block formatting
                content = f"```python\n{content}\n```"
        
        # Add educational elements if missing
        if request.content_type == "explanation" and "summary" not in content.lower():
            content += "\n\n## Summary\nKey points covered in this section."
        
        return content
    
    def _extract_title(self, content: str) -> str:
        """Extract or generate a title from content."""
        # Look for markdown header
        match = re.search(r'^# (.+)', content, re.MULTILINE)
        if match:
            return match.group(1)
        
        # Generate title based on content
        first_sentence = content.split('\n')[0].strip()
        if len(first_sentence) > 50:
            return first_sentence[:50] + "..."
        return first_sentence
    
    def _calculate_quality_score(self, content: str) -> float:
        """Calculate a basic quality score for the generated content."""
        score = 0.0
        
        # Check for code blocks
        if "```" in content:
            score += 0.2
        
        # Check for headers
        if "#" in content:
            score += 0.2
        
        # Check for educational elements
        if any(word in content.lower() for word in ["summary", "review", "example", "exercise"]):
            score += 0.3
        
        # Check content length (not too short)
        if len(content) > 200:
            score += 0.3
        
        return min(score, 1.0)  # Cap at 1.0
```

### Code Review Subagent

```python
# code_review_subagent.py
import re
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class CodeReviewRequest:
    code: str
    language: str  # python, cpp, etc.
    context: str  # surrounding content or purpose
    textbook_section: str

@dataclass
class CodeReviewIssue:
    severity: str  # critical, high, medium, low
    type: str  # bug, style, performance, security
    line_number: Optional[int]
    description: str
    suggestion: str

@dataclass
class CodeReviewResponse:
    original_code: str
    review_issues: List[CodeReviewIssue]
    suggested_improvements: str
    overall_score: float
    compliance: Dict[str, bool]  # ROS 2, safety, performance compliance

class CodeReviewSubagent:
    def __init__(self, claude_client):
        self.claude_client = claude_client
        self.name = "CodeReviewSubagent"
        
    async def review_code(self, request: CodeReviewRequest) -> CodeReviewResponse:
        """Review code for educational quality and technical accuracy."""
        
        # Analyze code for common issues
        issues = self._analyze_code(request.code, request.language)
        
        # Generate suggestions for improvements
        suggestions = await self._generate_suggestions(request, issues)
        
        # Calculate compliance scores
        compliance = self._check_compliance(request.code, request.textbook_section)
        
        return CodeReviewResponse(
            original_code=request.code,
            review_issues=issues,
            suggested_improvements=suggestions,
            overall_score=self._calculate_overall_score(issues),
            compliance=compliance
        )
    
    def _analyze_code(self, code: str, language: str) -> List[CodeReviewIssue]:
        """Analyze code for common issues."""
        issues = []
        
        # Language-specific analysis
        if language == "python":
            issues.extend(self._analyze_python_code(code))
        elif language == "cpp":
            issues.extend(self._analyze_cpp_code(code))
        
        # General analysis
        issues.extend(self._analyze_general_issues(code))
        
        # Educational quality analysis
        issues.extend(self._analyze_educational_quality(code))
        
        return issues
    
    def _analyze_python_code(self, code: str) -> List[CodeReviewIssue]:
        """Analyze Python-specific issues."""
        issues = []
        
        # Check for ROS 2 Python imports
        ros_imports = ["rclpy", "std_msgs", "geometry_msgs", "nav_msgs"]
        has_ros_imports = any(imp in code for imp in ros_imports)
        
        if not has_ros_imports and "ROS" in code.upper():
            issues.append(CodeReviewIssue(
                severity="high",
                type="dependency",
                line_number=None,
                description="ROS 2 Python imports missing",
                suggestion="Add required ROS 2 Python imports (rclpy, std_msgs, etc.)"
            ))
        
        # Check for proper rclpy lifecycle
        if "rclpy.init" in code and "rclpy.shutdown" not in code:
            issues.append(CodeReviewIssue(
                severity="medium",
                type="lifecycle",
                line_number=None,
                description="rclpy.shutdown() missing",
                suggestion="Add rclpy.shutdown() for proper cleanup in main()"
            ))
        
        # Check for try/except blocks for safety
        if "rclpy" in code and "try:" not in code and "except:" not in code:
            issues.append(CodeReviewIssue(
                severity="medium",
                type="safety",
                line_number=None,
                description="Missing error handling",
                suggestion="Add try-except blocks for robust error handling"
            ))
        
        return issues
    
    def _analyze_educational_quality(self, code: str) -> List[CodeReviewIssue]:
        """Analyze code for educational quality."""
        issues = []
        
        # Check for adequate comments
        lines = code.split('\n')
        comment_lines = [line for line in lines if line.strip().startswith('#')]
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        
        if code_lines and comment_lines:
            comment_ratio = len(comment_lines) / len(code_lines)
            if comment_ratio < 0.1:  # Less than 10% comments
                issues.append(CodeReviewIssue(
                    severity="medium",
                    type="documentation",
                    line_number=None,
                    description="Insufficient code comments",
                    suggestion="Add comments explaining key concepts and logic"
                ))
        
        # Check for educational elements
        if "TODO" in code or "FIXME" in code:
            issues.append(CodeReviewIssue(
                severity="high",
                type="quality",
                line_number=None,
                description="Educational content contains TODO or FIXME",
                suggestion="Replace TODO/FIXME with complete, educational content"
            ))
        
        return issues
    
    async def _generate_suggestions(self, request: CodeReviewRequest, issues: List[CodeReviewIssue]) -> str:
        """Generate detailed suggestions for code improvements."""
        if not issues:
            return "Code looks good! No issues found."
        
        prompt = f"""
        You are an expert code reviewer for the Physical AI & Humanoid Robotics textbook.
        Review this code and provide suggestions for improvement:
        
        Code:
        {request.code}
        
        Issues Found:
        {self._format_issues(issues)}
        
        Provide detailed suggestions for improvement, considering educational value for students.
        """
        
        response = await self.claude_client.generate(prompt)
        return response
    
    def _format_issues(self, issues: List[CodeReviewIssue]) -> str:
        """Format issues for prompt."""
        formatted = []
        for issue in issues:
            formatted.append(f"- {issue.severity.upper()}: {issue.description} (Type: {issue.type})")
        return "\n".join(formatted)
    
    def _check_compliance(self, code: str, section: str) -> Dict[str, bool]:
        """Check code compliance with textbook standards."""
        compliance = {
            "ros2_compliant": False,
            "safety_protocols": False,
            "educational_appropriate": True,
            "performance_optimal": False
        }
        
        # Check for ROS 2 compliance
        compliance["ros2_compliant"] = "rclpy.init" in code and "rclpy.shutdown" in code
        
        # Check for safety protocols
        compliance["safety_protocols"] = any([
            "try:" in code, "except:" in code,
            "if __name__ == '__main__':" in code,
            "main()" in code
        ])
        
        # Check for performance considerations
        compliance["performance_optimal"] = "async" in code or "threading" in code or "multiprocessing" in code
        
        return compliance
    
    def _calculate_overall_score(self, issues: List[CodeReviewIssue]) -> float:
        """Calculate overall code quality score."""
        if not issues:
            return 1.0
        
        critical_count = len([i for i in issues if i.severity == "critical"])
        high_count = len([i for i in issues if i.severity == "high"])
        medium_count = len([i for i in issues if i.severity == "medium"])
        low_count = len([i for i in issues if i.severity == "low"])
        
        score = 1.0
        score -= critical_count * 0.3  # Critical issues heavily penalize
        score -= high_count * 0.1
        score -= medium_count * 0.05
        score -= low_count * 0.01
        
        return max(0.0, score)  # Minimum 0.0
```

## Agent Skill System

### Core Skills Implementation

```python
# skills/core_skills.py
import os
import asyncio
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class Skill(ABC):
    """Base class for all skills."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the skill with given parameters."""
        pass

class DocumentProcessingSkill(Skill):
    """Skill for processing and analyzing documents."""
    
    def __init__(self):
        super().__init__(
            name="document_processing",
            description="Process and analyze textbook documents"
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Process document content."""
        document_path = kwargs.get("document_path")
        content = kwargs.get("content")
        
        if document_path and os.path.exists(document_path):
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        if not content:
            return {"error": "No content provided"}
        
        # Analyze document structure
        analysis = {
            "word_count": len(content.split()),
            "sentence_count": len(content.split('.')),
            "paragraph_count": len(content.split('\n\n')),
            "has_code_blocks": '```' in content,
            "has_headers": '#' in content,
            "reading_time": len(content.split()) / 200,  # Rough estimate at 200 wpm
        }
        
        return analysis

class CodeGenerationSkill(Skill):
    """Skill for generating code examples."""
    
    def __init__(self, claude_client):
        super().__init__(
            name="code_generation",
            description="Generate educational code examples"
        )
        self.claude_client = claude_client
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Generate code based on specifications."""
        topic = kwargs.get("topic")
        language = kwargs.get("language", "python")
        purpose = kwargs.get("purpose", "example")
        
        prompt = f"""
        Generate a {language} code example for {topic}.
        The code should be educational and demonstrate key concepts.
        Purpose: {purpose}
        
        Include:
        - Clear comments explaining the code
        - Proper structure and formatting
        - Error handling where appropriate
        - Follow best practices for the language
        """
        
        try:
            generated_code = await self.claude_client.generate(prompt)
            return {
                "code": generated_code,
                "language": language,
                "topic": topic,
                "purpose": purpose
            }
        except Exception as e:
            return {"error": f"Code generation failed: {str(e)}"}

class SimulationIntegrationSkill(Skill):
    """Skill for integrating with simulation frameworks."""
    
    def __init__(self):
        super().__init__(
            name="simulation_integration",
            description="Integrate with Gazebo, Unity, and Isaac Sim"
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Generate simulation configuration or code."""
        sim_platform = kwargs.get("platform")  # gazebo, unity, isaac
        task = kwargs.get("task")  # setup, configuration, integration
        
        if sim_platform == "gazebo" and task == "robot_model":
            return self._generate_gazebo_robot_config(**kwargs)
        elif sim_platform == "unity" and task == "robot_model":
            return self._generate_unity_robot_config(**kwargs)
        elif sim_platform == "isaac" and task == "robot_model":
            return self._generate_isaac_robot_config(**kwargs)
        
        return {"error": f"Unsupported simulation task: {sim_platform}/{task}"}
    
    def _generate_gazebo_robot_config(self, **kwargs) -> Dict[str, Any]:
        """Generate Gazebo robot configuration."""
        robot_name = kwargs.get("robot_name", "my_robot")
        
        urdf_content = f"""
<?xml version="1.0"?>
<robot name="{robot_name}">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>
</robot>
        """
        
        return {
            "platform": "gazebo",
            "robot_name": robot_name,
            "config_type": "urdf",
            "content": urdf_content,
            "file_extension": ".urdf"
        }

class AssessmentGenerationSkill(Skill):
    """Skill for generating quizzes and exercises."""
    
    def __init__(self, claude_client):
        super().__init__(
            name="assessment_generation",
            description="Generate quizzes, exercises, and assessments"
        )
        self.claude_client = claude_client
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Generate assessment content."""
        topic = kwargs.get("topic")
        difficulty = kwargs.get("difficulty", "intermediate")
        question_type = kwargs.get("type", "multiple_choice")
        count = kwargs.get("count", 3)
        
        prompt = f"""
        Generate {count} {question_type} questions about {topic} for {difficulty} level students.
        
        For multiple choice, include:
        - Question text
        - 4 answer choices
        - Correct answer
        - Brief explanation
        
        For coding exercises, include:
        - Problem description
        - Expected outcome
        - Hints for solving
        """
        
        try:
            assessment_content = await self.claude_client.generate(prompt)
            return {
                "topic": topic,
                "difficulty": difficulty,
                "type": question_type,
                "count": count,
                "content": assessment_content,
                "format": "educational_assessment"
            }
        except Exception as e:
            return {"error": f"Assessment generation failed: {str(e)}"}
```

## Skill Registry and Execution Framework

### Skill Registry

```python
# skill_registry.py
from typing import Dict, Type, List
from .skills.core_skills import Skill

class SkillRegistry:
    """Registry for managing and executing skills."""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.skill_classes: Dict[str, Type[Skill]] = {}
    
    def register_skill(self, skill: Skill):
        """Register a skill instance."""
        self.skills[skill.name] = skill
    
    def register_skill_class(self, name: str, skill_class: Type[Skill]):
        """Register a skill class for later instantiation."""
        self.skill_classes[name] = skill_class
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a registered skill."""
        return self.skills.get(name)
    
    async def execute_skill(self, name: str, **kwargs) -> Any:
        """Execute a skill with given parameters."""
        skill = self.get_skill(name)
        if not skill:
            raise ValueError(f"Skill '{name}' not found")
        
        return await skill.execute(**kwargs)
    
    def list_skills(self) -> List[str]:
        """List all registered skills."""
        return list(self.skills.keys())
    
    def initialize_default_skills(self, claude_client):
        """Initialize default skills for the textbook project."""
        from .skills.core_skills import (
            DocumentProcessingSkill, 
            CodeGenerationSkill, 
            SimulationIntegrationSkill, 
            AssessmentGenerationSkill
        )
        
        self.register_skill(DocumentProcessingSkill())
        self.register_skill(CodeGenerationSkill(claude_client))
        self.register_skill(SimulationIntegrationSkill())
        self.register_skill(AssessmentGenerationSkill(claude_client))

# Global skill registry
skill_registry = SkillRegistry()
```

## Agent Orchestration

### Main Agent Controller

```python
# agent_controller.py
from typing import Dict, Any, Optional
from .content_generation_subagent import ContentGenerationSubagent
from .code_review_subagent import CodeReviewSubagent
from .skill_registry import skill_registry

class TextbookAgentController:
    """Main controller for managing textbook enhancement agents."""
    
    def __init__(self, claude_client, knowledge_base):
        self.claude_client = claude_client
        self.knowledge_base = knowledge_base
        self.subagents = {}
        self.skill_registry = skill_registry
        
        # Initialize subagents
        self._initialize_subagents()
        
        # Initialize skills
        self.skill_registry.initialize_default_skills(claude_client)
    
    def _initialize_subagents(self):
        """Initialize all subagents."""
        self.subagents["content_generation"] = ContentGenerationSubagent(
            self.claude_client, 
            self.knowledge_base
        )
        
        self.subagents["code_review"] = CodeReviewSubagent(
            self.claude_client
        )
    
    async def generate_textbook_content(self, topic: str, **kwargs) -> Dict[str, Any]:
        """Generate textbook content using the content generation subagent."""
        request = {
            "topic": topic,
            "difficulty": kwargs.get("difficulty", "intermediate"),
            "content_type": kwargs.get("content_type", "explanation"),
            "target_audience": kwargs.get("target_audience", "student"),
            "prerequisites": kwargs.get("prerequisites", []),
            "learning_objectives": kwargs.get("learning_objectives", []),
        }
        
        # Convert to ContentRequest object
        from .content_generation_subagent import ContentRequest
        content_request = ContentRequest(**request)
        
        subagent = self.subagents["content_generation"]
        response = await subagent.generate_content(content_request)
        
        return {
            "title": response.title,
            "content": response.content,
            "metadata": response.metadata,
            "quality_score": response.quality_score
        }
    
    async def review_code(self, code: str, **kwargs) -> Dict[str, Any]:
        """Review code using the code review subagent."""
        request = {
            "code": code,
            "language": kwargs.get("language", "python"),
            "context": kwargs.get("context", ""),
            "textbook_section": kwargs.get("textbook_section", ""),
        }
        
        from .code_review_subagent import CodeReviewRequest
        code_request = CodeReviewRequest(**request)
        
        subagent = self.subagents["code_review"]
        response = await subagent.review_code(code_request)
        
        return {
            "original_code": response.original_code,
            "issues": [
                {
                    "severity": issue.severity,
                    "type": issue.type,
                    "description": issue.description,
                    "suggestion": issue.suggestion
                }
                for issue in response.review_issues
            ],
            "suggestions": response.suggested_improvements,
            "overall_score": response.overall_score,
            "compliance": response.compliance
        }
    
    async def execute_skill(self, skill_name: str, **kwargs) -> Any:
        """Execute a registered skill."""
        return await self.skill_registry.execute_skill(skill_name, **kwargs)
    
    async def enhance_chapter(self, chapter_content: str, chapter_topic: str) -> Dict[str, Any]:
        """Enhance a chapter using multiple agents and skills."""
        
        enhancements = {
            "original_content": chapter_content,
            "generated_examples": [],
            "code_quality_improvements": [],
            "additional_exercises": [],
            "content_quality": 0.0
        }
        
        # Process code blocks in the chapter
        code_blocks = self._extract_code_blocks(chapter_content)
        for code_block in code_blocks:
            review_result = await self.review_code(
                code_block, 
                context=chapter_topic
            )
            
            enhancements["code_quality_improvements"].append({
                "original": code_block,
                "reviews": review_result["issues"],
                "suggestions": review_result["suggestions"]
            })
        
        # Generate additional examples
        example_request = {
            "topic": chapter_topic,
            "content_type": "example",
            "difficulty": "intermediate",
            "target_audience": "student"
        }
        
        from .content_generation_subagent import ContentRequest
        content_request = ContentRequest(**example_request)
        example_subagent = self.subagents["content_generation"]
        example_response = await example_subagent.generate_content(content_request)
        
        enhancements["generated_examples"].append({
            "title": example_response.title,
            "content": example_response.content
        })
        
        # Generate exercises
        exercise_result = await self.execute_skill(
            "assessment_generation",
            topic=chapter_topic,
            difficulty="intermediate",
            type="multiple_choice",
            count=5
        )
        
        enhancements["additional_exercises"].append(exercise_result)
        
        # Calculate overall quality improvement
        enhancements["content_quality"] = (
            example_response.quality_score * 0.4 +
            (1 - len(code_blocks) * 0.1) * 0.6  # Less issues = higher quality
        )
        
        return enhancements
    
    def _extract_code_blocks(self, content: str) -> List[str]:
        """Extract code blocks from content."""
        import re
        pattern = r'```.*?\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches

# Global agent controller
agent_controller: Optional[TextbookAgentController] = None

def initialize_agent_controller(claude_client, knowledge_base):
    """Initialize the global agent controller."""
    global agent_controller
    agent_controller = TextbookAgentController(claude_client, knowledge_base)
    return agent_controller
```

## Integration with Textbook Workflow

### Chapter Enhancement Pipeline

```python
# chapter_enhancement_pipeline.py
from typing import Dict, Any
import asyncio
from .agent_controller import agent_controller

class ChapterEnhancementPipeline:
    """Pipeline for enhancing textbook chapters using agents."""
    
    async def process_chapter(self, chapter_path: str) -> Dict[str, Any]:
        """Process a chapter file with agent enhancements."""
        # Read chapter content
        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract topic from file path or frontmatter
        topic = self._extract_topic(chapter_path)
        
        # Enhance the chapter
        enhancements = await agent_controller.enhance_chapter(content, topic)
        
        # Create enhanced chapter
        enhanced_content = self._apply_enhancements(content, enhancements)
        
        # Save enhanced chapter
        enhanced_path = chapter_path.replace('.md', '_enhanced.md')
        with open(enhanced_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        return {
            "original_path": chapter_path,
            "enhanced_path": enhanced_path,
            "topic": topic,
            "enhancements": enhancements
        }
    
    def _extract_topic(self, file_path: str) -> str:
        """Extract topic from file path."""
        import re
        # Extract from path like 'ros2-fundamentals/nodes-topics.md'
        match = re.search(r'([^/\\]+)[/\\]([^/\\]+)\.md', file_path.replace('\\', '/'))
        if match:
            return f"{match.group(1)}: {match.group(2)}"
        return "unknown"
    
    def _apply_enhancements(self, original_content: str, enhancements: Dict[str, Any]) -> str:
        """Apply enhancements to original content."""
        enhanced_content = original_content
        
        # Add generated examples
        for example in enhancements["generated_examples"]:
            enhanced_content += f"\n\n## Additional Example: {example['title']}\n\n{example['content']}"
        
        # Add exercises
        for exercise in enhancements["additional_exercises"]:
            enhanced_content += f"\n\n## Practice Exercises\n\n{exercise['content']}"
        
        return enhanced_content

# Example usage
async def enhance_chapter_with_agents(chapter_path: str):
    """Enhance a chapter using the agent pipeline."""
    pipeline = ChapterEnhancementPipeline()
    result = await pipeline.process_chapter(chapter_path)
    return result
```

## Claude Code Integration

### Claude Code Task Automation

```python
# claude_code_integration.py
from typing import Dict, List
import asyncio

class ClaudeCodeIntegration:
    """Integration with Claude Code for task automation."""
    
    def __init__(self, claude_client):
        self.claude_client = claude_client
    
    async def create_subagent(self, agent_description: str) -> str:
        """Create a new subagent based on description."""
        prompt = f"""
        Create a Claude Code subagent for the Physical AI & Humanoid Robotics textbook project.
        
        Description: {agent_description}
        
        Requirements:
        - Inherit from the Skill base class
        - Follow the pattern shown in existing agents
        - Be specific to robotics/AI education
        - Include proper error handling
        - Be modular and reusable
        
        Return only the Python code for the subagent class.
        """
        
        code = await self.claude_client.generate(prompt)
        return code
    
    async def optimize_existing_agent(self, agent_name: str, requirements: List[str]) -> str:
        """Optimize an existing agent based on requirements."""
        current_code = await self.get_agent_code(agent_name)
        
        prompt = f"""
        Optimize the following Claude Code agent based on these requirements:
        {', '.join(requirements)}
        
        Current code:
        {current_code}
        
        Please return an optimized version that meets the requirements.
        """
        
        optimized_code = await self.claude_client.generate(prompt)
        return optimized_code
    
    async def get_agent_code(self, agent_name: str) -> str:
        """Get the current code for an agent."""
        # This would typically load from files or a code repository
        # For this example, we'll return a placeholder
        return f"# Code for {agent_name} agent"
    
    async def generate_skill(self, skill_purpose: str) -> str:
        """Generate a new skill for the agent system."""
        prompt = f"""
        Create a Claude Code skill for the Physical AI & Humanoid Robotics textbook project.
        
        Purpose: {skill_purpose}
        
        Requirements:
        - Inherit from the Skill base class
        - Include async execute method
        - Handle errors gracefully
        - Be specific to robotics/AI education
        - Include type hints
        - Be reusable across different agents
        
        Return only the Python code for the skill class.
        """
        
        skill_code = await self.claude_client.generate(prompt)
        return skill_code
```

## Practical Examples

### Example 1: Creating a Debugging Subagent

```python
# Example usage of the system
import asyncio
from .agent_controller import initialize_agent_controller, agent_controller

async def create_custom_debugging_subagent():
    """Create a specialized debugging subagent for ROS 2 issues."""
    
    # Create the subagent using Claude Code
    integration = ClaudeCodeIntegration(claude_client)
    
    agent_code = await integration.create_subagent(
        "A subagent that helps debug ROS 2 code issues commonly found in textbook examples. "
        "It should identify common ROS 2 mistakes, suggest fixes, and provide educational "
        "explanations about why the issues occur."
    )
    
    print("Generated Debugging Subagent Code:")
    print(agent_code)
    
    # Now register the subagent with the controller
    # (In a real implementation, you'd import and register it)
    
    return agent_code

async def demonstrate_content_generation():
    """Demonstrate content generation with agents."""
    
    # Initialize the agent controller (assuming we have clients)
    # controller = initialize_agent_controller(claude_client, knowledge_base)
    
    # Generate content
    content = await agent_controller.generate_textbook_content(
        topic="ROS 2 Services",
        difficulty="intermediate",
        content_type="explanation",
        target_audience="student"
    )
    
    print(f"Generated content for {content['metadata']['topic']}")
    print(f"Quality score: {content['quality_score']}")
    print(f"Title: {content['title']}")
    
    return content

# Run examples
async def main():
    # Demonstrate agent capabilities
    await demonstrate_content_generation()
    
    # Create custom subagent
    await create_custom_debugging_subagent()

# Uncomment to run
# asyncio.run(main())
```

### Example 2: Using Skills for Textbook Enhancement

```python
# Example of using skills to enhance textbook content
async def enhance_textbook_with_skills():
    """Enhance textbook content using registered skills."""
    
    # Example: Generate code for ROS 2 node
    code_result = await agent_controller.execute_skill(
        "code_generation",
        topic="Creating a ROS 2 Publisher Node",
        language="python",
        purpose="educational_example"
    )
    
    print("Generated code:")
    print(code_result["code"])
    
    # Process the generated content
    doc_analysis = await agent_controller.execute_skill(
        "document_processing",
        content=code_result["code"]
    )
    
    print("\nDocument analysis:")
    for key, value in doc_analysis.items():
        print(f"{key}: {value}")
    
    # Generate exercises for the topic
    exercises = await agent_controller.execute_skill(
        "assessment_generation",
        topic="ROS 2 Publisher Nodes",
        difficulty="intermediate",
        type="coding_exercise",
        count=2
    )
    
    print(f"\nGenerated exercises for {exercises['topic']}:")
    print(exercises['content'])
    
    return {
        "generated_code": code_result,
        "analysis": doc_analysis,
        "exercises": exercises
    }

# Uncomment to run
# asyncio.run(enhance_textbook_with_skills())
```

## Summary

The Reusable Intelligence system provides:

- ✅ Claude Code Subagents for specialized tasks (content generation, code review, etc.)
- ✅ Reusable Skills for common operations (document processing, code generation)
- ✅ Agent orchestration framework for managing complex workflows
- ✅ Integration with Claude Code for automated agent creation
- ✅ Modular design allowing easy extension of capabilities
- ✅ Educational focus aligned with Physical AI textbook goals

## Implementation Steps

1. **Initialize Skill Registry**: Set up the skill registry system
2. **Create Base Subagents**: Implement core subagents (content generation, code review)
3. **Develop Skills**: Create reusable skills for common operations
4. **Build Agent Controller**: Create the main orchestration system
5. **Integrate with Claude**: Connect to Claude Code API for AI capabilities
6. **Test Workflows**: Validate agent workflows with textbook content
7. **Deploy**: Integrate into the textbook generation pipeline

## Next Steps

- Integrate with the RAG chatbot for agent-powered responses
- Create Claude Code subagents for specific textbook sections
- Build a skill marketplace for community-contributed skills
- Connect to the authentication and personalization system