"""Offline contract tests for the ocas-reach skill package.

Run from the skill root:

    python3 -m unittest discover -s tests -v

Every test here is offline and deterministic: a test that needs a live API
would reintroduce exactly the flakiness the registry is meant to hide.
The suite guards the four things that silently rotted in this package before:
phantom `references/` paths, a `--help` that depends on an optional import,
connector modules the registry promises but does not ship, and PII/absolute
paths leaking into a public repo.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import reach  # noqa: E402  (sys.path set above; importing must not need PyYAML)

CLI_SCRIPTS = ["reach.py", "katzilla.py", "property_lookup.py"]

# Patterns that mean "this script can write to the outside world" — such a
# script must never be invoked with --help from a test.
OUTBOUND = re.compile(
    r"createRecord|putRecord|deleteRecord|smtplib|sendmail|send_email|"
    r"api\.telegram\.org/bot|hooks\.slack|discord\.com/api/webhooks|"
    r"submit_order|place_order|gh (pr|issue|release) create|git push"
)

EMAIL_OK = ("example.com", "example.org")


def _child_env(**overrides):
    """Host env with an isolated HERMES_HOME so no test touches live state."""
    env = dict(os.environ)
    env["HERMES_HOME"] = overrides.pop(
        "HERMES_HOME", tempfile.mkdtemp(prefix="reach-test-home-")
    )
    env.update(overrides)
    return env


def _run(args, env=None):
    return subprocess.run(
        [sys.executable] + args,
        capture_output=True,
        text=True,
        timeout=60,
        env=env or _child_env(),
    )


class TestRegistry(unittest.TestCase):
    def test_registry_parses_and_entries_are_wellformed(self):
        registry = reach.load_registry()
        sources = registry["sources"]
        self.assertGreater(len(sources), 50, "registry shrank unexpectedly")
        for name, entry in sources.items():
            self.assertIsInstance(entry, dict, name)
            self.assertTrue(
                entry.get("category"), "%s has no category" % name
            )
            self.assertTrue(
                entry.get("actions") or entry.get("custom") or entry.get("base_url"),
                "%s has no actions, custom connector or base_url" % name,
            )
            if entry.get("auth") == "required":
                self.assertTrue(
                    entry.get("env_var"),
                    "%s requires auth but declares no env_var" % name,
                )

    def test_every_registry_source_is_listed_in_the_index(self):
        names = set(reach.load_registry()["sources"])
        index = (ROOT / "references" / "sources" / "index.md").read_text()
        listed = set(re.findall(r"`([a-z0-9_]+)`", index))
        missing = sorted(names - listed)
        self.assertEqual(
            [], missing, "registry sources absent from references/sources/index.md"
        )


class TestCliBehaviour(unittest.TestCase):
    def test_unknown_source_is_actionable_not_a_traceback(self):
        proc = _run([str(SCRIPTS / "reach.py"), "query", "no_such_source", "x", "{}"])
        self.assertEqual(1, proc.returncode)
        self.assertIn("Unknown source", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_auth_required_without_key_returns_auth_missing_envelope(self):
        registry = reach.load_registry()["sources"]
        auth_required = [
            (name, entry)
            for name, entry in sorted(registry.items())
            if entry.get("auth") == "required" and entry.get("env_var")
        ]
        if not auth_required:
            self.fail("no auth-required source to exercise")
        name, entry = auth_required[0]
        env = _child_env()
        env.pop(entry["env_var"], None)
        proc = _run([str(SCRIPTS / "reach.py"), "query", name, "any_action", "{}"], env=env)
        self.assertEqual(1, proc.returncode)
        envelope = json.loads(proc.stdout)
        self.assertFalse(envelope["ok"])
        self.assertEqual("auth_missing", envelope["error"])
        self.assertIn(entry["env_var"], envelope["message"])
        self.assertNotIn("Traceback", proc.stderr)

    def test_missing_connector_returns_envelope_not_traceback(self):
        registry = reach.load_registry()["sources"]
        absent = [
            (name, entry)
            for name, entry in sorted(registry.items())
            if entry.get("custom")
            and not (SCRIPTS / "sources" / ("%s.py" % entry["custom"])).exists()
        ]
        if not absent:
            self.skipTest("every registry connector module is bundled")
        name, entry = absent[0]
        proc = _run([str(SCRIPTS / "reach.py"), "query", name, "any_action", "{}"])
        self.assertEqual(1, proc.returncode)
        self.assertEqual("connector_missing", json.loads(proc.stdout)["error"])
        self.assertNotIn("Traceback", proc.stderr)

    def test_help_exits_zero_for_every_readonly_cli(self):
        for script in CLI_SCRIPTS:
            path = SCRIPTS / script
            self.assertTrue(path.exists(), script)
            src = path.read_text()
            if OUTBOUND.search(src):
                continue  # never invoke an outbound script from a test
            proc = _run([str(path), "--help"])
            self.assertEqual(0, proc.returncode, "%s --help failed" % script)
            self.assertNotIn("Traceback", proc.stderr, script)
            self.assertTrue(proc.stdout.strip(), "%s --help printed nothing" % script)

    def test_missing_pyyaml_is_an_actionable_error(self):
        stub_dir = tempfile.mkdtemp(prefix="reach-test-stub-")
        (Path(stub_dir) / "yaml.py").write_text(
            'raise ImportError("simulated: PyYAML not installed")\n'
        )
        env = _child_env()
        env["PYTHONPATH"] = stub_dir + os.pathsep + env.get("PYTHONPATH", "")
        proc = _run([str(SCRIPTS / "reach.py"), "sources"], env=env)
        self.assertEqual(1, proc.returncode)
        self.assertIn("PyYAML", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_query_without_arguments_explains_usage(self):
        proc = _run([str(SCRIPTS / "reach.py"), "query"])
        self.assertEqual(1, proc.returncode)
        self.assertIn("Usage: reach.py query", proc.stderr)


class TestLibraryHygiene(unittest.TestCase):
    def test_scripts_carry_no_pii_or_absolute_host_paths(self):
        offenders = []
        for path in sorted(SCRIPTS.rglob("*.py")):
            text = path.read_text()
            for email in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
                if not email.endswith(EMAIL_OK):
                    offenders.append("%s: %s" % (path.relative_to(ROOT), email))
            for absolute in re.findall(r"/(?:root|home|Users)/[A-Za-z0-9_.\-/]*", text):
                offenders.append("%s: %s" % (path.relative_to(ROOT), absolute))
        self.assertEqual([], offenders, "PII or host paths in a public package")

    def test_no_source_reference_doc_is_orphaned(self):
        """Every `references/sources/*.md` is registered, indexed, or cataloged.

        A source doc that is neither in the registry nor named in the support
        file index is a doc an agent finds by accident and cannot place.
        """
        registered = set(reach.load_registry()["sources"])
        catalog = (ROOT / "references" / "support-file-map.md").read_text()
        orphans = []
        for doc in sorted((ROOT / "references" / "sources").glob("*.md")):
            stem = doc.stem
            if stem in ("index", "_template"):
                continue
            if stem in registered or stem.replace("-", "_") in registered:
                continue
            if stem in catalog:
                continue
            orphans.append(doc.name)
        self.assertEqual([], orphans, "source docs neither registered nor cataloged")

    def test_every_relative_markdown_link_resolves(self):
        """Catches the class of drift where a doc links a file that moved."""
        broken = []
        for doc in sorted((ROOT / "references").rglob("*.md")):
            for _label, target in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", doc.read_text()):
                if target.startswith(("http", "mailto:", "#")) or not target.endswith(".md"):
                    continue
                resolved = (doc.parent / target.split("#")[0].strip()).resolve()
                if not resolved.exists():
                    broken.append("%s -> %s" % (doc.relative_to(ROOT), target))
        self.assertEqual([], broken, "broken relative links")

    def test_every_referenced_reference_path_exists(self):
        """No phantom paths in this package's own docs.

        Two documented exceptions stay unchecked: host-side paths written as
        `scripts/references/...` (the negative lookbehind excludes them) and docs
        that point at a *sibling* skill's reference file — those paths are
        attributed to their owning skill on the same line ("Ocas Voyage ... owns
        `references/letsfg.md`") and are that skill's to keep alive.
        """
        docs = [ROOT / "SKILL.md"] + sorted((ROOT / "references").rglob("*.md"))
        pattern = re.compile(r"(?<![\w/])references/[A-Za-z0-9_./\-]+")
        dead = []
        for doc in docs:
            for line in doc.read_text().splitlines():
                if re.search(r"\bocas-(?!reach\b)[a-z][a-z-]*\b|\bOcas (?!Reach\b)[A-Z][a-z]+", line):
                    continue  # cross-skill pointer, not this package's file
                for ref in pattern.findall(line):
                    if any(tok in ref for tok in ("<", ">")) or ref.endswith("/"):
                        continue  # template placeholder, not a concrete path
                    if not (ROOT / ref).exists():
                        dead.append("%s -> %s" % (doc.relative_to(ROOT), ref))
        self.assertEqual([], dead, "phantom reference paths")


if __name__ == "__main__":
    unittest.main()
