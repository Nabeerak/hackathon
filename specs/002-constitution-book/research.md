# Research & Technology Decisions: Physical AI & Humanoid Robotics Textbook

**Feature**: 002-constitution-book
**Created**: 2025-11-30
**Phase**: Phase 0 - Research

## Overview

This document consolidates research findings and technology decisions for creating a comprehensive Physical AI & Humanoid Robotics textbook integrated into the existing Docusaurus site.

## Technology Stack Decisions

### 1. Content Format & Authoring

**Decision**: Markdown (MDX) with Docusaurus

**Rationale**:
- Docusaurus is already configured and running in the project
- MDX allows embedding React components for interactive elements if needed in future
- Markdown is widely accessible and version-controllable
- Supports code syntax highlighting out of the box
- Easy for multiple authors to collaborate via Git

**Alternatives Considered**:
- LaTeX/PDF: Rejected - not web-native, harder to maintain, no search functionality
- Jupyter Book: Rejected - adds complexity, Docusaurus already set up
- GitBook: Rejected - migration cost, vendor lock-in concerns

### 2. Code Example Management

**Decision**: Inline code blocks with language-specific syntax highlighting

**Rationale**:
- Docusaurus supports Prism.js for syntax highlighting
- Python and C++ are the primary languages for ROS 2 development
- Code blocks can include line numbers and highlighting
- Easy to maintain and update

**Best Practices**:
- Include setup requirements before code examples
- Provide expected output after code blocks
- Use consistent commenting style
- Test all code examples before including

**Alternatives Considered**:
- External code repositories: Rejected - breaks reading flow, harder to maintain
- Embedded IDEs: Rejected - out of scope per specification
- Code sandboxes: Rejected - requires backend infrastructure

### 3. Content Organization Strategy

**Decision**: Hierarchical chapter-based structure with sidebar navigation

**Rationale**:
- Aligns with traditional textbook organization
- Docusaurus sidebar supports nested navigation
- Enables progressive learning path
- Easy to reference specific sections

**Structure Pattern**:
```
docs/
├── physical-ai-textbook/
│   ├── index.md (book introduction)
│   ├── course-overview/
│   │   ├── learning-outcomes.md
│   │   ├── weekly-breakdown.md
│   │   └── prerequisites.md
│   ├── hardware-infrastructure/
│   │   ├── digital-twin-workstation.md
│   │   ├── physical-ai-edge-kits.md
│   │   ├── robot-lab-options.md
│   │   └── cloud-native-alternatives.md
│   ├── ros2-fundamentals/
│   │   ├── introduction.md
│   │   ├── installation.md
│   │   ├── nodes-topics.md
│   │   ├── services-actions.md
│   │   └── navigation-stack.md
│   ├── digital-twin-simulation/
│   │   ├── gazebo-basics.md
│   │   ├── unity-simulation.md
│   │   ├── urdf-modeling.md
│   │   └── sensor-integration.md
│   ├── nvidia-isaac/
│   │   ├── isaac-sim-intro.md
│   │   ├── omniverse-setup.md
│   │   ├── robot-brain-ai.md
│   │   └── perception-systems.md
│   ├── vision-language-action/
│   │   ├── vla-overview.md
│   │   ├── multimodal-models.md
│   │   ├── action-primitives.md
│   │   └── integration-patterns.md
│   └── humanoid-robotics/
│       ├── bipedal-locomotion.md
│       ├── manipulation-control.md
│       ├── conversational-robotics.md
│       └── gpt-integration.md
```

**Alternatives Considered**:
- Single-page format: Rejected - too long, poor performance
- Wiki-style linking: Rejected - less structured learning path
- Module-based (disconnected sections): Rejected - harder to follow progression

### 4. Search Functionality

**Decision**: Use existing Docusaurus search plugin (@easyops-cn/docusaurus-search-local)

**Rationale**:
- Already installed in the project (package.json line 20)
- Provides local search without external dependencies
- Indexes all content automatically
- No additional cost or infrastructure required

**Configuration Needed**:
- Ensure search plugin is configured in docusaurus.config.ts
- Verify indexing covers new textbook content
- Test search for technical terms (ROS 2, SLAM, VLA, etc.)

### 5. Responsive Design

**Decision**: Use Docusaurus default responsive theme

**Rationale**:
- Docusaurus theme is mobile-responsive by default
- No custom CSS required
- Consistent with existing site design
- Tested across devices

**Best Practices**:
- Keep tables simple or use responsive table components
- Ensure code blocks don't overflow on mobile
- Test navigation on mobile devices
- Use responsive images

### 6. Version Control & Collaboration

**Decision**: Git-based workflow with feature branches

**Rationale**:
- Repository already uses Git
- Spec-Driven Development workflow in place
- Enables peer review of content
- Track changes to educational material over time

**Workflow**:
- Each chapter set created in feature branch
- Review for technical accuracy before merge
- Main branch always contains deployable content

## Content Development Approach

### 1. Chapter Structure Template

**Decision**: Standardized chapter format

