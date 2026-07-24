# Controlled Technical English for Agent Instructions

## Status and Scope

This repository uses an ASD-STE100-inspired writing profile. It is a small team style guide, not an implementation or reproduction of ASD-STE100. Text that follows this profile is not necessarily conformant with ASD-STE100.

Apply this profile to English prose in:

- `AGENTS.md`, `SKILL.md`, and agent guidance files;
- setup, installation, validation, and check messages;
- safety or data-loss instructions;
- code comments and docstrings that explain non-obvious behavior.

Do not apply controlled vocabulary rules to commands, paths, identifiers, API names, product names, protocol terms, error text that must match an external system, or quoted text. This profile does not govern Chinese prose.

## Authoring Rules

1. Use one term for one concept. Do not use a synonym only for variety.
2. Write instructions in the imperative. Put one primary action in each sentence or list item.
3. Put a necessary condition before the action that depends on it.
4. Prefer active voice. Name the actor when the actor is not clear.
5. Replace an ambiguous pronoun with the applicable noun.
6. Use `must` for a requirement, `should` for a recommendation, and `may` for permission.
7. Replace “normally,” “probably,” “usually,” “as needed,” and “when appropriate” with a condition or measurable threshold.
8. Use a vertical list for multiple steps, alternatives, or conditions.
9. Keep related constraints together. Do not shorten text if the shorter text loses a prerequisite, exception, or failure behavior.
10. State the expected result of an action. For a risky action, also state the stop condition and recovery action.

Use 20 words as a review signal for a procedural sentence and 25 words as a review signal for a descriptive sentence. These values are not hard limits in this profile. Split a long sentence only when each new sentence remains complete and unambiguous.

## Code Comments

Add a comment only when it explains information that the code cannot express clearly. Explain a reason, invariant, constraint, compatibility requirement, or non-obvious risk. Do not add a comment that only restates an operation.

Keep exact code terms in comments. A technical identifier is preferable to a simpler but inaccurate synonym.

## Project Terms

Use these terms consistently in this repository:

| Term | Meaning |
| --- | --- |
| agent | The software process that follows instructions and uses tools. Use `model` only for the inference model. |
| skill | A reusable directory that contains `SKILL.md` and optional resources. |
| guidance | Instructions loaded from an agent file or client-specific sidecar. |
| check | An Amp review criterion stored in `checks/`. Do not use `validator` for this concept. |
| validator | `scripts/validate_skills.py`, which checks repository structure and metadata. |
| orb | An Amp sandbox execution environment. Do not use `container` or `VM` as a synonym. |
| setup | Initialization for a new orb. Use `resume` only for work that runs when an existing orb resumes. |

## Review Policy

Report language that creates a material ambiguity, changes an obligation, hides a condition, or makes an action unsafe. Include the smallest clear rewrite.

Do not report a finding only because a sentence exceeds a review signal or contains a word that is not in the ASD-STE100 dictionary. Do not rewrite exact technical text. Prefer clarity and technical accuracy over mechanical simplicity.

## Sources and Rights

- [ASD-STE100 official site](https://www.asd-ste100.org/)
- [ASD overview of Simplified Technical English](https://www.asd-europe.org/standards-specifications/simplified-technical-english/)
- [Official FAQ](https://www.asd-ste100.org/STE_faq.html)
- [Request the current official issue](https://www.asd-ste100.org/STE_downloads.html)

Issue 9 was published in January 2025. Confirm the current issue before work that requires formal conformance.

ASD states that ASD-STE100 Simplified Technical English is its copyright and trademark. Link to the official standard. Do not copy its PDF, controlled dictionary, logo, or substantial rule text into this repository without confirmed permission.
