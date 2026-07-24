# Writing

## Chinese

In Chinese text, use corner brackets 「」for quotes and always insert a space at CJK/Latin and CJK/digit boundaries.

## Controlled Technical English

Use this ASD-STE100-inspired profile for English prose in agent instructions (`AGENTS.md`, `SKILL.md`, and guidance files), setup and check messages, safety guidance, and substantive code comments:

- Use one term for one concept. Do not alternate between synonyms.
- Use imperative verbs for instructions. Put one primary action in each sentence or list item.
- State a necessary condition before the action that depends on it.
- Prefer active voice. Name the actor when the actor is not clear.
- Replace ambiguous pronouns such as `it`, `this`, and `they` with the applicable noun.
- Use `must` for requirements, `should` for recommendations, and `may` for permission.
- Replace vague qualifiers such as “normally,” “probably,” and “when appropriate” with a condition or measurable threshold.
- Use a list when one sentence contains multiple steps, alternatives, or conditions.

Treat 20 words for a procedural sentence and 25 words for a descriptive sentence as review signals, not hard limits. Keep a longer sentence when splitting it would hide an important relationship.

Preserve the exact spelling of commands, paths, identifiers, API names, product names, protocol terms, and quoted text. Do not add a code comment only to restate the code; explain a reason, invariant, constraint, or non-obvious risk.

This profile is inspired by ASD-STE100. It does not claim conformance with ASD-STE100 and does not use its controlled dictionary as a repository-wide vocabulary.
