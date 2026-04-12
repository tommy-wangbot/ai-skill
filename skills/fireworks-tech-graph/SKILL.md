---
name: fireworks-tech-graph
description: "生成生产级 SVG+PNG 技术图表，支持 14 种 UML 图、8 种 AI/Agent 专用图、7 种视觉风格，输出 1920px 高清 PNG。触发词：画图、画一张、生成图表、draw diagram、visualize、架构图、流程图、时序图、组织结构图、脑图、mind map、diagram。"
---

# Fireworks Tech Graph — 技术图表生成

自然语言描述 → 生产级 SVG + 1920px PNG。

**前置依赖**：`rsvg-convert`（`brew install librsvg`）

## 支持的图表类型

| 分类 | 类型 |
|------|------|
| 通用 | 架构图、数据流图、流程图、时间轴、对比矩阵、思维导图 |
| UML | 类图、序列图、状态机图、用例图、活动图、ER图、网络拓扑 |
| AI/Agent | RAG管道、Agent架构、记忆层、多Agent协作、工具调用流程 |

## 7种视觉风格

| 风格关键词 | 适用场景 |
|-----------|----------|
| `flat-icon`（**默认**）| 正式文档、汇报材料 |
| `dark-terminal` | 技术演示、暗色背景PPT |
| `blueprint` | 工程设计感 |
| `glassmorphism` | 现代UI风格 |
| `minimal` | 极简，报告内嵌 |
| `colorful` | 演示文稿、多色区分 |
| `monochrome` | 黑白打印 |

## 形状语义（AI图专用）

| 概念 | SVG形状 |
|------|---------|
| LLM | 双边框圆角矩形 |
| Agent | 六边形 |
| Memory | 圆柱体（cylinder） |
| Tool | 圆角矩形 + 小图标 |
| User | 椭圆 |
| 数据库 | 圆柱体 |
| 决策 | 菱形 |

## 箭头颜色语义

| 颜色 | 含义 |
|------|------|
| 蓝色 `#2196F3` | 数据流 |
| 橙色 `#FF9800` | 控制/触发 |
| 绿色虚线 `#4CAF50` | 写入/存储 |
| 灰色 `#9E9E9E` | 辅助/弱关联 |

## 完整生成流程

1. **分类**：识别图表类型和视觉风格需求
2. **提取结构**：从描述中列出所有节点、层次、连接关系
3. **规划布局**：8px网格对齐，节点间距≥120px，层间距≥80px
4. **生成 SVG**：按复杂度选择策略（见下）
5. **验证语法**：`rsvg-convert file.svg -o /dev/null`
6. **导出 PNG**：`rsvg-convert file.svg -w 1920 -o file.png`
7. **告知结果**：返回 SVG 和 PNG 路径

## 按复杂度选择生成策略

| 规模 | SVG行数 | 策略 |
|------|---------|------|
| 简单 | < 150行 | 直接用 Write 工具写文件 |
| 中等 | 150–300行 | 写 Python 脚本生成（避免 heredoc 转义问题） |
| 复杂 | > 300行 | 分块追加 + 逐块验证 |

## SVG 质量检查（写文件前必做）

- [ ] 所有标签开闭配对（`<g>...</g>`，`<text>...</text>`）
- [ ] 属性值用双引号包裹
- [ ] 特殊字符已转义：`<` → `&lt;`，`>` → `&gt;`，`&` → `&amp;`
- [ ] marker（箭头）定义与引用 ID 一致
- [ ] 文件末尾有 `</svg>` 标签
- [ ] `viewBox` 与实际内容范围匹配

## 调用示例

### 示例1：RAG 架构图

用户说"画一张RAG流程架构图，dark风格"：

```
1. 确定风格：dark-terminal
2. 规划节点：用户输入 → 查询改写 → 向量检索 → 重排序 → LLM生成 → 输出
             外部组件：向量库（Memory形状）
3. 生成 SVG 文件：rag_architecture.svg
4. 验证：rsvg-convert rag_architecture.svg -o /dev/null
5. 导出：rsvg-convert rag_architecture.svg -w 1920 -o rag_architecture.png
```

SVG 骨架结构：
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">
  <defs>
    <!-- 箭头 marker 定义 -->
    <marker id="arrow-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#2196F3"/>
    </marker>
  </defs>
  <!-- 背景 -->
  <rect width="1200" height="600" fill="#1a1a2e"/>
  <!-- 节点组 -->
  <g id="nodes">
    <!-- 每个节点：rect + text -->
    <rect x="80" y="250" width="140" height="60" rx="8" fill="#0f3460" stroke="#2196F3" stroke-width="2"/>
    <text x="150" y="285" text-anchor="middle" fill="#ffffff" font-size="14">用户输入</text>
    <!-- 更多节点... -->
  </g>
  <!-- 连线 -->
  <g id="edges">
    <line x1="220" y1="280" x2="300" y2="280" stroke="#2196F3" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <!-- 更多连线... -->
  </g>
</svg>
```

### 示例2：组织架构图

用户说"画歌华有线的组织架构图，minimal风格"：

```
1. 确定风格：minimal（白底黑字）
2. 布局：树形，从上到下
3. 节点：公司名（顶部）→ 各部门（第二层）→ 子部门（第三层）
4. 连线：hierarchical，灰色实线，无箭头
```

### 示例3：多Agent协作流程

用户说"画一张多Agent协作图"：

```
1. 确定风格：flat-icon（默认）
2. 形状映射：
   - Orchestrator Agent → 六边形（大，居中）
   - Sub-Agent → 六边形（小）
   - Tool → 圆角矩形
   - Memory → 圆柱体
3. 箭头：
   - 控制指令 → 橙色实线
   - 数据传递 → 蓝色实线
   - 写入记忆 → 绿色虚线
```

## 文件命名与保存位置

- 保存到当前工作目录（`./`）
- 文件名用英文小写+下划线，例：`rag_pipeline.svg`，`org_chart.png`
- SVG 和 PNG 同名不同扩展名，成对输出

## 用户未指定风格时的默认选择

| 用途 | 推荐风格 |
|------|----------|
| 汇报PPT / 正式文档 | `flat-icon` |
| 技术博客 / README | `minimal` |
| 内部讨论 / 草稿 | `colorful` |
| AI/技术演示 | `dark-terminal` |
| 打印材料 | `monochrome` |
