#!/usr/bin/env bash
# Explicit credential rotation; no API calls or runtime state changes.
set +x
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$script_dir/setup-universitydb-key.sh" --replace
