#!/usr/bin/env bash
# =============================================================================
# sync-skills.sh
# 把 skills/ + overlays/<platform>/ 合并生成到各平台的运行时目录
#
# 用法：
#   ./scripts/sync-skills.sh              # 同步全部平台
#   ./scripts/sync-skills.sh claude       # 只同步 Claude Code
#   ./scripts/sync-skills.sh codex        # 只同步 Codex
#   ./scripts/sync-skills.sh openclaw     # 只同步 OpenClaw
#
# 合并规则：
#   dist/<platform>/<skill>/ = skills/<skill>/ 内容
#                            + overlays/<platform>/<skill>/ 内容（同名文件覆盖）
# =============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
OVERLAYS_SRC="$REPO_ROOT/overlays"
DIST="$REPO_ROOT/dist"

# ── 运行时目标目录 ────────────────────────────────────────────────
CLAUDE_DEST="$HOME/.claude/skills"
CODEX_DEST="$HOME/.codex/skills"
OPENCLAW_DEST="$HOME/clawd/skills"

# ── 颜色输出 ──────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
RESET='\033[0m'

log()  { echo -e "${CYAN}[sync]${RESET} $*"; }
ok()   { echo -e "${GREEN}  ✅ $*${RESET}"; }
warn() { echo -e "${YELLOW}  ⚠️  $*${RESET}"; }
err()  { echo -e "${RED}  ❌ $*${RESET}"; }

# ── 核心：生成单个平台的 dist ─────────────────────────────────────
build_platform() {
  local platform="$1"
  local dist_dir="$DIST/$platform"

  log "Building dist/$platform ..."
  rm -rf "$dist_dir"
  mkdir -p "$dist_dir"

  for skill_dir in "$SKILLS_SRC"/*/; do
    local skill
    skill=$(basename "$skill_dir")
    local dest="$dist_dir/$skill"

    # 1. 复制公共内容
    cp -r "$skill_dir" "$dest"

    # 2. 合并 overlay（同名文件覆盖，新文件追加）
    local overlay="$OVERLAYS_SRC/$platform/$skill"
    if [ -d "$overlay" ]; then
      cp -r "$overlay/." "$dest/"
      ok "$skill  (+overlay)"
    else
      ok "$skill"
    fi
  done
}

# ── 部署：把 dist/<platform>/ 同步到运行时目录 ───────────────────
deploy_platform() {
  local platform="$1"
  local dist_dir="$DIST/$platform"
  local dest

  case "$platform" in
    claude)   dest="$CLAUDE_DEST" ;;
    codex)    dest="$CODEX_DEST" ;;
    openclaw) dest="$OPENCLAW_DEST" ;;
    *)
      warn "未知平台 '$platform'，跳过部署"
      return
      ;;
  esac

  log "Deploying dist/$platform → $dest"
  mkdir -p "$dest"

  for skill_dir in "$dist_dir"/*/; do
    local skill
    skill=$(basename "$skill_dir")
    # 覆盖式同步：删旧建新
    rm -rf "$dest/$skill"
    cp -r "$skill_dir" "$dest/$skill"
  done

  ok "已部署 $(ls "$dist_dir" | wc -l | tr -d ' ') 个 skills → $dest"
}

# ── 主流程 ────────────────────────────────────────────────────────
PLATFORMS=("claude" "codex" "openclaw")

# 如果指定了平台参数，只处理该平台
if [ $# -ge 1 ]; then
  PLATFORMS=("$@")
fi

echo ""
echo "=================================================="
echo "  ai-skill sync-skills.sh"
echo "  repo: $REPO_ROOT"
echo "  platforms: ${PLATFORMS[*]}"
echo "=================================================="
echo ""

for platform in "${PLATFORMS[@]}"; do
  build_platform "$platform"
  deploy_platform "$platform"
  echo ""
done

echo "=================================================="
log "全部完成 🎉"
echo "  Claude Code : $CLAUDE_DEST"
echo "  Codex       : $CODEX_DEST"
echo "  OpenClaw    : $OPENCLAW_DEST"
echo "=================================================="
