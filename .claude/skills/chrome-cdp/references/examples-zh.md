# 中文使用示例

下面的例子分成两类:

- 给 Codex 的中文提示模板
- 直接运行的 CLI 命令模板

优先让 Codex 使用这个 skill；只有在你自己手动排查时才需要直接敲 CLI。

## 给 Codex 的提示模板

```text
用 $chrome-cdp 列出我当前 Chrome 的标签页，找到标题里包含“GitHub”的那个，只返回 target 前缀、标题和 URL。
```

```text
用 $chrome-cdp 查看我当前打开页面的语义结构，重点列出主区域、按钮、输入框和对话框。
```

```text
用 $chrome-cdp 把当前页面 main 区域的 HTML 提取出来，忽略导航栏和页脚。
```

```text
用 $chrome-cdp 在当前标签页执行 JS，提取所有 H2 标题及其链接，按 Markdown 列表返回。
```

```text
用 $chrome-cdp 给当前页面截一张图到 /tmp/current-page.png，并告诉我如果我要点击截图上的某个点，应该怎样换算成 CSS 坐标。
```

```text
用 $chrome-cdp 找到当前页面的“Load more”按钮，持续点击直到消失，然后告诉我一共点击了几次。
```

```text
用 $chrome-cdp 先聚焦当前页面的搜索框，再输入“OpenAI Codex”，不要提交。
```

```text
用 $chrome-cdp 检查当前页面的网络资源，按耗时从高到低列出前 10 个请求。
```

## CLI 命令模板

先列出标签页，拿到目标前缀:

```bash
/Users/tommy/.codex/skills/chrome-cdp/scripts/cdp.mjs list
```

查看语义结构:

```bash
/Users/tommy/.codex/skills/chrome-cdp/scripts/cdp.mjs snap A1B2C3D4
```

提取 `main` 区域 HTML:

```bash
/Users/tommy/.codex/skills/chrome-cdp/scripts/cdp.mjs html A1B2C3D4 "main"
```

执行 JS 提取信息:

```bash
/Users/tommy/.codex/skills/chrome-cdp/scripts/cdp.mjs eval A1B2C3D4 'Array.from(document.querySelectorAll("h2")).map(el => ({text: el.textContent.trim(), href: el.querySelector("a")?.href || ""}))'
```

截图并保存到指定路径:

```bash
/Users/tommy/.codex/skills/chrome-cdp/scripts/cdp.mjs shot A1B2C3D4 /tmp/current-page.png
```

点击按钮:

```bash
/Users/tommy/.codex/skills/chrome-cdp/scripts/cdp.mjs click A1B2C3D4 "button"
```

在当前焦点输入文本:

```bash
/Users/tommy/.codex/skills/chrome-cdp/scripts/cdp.mjs type A1B2C3D4 "OpenAI Codex"
```

循环点击“加载更多”:

```bash
/Users/tommy/.codex/skills/chrome-cdp/scripts/cdp.mjs loadall A1B2C3D4 ".load-more" 1200
```

查看资源加载耗时:

```bash
/Users/tommy/.codex/skills/chrome-cdp/scripts/cdp.mjs net A1B2C3D4
```

## 编写表达式的小建议

- 在 `zsh` 里优先用单引号包住整段 JS 表达式。
- 如果页面可能变化，不要把 `querySelectorAll(...)[i]` 分散到多个命令里。
- 需要稳定提取时，尽量一次 `eval` 返回完整 JSON 结果。
