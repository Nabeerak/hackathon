# Quickstart Guide: Adding Content to Physical AI Textbook

**Feature**: 002-constitution-book
**Created**: 2025-11-30
**Phase**: Phase 1 - Design
**For**: Content authors and contributors

## Overview

This guide provides step-by-step instructions for adding new chapters, sections, and content to the Physical AI & Humanoid Robotics textbook.

## Prerequisites

- Git repository cloned locally
- Node.js 20+ installed
- Docusaurus site running (`npm start` in `docusaurus-book/`)
- Text editor (VS Code recommended)
- Basic Markdown knowledge

## Quick Reference

### File Locations

```
docusaurus-book/
├── docs/
│   └── physical-ai-textbook/          # All textbook content here
│       ├── index.md                   # Book introduction
│       ├── course-overview/           # Course structure
│       ├── hardware-infrastructure/   # Hardware chapter
│       ├── ros2-fundamentals/         # ROS 2 chapter
│       └── [other-chapters]/          # Additional chapters
├── static/
│   └── img/
│       └── physical-ai-textbook/      # Images for textbook
└── sidebars.ts                        # Navigation configuration
```

### Content Structure Pattern

```
Chapter Directory:
docs/physical-ai-textbook/{chapter-slug}/
├── index.md                           # Chapter introduction
├── {section-1-slug}.md               # Section 1
├── {section-2-slug}.md               # Section 2
└── ...

Image Directory:
static/img/physical-ai-textbook/{chapter-slug}/
├── {image-1}.svg
├── {image-2}.png
└── ...
```

## Adding a New Chapter

### Step 1: Create Chapter Directory

```bash
cd docusaurus-book/docs/physical-ai-textbook
mkdir new-chapter-name
cd new-chapter-name
```

### Step 2: Create Chapter Index

Create `index.md` with this template:

```markdown
---
title: Your Chapter Title
sidebar_label: Chapter Title
sidebar_position: 5  # Adjust based on order
chapter_number: 4    # Sequential chapter number
description: Brief description of chapter content
keywords: [keyword1, keyword2, keyword3]
last_updated: 2025-11-30
estimated_read_time: 30
---

# Your Chapter Title

## Introduction

[2-3 paragraphs introducing the chapter topic and its importance]

## Learning Objectives

By the end of this chapter, you will be able to:

- **Objective 1**: [Action verb] [specific skill/knowledge]
- **Objective 2**: [Action verb] [specific skill/knowledge]
- **Objective 3**: [Action verb] [specific skill/knowledge]
- **Objective 4**: [Action verb] [specific skill/knowledge]

## Prerequisites

To get the most from this chapter, you should have:

- [Prerequisite 1]
- [Prerequisite 2]
- [Prerequisite 3]

## Chapter Overview

This chapter is organized as follows:

1. **[Section 1 Name](./section-1-slug.md)**: Brief description
2. **[Section 2 Name](./section-2-slug.md)**: Brief description
3. **[Section 3 Name](./section-3-slug.md)**: Brief description

## Summary

[This will be filled in after sections are complete]
```

### Step 3: Add Chapter to Sidebar

Edit `docusaurus-book/sidebars.ts`:

```typescript
// Find the physicalAiTextbook array and add:
{
  type: 'category',
  label: 'Your Chapter Title',
  collapsed: true,
  items: [
    {
      type: 'doc',
      id: 'physical-ai-textbook/new-chapter-name/index',
      label: 'Introduction'
    },
    {
      type: 'doc',
      id: 'physical-ai-textbook/new-chapter-name/section-1-slug',
      label: 'Section 1 Title'
    },
    {
      type: 'doc',
      id: 'physical-ai-textbook/new-chapter-name/section-2-slug',
      label: 'Section 2 Title'
    }
    // Add more sections...
  ]
}
```

### Step 4: Verify Navigation

1. Save `sidebars.ts`
2. Check browser (Docusaurus hot-reloads automatically)
3. Verify new chapter appears in sidebar
4. Click through to confirm link works

## Adding a New Section

### Step 1: Create Section File

In your chapter directory, create `section-name.md`:

```markdown
---
title: Section Title
sidebar_label: Short Label
sidebar_position: 2  # Order within chapter
description: Brief description
keywords: [keyword1, keyword2, keyword3]
last_updated: 2025-11-30
code_examples: true  # Set to true if including code
difficulty: beginner # Or intermediate, advanced
---

# Section Title

## Introduction

[2-3 paragraphs introducing the section topic]

## Core Concepts

### Concept 1

[Explanation with examples]

### Concept 2

[Explanation with examples]

## Practical Examples

[See code example template below]

## Summary

**Key Takeaways**:

- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

## Further Reading

- [Resource 1](URL)
- [Resource 2](URL)
```

