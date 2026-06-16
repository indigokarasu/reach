"""Minimal YAML loader — thin wrapper around PyYAML (always available)."""
import yaml


def _load_yaml_min(text):
    """Parse YAML text. PyYAML is a project dependency."""
    return yaml.safe_load(text)
