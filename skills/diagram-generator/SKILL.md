---
name: diagram-generator
description: "多格式图表生成工具，支持 Draw.io / Mermaid / Excalidraw 三种格式，通过自然语言描述生成流程图、序列图、架构图、ER 图、思维导图、网络拓扑图。触发词：画图、生成图表、draw diagram、流程图、时序图、架构图、ER 图、mind map、network diagram、drawio、mermaid、excalidraw。"
---

# Diagram Generator — 多格式图表生成

通过自然语言描述生成 Draw.io / Mermaid / Excalidraw 三种格式的图表。

## MCP 工具（已配置，直接调用）

| 工具 | 用途 |
|------|------|
| `mcp__mcp-diagram-generator__generate_diagram` | 生成图表文件（核心工具） |
| `mcp__mcp-diagram-generator__get_config` | 查看当前输出路径配置 |
| `mcp__mcp-diagram-generator__init_config` | 初始化配置文件 |

## 格式选择原则

| 格式 | 适用场景 | 输出文件 |
|------|----------|----------|
| `mermaid` | 序列图、流程图、ER图、快速原型、嵌入文档 | `.md` |
| `excalidraw` | 架构图、讨论草稿、非正式场合 | `.excalidraw` |
| `drawio` | 网络拓扑、复杂层次图、需精细调整 | `.drawio` |

## generate_diagram 参数规范

```
diagram_spec  (object, 必填): 图表结构 JSON
output_path   (string, 可选): 输出目录，默认 diagrams/<format>/
filename      (string, 可选): 文件名（不含扩展名）
format        (string, 可选): 覆盖 diagram_spec 中的 format
```

### diagram_spec 完整结构

```json
{
  "format": "mermaid | excalidraw | drawio",
  "title": "图表标题",
  "elements": [
    节点、容器、连线对象数组
  ]
}
```

### 三种元素类型

**节点 node**
```json
{
  "id": "node1",
  "type": "node",
  "name": "显示文字",
  "shape": "rect | ellipse | diamond | rounded | cylinder | cloud",
  "geometry": { "x": 100, "y": 100, "width": 120, "height": 60 },
  "style": { "fillColor": "#ffffff", "strokeColor": "#1976d2", "strokeWidth": 2, "fontSize": 14 }
}
```

**容器 container**（用于分层/分区，支持嵌套最多10层）
```json
{
  "id": "c1",
  "type": "container",
  "name": "层名称",
  "geometry": { "x": 50, "y": 50, "width": 500, "height": 300 },
  "style": { "fillColor": "#e3f2fd", "strokeColor": "#1976d2", "strokeWidth": 2 },
  "children": [ ...节点或子容器... ]
}
```

**连线 edge**
```json
{
  "id": "e1",
  "type": "edge",
  "source": "node1",
  "target": "node2",
  "label": "连线标签（可选）",
  "style": { "strokeColor": "#666", "strokeWidth": 2, "dashPattern": "5,5", "endArrow": "arrow" }
}
```

### 标准配色方案

| 层次 | fillColor | strokeColor |
|------|-----------|-------------|
| 客户端层 | `#e3f2fd` | `#1976d2` |
| 网关层 | `#f3e5f5` | `#7b1fa2` |
| 服务层 | `#e8f5e9` | `#388e3c` |
| 数据层 | `#fff3e0` | `#f57c00` |
| 外部服务 | `#fce4ec` | `#c2185b` |

## 调用示例

### 示例1：序列图（Mermaid）

用户说"画一个用户登录的时序图"：

```python
mcp__mcp-diagram-generator__generate_diagram(
  diagram_spec={
    "format": "mermaid",
    "title": "用户登录序列图",
    "elements": [
      {"id": "user",    "type": "node", "name": "用户"},
      {"id": "gateway", "type": "node", "name": "API网关"},
      {"id": "auth",    "type": "node", "name": "认证服务"},
      {"id": "e1", "type": "edge", "source": "user",    "target": "gateway", "label": "登录请求"},
      {"id": "e2", "type": "edge", "source": "gateway", "target": "auth",    "label": "验证Token"},
      {"id": "e3", "type": "edge", "source": "auth",    "target": "user",    "label": "返回Token"}
    ]
  },
  filename="user_login_sequence"
)
```

