---
name: apify-data-pipeline
description: Run Apify Actors from Codex with a repeatable pipeline (discover actor, run sync/async, fetch dataset, and save outputs). Use when the user asks to scrape or collect structured data and wants files saved locally.
---

# Apify Data Pipeline

## Overview

Use this skill to run Apify Actors from Codex and persist results to local files in a predictable way.

This skill is for operational data collection, not actor development. For building or editing actors, use `apify-actor-development`.

## Prerequisites

- `APIFY_TOKEN` is available in environment.
- `curl` and `jq` are installed.

Quick checks:

```bash
apify info
openclaw skills info apify
```

## Workflow

1. Discover candidate actors by keyword.
2. Inspect actor input schema.
3. Run actor with sync endpoint when possible.
4. If runtime is long, use async run and poll.
5. Fetch dataset items.
6. Save JSON and CSV/Markdown in a task folder under `output/`.

## Commands

### 1) Search actor

```bash
scripts/search_actor.sh "sec filings"
```

### 2) Run sync

```bash
scripts/run_actor_sync.sh <actor_id> '<json_input>' <output_json_path>
```

Example:

```bash
scripts/run_actor_sync.sh constant_quadruped~sec-edgar-filings-scraper '{"searchType":"ticker","tickers":["XPEV"],"formTypes":["20-F","6-K"],"limit":20}' /Users/tommy/Documents/output/apify/sec_xpev.json
```

### 3) Run async + fetch dataset

```bash
scripts/run_actor_async.sh <actor_id> '<json_input>'
scripts/fetch_dataset.sh <dataset_id> <output_json_path>
```

## Output conventions

- Default directory: `/Users/tommy/Documents/output/apify/`
- Keep raw output as `*_raw.json`.
- Write cleaned tables to `*.csv` and `*.md` when user asks.
- Keep source URLs and extraction timestamp in final output.

## Safety rules

- Never print token values.
- Do not hardcode credentials into files.
- Validate JSON input before run.
- Prefer primary sources (issuer IR, regulator filings, official docs).
