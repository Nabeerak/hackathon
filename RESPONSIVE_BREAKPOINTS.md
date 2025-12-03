# Chatbot Responsive Breakpoints - Visual Guide

## 📐 Breakpoint Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Responsive Breakpoints                    │
├──────────────┬──────────┬─────────────────────────────────────┤
│ Screen Size  │ Width    │ Chatbot Behavior                   │
├──────────────┼──────────┼─────────────────────────────────────┤
│ Tiny Phone   │ ≤ 360px  │ Fullscreen + Compact UI            │
│ Small Phone  │ 361-480px│ Fullscreen + Standard UI           │
│ Tablet       │ 481-768px│ Floating (450px max)               │
│ Laptop       │ 769-1199 │ Floating (400px)                   │
│ Desktop      │ ≥ 1200px │ Floating (450px) + Larger Button   │
└──────────────┴──────────┴─────────────────────────────────────┘
```

## 📱 Mobile Portrait (≤ 480px)

```
┌────────────────────────┐
│  ☰ Navbar              │ ← Docusaurus navbar
├────────────────────────┤
│                        │
│   📖 Textbook Content  │
│                        │
│   FULLSCREEN MODE:     │
│   When chatbot opens:  │
│                        │
│  ┌────────────────────┐│
│  │ AI Assistant    [×]││ ← Header (12px padding)
│  ├────────────────────┤│
│  │                    ││
│  │ 💬 Messages fill   ││ ← Messages (100% height)
│  │    entire screen   ││   Font: 14px
│  │                    ││   Padding: 12px
│  │                    ││
│  │                    ││
│  ├────────────────────┤│
│  │ [Type message...]  ││ ← Input (16px to prevent zoom)
│  │ [Send]             ││ ← Button (70px min-width)
│  └────────────────────┘│
│                        │
│                   💬   │ ← Toggle (60×60px)
└────────────────────────┘
```

**Features:**
- Takes full viewport when open
- No border radius (fills screen edge-to-edge)
- Immersive chat experience
- Close button to return to content

## 📱 Tablet (481px - 768px)

```
┌────────────────────────────────────────┐
│  ☰ Navbar                              │
├────────────────────────────────────────┤
│                                        │
│   📖 Textbook Content (full width)     │
│                                        │
│   ADAPTIVE MODE:          ┌──────────┐│
│   Chatbot floats right:   │AI Asst[×]││
│                           ├──────────┤│
│                           │          ││
│                           │ Messages ││
│                           │ 450px    ││
│                           │ max      ││
│                           │          ││
│                           ├──────────┤│
│                           │[Input..] ││
│                           │[Send]    ││
│                           └──────────┘│
│                              💬        │
└────────────────────────────────────────┘
                                56×56px
```

**Features:**
- Max width: 450px
- Height: 550px
- Rounded corners return
- Floats bottom-right
- Content remains visible

## 💻 Desktop (769px - 1199px)

```
┌──────────────────────────────────────────────────────────────┐
│  Logo  Physical AI & Humanoid Robotics Textbook  🔍  GitHub  │
│        ↑ Gradient text (pink→blue)                           │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  📖 Textbook Content (wide layout)                           │
│                                                               │
│                                    STANDARD MODE:             │
│                                    ┌────────────────┐        │
│                                    │AI Assistant [×]│        │
│                                    ├────────────────┤        │
│                                    │                │        │
│                                    │  Hello! Ask me │ ← Assistant
│                                    │                │        │
│                                    │     Hi there! ─┤ ← User  │
│                                    │                │   (gradient)
│                                    │  How can I...  │        │
│                                    │                │        │
│                                    ├────────────────┤        │
│                                    │[Type message...]│        │
│                                    │     [Send]     │ ← Gradient
│                                    └────────────────┘        │
│    400px × 600px                          💬                 │
│                                        60×60px                │
└──────────────────────────────────────────────────────────────┘
```

**Features:**
- Width: 400px
- Height: 600px
- Doesn't obstruct content
- Professional appearance
- Smooth animations

## 🖥️ Large Desktop (≥ 1200px)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Logo  Physical AI & Humanoid Robotics Textbook  🔍  GitHub             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  📖 Textbook Content (extra wide layout)                                │
│                                                                          │
│                                         ENHANCED MODE:                  │
│                                         ┌─────────────────┐             │
│                                         │ AI Assistant [×]│             │
│                                         ├─────────────────┤             │
│                                         │                 │             │
│                                         │   More space    │             │
│                                         │   for messages  │             │
│                                         │                 │             │
│                                         │   Better        │             │
│                                         │   readability   │             │
│                                         │                 │             │
│                                         ├─────────────────┤             │
│                                         │[Type message...] │             │
│                                         │      [Send]      │             │
│                                         └─────────────────┘             │
│      450px × 650px                             💬                       │
│                                             64×64px                      │
└─────────────────────────────────────────────────────────────────────────┘
```

