#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mode="${1:-install}"

if [ "$mode" != "install" ] && [ "$mode" != "--check" ] && [ "$mode" != "check" ]; then
  echo "Usage: ./install.sh [--check]" >&2
  exit 2
fi

link() {
  local target="$1"
  local dest="$2"

  mkdir -p "$(dirname -- "$dest")"

  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$target" ]; then
    return 0
  fi

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    echo "Refusing to replace existing path: $dest" >&2
    echo "Move or merge it manually, then rerun ./install.sh." >&2
    return 1
  fi

  ln -s "$target" "$dest"
}

ensure_real_dir() {
  local dir="$1"

  if [ -L "$dir" ]; then
    echo "Refusing to replace symlinked directory: $dir" >&2
    echo "Move or merge it manually, then rerun ./install.sh." >&2
    return 1
  fi

  if [ -e "$dir" ] && [ ! -d "$dir" ]; then
    echo "Refusing to replace non-directory path: $dir" >&2
    return 1
  fi

  mkdir -p "$dir"
}

check_link() {
  local target="$1"
  local dest="$2"

  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$target" ]; then
    echo "ok   $dest"
    return 0
  fi

  echo "fail $dest -> $target" >&2
  return 1
}

check_install() {
  local failed=0
  local hooks_path

  hooks_path="$(git -C "$repo_root" config --get core.hooksPath || true)"
  if [ "$hooks_path" = ".githooks" ]; then
    echo "ok   git core.hooksPath"
  else
    echo "fail git core.hooksPath -> .githooks" >&2
    failed=1
  fi

  check_link "$repo_root/skills" "$HOME/.agents/skills" || failed=1
  check_link "$repo_root/global/AGENTS.md" "$HOME/.config/amp/AGENTS.md" || failed=1
  check_link "$repo_root/checks" "$HOME/.config/amp/checks" || failed=1
  check_link "$repo_root/global/CLAUDE.md" "$HOME/.claude/CLAUDE.md" || failed=1
  check_link "$repo_root/global/CODEX.md" "$HOME/.codex/AGENTS.md" || failed=1

  for skill in "$repo_root"/skills/*; do
    if [ -L "$skill" ] && [ ! -e "$skill" ]; then
      echo "fail $skill is a broken symlink" >&2
      failed=1
      continue
    fi

    [ -d "$skill" ] || continue
    name="$(basename -- "$skill")"
    target="$(cd -- "$skill" && pwd)"

    check_link "$target" "$HOME/.claude/skills/$name" || failed=1
    check_link "$target" "$HOME/.codex/skills/$name" || failed=1
  done

  check_stale_skill_links "$HOME/.claude/skills" || failed=1
  check_stale_skill_links "$HOME/.codex/skills" || failed=1

  return "$failed"
}

check_stale_skill_links() {
  local skills_dir="$1"
  local failed=0
  local link
  local target

  [ -d "$skills_dir" ] || return 0

  for link in "$skills_dir"/*; do
    [ -L "$link" ] || continue
    target="$(readlink "$link")"

    case "$target" in
      "$repo_root"/skills/*)
        if [ ! -e "$target" ]; then
          echo "fail $link is a stale skill link" >&2
          failed=1
        fi
        ;;
    esac
  done

  return "$failed"
}

remove_stale_skill_links() {
  local skills_dir="$1"
  local link
  local target

  [ -d "$skills_dir" ] || return 0

  for link in "$skills_dir"/*; do
    [ -L "$link" ] || continue
    target="$(readlink "$link")"

    case "$target" in
      "$repo_root"/skills/*)
        [ -e "$target" ] || unlink "$link"
        ;;
    esac
  done
}

if [ "$mode" = "--check" ] || [ "$mode" = "check" ]; then
  check_install
  exit $?
fi

git -C "$repo_root" config core.hooksPath .githooks
git -C "$repo_root" submodule update --init

link "$repo_root/skills" "$HOME/.agents/skills"
link "$repo_root/global/AGENTS.md" "$HOME/.config/amp/AGENTS.md"
link "$repo_root/checks" "$HOME/.config/amp/checks"
link "$repo_root/global/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
link "$repo_root/global/CODEX.md" "$HOME/.codex/AGENTS.md"

ensure_real_dir "$HOME/.claude/skills"
ensure_real_dir "$HOME/.codex/skills"

remove_stale_skill_links "$HOME/.claude/skills"
remove_stale_skill_links "$HOME/.codex/skills"

for skill in "$repo_root"/skills/*; do
  [ -d "$skill" ] || continue
  name="$(basename -- "$skill")"
  target="$(cd -- "$skill" && pwd)"

  link "$target" "$HOME/.claude/skills/$name"
  link "$target" "$HOME/.codex/skills/$name"
done

cat <<EOF
Linked agent-skills from:
  $repo_root

Amp, Claude, and Codex need a new session to reload skills and guidance.
EOF
