---
title: Training and Fine-Tuning
sidebar_label: Training and Fine-Tuning
sidebar_position: 6
description: Adapting VLA models to custom tasks
keywords: [training, fine-tuning, VLA]
---

# Training and Fine-Tuning

Adapt pre-trained VLA models to specific tasks.

## Data Collection

- Teleoperation demonstrations
- Simulation rollouts
- Real robot data

## Fine-Tuning

```python
# Fine-tune VLA model
model.train()
for batch in dataloader:
    loss = model(batch)
    loss.backward()
```

## Summary

Fine-tuning adapts VLA models to custom robot tasks.