**Features:**
- Width: 450px (larger)
- Height: 650px (taller)
- Button: 64×64px (more visible)
- Optimized for large screens

## 🎨 Gradient Theme Applied

```
┌────────────────────────────┐
│ Navbar Title               │ ← Gradient text
│ [Dark Pink → Bright Blue]  │
└────────────────────────────┘

┌────────────────────────────┐
│ 💬 Toggle Button           │ ← Gradient background
│ [#C2185B → #1565C0]        │
└────────────────────────────┘

┌────────────────────────────┐
│ AI Assistant          [×]  │ ← Gradient header
│ [Dark Pink → Blue]         │
├────────────────────────────┤
│  Welcome! Ask anything     │ ← White background
│                            │
│     User message here   ◄──┤ ← Gradient bubble
│     [Pink → Blue]          │
├────────────────────────────┤
│ [Type message...]          │ ← Pink border on focus
│ [Send]                     │ ← Gradient button
└────────────────────────────┘
```

## 📏 Spacing & Constraints

```
Desktop Layout:
┌─────── 100vw (Full Width) ────────┐
│                                   │
│  ┌─── max: calc(100vw - 40px) ───┤
│  │                                │
│  │  Content    ┌────────────┐    │ ← 20px margin
│  │             │  Chatbot   │    │
│  │             │  400×600   │    │
│  │             │            │◄───┤ ← 20px from right
│  │             └────────────┘    │
│  │                  ▲             │
│  └──────────────────┼─────────────┘
│                     │
│                  90px from bottom
│
│            💬 (60×60px)
│              ▲
│              └─ 20px from bottom
└───────────────────────────────────┘

Mobile Fullscreen:
┌───── 100vw ─────┐
│                 │
│  ┌─ 100vh ─┐   │
│  │         │   │
│  │ Chatbot │   │
│  │ Full    │   │
│  │ Screen  │   │
│  │         │   │
│  └─────────┘   │
└─────────────────┘
```

## ✅ Responsive Features Summary

| Feature | Mobile | Tablet | Desktop | Large |
|---------|--------|--------|---------|-------|
| **Layout** | Fullscreen | Float | Float | Float |
| **Width** | 100% | 450px | 400px | 450px |
| **Height** | 100% | 550px | 600px | 650px |
| **Button** | 60px | 56px | 60px | 64px |
| **Font** | 14px | 14px | Default | Default |
| **Input** | 16px | 16px | 14px | 14px |
| **Radius** | 0 | 12px | 12px | 12px |
| **Position** | Fixed | Fixed | Fixed | Fixed |

## 🎯 Result

The chatbot seamlessly adapts to ANY screen size, providing an optimal experience whether users are on:
- 📱 iPhone SE (375px)
- 📱 iPhone Pro Max (428px)
- 📱 iPad (768px)
- 💻 MacBook (1440px)
- 🖥️ 4K Monitor (3840px)

**Status:** FULLY RESPONSIVE ✅
