---
name: fireworks-tech-graph
description: "生成生产级 SVG+PNG 技术图表，支持 14 种 UML 图、8 种 AI/Agent 专用图、7 种视觉风格，输出 1920px 高清 PNG。触发词：画图、画一张、生成图表、draw diagram、visualize、架构图、流程图、时序图、组织结构图、脑图、mind map、diagram。"
---

# Fireworks Tech Graph — 技术图表生成指南

自然语言描述 → 生产级 SVG + 1920px PNG。

## 支持的图表类型

**通用类**：架构图、数据流图、流程图、时间轴、对比矩阵、思维导图  
**UML 类**：类图、序列图、状态机图、用例图、活动图、ER 图、网络拓扑  
**AI/Agent 专用**：RAG 管道、Agent 架构、记忆层设计、多 Agent 协作、工具调用流程

## 7 种视觉风格

| 风格 | 适用场景 |
|------|----------|
| flat-icon（默认）| 通用，适合正式文档 |
| dark-terminal | 技术演示，暗色背景 |
| blueprint | 蓝图/工程设计感 |
| glassmorphism | 现代 UI 风格 |
| minimal | 极简，适合报告内嵌 |
| colorful | 多色，适合演示文稿 |
| monochrome | 单色，适合打印 |

## 生成流程

1. **分类**：识别图表类型（架构/流程/序列等）
2. **提取结构**：从描述中识别节点、层次、关系
3. **规划布局**：按类型加载布局规则（8px 网格对齐，节点间距 120px）
4. **形状映射**：概念 → 形状（LLM=双边框圆角矩形，Agent=六边形，Memory=圆柱体）
5. **箭头语义**：颜色区分流向（蓝=数据流，橙=控制触发，绿虚线=写入）
6. **生成 SVG**：按复杂度选择策略
7. **语法验证**：`rsvg-convert file.svg -o /dev/null` 确认无误
8. **导出 PNG**：`rsvg-convert file.svg -w 1920 -o file.png`

## 按复杂度选择生成策略

- **简单**（<150 行 SVG）：直接写文件
- **中等**（150-300 行）：Python 脚本生成（推荐，避免 heredoc 转义问题）
- **复杂**（>300 行）：分块追加 + 逐块验证

## 质量检查（写 SVG 前必做）

- 标签开闭配对检查
- 属性引号语法检查
- 特殊字符转义（`<` `>` `&`）
- marker 引用完整性
- 末尾 `</svg>` 标签存在

## 依赖

- `rsvg-convert`（librsvg）：用于 SVG 验证和 PNG 导出

```bash
# macOS
brew install librsvg
```

## 输出

- `./[name].svg`：可编辑矢量图
- `./[name].png`：1920px 宽高清 PNG（适合 Notion、GitHub README、PPT 插入）
