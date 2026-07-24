#!/usr/bin/env python3
"""Validate first-party skills and repository skill metadata without external packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

PORTABLE_FIELDS = {
    "allowed-tools",
    "compatibility",
    "description",
    "license",
    "metadata",
    "name",
}
CHECK_FIELDS = {"description", "name", "severity-default", "tools"}
CHECK_SEVERITIES = {"critical", "high", "low", "medium"}
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
FIELD_PATTERN = re.compile(r"([A-Za-z0-9_-]+):(?:[ \t]*(.*))?")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^]]*]\(([^)]+)\)")
BUNDLED_PATH_PATTERN = re.compile(r"`((?:assets|references|scripts)/[A-Za-z0-9._/-]+)`")
README_SKILL_PATTERN = re.compile(
    r"]\((skills|project-skills)/([a-z0-9]+(?:-[a-z0-9]+)*)/SKILL\.md\)"
)
EXACT_NPM_PACKAGE_PATTERN = re.compile(
    r"(?:@[^/@\s]+/[^@\s]+|[^@/\s]+)@\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?"
)


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    validated: int = 0
    validated_checks: int = 0
    skipped: int = 0

    def error(self, path: Path, message: str, root: Path) -> None:
        self.errors.append(f"{_display_path(path, root)}: {message}")

    def warning(self, path: Path, message: str, root: Path) -> None:
        self.warnings.append(f"{_display_path(path, root)}: {message}")


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _parse_frontmatter(
    manifest: Path, root: Path, result: ValidationResult
) -> tuple[str, dict[str, tuple[str, int]]] | None:
    try:
        text = manifest.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        result.error(manifest, f"cannot read UTF-8 text: {error}", root)
        return None

    lines = text.splitlines()
    if not lines or lines[0] != "---":
        result.error(manifest, "must start with an exact '---' frontmatter delimiter", root)
        return None

    try:
        closing_index = lines[1:].index("---") + 1
    except ValueError:
        result.error(manifest, "frontmatter is not closed by an exact '---' line", root)
        return None

    fields: dict[str, tuple[str, int]] = {}
    for line_number, line in enumerate(lines[1:closing_index], start=2):
        if not line.strip() or line.lstrip().startswith("#") or line[0].isspace():
            continue
        match = FIELD_PATTERN.fullmatch(line)
        if not match:
            result.error(manifest, f"line {line_number} is not a valid top-level field", root)
            continue
        key, value = match.groups()
        if key in fields:
            result.error(manifest, f"line {line_number} duplicates frontmatter field '{key}'", root)
            continue
        fields[key] = (value or "", line_number)

    if not any(line.strip() for line in lines[closing_index + 1 :]):
        result.warning(manifest, "has no instruction body after frontmatter", root)
    if len(lines) > 500:
        result.warning(
            manifest, f"has {len(lines)} lines; the format recommends fewer than 500", root
        )

    return text, fields


def _parse_scalar(
    manifest: Path,
    key: str,
    raw_value: str,
    line_number: int,
    root: Path,
    result: ValidationResult,
) -> str | None:
    value = raw_value.strip()
    if not value:
        result.error(manifest, f"line {line_number} field '{key}' must be a one-line string", root)
        return None

    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            result.error(
                manifest, f"line {line_number} field '{key}' has invalid quotes: {error}", root
            )
            return None
        if not isinstance(parsed, str):
            result.error(manifest, f"line {line_number} field '{key}' must be a string", root)
            return None
        return parsed

    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            result.error(manifest, f"line {line_number} field '{key}' has invalid quotes", root)
            return None
        return value[1:-1].replace("''", "'")

    if value[0] in "[{|>&*!" or re.fullmatch(r"(?i:null|~|true|false|[-+]?\d+(?:\.\d+)?)", value):
        result.error(manifest, f"line {line_number} field '{key}' must be a string", root)
        return None
    return value


def _validate_references(
    skill_dir: Path, manifest: Path, text: str, root: Path, result: ValidationResult
) -> None:
    references = {match.group(1) for match in BUNDLED_PATH_PATTERN.finditer(text)}
    for match in MARKDOWN_LINK_PATTERN.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")]
        else:
            parts = target.split(maxsplit=1)
            if not parts:
                result.error(manifest, "Markdown link has an empty target", root)
                continue
            target = parts[0]
        references.add(target)

    skill_root = skill_dir.resolve()
    for reference in sorted(references):
        if not reference or reference.startswith(("#", "/")) or "://" in reference:
            continue
        path_text = unquote(reference.split("#", 1)[0].split("?", 1)[0])
        candidate = (skill_dir / path_text).resolve(strict=False)
        if not candidate.is_relative_to(skill_root):
            result.error(
                manifest, f"bundled reference escapes the skill directory: {reference}", root
            )
        elif not candidate.exists():
            result.error(manifest, f"bundled reference does not exist: {reference}", root)


def _validate_mcp(skill_dir: Path, root: Path, result: ValidationResult) -> None:
    config_path = skill_dir / "mcp.json"
    if not config_path.exists():
        return

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        result.error(config_path, f"invalid JSON: {error}", root)
        return
    if not isinstance(data, dict) or not data:
        result.error(config_path, "must contain at least one named MCP server", root)
        return

    for server_name, config in data.items():
        if not isinstance(server_name, str) or not isinstance(config, dict):
            result.error(config_path, "server names must map to objects", root)
            continue
        has_command = isinstance(config.get("command"), str) and bool(config["command"])
        has_url = isinstance(config.get("url"), str) and bool(config["url"])
        if has_command == has_url:
            result.error(
                config_path,
                f"server '{server_name}' must define exactly one of 'command' or 'url'",
                root,
            )
        if has_url and not config["url"].startswith("https://"):
            result.error(config_path, f"server '{server_name}' must use an HTTPS URL", root)

        include_tools = config.get("includeTools")
        if include_tools is None:
            result.warning(
                config_path, f"server '{server_name}' should restrict includeTools", root
            )
        elif (
            not isinstance(include_tools, list)
            or not include_tools
            or not all(isinstance(tool, str) and tool for tool in include_tools)
        ):
            result.error(
                config_path,
                f"server '{server_name}' includeTools must be a non-empty string list",
                root,
            )

        args = config.get("args", [])
        if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
            result.error(config_path, f"server '{server_name}' args must be a string list", root)
            continue
        if has_command and Path(config["command"]).name in {"npx", "npx.cmd"}:
            package = next((arg for arg in args if not arg.startswith("-")), None)
            if package is None or not EXACT_NPM_PACKAGE_PATTERN.fullmatch(package):
                result.error(
                    config_path,
                    f"server '{server_name}' must pin its npx package to an exact version",
                    root,
                )


def _validate_amp_guidance(skill_dir: Path, root: Path, result: ValidationResult) -> None:
    guidance = skill_dir / "amp-guidance.md"
    if not guidance.exists():
        return

    parsed = _parse_frontmatter(guidance, root, result)
    if parsed is None:
        return
    text, fields = parsed

    unknown_fields = sorted(set(fields) - {"globs"})
    if unknown_fields:
        result.error(guidance, f"unsupported top-level fields: {', '.join(unknown_fields)}", root)
    if "globs" not in fields:
        result.error(guidance, "missing required frontmatter field 'globs'", root)
        return

    raw_value, field_line = fields["globs"]
    if raw_value.strip():
        result.error(guidance, "globs must use an indented YAML list", root)

    lines = text.splitlines()
    closing_index = lines[1:].index("---") + 1
    patterns: list[str] = []
    for line_number, line in enumerate(lines[field_line:closing_index], start=field_line + 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"  -[ \t]+(.+)", line)
        if not match:
            result.error(guidance, f"line {line_number} is not a canonical globs item", root)
            continue
        value = _parse_scalar(guidance, "globs item", match.group(1), line_number, root, result)
        if value is not None:
            patterns.append(value)
    if not patterns:
        result.error(guidance, "globs must contain at least one pattern", root)


def _validate_skill(skill_dir: Path, root: Path, result: ValidationResult) -> None:
    manifest = skill_dir / "SKILL.md"
    if not manifest.is_file():
        result.error(skill_dir, "is missing SKILL.md", root)
        return

    parsed = _parse_frontmatter(manifest, root, result)
    if parsed is None:
        return
    text, fields = parsed

    unknown_fields = sorted(set(fields) - PORTABLE_FIELDS)
    if unknown_fields:
        result.error(manifest, f"unsupported top-level fields: {', '.join(unknown_fields)}", root)

    values: dict[str, str] = {}
    for key in ("name", "description"):
        if key not in fields:
            result.error(manifest, f"missing required frontmatter field '{key}'", root)
            continue
        raw_value, line_number = fields[key]
        value = _parse_scalar(manifest, key, raw_value, line_number, root, result)
        if value is not None:
            values[key] = value

    name = values.get("name")
    if name is not None:
        if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
            result.error(
                manifest, "name must be 1-64 ASCII lowercase letters, digits, or hyphens", root
            )
        if name != skill_dir.name:
            result.error(
                manifest, f"name '{name}' does not match directory '{skill_dir.name}'", root
            )

    description = values.get("description")
    if description is not None and not 1 <= len(description) <= 1024:
        result.error(manifest, "description must contain 1-1024 characters", root)

    for key, maximum in (("license", None), ("compatibility", 500), ("allowed-tools", None)):
        if key not in fields:
            continue
        raw_value, line_number = fields[key]
        value = _parse_scalar(manifest, key, raw_value, line_number, root, result)
        if value is not None and maximum is not None and not 1 <= len(value) <= maximum:
            result.error(manifest, f"{key} must contain 1-{maximum} characters", root)

    _validate_references(skill_dir, manifest, text, root, result)
    _validate_mcp(skill_dir, root, result)
    _validate_amp_guidance(skill_dir, root, result)
    result.validated += 1


def _validate_check(check: Path, root: Path, result: ValidationResult) -> None:
    parsed = _parse_frontmatter(check, root, result)
    if parsed is None:
        return
    _, fields = parsed

    unknown_fields = sorted(set(fields) - CHECK_FIELDS)
    if unknown_fields:
        result.error(check, f"unsupported top-level fields: {', '.join(unknown_fields)}", root)

    if "name" not in fields:
        result.error(check, "missing required frontmatter field 'name'", root)
    else:
        raw_value, line_number = fields["name"]
        name = _parse_scalar(check, "name", raw_value, line_number, root, result)
        if name is not None:
            if not NAME_PATTERN.fullmatch(name):
                result.error(
                    check, "name must use ASCII lowercase letters, digits, or hyphens", root
                )
            if name != check.stem:
                result.error(check, f"name '{name}' does not match filename '{check.stem}'", root)

    if "description" in fields:
        raw_value, line_number = fields["description"]
        _parse_scalar(check, "description", raw_value, line_number, root, result)

    if "severity-default" in fields:
        raw_value, line_number = fields["severity-default"]
        severity = _parse_scalar(check, "severity-default", raw_value, line_number, root, result)
        if severity is not None and severity not in CHECK_SEVERITIES:
            allowed = ", ".join(sorted(CHECK_SEVERITIES))
            result.error(check, f"severity-default must be one of: {allowed}", root)

    result.validated_checks += 1


def _validate_checks(root: Path, result: ValidationResult) -> None:
    checks_dir = root / "checks"
    if not checks_dir.is_dir():
        return
    for check in sorted(checks_dir.glob("*.md")):
        _validate_check(check, root, result)


def _skill_entries(root: Path) -> set[tuple[str, str]]:
    entries: set[tuple[str, str]] = set()
    for directory_name in ("skills", "project-skills"):
        directory = root / directory_name
        if not directory.is_dir():
            continue
        for entry in directory.iterdir():
            if entry.is_dir() or entry.is_symlink():
                entries.add((directory_name, entry.name))
    return entries


def _validate_readme(root: Path, actual: set[tuple[str, str]], result: ValidationResult) -> None:
    readme = root / "README.md"
    try:
        text = readme.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        result.error(readme, f"cannot read UTF-8 text: {error}", root)
        return
    documented = set(README_SKILL_PATTERN.findall(text))
    for directory_name, name in sorted(actual - documented):
        result.error(readme, f"does not list {directory_name}/{name}", root)
    for directory_name, name in sorted(documented - actual):
        result.error(readme, f"lists missing skill {directory_name}/{name}", root)


def validate_repository(root: Path) -> ValidationResult:
    root = root.resolve()
    result = ValidationResult()
    actual = _skill_entries(root)
    vendor_root = (root / "vendor").resolve()

    for directory_name, name in sorted(actual):
        skill_dir = root / directory_name / name
        if skill_dir.is_symlink():
            target = skill_dir.resolve(strict=False)
            if directory_name != "skills" or not target.is_relative_to(vendor_root):
                result.error(skill_dir, "symlink target must stay inside vendor/", root)
            else:
                result.skipped += 1
            continue
        _validate_skill(skill_dir, root, result)

    _validate_checks(root, result)
    _validate_readme(root, actual, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to this script's parent repository)",
    )
    args = parser.parse_args()
    result = validate_repository(args.root)

    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)

    if result.errors:
        print(
            f"Validation failed with {len(result.errors)} error(s) and "
            f"{len(result.warnings)} warning(s).",
            file=sys.stderr,
        )
        return 1
    print(
        f"Validated {result.validated} first-party skill(s) and "
        f"{result.validated_checks} check(s); "
        f"skipped {result.skipped} vendored skill(s); {len(result.warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
