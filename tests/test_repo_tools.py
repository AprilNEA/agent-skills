from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate_skills import validate_repository

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def write_skill(
    root: Path, name: str, extra_frontmatter: str = "", body: str = "Instructions."
) -> Path:
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        f'description: "Performs {name} tasks. Use when {name} work is requested."\n'
        f"{extra_frontmatter}"
        "---\n\n"
        f"{body}\n",
        encoding="utf-8",
    )
    return skill_dir


def write_readme(root: Path, *names: str) -> None:
    links = "\n".join(f"- [{name}](skills/{name}/SKILL.md)" for name in names)
    (root / "README.md").write_text(f"# Skills\n\n{links}\n", encoding="utf-8")


def write_amp_guidance(skill_dir: Path, *patterns: str) -> None:
    items = "\n".join(f"  - {pattern!r}" for pattern in patterns)
    (skill_dir / "amp-guidance.md").write_text(
        f"---\nglobs:\n{items}\n---\n\nLoad and follow the matching skill.\n",
        encoding="utf-8",
    )


class SkillValidatorTests(unittest.TestCase):
    def test_validates_references_amp_guidance_and_pinned_mcp(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill = write_skill(
                root,
                "browser-testing",
                'compatibility: "Requires Node.js and network access."\n',
                "Read `references/usage.md` when examples are needed.",
            )
            write_amp_guidance(skill, "**/*.html")
            (skill / "references").mkdir()
            (skill / "references" / "usage.md").write_text("# Usage\n", encoding="utf-8")
            (skill / "mcp.json").write_text(
                '{"playwright":{"command":"npx","args":["-y",'
                '"@playwright/mcp@0.0.78"],"includeTools":["browser_navigate"]}}\n',
                encoding="utf-8",
            )
            write_readme(root, "browser-testing")

            result = validate_repository(root)

            self.assertEqual(result.errors, [])
            self.assertEqual(result.validated, 1)

    def test_rejects_mismatched_name_missing_reference_and_floating_mcp(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill = write_skill(
                root,
                "browser-testing",
                extra_frontmatter='paths:\n  - "**/*.html"\n',
                body="Read `references/missing.md` or [an empty link]( ).",
            )
            manifest = skill / "SKILL.md"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "name: browser-testing", "name: other-name"
                ),
                encoding="utf-8",
            )
            (skill / "mcp.json").write_text(
                '{"playwright":{"command":"npx","args":["-y",'
                '"@playwright/mcp@latest"],"includeTools":["browser_navigate"]}}\n',
                encoding="utf-8",
            )
            write_readme(root, "browser-testing")

            messages = "\n".join(validate_repository(root).errors)

            self.assertIn("does not match directory", messages)
            self.assertIn("unsupported top-level fields: paths", messages)
            self.assertIn("bundled reference does not exist", messages)
            self.assertIn("Markdown link has an empty target", messages)
            self.assertIn("pin its npx package", messages)

    def test_rejects_non_list_amp_guidance_globs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill = write_skill(root, "rust-coding")
            (skill / "amp-guidance.md").write_text(
                '---\nglobs: "**/*.rs"\n---\n\nLoad the skill.\n', encoding="utf-8"
            )
            write_readme(root, "rust-coding")

            messages = "\n".join(validate_repository(root).errors)

            self.assertIn("globs must use an indented YAML list", messages)
            self.assertIn("globs must contain at least one pattern", messages)

    def test_allows_only_vendored_skill_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "skills").mkdir()
            (root / "vendor").mkdir()
            os.symlink("../vendor/upstream/skill", root / "skills" / "vendored")
            outside = root / "outside"
            write_skill(outside, "escaped")
            os.symlink("../outside/skills/escaped", root / "skills" / "escaped")
            write_readme(root, "escaped", "vendored")

            result = validate_repository(root)

            self.assertEqual(result.skipped, 1)
            self.assertTrue(any("must stay inside vendor" in error for error in result.errors))


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name) / "repo"
        self.home = Path(self.temporary_directory.name) / "home"
        self.root.mkdir()
        self.home.mkdir()
        shutil.copy2(REPOSITORY_ROOT / "install.sh", self.root / "install.sh")
        for name in ("AGENTS.md", "CLAUDE.md", "CODEX.md"):
            path = self.root / "global" / name
            path.parent.mkdir(exist_ok=True)
            path.write_text(f"# {name}\n", encoding="utf-8")
        (self.root / "checks").mkdir()
        skill = write_skill(self.root, "example")
        write_amp_guidance(skill, "**/*.example")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_installer(self) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(self.home)
        return subprocess.run(
            [str(self.root / "install.sh")],
            cwd=self.root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_install_is_idempotent(self) -> None:
        first = self.run_installer()
        second = self.run_installer()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(
            (self.home / ".agents" / "skills").resolve(), (self.root / "skills").resolve()
        )
        self.assertEqual(
            (self.home / ".claude" / "skills" / "example").resolve(),
            (self.root / "skills" / "example").resolve(),
        )
        self.assertEqual(
            (self.home / ".agents" / "skills" / "example" / "amp-guidance.md").resolve(),
            (self.root / "skills" / "example" / "amp-guidance.md").resolve(),
        )

    def test_install_refuses_to_replace_existing_path(self) -> None:
        conflict = self.home / ".agents" / "skills"
        conflict.mkdir(parents=True)
        sentinel = conflict / "keep.txt"
        sentinel.write_text("keep\n", encoding="utf-8")

        completed = self.run_installer()

        self.assertNotEqual(completed.returncode, 0)
        self.assertTrue(sentinel.exists())
        self.assertIn("Refusing to replace", completed.stderr)


if __name__ == "__main__":
    unittest.main()
