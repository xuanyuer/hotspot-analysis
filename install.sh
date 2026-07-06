#!/usr/bin/env bash
# install.sh — Set up hotspot-analysis tool in one step.
# Usage: bash install.sh [install_dir]
#   install_dir: where to clone (default: ../hotspot-analysis relative to script)

set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"

# Default: install alongside script_dir (one level up)
install_dir="${1:-$script_dir}"

if [ -d "$install_dir/.git" ]; then
    echo "✓ Repo already cloned at $install_dir"
else
    echo "→ Cloning to $install_dir ..."
    git clone https://github.com/xuanyuer/hotspot-analysis "$install_dir"
fi

cd "$install_dir"

cd "$install_dir"

# Detect Python
if command -v python3 &>/dev/null; then
    python="python3"
else
    echo "Error: python3 not found. Install Python 3.10+ first."
    exit 1
fi

# Create venv if missing
if [ ! -d ".venv" ]; then
    echo "→ Creating virtual environment ..."
    $python -m venv .venv
fi

# Activate
. .venv/bin/activate

# Upgrade pip, install deps
echo "→ Installing dependencies ..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Verify lizard is available
if ! command -v lizard &>/dev/null && [ -f ".venv/bin/lizard" ]; then
    echo "  (lizard in venv bin)"
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "  Usage:"
echo "    # Activate venv"
echo "    . $install_dir/.venv/bin/activate"
echo ""
echo "    # Analyze a single repo"
echo "    python $install_dir/main.py --repo /path/to/repo"
echo ""
echo "    # Analyze multiple repos"
echo "    python $install_dir/main.py --repo-list $install_dir/sample-repos.txt"
echo ""
echo "  Then activate with:"
echo "    . $install_dir/.venv/bin/activate"
