"""Minimal YAML loader — thin wrapper around PyYAML (always available).

Usage:
  python3 _load_yaml.py --help     # this text

Import:
  from _load_yaml import _load_yaml_min

PyYAML is imported lazily below so a host without it fails with one actionable
line instead of an ImportError traceback, and so importing this module never
breaks the caller's own --help handling.
"""
import sys

_HELP_ARGS = {"--help", "-h"}
# __main__-scoped on purpose: reach.py imports this module, and a bare argv
# guard would hijack the parent CLI (`python3 reach.py --help` would print this
# loader's usage instead of reach's own).
if __name__ == "__main__" and set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 _load_yaml.py")
    sys.exit(0)

# Optimization: use the C-based CSafeLoader when PyYAML ships libyaml (~8x
# faster on large files like sources.yml: ~186ms -> ~23ms). Both imports are
# inside the guard so a missing PyYAML surfaces as a clear message, not a
# traceback before the caller can print usage.
try:
    from yaml import CSafeLoader as _SafeLoader, load as _yaml_load
except ImportError:
    try:
        from yaml import SafeLoader as _SafeLoader, load as _yaml_load
    except ImportError as exc:  # pragma: no cover - host without PyYAML
        raise SystemExit(
            "_load_yaml: PyYAML is required to parse scripts/sources.yml "
            "(pip install pyyaml): %s" % exc
        )


def _load_yaml_min(text):
    """Parse YAML text with the fastest available safe loader."""
    return _yaml_load(text, Loader=_SafeLoader)
