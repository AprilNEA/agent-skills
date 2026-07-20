---
name: slides-creator
description: "Use this skill any time the user wants to create a slide deck, presentation, or .pptx file from scratch. Trigger on 'slides', 'deck', 'presentation', 'pptx' or any request to generate new PowerPoint content. Do NOT use for reading or editing existing .pptx files."
compatibility: "Requires Deno and network access to fetch jsr:@pixel/pptx@0.15.0. Visual QA also requires LibreOffice and pdftoppm."
---

# Slides Creator

Create presentations using `jsr:@pixel/pptx@0.15.0`.

## Workflow

1. **Check prerequisites.** Verify Deno, LibreOffice, and `pdftoppm` are available. If not, report the missing prerequisite; do not install system software without approval.
2. **Inspect the pinned API:** run `deno doc jsr:@pixel/pptx@0.15.0` and filter for the symbols needed by the deck. Do not write code from memory.
3. **Write a one-shot script** in a temp directory that imports `jsr:@pixel/pptx@0.15.0`, then run it with Deno.
4. **QA visually.** Convert the `.pptx` to PDF with LibreOffice, then PDF to PNG with `pdftoppm`. Inspect every slide image. Fix and re-verify.

Update the pinned version only after reviewing its release and regenerating a representative deck.
