# YAML config file replaces inline-token text files

Use `repos.yaml` (YAML) as the single source of truth for repo paths and include/exclude patterns. Per-repo overrides replace global defaults. No separate CLI `--include`/`--exclude` flags.

Old `.txt` files with inline `include:*`/`exclude:*` tokens were rejected as hard to read and error-prone. YAML was chosen over JSON and TOML for comment support and readability. The default file `repos.yaml` is auto-discovered in the working directory.
