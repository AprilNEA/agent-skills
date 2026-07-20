---
name: rust-coding
description: "Guides idiomatic Rust implementation and review. Use for any Rust task, especially API design, refactors, conversions, error handling, async code, unsafe code, and tests."
---

# Rust Coding

Write Rust in Rust's idioms, not as Python/JavaScript with types. Model the domain with types, keep ownership explicit, and let APIs communicate invariants.

## API Shape

- Prefer domain structs, enums, and newtypes over loose primitive parameter bundles.
- If a function takes more than four parameters, or repeatedly passes the same related values through layers, introduce or reuse a named input/config/context struct.
- Put behavior in `impl` blocks when it primarily operates on a type. Keep free functions for cross-type orchestration, local helpers, or operations without a natural receiver.
- Avoid boolean-heavy APIs. Replace multiple flags with an enum, options struct, or typed state when the combinations have meaning.
- Keep public APIs small and hard to misuse. Validate once at the boundary, then represent the validated state with types.

## Conversions

- Prefer `From<T> for U` for infallible, unsurprising, context-free conversions.
- Prefer `TryFrom<T> for U` when validation can fail and the failure belongs to the conversion.
- Prefer `AsRef`, `AsMut`, `Borrow`, or `Deref` only when they match established Rust semantics for cheap reference access.
- Avoid one-off `xxx_to_yyy` helpers when a standard conversion trait expresses the same relationship.
- Keep named conversion functions when the transformation is lossy, expensive, needs external context, has multiple valid meanings, performs I/O, or has a domain verb clearer than “convert”.
- At call sites, use `Target::from(value)` when the target type would not be obvious; use `.into()` only when inference and readability are clear.

## Ownership

- Accept borrowed inputs (`&str`, `&Path`, `&[T]`, references) when the function only reads data.
- Take ownership when storing, spawning, transferring, or intentionally consuming a value.
- Avoid defensive `clone()`. Clone at clear ownership boundaries and prefer restructuring signatures before cloning internally.
- Prefer iterator and slice APIs that let callers keep ownership.

## Module Layout

Use `foo/mod.rs` only when `foo` is a namespace shell that mainly declares or re-exports child modules with `mod`, `pub mod`, or `pub use`.
Use `foo.rs` when the module has its own semantics: types, functions, trait impls, errors, business rules, or module docs.
A `foo.rs` file may still declare child modules. Do not decide based on whether children exist; decide based on whether the parent module carries meaning.
Different modules may mix both styles, but the same module must not have both `foo.rs` and `foo/mod.rs`. Follow existing project style and avoid churn-only migrations.

## File Size

Recommended file size is under 500 lines. Hard limit is 1000 lines; if reached, break the file down.

## Error Handling

Use `thiserror` for library errors, `anyhow` in binary/CLI layers.

- Preserve typed errors across library boundaries.
- Add context at boundary layers where it helps the caller understand what failed.
- Do not convert errors to strings early unless crossing a boundary that requires strings.

## Documentation

Doc comments on every public item. `cargo doc` should produce useful, navigable documentation.

## Before Commit

Before committing, `cargo fmt --check`, `cargo clippy`, and `cargo test` must pass. For narrow changes, run the smallest equivalent targeted commands first, then broaden when shared contracts changed.

## Lint Suppressions

Follow the lint policy. Any non-test lint suppression must use the narrowest scope possible and include an explicit `reason = "..."`.

## Panic Policy

Do not use panic-prone code casually in non-test code. `unwrap`, `expect`, and similar operations are acceptable when a local invariant guarantees the value and making it fallible would only force fallibility onto callers up the call chain; make that invariant explicit in the code or comments.

## Unsafe Policy

Each unsafe block must contain a single operation with a `SAFETY` comment explaining why the invariant holds. Every unsafe function must have a `# Safety` doc section.

## Performance

Hot paths must have benchmarks. Any performance regression must be explained to the human before committing.

## Hygiene

Handle every `Result` — never silently discard. Do not hold locks or `RefCell` borrows across await points. Do not mark functions async unless they await.

## Review Checklist

Before finishing Rust work, check:

- Can a long parameter list become a named struct?
- Is a repeated parameter group being passed instead of modeled?
- Does a free function belong as a method on a type?
- Should an `xxx_to_yyy` helper be `From` or `TryFrom`?
- Are strings or booleans hiding an enum/newtype/domain state?
- Are clones, owned inputs, or async annotations justified by ownership or await points?
