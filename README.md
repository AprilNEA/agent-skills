# Skills

Use this repo as your user skills directory:

```bash
./install.sh
```

The root-level installer bootstraps this repository's user-wide skills, global instructions, Amp checks, vendored submodules, and Git hook. Individual skills do not have or need their own installers.

`git submodule update --init` populates `vendor/vercel-agent-skills` and `vendor/karpathy-skills`, which the vendored skill symlinks point into. Both submodules are declared `shallow = true` in `.gitmodules`, so this fetches only their pinned commits without full history.

For Amp, `~/.config/amp/settings.json` can also point directly at this directory with `amp.skills.path`. Keep `~/.agents/skills` linked too; Amp path-scoped guidance `@`-mentions that path.

## Global Instructions

`install.sh` symlinks:

- Amp: `global/AGENTS.md`, `checks/`, and `~/.agents/skills`
- Claude Code: `global/CLAUDE.md` and each skill under `~/.claude/skills/`
- Codex: `global/CODEX.md` and each skill under `~/.codex/skills/`

The installer is idempotent but never replaces a non-matching file, directory, or symlink. Move or merge a conflicting path manually, then rerun it.

Check an existing install without changing links:

```bash
./install.sh --check
```

### Amp Orb Installation

From a pinned checkout of this repository, install only the Amp configuration needed by an orb:

```bash
./install.sh --orb
./install.sh --check-orb
```

Orb mode initializes vendored submodules and links `skills/` to `~/.agents/skills`, `global/AGENTS.md` to `~/.config/AGENTS.md`, and `checks/` to `~/.config/agents/checks`. It does not modify `~/.config/amp/AGENTS.md`, Claude Code, Codex, or Git hooks. Run `--orb` from `.agents/setup`, not `.agents/resume`; pin this repository to a reviewed tag or commit so fresh orbs are reproducible.

After `./install.sh` configures this repository's hook, edits under `global/parts/` are rebuilt automatically before commit.

`global/claude.settings.json` is a reference settings file. Merge it manually instead of symlinking it over an existing `~/.claude/settings.json`.

Shared `SKILL.md` files use only portable Agent Skills frontmatter. Amp path-scoped behavior lives in optional sibling `amp-guidance.md` files whose `globs` frontmatter applies because `global/parts/20-path-scoped.amp.md` explicitly `@`-mentions them. Claude Code and Codex rely on each skill's `description`; do not add generated client variants until trigger evaluations show they are necessary.

## Controlled Technical English

The generated global instructions and `better-skill-creator` use a controlled writing profile inspired by ASD-STE100 Simplified Technical English. Apply it to English agent instructions, setup and check messages, safety guidance, and substantive code comments. Preserve exact commands, paths, identifiers, API names, product names, protocol terms, and quoted text.

The detailed team profile and terminology are in [controlled-technical-english.md](skills/better-skill-creator/references/controlled-technical-english.md). The global Amp installation also provides `controlled-technical-english` as an advisory review check. The check reports material ambiguity; it does not reject text only for sentence length or vocabulary.

This repository does not claim formal ASD-STE100 conformance and does not redistribute the official controlled dictionary or standard. Request the current standard from the [ASD-STE100 official site](https://www.asd-ste100.org/STE_downloads.html) when formal conformance is required.

## Validation and Maintenance

Run the repository checks before committing skill or installer changes:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
ruff format --check .
ruff check .
```

The dependency-free validator enforces portable frontmatter in first-party `SKILL.md` files, validates Amp guidance globs, bundled references, check frontmatter, README inventory, vendored symlink confinement, and Amp `mcp.json` safety basics. It skips vendored skill contents; review upstream diffs separately when updating submodule pins.

For each skill change, manually review what cannot be linted reliably: whether `description` says both what and when without over-triggering, whether the main file contains only always-needed instructions, whether references have explicit loading conditions, and whether positive and negative trigger examples still select the intended skill. Pin executable dependencies, keep credentials out of skill files and fixtures, declare runtime/network requirements with `compatibility`, and restrict bundled MCP servers with `includeTools`.

Authoritative references: [Agent Skills specification](https://agentskills.io/specification), [skill authoring best practices](https://agentskills.io/skill-creation/best-practices), and [Amp Agent Skills documentation](https://ampcode.com/manual#agent-skills).

## Preferred Tools

The global instructions assume these CLI tools are available:

```bash
brew install jq yq
```

## Available Skills

- [better-skill-creator](skills/better-skill-creator/SKILL.md): write better skills than the default
- [browser-testing](skills/browser-testing/SKILL.md): browser automation with Playwright MCP
- [rust-coding](skills/rust-coding/SKILL.md): write high-quality Rust code

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
