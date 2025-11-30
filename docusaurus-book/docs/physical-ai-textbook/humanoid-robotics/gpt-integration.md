---
title: GPT Integration
sidebar_label: GPT Integration
sidebar_position: 6
description: Large language models for robot dialogue
keywords: [GPT, LLM, dialogue]
---

# GPT Integration

Use large language models for intelligent robot dialogue.

## GPT-4 for Robotics

```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful robot assistant."},
        {"role": "user", "content": user_input}
    ]
)
```

## Summary

LLMs enable sophisticated human-robot conversations.
