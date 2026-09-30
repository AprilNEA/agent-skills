# Tool Use

- Do not bundle unrelated commands in a single shell call.
- Do not add decorative output or comments to commands whose output only the agent will see.
- Search before speculating about unfamiliar APIs, libraries, commands, or product behavior. Prefer authoritative sources and source code over SEO pages or generated summaries.
- Code is the primary source of truth. Read local code first; use external docs or web research only when local code is insufficient.
- For non-HTML or source artifacts, prefer CLI tools, repository source, or direct downloads over webpage extraction.
- Do not read or scan outside the working directory without user permission. If the user mentions a local codebase outside it, ask for the path.
