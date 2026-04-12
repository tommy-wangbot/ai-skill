---
name: diagram-generator
description: "多格式图表生成工具，支持 Draw.io / Mermaid / Excalidraw 三种格式，通过自然语言描述生成流程图、序列图、架构图、ER 图、思维导图、网络拓扑图。触发词：画图、生成图表、draw diagram、流程图、时序图、架构图、ER 图、mind map、network diagram、drawio、mermaid、excalidraw。"
---

# Diagram Generator — 多格式图表生成

通过自然语言描述生成 Draw.io / Mermaid / Excalidraw 三种格式的图表。

## 前置要求：MCP 服务器

本 skill 依赖 `mcp-diagram-generator` MCP 服务器。在 Claude Code 中添加配置：

```json
// .claude.json 或全局 MCP 配置
{
  "mcpServers": {
    "mcp-diagram-generator": {
      "command": "npx",
      "args": ["-y", "mcp-diagram-generator"]
    }
  }
}
```

配置后验证以下工具可用：
- `mcp__mcp-diagram-generator__get_config`
- `mcp__mcp-diagram-generator__generate_diagram`
- `mcp__mcp-diagram-generator__init_config`

## 支持的图表类型

流程图、序列图、类图、ER 图、思维导图、架构图、网络拓扑图

## 三种格式及选择原则

| 格式 | 适用场景 | 优势 |
|------|----------|------|
| **Draw.io**（.drawio）| 复杂图、网络拓扑、需精细调整 | 可视化编辑，支持嵌套容器 |
| **Mermaid**（.md）| 快速生成、文档内嵌、版本控制 | 纯文本，可直接嵌入 Markdown |
| **Excalidraw**（.excalidraw）| 草稿讨论、非正式场合 | 手绘风格，适合头脑风暴 |

## 工作流程

1. 从用户描述中提取图表需求
2. 根据复杂度和用途选择格式（Draw.io 复杂图 / Mermaid 文档 / Excalidraw 草图）
3. 构建 JSON 规范传递给 MCP 服务器
4. MCP 服务器生成文件，自动创建目录

## 默认输出路径

```
diagrams/
  drawio/    ← Draw.io 文件
  mermaid/   ← Mermaid 文件
  excalidraw/ ← Excalidraw 文件
```

## 网络拓扑特别说明

网络拓扑图要求严格遵守 4 层层次结构：
`环境 → 数据中心 → 区域 → 设备`
