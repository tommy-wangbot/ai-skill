---
name: wechat-to-markdown
description: Convert WeChat public account article links (mp.weixin.qq.com) into Markdown files with local image downloads. Use when the user asks to transform a WeChat article URL into .md, keep/retain inline images, batch-convert multiple links, or regenerate cleaner Markdown from a WeChat page.
---

# WeChat To Markdown

## Overview

Convert a WeChat article URL into a local Markdown file and a companion image folder.
Use the bundled script to keep output consistent and reduce manual parsing steps.

## Requirements

- Ensure `python3` is available.
- Ensure `pandoc` is installed and available in `PATH`.
- Ensure network access can reach `mp.weixin.qq.com` and image CDN domains.

## Workflow

1. Run the converter script with a WeChat article URL.
2. Let the script download HTML, extract `#js_content`, localize images, and generate Markdown via `pandoc`.
3. Return output paths and image counts to the user.

## Commands

```bash
python3 scripts/wechat_to_markdown.py "https://mp.weixin.qq.com/s/xxxx"
```

Default output location (when no custom paths are passed):
- `/Users/tommy/Documents/output/<article>.md`
- `/Users/tommy/Documents/output/<article>_images/`

Use custom output names when needed:

```bash
python3 scripts/wechat_to_markdown.py "https://mp.weixin.qq.com/s/xxxx" \
  --output article.md \
  --images article_images
```

## Output Rules

- Create one Markdown file.
- Create one image directory with relative links used inside Markdown.
- Default output base directory: `/Users/tommy/Documents/output`.
- Preserve visible article text and inline images.
- Keep source links for clickable image anchors when present.
- Remove common WeChat placeholder SVG images and excessive empty wrapper tags.

## Troubleshooting

- If conversion fails with `pandoc failed`, install `pandoc` first.
- If no body is found, verify the URL is a valid public WeChat article page.
- If some images fail to download, keep their original remote URLs in the Markdown instead of failing the whole run.
