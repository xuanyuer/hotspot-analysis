# Default exclude patterns per language
EXCLUDE_DEFAULTS = {
    "js": ["node_modules/*", "dist/*", "build/*", "*.min.js", "coverage/*", ".next/*", ".angular/*"],
    "java": ["target/*", "build/*", ".gradle/*", "generated/*", "*.class", "coverage/*"],
    "python": ["__pycache__/*", "*.pyc", ".venv/*", "venv/*", "build/*", "dist/*", ".mypy_cache/*"],
    "default": [".git/*"],
}

DEFAULT_HOTSPOT_PERCENTILE = 75