### Step 2: Add Section to Sidebar

Update the chapter's `items` array in `sidebars.ts`:

```typescript
{
  type: 'doc',
  id: 'physical-ai-textbook/chapter-name/section-name',
  label: 'Section Title'
}
```

## Adding Code Examples

### Template for Code Examples

```markdown
## Example: [Description]

**Prerequisites**:
- [Software/package needed]
- [Environment setup required]
- [Configuration needed]

**Code** (`filename.py`):

```python
#!/usr/bin/env python3
"""
Brief description of what this code does.
"""

import necessary_modules

def main():
    # Your code here with clear comments
    print("Hello, Physical AI!")

if __name__ == '__main__':
    main()
```

**Expected Output**:

```
Hello, Physical AI!
```

**Explanation**:

1. [Line-by-line or block-by-block explanation]
2. [Key concepts highlighted]
3. [Common pitfalls or notes]

**Exercise**: [Optional challenge for students]
```

### Code Block Best Practices

1. **Always specify language** for syntax highlighting:
   - Python: ` ```python `
   - C++: ` ```cpp `
   - Bash: ` ```bash `
   - YAML: ` ```yaml `

2. **Include setup instructions** if code requires specific environment

3. **Test all code** before including in textbook

4. **Use clear comments** to explain non-obvious logic

5. **Show expected output** so students can verify their results

## Adding Images and Diagrams

### Step 1: Add Image File

```bash
# Create image directory if it doesn't exist
mkdir -p docusaurus-book/static/img/physical-ai-textbook/chapter-name

# Add your image
cp your-image.svg docusaurus-book/static/img/physical-ai-textbook/chapter-name/
```

### Step 2: Reference Image in Markdown

```markdown
![Alt text description](/img/physical-ai-textbook/chapter-name/image-name.svg)

**Figure 1**: Caption describing the image
```

### Image Best Practices

1. **Prefer SVG** for diagrams (scalable, small file size)
2. **Compress PNG/JPG** before adding (use TinyPNG or similar)
3. **Use descriptive filenames**: `ros2-architecture-diagram.svg` not `image1.svg`
4. **Add alt text** for accessibility
5. **Keep images under 500KB** for fast page loads

## Adding Hardware Specifications

### Template for Hardware Tables

```markdown
## Hardware Specifications

### Recommended Configuration

| Component | Specification | Purpose | Est. Cost |
|-----------|--------------|---------|-----------|
| GPU | NVIDIA RTX 4070 Ti (12GB) | Isaac Sim rendering | $800 |
| CPU | Intel Core i7 13700K | Parallel processing | $400 |
| RAM | 64GB DDR5-5600 | Scene loading | $200 |
| Storage | 1TB NVMe SSD | Fast asset loading | $100 |

**Total Estimated Cost**: $1,500

### Budget Alternative

| Component | Specification | Purpose | Est. Cost |
|-----------|--------------|---------|-----------|
| GPU | NVIDIA RTX 4060 Ti (8GB) | Basic rendering | $450 |
| CPU | Intel Core i5 13400F | Processing | $200 |
| RAM | 32GB DDR5-4800 | Essential needs | $100 |
| Storage | 512GB NVMe SSD | Basic storage | $50 |

**Total Estimated Cost**: $800

### Notes

- [Important considerations]
- [Where to purchase]
- [Compatibility notes]
```

## Content Quality Checklist

Before submitting new content, verify:

### Frontmatter
- [ ] All required fields present (title, sidebar_label, sidebar_position)
- [ ] sidebar_position is unique within chapter
- [ ] last_updated is current date (YYYY-MM-DD)
- [ ] keywords includes 3-10 relevant terms

