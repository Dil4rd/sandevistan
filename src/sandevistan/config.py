"""Configuration management for Sandevistan."""

import os
import tomllib
import tomli_w
from pathlib import Path
from typing import Optional


def get_config_path() -> Path:
    """Get the configuration file path."""
    # Try XDG config directory first
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        config_dir = Path(xdg_config) / "sandevistan"
    else:
        config_dir = Path.home() / ".config" / "sandevistan"

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.toml"


def get_api_key() -> Optional[str]:
    """
    Get the Google API key from config file.

    Returns:
        API key string or None if not found
    """
    config_path = get_config_path()
    if not config_path.exists():
        return None

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
            return config.get("api", {}).get("google_api_key")
    except Exception:
        return None


def get_model() -> str:
    """
    Get the Gemini model name from config file.

    Returns:
        Model name string, defaults to "gemini-3-flash-preview" if not configured
    """
    config_path = get_config_path()
    if not config_path.exists():
        return "gemini-3-flash-preview"

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
            return config.get("model", {}).get("name", "gemini-3-flash-preview")
    except Exception:
        return "gemini-3-flash-preview"


def save_api_key(api_key: str) -> None:
    """
    Save the API key to the config file.

    Args:
        api_key: Google API key to save
    """
    config_path = get_config_path()

    # Load existing config if it exists
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "rb") as f:
                config = tomllib.load(f)
        except Exception:
            pass

    # Update API key
    if "api" not in config:
        config["api"] = {}
    config["api"]["google_api_key"] = api_key

    # Save config
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)


def save_model(model_name: str) -> None:
    """
    Save the model name to the config file.

    Args:
        model_name: Gemini model name to use
    """
    config_path = get_config_path()

    # Load existing config if it exists
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "rb") as f:
                config = tomllib.load(f)
        except Exception:
            pass

    # Update model
    if "model" not in config:
        config["model"] = {}
    config["model"]["name"] = model_name

    # Save config
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)


def get_scraper_url() -> str:
    """
    Get the scraper URL from config file.

    Returns:
        URL string, defaults to Apple's security updates page if not configured
    """
    config_path = get_config_path()
    if not config_path.exists():
        return "https://support.apple.com/en-us/100100"

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
            return config.get("scraper", {}).get("url", "https://support.apple.com/en-us/100100")
    except Exception:
        return "https://support.apple.com/en-us/100100"


def get_scraper_delay() -> float:
    """
    Get the scraper delay from config file.

    Returns:
        Delay in seconds, defaults to 1.0 if not configured
    """
    config_path = get_config_path()
    if not config_path.exists():
        return 1.0

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
            return float(config.get("scraper", {}).get("delay", 1.0))
    except Exception:
        return 1.0


def save_scraper_url(url: str) -> None:
    """
    Save the scraper URL to the config file.

    Args:
        url: Scraper URL to save
    """
    config_path = get_config_path()

    # Load existing config if it exists
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "rb") as f:
                config = tomllib.load(f)
        except Exception:
            pass

    # Update scraper URL
    if "scraper" not in config:
        config["scraper"] = {}
    config["scraper"]["url"] = url

    # Save config
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)


def save_scraper_delay(delay: float) -> None:
    """
    Save the scraper delay to the config file.

    Args:
        delay: Delay in seconds between requests
    """
    config_path = get_config_path()

    # Load existing config if it exists
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "rb") as f:
                config = tomllib.load(f)
        except Exception:
            pass

    # Update scraper delay
    if "scraper" not in config:
        config["scraper"] = {}
    config["scraper"]["delay"] = delay

    # Save config
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)


def get_config() -> dict:
    """
    Get the full configuration.

    Returns:
        Dictionary containing all configuration values
    """
    config_path = get_config_path()
    if not config_path.exists():
        return {}

    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}
