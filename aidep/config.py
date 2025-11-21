"""
Configuration management for aidep.
Allows users to customize behavior.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_CONFIG = {
    "check_cuda_versions": True,
    "strict_mode": False,  # If True, warns on ALL potential conflicts, not just known ones
    "ignore_conflicts": [],  # List of conflict IDs to ignore
    "custom_conflicts": [],  # User-defined conflicts
    "output_format": "rich",  # "rich", "simple", or "json"
}


class Config:
    """Manages aidep configuration."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".aidep" / "config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load config from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except Exception:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    def save(self):
        """Save current config to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default=None):
        """Get config value."""
        return self.config.get(key, default)

    def set(self, key: str, value):
        """Set config value."""
        self.config[key] = value
        self.save()

    def is_conflict_ignored(self, conflict_id: str) -> bool:
        """Check if a conflict ID should be ignored."""
        ignored = self.get("ignore_conflicts", [])
        return conflict_id in ignored