Each chapter MUST include:
1. **Title and Introduction** (2-3 paragraphs)
2. **Learning Objectives** (3-5 bullet points)
3. **Prerequisites** (if applicable)
4. **Core Content** (sections and subsections)
5. **Code Examples** (practical demonstrations)
6. **Summary** (key takeaways)
7. **Further Reading** (optional references)

**Rationale**:
- Consistent structure aids learning
- Learning objectives set expectations
- Summaries reinforce key concepts
- Meets FR-012 requirement

### 2. Code Example Standards

**Decision**: Tested, runnable code with setup instructions

**Format**:
```markdown
## Example: [Description]

**Prerequisites**:
- Ubuntu 22.04 LTS
- ROS 2 Humble installed
- Workspace configured

**Code**:
```python
# Code here with comments
```

**Expected Output**:
```
Output shown here
```
```

**Rationale**:
- Meets FR-013 requirement
- Reduces student confusion
- Ensures code quality
- Handles edge case from spec (different backgrounds)

### 3. Hardware Specification Format

**Decision**: Structured hardware tables with options

**Format**:
| Component | Minimum Spec | Recommended | Purpose |
|-----------|-------------|-------------|---------|
| GPU | RTX 4070 Ti | RTX 4090 | Isaac Sim rendering |
| CPU | i7 13th Gen | i9 14th Gen | Parallel processing |

**Rationale**:
- Clear comparison for students/administrators
- Meets FR-007, FR-008, FR-009, FR-010
- Addresses edge case (hardware access)
- Supports SC-005 (3+ implementation options)

## Integration with Existing Docusaurus

### Current State Analysis

**Existing Structure** (from `docusaurus-book/docs/`):
- `intro.md` - Site introduction
- `constitution.md` - Project constitution
- `module1.md`, `module2.md` - Placeholder modules
- `tutorial-basics/`, `tutorial-extras/` - Tutorial sections

**Decision**: Add new `physical-ai-textbook/` directory alongside existing content

**Rationale**:
- Preserves existing content
- Clear separation between tutorial and textbook
- Allows independent navigation structure
- Meets FR-011 (integration requirement)

**Sidebar Configuration Needed**:
- Add new sidebar category "Physical AI Textbook"
- Maintain existing sidebar structure
- Configure in `sidebars.ts`

## Performance Considerations

### Build Time

**Decision**: Static generation with incremental builds

**Rationale**:
- Docusaurus generates static HTML
- Fast page loads
- Can deploy to GitHub Pages
- Incremental builds speed up development

### Asset Management

**Decision**: Minimal images, code-heavy content

**Rationale**:
- Reduces bundle size
- Faster page loads
- Focus on technical content
- Images only where necessary (architecture diagrams)

**Best Practices**:
- Use SVG for diagrams when possible
- Compress PNG/JPG images
- Store images in `static/img/physical-ai-textbook/`

## Deployment Strategy

**Decision**: GitHub Pages (as specified in constitution)

**Current Setup**:
- Project has `gh-pages` branch (from git fetch output)
- Docusaurus supports GitHub Pages deployment
- Base URL configured to `/hackathon/`

**Deployment Steps**:
1. Build: `npm run build` in `docusaurus-book/`
2. Deploy: `npm run deploy` (uses gh-pages)
3. Verify: Check https://[username].github.io/hackathon/

## Accessibility Considerations

**Decision**: Semantic HTML with ARIA labels where needed

**Rationale**:
- Docusaurus generates semantic HTML
- Code blocks are accessible
- Navigation is keyboard-accessible
- Meets responsive design requirement (SC-010)

**Best Practices**:
- Use proper heading hierarchy (h1 → h2 → h3)
- Add alt text to images
- Ensure sufficient color contrast
- Test with screen readers

## Content Accuracy & Maintenance

**Decision**: Version-specific documentation with update strategy

**Approach**:
- Document software versions used (ROS 2 Humble, Isaac Sim 4.0, etc.)
- Add "Last Updated" date to chapters
- Create maintenance checklist for version updates
- Include version compatibility notes

**Rationale**:
- Meets FR-015 (technical accuracy)
- Robotics tools evolve rapidly
- Helps students troubleshoot version issues
- Enables future updates

## Research Summary

All technical context questions have been resolved:

1. **Language/Version**: Markdown (MDX), Docusaurus 3.9.2
2. **Primary Dependencies**: Docusaurus, @easyops-cn/docusaurus-search-local
3. **Storage**: Git repository, static files
4. **Testing**: Manual content review, link checking
5. **Target Platform**: Web (GitHub Pages)
6. **Project Type**: Documentation site (existing Docusaurus)
7. **Performance Goals**: <3 second page load, responsive navigation
8. **Constraints**: Static content only (no backend), Markdown format
9. **Scale/Scope**: ~100-150 pages of content across 7 major topic areas

## Next Steps

Phase 1 will create:
1. **data-model.md** - Content entity structure
2. **contracts/** - Sidebar navigation schema
3. **quickstart.md** - Guide for adding new chapters
