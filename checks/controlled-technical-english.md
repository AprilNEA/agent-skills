---
name: controlled-technical-english
description: Review English agent instructions and substantive code comments for material ambiguity using the repository's ASD-STE100-inspired profile.
severity-default: low
---

Review changed English prose in agent instructions, skills, guidance files, setup and check messages, safety guidance, and substantive code comments.

Look for:

- Different terms that refer to the same concept.
- Instructions without an imperative action or with multiple primary actions.
- Conditions stated after the actions that depend on them.
- Passive sentences that hide the actor.
- Pronouns with more than one possible referent.
- Inconsistent use of `must`, `should`, and `may`.
- Vague qualifiers without a condition or measurable threshold.
- Risky actions without a stop condition or failure behavior.
- Comments that restate code instead of explaining a reason, invariant, constraint, or risk.

Preserve exact commands, paths, identifiers, API names, product names, protocol terms, and quoted text. Treat 20 words for procedural sentences and 25 words for descriptive sentences as review signals, not hard limits.

This is an advisory check based on the repository's ASD-STE100-inspired profile. Do not require the official controlled dictionary and do not claim formal ASD-STE100 conformance. Report only material issues. For each finding, quote the ambiguous text and give the smallest clear rewrite.
