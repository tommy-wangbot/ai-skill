#!/usr/bin/env python3
"""
自动生成 README.md 中的 Skills 目录部分。
读取 skills/*/SKILL.md 的 frontmatter，
按 scripts/skill_categories.yaml 分组，
替换 README 中 <!-- SKILLS_START --> 和 <!-- SKILLS_END --> 之间的内容。
"""

import os
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
CATEGORIES_FILE = REPO_ROOT / "scripts" / "skill_categories.yaml"
README_FILE = REPO_ROOT / "README.md"

SKILLS_START = "<!-- SKILLS_START -->"
SKILLS_END = "<!-- SKILLS_END -->"


def parse_frontmatter(skill_path: Path) -> dict:
    """从 SKILL.md 中提取 YAML frontmatter。"""
    text = skill_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def load_all_skills() -> dict[str, dict]:
    """返回 {skill_name: {name, description}} 字典。"""
    skills = {}
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = parse_frontmatter(skill_md)
        name = fm.get("name") or skill_dir.name
        desc = fm.get("description") or ""
        # description 可能很长，截取第一句（到句号/。/，）
        desc = re.split(r"[。，,\.。；;]", desc)[0].strip()
        # 去掉触发词部分（"触发词：..." 开始的内容）
        desc = re.sub(r"[，,]?\s*触发词[：:].*", "", desc).strip()
        skills[skill_dir.name] = {"name": name, "description": desc}
    return skills


def generate_table(skill_names: list[str], all_skills: dict) -> str:
    """生成 Markdown 表格行。"""
    lines = []
    for name in skill_names:
        if name not in all_skills:
            continue
        desc = all_skills[name]["description"]
        lines.append(f"| `{name}` | {desc} |")
    return "\n".join(lines)


def generate_skills_section(categories: dict, all_skills: dict) -> str:
    """生成完整的 Skills 目录 Markdown 块。"""
    lines = []

    # 统计已分类的 skill
    categorized = set()
    for cat in categories["categories"].values():
        categorized.update(cat["skills"])

    # 未分类的 skill（在 skills/ 目录但不在任何 category 中）
    uncategorized = [s for s in sorted(all_skills.keys()) if s not in categorized]

    total = sum(
        len([s for s in cat["skills"] if s in all_skills])
        for cat in categories["categories"].values()
    ) + len(uncategorized)

    lines.append(f"## Skills 目录（共 {total} 个）\n")

    for cat_key, cat in categories["categories"].items():
        valid_skills = [s for s in cat["skills"] if s in all_skills]
        if not valid_skills:
            continue
        lines.append(f"### {cat['label']}（{len(valid_skills)}个）\n")
        lines.append("| Skill | 功能描述 |")
        lines.append("|-------|---------|")
        lines.append(generate_table(valid_skills, all_skills))
        lines.append("")

    if uncategorized:
        lines.append(f"### 未分类（{len(uncategorized)}个）\n")
        lines.append("> 新增 skill，请在 `scripts/skill_categories.yaml` 中归类。\n")
        lines.append("| Skill | 功能描述 |")
        lines.append("|-------|---------|")
        lines.append(generate_table(uncategorized, all_skills))
        lines.append("")

    return "\n".join(lines)


def update_readme(new_section: str) -> bool:
    """替换 README 中标记区间内的内容，返回是否有变化。"""
    readme = README_FILE.read_text(encoding="utf-8")

    pattern = re.compile(
        rf"{re.escape(SKILLS_START)}.*?{re.escape(SKILLS_END)}",
        re.DOTALL,
    )

    replacement = f"{SKILLS_START}\n{new_section}\n{SKILLS_END}"

    if not pattern.search(readme):
        print("ERROR: README 中找不到 SKILLS_START/SKILLS_END 标记", file=sys.stderr)
        sys.exit(1)

    new_readme = pattern.sub(replacement, readme)
    if new_readme == readme:
        print("README 无变化，跳过写入。")
        return False

    README_FILE.write_text(new_readme, encoding="utf-8")
    print(f"README 已更新。")
    return True


def main():
    all_skills = load_all_skills()
    print(f"发现 {len(all_skills)} 个 skill")

    categories = yaml.safe_load(CATEGORIES_FILE.read_text(encoding="utf-8"))
    section = generate_skills_section(categories, all_skills)
    changed = update_readme(section)
    sys.exit(0 if True else 1)


if __name__ == "__main__":
    main()
