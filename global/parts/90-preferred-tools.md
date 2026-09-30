# Preferred Tools

Prefer these CLI tools:

- `sg` (ast-grep) for structural code search and rewrite
- `fd` over `find`
- `jq` for JSON
- `rg` (ripgrep) over `grep`
- `sd` over `sed`
- `yq` for YAML

If a needed tool is missing, stop and ask the user to install it. Never install it yourself.

## ripgrep

- `rg` is recursive by default and respects `.gitignore`. Never pass `-r`: in ripgrep `-r`/`--replace` rewrites the printed match, it is not "recursive".
- Use `-F` for literal strings, and `-e PATTERN` or `--` before a pattern that starts with `-`.
- Scope with `-t rust`, `-g '*.md'`, or `-g '!vendor'` instead of piping into `grep`; `--files` lists what would be searched. Add `--hidden` for dotfiles, `--no-ignore` or `-u` for ignored files, `-a` for binaries.
- Shape output with `-n`, `-l`, `-c`, `-o`, `-A`/`-B`/`-C`, `-m N`; use `-U` for multiline patterns.
- Exit status 1 means no match, 2 means error. In `&&` chains a no-match aborts the chain; append `|| true` when an empty result is acceptable.
