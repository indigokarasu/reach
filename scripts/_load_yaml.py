"""Minimal YAML loader — thin wrapper around PyYAML (always available)."""
import yaml
import sys

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 _load_yaml.py")
    sys.exit(0)



def _load_yaml_min(text):
    """Parse YAML text. PyYAML is a project dependency."""
    return yaml.safe_load(text)
