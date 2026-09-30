# Skills

Use this repo as your user skills directory:

```bash
./install.sh
```

`git submodule update --init` populates `vendor/vercel-agent-skills`, which the `skills/react-best-practices` symlink points into. The submodule is declared `shallow = true` in `.gitmodules`, so this fetches only the latest commit.

For Amp, `~/.config/amp/settings.json` can also point directly at this directory with `amp.skills.path`. Keep `~/.agents/skills` linked too; Amp path-scoped guidance `@`-mentions that path.

## Global Instructions

`install.sh` symlinks:

- Amp: `global/AGENTS.md`, `checks/`, and `~/.agents/skills`
- Claude Code: `global/CLAUDE.md` and each skill under `~/.claude/skills/`
- Codex: `global/CODEX.md` and each skill under `~/.codex/skills/`

Check an existing install without changing links:

```bash
./install.sh --check
```

Edit `global/parts/` — the pre-commit hook rebuilds automatically.

`global/claude.settings.json` is a reference settings file. Merge it manually instead of symlinking it over an existing `~/.claude/settings.json`.

Path-scoped guidance uses Claude Code `paths` and Amp `globs` frontmatter in skill files. For Amp, add or remove `@` mentions in `global/parts/20-path-scoped.amp.md`.

## Preferred Tools

The global instructions assume these CLI tools are available:

```bash
brew install ast-grep fd jq ripgrep sd yq
```

## Project-scoped Skills

Skills under `project-skills/` are **not** installed globally — `install.sh` ignores them. They carry conventions specific to one codebase, so install them only into the repos where they apply, with [skills.sh](https://skills.sh) (`npx skills`). Run inside the target repo and pick the **project** scope when prompted:

```bash
npx skills add arcboxlabs/agent-skills/project-skills/linear
```

This installs into the repo's own `.claude/skills/` (and any other detected agent's project dir), so Claude Code loads it only within that repo. The repo is private, so `npx skills` needs GitHub auth. Add `--copy` to vendor the files instead of symlinking; `--global` installs into `~/.claude/skills` for every project (the opposite of what you usually want here).

- [linear](project-skills/linear/SKILL.md): ArcBox Linear workflow — issue lifecycle, comment-driven sync, status, triage

## Available Skills

- [better-skill-creator](skills/better-skill-creator/SKILL.md): write better skills than the default
- [browser-testing](skills/browser-testing/SKILL.md): browser automation with Playwright MCP
- [rust-coding](skills/rust-coding/SKILL.md): write high-quality Rust code
- [slides-creator](skills/slides-creator/SKILL.md): create new slide decks and `.pptx` presentations
- [waku-idiomatic](skills/waku-idiomatic/SKILL.md): opinionated Waku patterns and structure

### Vendored

Symlinked from `vendor/vercel-agent-skills` ([vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)):

- [react-best-practices](skills/react-best-practices/SKILL.md): React and Next.js performance patterns from Vercel Engineering
- [composition-patterns](skills/composition-patterns/SKILL.md): React composition patterns for compound components, render props, and context providers
- [web-design-guidelines](skills/web-design-guidelines/SKILL.md): review UI code against Vercel's Web Interface Guidelines

Symlinked from `vendor/karpathy-skills` ([multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)):

- [karpathy-guidelines](skills/karpathy-guidelines/SKILL.md): behavioral guidelines to reduce common LLM coding mistakes

Symlinked from `vendor/rust-skills` ([leonardomso/rust-skills](https://github.com/leonardomso/rust-skills)):

- [rust-skills](skills/rust-skills/SKILL.md): 265 idiomatic Rust rules across 26 categories, loaded per rule on demand; `rust-coding` wins on conflicts

Symlinked from `vendor/vercel-skills` ([vercel-labs/skills](https://github.com/vercel-labs/skills)):

- [find-skills](skills/find-skills/SKILL.md): discover and install skills from skills.sh with `npx skills`
