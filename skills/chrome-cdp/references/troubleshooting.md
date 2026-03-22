# Troubleshooting

## `Could not find DevToolsActivePort`

Chrome 远程调试没有开启，或者当前不是默认 Chrome 配置目录。

处理方式:

- 打开 `chrome://inspect/#remote-debugging`
- 确认 Remote Target Discovery 已启用
- 保持 Chrome 进程继续运行

## `list` 首次连接卡住或等待很久

通常是 Chrome 弹出了首次授权调试的确认框。

处理方式:

- 切回 Chrome 看是否有 "Allow debugging" 弹窗
- 对目标标签页授权一次
- 再次执行同一条命令

## `Ambiguous prefix`

你给的 target 前缀太短，匹配到了多个标签页。

处理方式:

- 重新执行 `list`
- 复制更长的 target 前缀

## `click` 没反应

常见原因:

- 选择器不对
- 元素还没出现在 DOM 里
- 页面真正可点击的是别的节点

处理方式:

- 先用 `snap` 看页面结构
- 再用 `html <target> "<selector>"` 检查选中的节点
- 必要时改用 `shot` + `clickxy`

## `type` 没输入到预期位置

`type` 只会往当前焦点输入。

处理方式:

- 先用 `click` 或 `clickxy` 把焦点放到目标输入框
- 再执行 `type`

## 坐标点错位置

`clickxy` 需要的是 CSS 像素，截图文件是设备像素。

处理方式:

- 先执行 `shot`
- 读取输出里的 DPR
- 按 `CSS px = 截图像素 / DPR` 换算

## 多步 `eval` 结果不稳定

页面在每次点击或刷新后可能变化，导致索引失效。

处理方式:

- 不要把 `querySelectorAll(...)[i]` 跨多条命令复用
- 尽量在一次 `eval` 里收集完整结果
- 改用更稳定的选择器，例如文本、属性或结构限定
