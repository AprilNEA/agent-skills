---
name: browser-testing
description: "Uses Playwright browser automation for web UI testing, debugging, screenshots, console/network inspection, and interactive browser workflows. Use when a task needs browser interaction or visual verification."
compatibility: "Amp requires Node.js, npx, and network access for the bundled MCP server. Other agents need equivalent Playwright browser tools configured separately."
---

# Browser Testing

Use Playwright only when browser behavior matters: UI flows, screenshots, DOM inspection, console errors, network requests, or visual verification.
If the browser tools are unavailable, report the missing prerequisite instead of silently substituting unrelated automation.

## Workflow

1. Navigate to the target URL.
2. Use accessibility snapshots before screenshots for interaction targets.
3. Inspect console and network output when debugging behavior.
4. Prefer user-visible interactions over DOM mutation.
5. Take screenshots only when visual evidence is needed.
6. Close tabs/pages when done.

Do not use browser automation for tasks answerable by local code, tests, or direct HTTP requests.