### 示例2：分层架构图（Excalidraw）

用户说"画微服务架构图"：

```python
mcp__mcp-diagram-generator__generate_diagram(
  diagram_spec={
    "format": "excalidraw",
    "title": "微服务架构",
    "elements": [
      {
        "id": "client-layer", "type": "container", "name": "客户端层",
        "geometry": {"x": 50, "y": 50, "width": 700, "height": 100},
        "style": {"fillColor": "#e3f2fd", "strokeColor": "#1976d2", "strokeWidth": 2},
        "children": [
          {"id": "web",    "type": "node", "name": "Web App",    "geometry": {"x": 100, "y": 75, "width": 120, "height": 50}},
          {"id": "mobile", "type": "node", "name": "Mobile App", "geometry": {"x": 280, "y": 75, "width": 120, "height": 50}}
        ]
      },
      {
        "id": "svc-layer", "type": "container", "name": "服务层",
        "geometry": {"x": 50, "y": 200, "width": 700, "height": 100},
        "style": {"fillColor": "#e8f5e9", "strokeColor": "#388e3c", "strokeWidth": 2},
        "children": [
          {"id": "auth", "type": "node", "name": "认证服务", "geometry": {"x": 100, "y": 225, "width": 120, "height": 50}},
          {"id": "user", "type": "node", "name": "用户服务", "geometry": {"x": 280, "y": 225, "width": 120, "height": 50}}
        ]
      },
      {"id": "e1", "type": "edge", "source": "web",  "target": "auth", "label": "HTTPS"},
      {"id": "e2", "type": "edge", "source": "web",  "target": "user", "label": "REST"},
      {"id": "e3", "type": "edge", "source": "mobile","target": "auth", "label": "HTTPS"}
    ]
  },
  filename="microservices_arch"
)
```

### 示例3：网络拓扑（Draw.io，4层嵌套）

```python
mcp__mcp-diagram-generator__generate_diagram(
  diagram_spec={
    "format": "drawio",
    "title": "网络拓扑",
    "elements": [
      {
        "id": "env1", "type": "container", "name": "生产环境", "level": "environment",
        "geometry": {"x": 50, "y": 50, "width": 600, "height": 450},
        "children": [
          {
            "id": "dc1", "type": "container", "name": "数据中心1", "level": "datacenter",
            "geometry": {"x": 100, "y": 100, "width": 250, "height": 350},
            "children": [
              {
                "id": "zone1", "type": "container", "name": "应用区", "level": "zone",
                "geometry": {"x": 130, "y": 150, "width": 180, "height": 250},
                "children": [
                  {"id": "router", "type": "node", "name": "路由器", "deviceType": "router"},
                  {"id": "switch", "type": "node", "name": "交换机", "deviceType": "switch"}
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  filename="network_topology"
)
```

## 工作流程

1. 识别用户要求的图表类型 → 选择格式（序列/流程→mermaid，架构草图→excalidraw，网络/复杂→drawio）
2. 从描述中提取所有节点、层次、关系
3. 为每个元素分配唯一 id（不得重复）
4. 构建 diagram_spec JSON，容器内的 children 坐标相对于父容器
5. 调用 `mcp__mcp-diagram-generator__generate_diagram`
6. 返回生成的文件路径，告知用户用哪个工具打开

## 输出路径

默认保存到当前工作目录下：
```
diagrams/mermaid/      ← Mermaid 文件（.md）
diagrams/excalidraw/   ← Excalidraw 文件（.excalidraw）在 excalidraw.com 打开
diagrams/drawio/       ← Draw.io 文件（.drawio）在 app.diagrams.net 打开
```
