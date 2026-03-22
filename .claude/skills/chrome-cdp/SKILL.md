---
name: chrome-cdp
description: Inspect or interact with pages already open in the local Chrome browser via Chrome DevTools Protocol. Use when the user wants to debug, inspect, navigate, click, type, take screenshots, or run JavaScript in their existing Chrome session instead of opening a separate browser.
---

# Chrome CDP

Lightweight Chrome DevTools Protocol CLI for the local Google Chrome session. It connects directly over WebSocket, so it is fast and works with tabs the user already has open.

## When To Use

Use this skill when the user explicitly wants work done in their existing local Chrome session, for example:

- inspect a page already open in Chrome
- debug DOM or network behavior in a live tab
- click, type, or navigate inside an existing tab
- capture a screenshot from the current Chrome page

Prefer the built-in browser tools when opening a fresh automated browser is fine. Prefer this skill when the user cares about their real logged-in Chrome state.

## Operating Boundary

This skill acts on the user's real local Chrome session. Treat it as higher-sensitivity than a disposable browser.

- Use it only when the user explicitly wants work done in their current Chrome session.
- If multiple tabs could match, identify the target tab by title or URL before acting.
- Prefer read-only commands first: `list`, `snap`, `html`, `net`, `shot`.
- Before `click`, `type`, or `nav`, make sure the requested action is clear.

## Prerequisites

- Chrome remote debugging is enabled in `chrome://inspect/#remote-debugging`
- Node.js 22+ is available
- The script assumes the default local Chrome profile path and reads `DevToolsActivePort` automatically

## Quick Workflow

1. Run `scripts/cdp.mjs list` and match the right tab by title or URL.
2. Use `snap` to understand semantic structure quickly.
3. Use `html` or `eval` for targeted extraction.
4. Use `shot` before coordinate-based interaction.
5. Use `click`, `clickxy`, `type`, or `nav` only after the target is confirmed.

For Chinese prompt examples and CLI templates, read [references/examples-zh.md](references/examples-zh.md).

For common failures and recovery steps, read [references/troubleshooting.md](references/troubleshooting.md).

## Commands

All commands use `scripts/cdp.mjs`. Start with `list` to find the target tab.

### List open pages

```bash
scripts/cdp.mjs list
```

Use the unique target ID prefix shown in the output for later commands.

### Accessibility snapshot

```bash
scripts/cdp.mjs snap <target>
```

### Evaluate JavaScript

```bash
scripts/cdp.mjs eval <target> '<expr>'
```

Avoid brittle index-based selectors across multiple calls when the DOM may change. If the page can mutate, collect the needed data in one `eval` call or use stable selectors.

### Take a screenshot

```bash
scripts/cdp.mjs shot <target> [file]
```

The screenshot is viewport-only. If needed, scroll first with `eval`.

### Other commands

```bash
scripts/cdp.mjs html    <target> [selector]
scripts/cdp.mjs nav     <target> <url>
scripts/cdp.mjs net     <target>
scripts/cdp.mjs click   <target> <selector>
scripts/cdp.mjs clickxy <target> <x> <y>
scripts/cdp.mjs type    <target> <text>
scripts/cdp.mjs loadall <target> <selector> [ms]
scripts/cdp.mjs evalraw <target> <method> [json]
scripts/cdp.mjs stop    [target]
```

## Working Notes

- `type` uses `Input.insertText`, so it works in cross-origin iframes after focus is set.
- `clickxy` expects CSS pixels, not screenshot image pixels.
- The first connection to a tab may trigger Chrome's "Allow debugging" prompt.
- A background daemon keeps the session alive per tab and exits after inactivity.
- `snap` is usually a better first inspection step than dumping full HTML.