### Content
- [ ] Introduction clearly explains the topic
- [ ] Headings use proper hierarchy (## for main sections, ### for subsections)
- [ ] Learning objectives use action verbs (Bloom's taxonomy)
- [ ] Code examples include prerequisites and expected output
- [ ] Images have alt text and captions
- [ ] Links are tested and working
- [ ] Technical terms are explained or linked to glossary

### Style
- [ ] Professional tone, accessible to students
- [ ] Active voice preferred over passive
- [ ] Technical accuracy verified
- [ ] No spelling or grammar errors
- [ ] Consistent terminology throughout

### Navigation
- [ ] Page appears in sidebars.ts
- [ ] sidebar_position orders pages logically
- [ ] Links to related sections included

## Testing Your Changes

### Local Testing

1. **Start development server**:
   ```bash
   cd docusaurus-book
   npm start
   ```

2. **Navigate to your new content** in the browser

3. **Check for**:
   - Proper rendering of Markdown
   - Code syntax highlighting working
   - Images displaying correctly
   - Links navigating properly
   - Sidebar navigation showing correct structure

4. **Test responsive design**:
   - Resize browser window
   - Check mobile view (Chrome DevTools)
   - Verify tables are readable on narrow screens

### Build Testing

Before committing, verify production build works:

```bash
cd docusaurus-book
npm run build
npm run serve
```

Visit http://localhost:3000/hackathon/ and verify everything works.

## Common Issues and Solutions

### Issue: Page Not Showing in Sidebar

**Solution**:
- Check `sidebars.ts` includes the correct document ID
- Verify file exists at expected path
- Restart development server

### Issue: Code Block Not Highlighting

**Solution**:
- Ensure language is specified: ` ```python ` not just ` ``` `
- Check Prism supports the language
- Restart development server

### Issue: Image Not Displaying

**Solution**:
- Verify image path is correct (starts with `/img/`)
- Check file exists in `static/img/` directory
- Ensure filename matches exactly (case-sensitive)
- Clear browser cache

### Issue: Frontmatter Errors

**Solution**:
- Validate YAML syntax (use YAML validator)
- Ensure proper indentation (2 spaces)
- Check for missing closing quotes
- Verify required fields are present

## Git Workflow

### Creating Feature Branch

```bash
# Ensure you're on latest main
git checkout main
git pull origin main

# Create feature branch
git checkout -b add-chapter-name

# Make your changes...

# Stage changes
git add docs/physical-ai-textbook/chapter-name/
git add docusaurus-book/sidebars.ts
git add static/img/physical-ai-textbook/chapter-name/

# Commit with descriptive message
git commit -m "Add [Chapter Name] to Physical AI textbook

- Create chapter introduction and learning objectives
- Add [X] sections covering [topics]
- Include code examples for [concepts]
- Add hardware specifications for [equipment]"

# Push to remote
git push origin add-chapter-name
```

### Content Review Process

1. Create pull request on GitHub
2. Request review from technical expert
3. Address review comments
4. Merge to main branch after approval
5. Verify deployment to GitHub Pages

## Style Guide Summary

### Markdown Conventions

- **Headers**: Use sentence case ("Introduction to ROS 2" not "Introduction To ROS 2")
- **Bold**: Use for emphasis and important terms: **bold text**
- **Italic**: Use for variable names or placeholders: *your_package_name*
- **Code**: Use backticks for inline code: `ros2 run`
- **Lists**: Use `-` for unordered, `1.` for ordered
- **Links**: Use descriptive text: [ROS 2 documentation](URL) not [click here](URL)

### Technical Writing

- **Be specific**: "Ubuntu 22.04 LTS" not "recent Ubuntu version"
- **Use active voice**: "Run the command" not "The command should be run"
- **Define acronyms**: "Robot Operating System (ROS)" on first use
- **Be consistent**: Pick one term and stick with it (e.g., "node" not "node/process")
- **Explain why**: Not just how, but why it's done this way

### Code Style

- **Python**: Follow PEP 8
- **C++**: Follow ROS 2 style guide
- **Comments**: Explain intent, not just what the code does
- **Naming**: Use descriptive variable names

## Additional Resources

### Docusaurus Documentation
- [Markdown Features](https://docusaurus.io/docs/markdown-features)
- [Sidebar Configuration](https://docusaurus.io/docs/sidebar)
- [Frontmatter](https://docusaurus.io/docs/api/plugins/@docusaurus/plugin-content-docs#markdown-frontmatter)

### Content References
- [data-model.md](./data-model.md) - Complete content structure
- [contracts/sidebar-schema.ts](./contracts/sidebar-schema.ts) - Sidebar configuration
- [contracts/frontmatter-schema.yaml](./contracts/frontmatter-schema.yaml) - Metadata standards

### Writing Resources
- Bloom's Taxonomy for learning objectives
- Technical writing best practices
- Markdown syntax guide

## Getting Help

If you encounter issues:

1. Check this quickstart guide
2. Review existing chapters for examples
3. Consult Docusaurus documentation
4. Ask in project discussions
5. Create GitHub issue for bugs

## Next Steps

Now that you understand the structure:

1. Review the [data model](./data-model.md) for complete entity definitions
2. Examine existing chapters as templates
3. Start with a simple section to get comfortable
4. Iterate and improve based on feedback

Happy writing!
