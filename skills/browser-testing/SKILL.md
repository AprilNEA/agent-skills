---
name: browser-testing
description: "Uses Playwright browser automation for web UI testing, debugging, screenshots, console/network inspection, and interactive browser workflows. Use when a task needs browser interaction or visual verification."
compatibility: "Amp requires Node.js, npx, and network access for the bundled MCP server. Other agents need equivalent Playwright browser tools configured separately."
---

# Browser Testing

Use Playwright only when browser behavior matters: UI flows, screenshots, DOM inspection, console errors, network requests, or visual verification.
If the browser tools are unavailable, report the missing prerequisite instead of silently substituting unrelated automation.

In Claude Code the MCP server runs with `--extension`, so it attaches to the user's own Chrome through the Playwright Extension. Tabs, cookies, and logged-in sessions are real. Treat every action as happening in the user's live browser.

## Workflow

1. Navigate to the target URL.
2. Use accessibility snapshots before screenshots for interaction targets.
3. Inspect console and network output when debugging behavior.
4. Prefer user-visible interactions over DOM mutation.
5. Take screenshots only when visual evidence is needed.
6. Close only tabs you opened. Never close or navigate away from a tab the user was already using.

Do not use browser automation for tasks answerable by local code, tests, or direct HTTP requests.

## Setup

Claude Code loads this skill as a plugin through `.claude-plugin/plugin.json` and `.mcp.json`. It requires the [Playwright Extension](https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm). On the first browser action the extension opens a tab-picker page and the user chooses which tab to expose. To skip the per-connection approval dialog, copy `PLAYWRIGHT_MCP_EXTENSION_TOKEN` from the extension's status page into the `env` block of `~/.claude/settings.json`, never into this repository.
Amp uses the bundled `mcp.json`, which starts a headless browser instead.
