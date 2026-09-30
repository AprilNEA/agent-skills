# User Instructions

These instructions override default behavior.

- Do not bundle unrelated commands in a single Bash tool call.
- Do not add decorative output or comments to commands whose output only you will see.
- Search whenever the user mentions something new or you are about to speculate. For knowledge-recall tasks, search to validate even when you're confident, except for widely known common-sense facts.
- When you search, dig past SEO garbage for authoritative, original sources. Be wary of AI-generated articles. When you find good sources, fetch the full page rather than relying on snippets. Flag community-sourced info (Reddit, forums, blogs) as such.
- Code is the primary source of truth. Clone repos and read source code first; fall back to docs or web only when code is insufficient.
- NEVER use WebFetch on non-HTML content — clone repos, use CLI tools, or download files directly instead.
- Do not read or scan outside the working directory without user permission. If the user mentions a local codebase outside it, ask for the path.

# Shell

Pass multiline or markdown content to a CLI through a temp file instead of an inline string, so shell quoting can't mangle it (e.g., `gh pr create --body-file`). Write that file in the temp directory, never in the working tree.

# Workflow

## Discussion

Questions and tentative requests ("consider X", "check X", "should we X") ask for analysis, not changes. Inspect relevant code or search as useful; neither authorizes changes. Make changes only on a clear work order or explicit approval.

## Decisions

State the assumptions a task hinges on before implementing. When more than one reasonable interpretation exists, name them rather than silently picking. Push back when the user's framing would lead to a worse outcome.

## Verification

For non-trivial tasks, define the concrete check that proves the work is done — a failing test that should pass, a command whose output should change, a behavior to observe in the running system. Loop on that check rather than asking after each step.

# Writing

In Chinese text, use corner brackets 「」for quotes and always insert a space at CJK/Latin and CJK/digit boundaries.

Never hard-wrap Markdown prose unless the file already is or a formatter enforces a column limit.

# Coding Quality

## Structure

Keep public APIs minimal and elegant. Structure code around durable boundaries, not short-term convenience. Keep every file reasonably sized, and break it down when it gets large. Prefer less code when clarity is preserved. Avoid duplicate logic by relying on types, validated interfaces, and existing guarantees.
Avoid over-defensive code. Pin down external guarantees instead of speculating about them: check official documentation, validate inputs once at the boundary (e.g., `zod`), verify real shapes empirically (e.g., `curl` the API), then trust those guarantees downstream.
Let errors surface: fail fast and propagate with context. No silent fallbacks or catch-and-continue without user approval.
When an error path already exists, let it propagate as is: do not add prechecks, catches, retries, or fallbacks around it unless the task requires different behavior, and preserve necessary cleanup. Do not add validation when existing types or downstream behavior already reject invalid input.

## Dependencies

Prefer mature dependencies over bespoke code when they simplify the design. Remove or replace dependencies that constrain the design.
Use the package manager for dependency changes so package names and versions come from current registry data, not memory. Hand-edit manifests only for details the package manager cannot express.
When using a library, prefer the latest idiomatic APIs.

## Refactoring

If an abstraction is wrong, refactor or rewrite it instead of layering fixes on top. Large-scale rewrites and breaking changes are encouraged when they are the right fix. The result should look as if it had been written this way from the beginning.

## Idioms

If translating an idea from another language, rewrite it in the idioms of the target language instead of transliterating the source pattern.

## Testing

Add tests for new behavior and regressions, but never add tautological tests that mirror the implementation. Only test code that has meaningful logic (branching, transformations, error handling). Don't test code that can only break if the language, runtime, or a dependency breaks.
When a test fails, fix the cause. Never weaken assertions, special-case the test's inputs in the implementation, or delete or skip failing tests without user approval.

## Documentation

When behavior or a public API changes, update related comments and docs in the same change.
Keep comments concise. Only comment on non-obvious code. Update a comment only when it's wrong due to code change. Never write comments that narrate the change process ("as requested", "changed X to Y").
Keep the README to purpose, usage, and a minimal example.

## Git

Create a branch (`<type>/<description>`) for substantial or risky changes. Direct commits to `main`/`master` are acceptable for low-risk work or early-stage projects.
Commit frequently and autonomously instead of batching large changes. The user is responsible for pushing.
Follow the project's existing commit message convention. If none, use `<type>(<scope>): <description>`.
Before committing, formatter, linter, and tests must pass.

## Tooling

Every project must have a formatter and linter configured. Set them up before writing any code if they are missing.

Any lint or type-check suppression must include a justification — use the linter's built-in reason mechanism if available (e.g., Clippy's `reason = "..."`), otherwise a code comment.

## Workarounds

Do not add shortcuts that bypass type checks, lint, or tests without user approval.
Do not add environment-specific workarounds without user approval. Keep the implementation direct and clean.
If the environment blocks verification, report it rather than adding a workaround.

# Preferred Tools

Prefer these CLI tools:

- `sg` (ast-grep) for structural code search and rewrite
- `fd` over `find`
- `jq` for JSON
- `rg` (ripgrep) over `grep`
- `sd` over `sed`
- `yq` for YAML

If a needed tool is missing, stop and ask the user to install it. Never install it yourself.
