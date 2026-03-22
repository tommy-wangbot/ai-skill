---
name: jina-cli
description: A lightweight CLI tool wrapping Jina AI Reader API for fetching and parsing URLs into LLM-friendly formats (Markdown/Text/HTML). Use when you need to extract clean content from web pages, X (Twitter) posts, blogs, news sites, or any URL for AI processing.
---

# Jina CLI

## Overview

This skill provides instructions for using `jina-cli` to fetch and parse any URL into LLM-friendly formats using Jina AI's Reader API.

## Installation

```bash
npm install -g jina-cli
# or
pip install jina-cli
```

## Basic Usage

```bash
# Fetch a URL and output as Markdown (default)
jina https://example.com

# Fetch as text
jina https://example.com --format text

# Fetch as HTML
jina https://example.com --format html

# Read X (Twitter) posts
jina https://x.com/username/status/123456789

# Pipe to other tools
jina https://news.site.com/article | grep -A 5 "key phrase"
```

## Options

- `--format, -f`: Output format: `markdown` (default), `text`, or `html`
- `--output, -o`: Save output to file
- `--no-cache`: Disable caching
- `--help`: Show help

## Use Cases

1. **AI content extraction**: Fetch web articles for summarization
2. **Research**: Extract content from multiple URLs for analysis
3. **Data pipeline**: Integrate with other CLI tools for automation
4. **X/Twitter scraping**: Get clean text from social media posts

## API Key

Jina CLI uses Jina AI Reader API. Some features may require an API key:
```bash
export JINA_API_KEY=your_api_key
```

## Resources

### scripts/
- `jina-wrapper.sh` - Example wrapper script for common operations