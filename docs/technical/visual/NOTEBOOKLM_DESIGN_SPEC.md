# NotebookLM Analytical Aesthetic: 视觉设计规范与 SVG 模板
# NotebookLM Analytical Aesthetic: Design Specification & SVG Templates

> **规范目的 (Objective)**：
> 本规范旨在通过代码（SVG/Mermaid）复刻 Google NotebookLM 特有的“学术级分析感”视觉风格。这种风格结合了极简主义的网格布局、柔和的莫兰迪色系（Pastel Colors）以及高密度的信息架构，非常适合展示复杂的工业架构、OS 逻辑或商业闭环。

---

## 1. 核心视觉原则 (Core Principles)

1. **结构化卡片 (Structured Cards)**：所有核心观点必须包裹在带有圆角（`rx="16"`）和微弱投影（`Drop Shadow`）的卡片中。
2. **莫兰迪色标 (Pastel Palette)**：严禁使用高饱和度对比色。使用低饱和度、高明度的色彩（见下文色表）。
3. **中央锚点 (Central Anchor)**：页面中心应有一个具有技术美感的“核心图示”（如 CPU、大脑、中枢节点），作为全屏视觉的引力中心。
4. **对比表格 (Contrast Table)**：使用 Notion 风格的简约对比表来强化“代际差”和“降维打击”的商业叙事。
5. **极简字体 (Lean Typography)**：优先使用系统默认无衬线字体（`-apple-system`, `Inter`, `Segoe UI`），字重（`font-weight`）要有明显的层级感（900 vs 500 vs 400）。

---

## 2. 标准色彩规范 (Color Tokens)

| 组件 (Component) | 背景色 (Fill) | 标题/描边色 (Accent) | 语义 (Semantic) |
| :--- | :--- | :--- | :--- |
| **全局背景** | `#F8F9FA` | - | 极简、学术、干净 |
| **核心架构卡片** | `#FFF1DF` | `#FA9D81` | 橘色：代表动力与基础 |
| **模块生态卡片** | `#FFFCE0` | `#FFC773` | 黄色：代表繁荣与多样性 |
| **安全/RLS 卡片** | `#EBF7F6` | `#6CD4CA` | 青色：代表冷静、安全、防护 |
| **演化/JA 卡片** | `#F8F0F9` | `#CE8EDC` | 紫色：代表深邃、演化、未来 |
| **主标题文字** | - | `#1F2937` | 深炭灰：最高可读性 |
| **副标题文字** | - | `#4B5563` | 中灰：辅助说明 |

---

## 3. SVG 组件代码块 (Reusable SVG Snippets)

### 3.1 带有标题栏的标准卡片容器
```xml
<g filter="url(#shadow-sm)">
  <rect width="440" height="300" rx="16" fill="#FFF1DF"/>
  <!-- Header Badge -->
  <rect width="440" height="40" rx="16" fill="#FA9D81"/>
  <rect y="20" width="440" height="20" fill="#FA9D81"/> <!-- 消除底部圆角 -->
  <text x="220" y="27" font-size="18" font-weight="bold" fill="#FFFFFF" text-anchor="middle">标题文本</text>
</g>
```

### 3.2 Notion 风格对比表行
```xml
<line x1="20" y1="200" x2="540" y2="200" stroke="#E5E7EB" stroke-width="2"/>
<text x="145" y="235" font-size="15" font-weight="bold" fill="#1F2937" text-anchor="middle">左侧核心点</text>
<text x="415" y="235" font-size="15" fill="#4B5563" text-anchor="middle">右侧落后点</text>
<text x="280" y="220" font-size="12" fill="#9CA3AF" text-anchor="middle">对比维度标签</text>
```

### 3.3 阴影滤镜定义
```xml
<defs>
  <filter id="shadow-sm" x="-5%" y="-5%" width="110%" height="110%">
    <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.06"/>
  </filter>
</defs>
```

---

## 4. 商业叙事逻辑 (Narrative Logic)

使用此规范生成内容时，应遵循以下叙事路径：
1. **Header**: 提出一个宏大的“范式转移”命题。
2. **Left Column**: 展示物理底座与工程实现（Hardcore Tech）。
3. **Right Column**: 展示社会学治理与未来演化（Social/Business Value）。
4. **Center Bottom**: 总结“我们 vs 传统”的本质区别。

---
*Created for Odoo Farm 19.0. This spec ensures visual consistency across the entire ecosystem.*
