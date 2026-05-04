"""OpenBB provider configuration loader.

The template file is safe to commit. Real API keys should live in
config/openbb_providers.local.json or environment variables and must not be
committed.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_CONFIG_PATH = Path("config/openbb_providers.local.json")
TEMPLATE_CONFIG_PATH = Path("config/openbb_providers.template.json")


@dataclass
class OpenBBProvider:
    name: str
    enabled: bool
    api_key_env: str
    has_api_key: bool
    api_key_source: str
    use_for: List[str] = field(default_factory=list)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_openbb_provider_config(path: str | Path | None = None) -> Dict[str, Any]:
    """Load OpenBB provider config and resolve API keys from env/local file."""

    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    source_path = config_path if config_path.exists() else TEMPLATE_CONFIG_PATH
    if not source_path.exists():
        return {
            "enabled": False,
            "config_path": str(config_path),
            "providers": [],
            "usable_providers": [],
            "missing_config": True,
            "message": "No OpenBB provider config template found.",
        }

    raw = _load_json(source_path)
    providers: List[OpenBBProvider] = []
    for name, provider in raw.get("providers", {}).items():
        env_name = str(provider.get("api_key_env", "")).strip()
        key_from_env = os.environ.get(env_name, "") if env_name else ""
        key_from_file = str(provider.get("api_key", "") or "").strip()
        has_key = bool(key_from_env or key_from_file)
        if key_from_env:
            source = "environment"
        elif key_from_file:
            source = "local_config"
        else:
            source = "missing"
        providers.append(
            OpenBBProvider(
                name=name,
                enabled=bool(provider.get("enabled", False)),
                api_key_env=env_name,
                has_api_key=has_key,
                api_key_source=source,
                use_for=[str(item) for item in provider.get("use_for", [])],
            )
        )

    usable = [provider for provider in providers if provider.enabled and provider.has_api_key]
    return {
        "enabled": bool(raw.get("enabled", True)),
        "config_path": str(source_path),
        "using_template": source_path == TEMPLATE_CONFIG_PATH,
        "providers": [asdict(provider) for provider in providers],
        "usable_providers": [asdict(provider) for provider in usable],
        "missing_config": False,
        "message": "OpenBB providers usable." if usable else "No enabled provider has an API key.",
    }


def openbb_runtime_status(config_path: str | Path | None = None) -> Dict[str, Any]:
    """Return whether the optional OpenBB package and providers are usable."""

    try:
        import openbb  # type: ignore  # noqa: F401

        installed = True
    except ImportError:
        installed = False
    config = load_openbb_provider_config(config_path)
    return {
        "openbb_installed": installed,
        "provider_config": config,
        "usable": installed and bool(config.get("usable_providers")),
        "message": (
            "OpenBB is installed and at least one provider has a key."
            if installed and config.get("usable_providers")
            else "OpenBB is optional. Install openbb and provide provider keys to enable it."
        ),
    }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(openbb_runtime_status(path), indent=2, ensure_ascii=False))
